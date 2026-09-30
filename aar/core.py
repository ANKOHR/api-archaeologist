"""Deterministic evidence parsing and conservative contract inference."""
import ast
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

BANNER = 'INFERRED, NOT VERIFIED. Schema is inferred from synthetic fixtures; unknowns are marked, not filled in.'
METHODS = {'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'}


class EvidenceError(ValueError):
    """Named rejection for invalid evidence."""


class MalformedCaptureError(EvidenceError):
    """HTTP capture does not satisfy the supported capture format."""


class CodeExampleError(EvidenceError):
    """Code sample cannot be parsed safely."""


def dump(value):
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + '\n'


def write(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content.encode('utf-8'))


def capture(value, source, kind='traffic'):
    try:
        req = value['request']
        method = req['method'].upper()
        url = urlsplit(req['path'])
        if method not in METHODS or not url.path.startswith('/'):
            raise ValueError('method or path invalid')
        headers = req.get('headers', {})
        query = req.get('query', {})
        response = value.get('response')
        if not isinstance(headers, dict) or not isinstance(query, dict):
            raise ValueError('headers and query must be objects')
        if any(not isinstance(k, str) or not isinstance(v, str) for k, v in headers.items()):
            raise ValueError('headers must map strings to strings')
        if response is not None:
            if not isinstance(response, dict) or type(response.get('status')) is not int or not 100 <= response['status'] <= 599:
                raise ValueError('status must be an integer from 100 to 599')
        parsed = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(url.query, keep_blank_values=True).items()}
        parsed.update(query)
        record = {'kind': kind, 'source': source, 'synthetic': value.get('synthetic') is True,
                  'request': {'method': method, 'path': url.path, 'query': parsed,
                              'headers': {k.lower(): v for k, v in headers.items()},
                              'body': req.get('body'), 'body_known': 'body' in req},
                  'response': response}
        record['id'] = 'ev-' + hashlib.sha256(dump(record).encode()).hexdigest()[:16]
        return record
    except (KeyError, TypeError, AttributeError, ValueError) as exc:
        raise MalformedCaptureError(f'{source}: {exc}') from exc


def ingest(directory):
    records = []
    for path in sorted(Path(directory).rglob('*')):
        if not path.is_file() or path.suffix not in {'.json', '.py'}:
            continue
        source = path.relative_to(directory).as_posix()
        if path.suffix == '.json':
            try:
                data = json.loads(path.read_text(encoding='utf-8'))
            except (ValueError, UnicodeError) as exc:
                raise MalformedCaptureError(f'{source}: invalid JSON') from exc
            for index, item in enumerate(data if isinstance(data, list) else [data]):
                records.append(capture(item, f'{source}#{index}', 'error' if 'error' in path.stem else 'traffic'))
        else:
            try:
                tree = ast.parse(path.read_text(encoding='utf-8'))
            except (SyntaxError, UnicodeError) as exc:
                raise CodeExampleError(f'{source}: invalid Python') from exc
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute) or node.func.attr.upper() not in METHODS:
                    continue
                if not isinstance(node.func.value, ast.Name) or node.func.value.id not in {'requests', 'client', 'session'}:
                    continue
                try:
                    url = ast.literal_eval(node.args[0])
                    kwargs = {k.arg: ast.literal_eval(k.value) for k in node.keywords if k.arg in {'params', 'headers', 'json'}}
                except (ValueError, TypeError, IndexError):
                    continue
                req = {'method': node.func.attr.upper(), 'path': url,
                       'query': kwargs.get('params', {}), 'headers': kwargs.get('headers', {})}
                if 'json' in kwargs:
                    req['body'] = kwargs['json']
                records.append(capture({'synthetic': 'SYNTHETIC' in ast.get_docstring(tree) if ast.get_docstring(tree) else False,
                                        'request': req}, f'{source}#L{node.lineno}', 'code'))
    if not records:
        raise EvidenceError('NoEvidenceError: no supported evidence found')
    return {'banner': BANNER, 'records': sorted(records, key=lambda r: (r['source'], r['id']))}


def value_type(value, parameter=False):
    if value is None:
        return 'null'
    if type(value) is bool:
        return 'boolean'
    if type(value) is int or parameter and isinstance(value, str) and re.fullmatch(r'-?\d+', value):
        return 'integer'
    if type(value) is float or parameter and isinstance(value, str) and re.fullmatch(r'-?\d+\.\d+', value):
        return 'number'
    if isinstance(value, dict):
        return 'object'
    if isinstance(value, list):
        return 'array'
    return 'string'


def claim(value, ids, note=None):
    ids = sorted(set(ids))
    return {'value': value, 'evidence_ids': ids,
            'confidence': note or ('low: one observation' if len(ids) == 1 else 'medium: repeated observations; not verified')}


def shape(value):
    result = {'type': value_type(value)}
    if isinstance(value, dict):
        result['fields'] = {k: shape(v) for k, v in sorted(value.items())}
    if isinstance(value, list):
        result['items'] = sorted({dump(shape(v)) for v in value})
    return result


def compatible(shapes):
    types = {s['type'] for s in shapes}
    if len(types) > 1:
        return False
    if 'object' in types:
        keys = set().union(*(s['fields'] for s in shapes))
        return all(compatible([s['fields'][k] for s in shapes if k in s['fields']]) for k in keys)
    if 'array' in types:
        items = [json.loads(item) for s in shapes for item in s['items']]
        return not items or compatible(items)
    return True


def merged_shape(observations):
    shapes = [shape(v) for v, _ in observations]
    ids = [i for _, i in observations]
    result = claim({'type': shapes[0]['type']}, ids)
    if shapes[0]['type'] == 'object':
        result['value']['fields'] = {}
        for key in sorted(set().union(*(v for v, _ in observations))):
            present = [(v[key], i) for v, i in observations if key in v]
            field = merged_shape(present)
            field['required'] = claim(len(present) == len(observations), ids,
                                      f'observed in {len(present)}/{len(observations)} samples; inferred only')
            result['value']['fields'][key] = field
    if shapes[0]['type'] == 'array':
        items = [(item, i) for v, i in observations for item in v]
        result['value']['items'] = merged_shape(items) if items else claim('unknown', ids, 'unknown: no array items observed')
    return result


def infer(evidence):
    records = evidence['records']
    groups = {}
    for record in records:
        req = record['request']
        segments = req['path'].strip('/').split('/')
        template = '/' + '/'.join('{param_' + str(i + 1) + '}' if re.fullmatch(r'\d+|[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}', s) else s for i, s in enumerate(segments))
        groups.setdefault((req['method'], template), []).append(record)
    endpoints, conflicts, unknowns = [], [], []
    for (method, path), rows in sorted(groups.items()):
        ids = [r['id'] for r in rows]
        endpoint = {'method': claim(method, ids), 'path': claim(path, ids), 'path_parameters': {}, 'query_parameters': {},
                    'request_shape': None, 'responses': {}, 'auth': [], 'evidence_ids': sorted(ids)}
        for index, segment in enumerate(path.strip('/').split('/')):
            if segment.startswith('{'):
                endpoint['path_parameters'][segment[1:-1]] = claim(sorted({value_type(r['request']['path'].strip('/').split('/')[index], True) for r in rows}), ids)
        keys = sorted(set().union(*(r['request']['query'] for r in rows)))
        for key in keys:
            found = [r for r in rows if key in r['request']['query']]
            types = sorted({value_type(r['request']['query'][key], True) for r in found})
            endpoint['query_parameters'][key] = claim(types, [r['id'] for r in found])
            endpoint['query_parameters'][key]['required'] = claim('unknown', ids, 'unknown: observations cannot establish query necessity')
            unknowns.append({'endpoint': f'{method} {path}', 'location': f'query.{key}.required', 'reason': 'observations cannot establish query necessity', 'evidence_ids': sorted(ids)})
            if len(types) > 1:
                conflicts.append({'endpoint': f'{method} {path}', 'location': f'query.{key}', 'variants': types, 'evidence_ids': sorted(r['id'] for r in found)})
        def contract(location, observations):
            if not observations:
                unknowns.append({'endpoint': f'{method} {path}', 'location': location, 'reason': 'no observed body', 'evidence_ids': sorted(ids)})
                return claim('unknown', ids, 'unknown: no observed body')
            if compatible([shape(v) for v, _ in observations]):
                return merged_shape(observations)
            variants = [claim(shape(v), [i], 'conflicting: incompatible observed types') for v, i in observations]
            conflicts.append({'endpoint': f'{method} {path}', 'location': location, 'variants': variants, 'evidence_ids': sorted(i for _, i in observations)})
            return claim({'state': 'conflicting', 'variants': variants}, [i for _, i in observations], 'conflicting: no merged contract')
        endpoint['request_shape'] = contract('request', [(r['request']['body'], r['id']) for r in rows if r['request']['body_known']])
        statuses = sorted({r['response']['status'] for r in rows if r['response']})
        if not statuses:
            unknowns.append({'endpoint': f'{method} {path}', 'location': 'responses', 'reason': 'no response or status observed', 'evidence_ids': sorted(ids)})
        for status in statuses:
            selected = [r for r in rows if r['response'] and r['response']['status'] == status]
            endpoint['responses'][str(status)] = {'status': claim(status, [r['id'] for r in selected]),
                                                 'shape': contract(f'response.{status}', [(r['response']['body'], r['id']) for r in selected if 'body' in r['response']])}
        for scheme, header, pattern in [('bearer', 'authorization', r'^Bearer\s+\S+$'), ('basic', 'authorization', r'^Basic\s+\S+$'), ('api-key', 'x-api-key', r'^\S+$')]:
            found = [r['id'] for r in rows if re.match(pattern, r['request']['headers'].get(header, ''), re.I)]
            if found:
                endpoint['auth'].append(claim({'scheme': scheme, 'header': header, 'required': 'unknown'}, found))
        for location, reason in [('auth_requirement', 'observed headers do not prove authentication requirements'), ('unobserved_behavior', 'unseen statuses, fields, and endpoints are unknown')]:
            unknowns.append({'endpoint': f'{method} {path}', 'location': location, 'reason': reason, 'evidence_ids': sorted(ids)})
        if not endpoint['auth']:
            endpoint['auth'] = [claim('unknown', ids, 'unknown: no declared auth scheme observed')]
        endpoints.append(endpoint)
    return {'banner': BANNER, 'synthetic': all(r['synthetic'] for r in records), 'endpoints': endpoints,
            'conflicts': conflicts, 'unknowns': unknowns, 'evidence': records}


def fixtures(directory):
    root = Path(directory)
    def row(method, path, status, body, **kwargs):
        return {'synthetic': True, 'request': {'method': method, 'path': path, 'headers': {'Authorization': 'Bearer fictional-token'}, **kwargs}, 'response': {'status': status, 'body': body}}
    rows = [row('GET', '/orders/101', 200, {'id': 101, 'total': 12, 'note': 'gift'}),
            row('GET', '/orders/202', 200, {'id': 202, 'total': 24}),
            row('GET', '/orders?include_archived=true', 200, {'orders': [{'id': 101}]}),
            row('GET', '/orders', 200, {'orders': [{'id': 202}]}),
            row('POST', '/orders', 201, {'id': 303}, body_known=True)]
    rows[-1]['request'].pop('body_known')
    rows[-1]['request']['body'] = {'sku': 'FICTIONAL-A', 'quantity': 2}
    rows += [row('GET', '/inventory', 200, {'available': True}), row('GET', '/inventory', 200, {'available': 'unknown'})]
    write(root / 'traffic.json', dump(rows))
    write(root / 'errors.json', dump(row('GET', '/orders/999', 404, {'error': 'fictional order missing'})))
    write(root / 'examples.py', '"""SYNTHETIC acme-orders code remains. Never contact a real API."""\nimport requests\nrequests.get("https://acme-orders.invalid/orders/101")\nrequests.post("https://acme-orders.invalid/orders", json={"sku": "FICTIONAL-B", "quantity": 1})\n')
    write(root / 'README.md', '# SYNTHETIC acme-orders remains\nAll records and tokens are fictional. No randomness is used; no seed is needed.\n')
