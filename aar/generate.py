"""Generate reviewable artifacts from inference, without network verification."""
import json
import re
from .core import BANNER, dump, write


def names(schema):
    for index, endpoint in enumerate(schema['endpoints']):
        yield 'endpoint_' + str(index + 1) + '_' + re.sub(r'[^a-z0-9]+', '_', endpoint['method']['value'].lower() + endpoint['path']['value']).strip('_'), endpoint


def markdown(schema):
    lines = ['# API Archaeologist inferred reference', '', BANNER, '',
             f"All input records explicitly labelled synthetic: {schema['synthetic']}. The synthetic-fixture banner describes the bundled demonstration; other input provenance is unverified.", '',
             '## Endpoint catalogue', '', 'All entries are inferred observations, never confirmed contracts.', '']
    for name, endpoint in names(schema):
        lines += [f"### {endpoint['method']['value']} {endpoint['path']['value']}", '',
                  f"Confidence: {endpoint['path']['confidence']}", '',
                  'Evidence: ' + ', '.join(f'[{i}](#{i})' for i in endpoint['evidence_ids']), '',
                  'Unknown: auth necessity, unobserved behavior, and query necessity.', '',
                  '```json', dump(endpoint).rstrip(), '```', '']
    for title, key in [('Conflict list', 'conflicts'), ('Unknown list', 'unknowns')]:
        lines += [f'## {title}', '', '```json', dump(schema[key]).rstrip(), '```', '']
    lines += ['## Evidence catalogue', '']
    for record in schema['evidence']:
        lines += [f"<a id=\"{record['id']}\"></a>", f"### {record['id']}", '',
                  f"Source: `{record['source']}`. Synthetic: {record['synthetic']}.", '',
                  '```json', dump(record).rstrip(), '```', '']
    return '\n'.join(lines)


def report(schema, fmt):
    if fmt == 'md':
        return markdown(schema)
    return dump({'banner': BANNER, 'synthetic': schema['synthetic'], 'endpoint_catalogue': schema['endpoints'],
                 'conflicts': schema['conflicts'], 'unknowns': schema['unknowns']})


def client(schema):
    lines = ['"""' + BANNER + '\nRequest builders only. No real API verification or network calls.\n"""',
             'from typing import Any, TypedDict', 'from urllib.parse import quote', '',
             'class Request(TypedDict):', '    method: str', '    path: str',
             '    query: dict[str, Any]', '    headers: dict[str, str]', '    body: Any', '']
    scalar = {'integer': 'int', 'number': 'float', 'string': 'str', 'boolean': 'bool', 'null': 'None'}
    for name, endpoint in names(schema):
        fields = endpoint['request_shape']['value']
        body_type = 'Any | None'
        if isinstance(fields, dict) and fields.get('type') == 'object':
            body_type = name.title().replace('_', '') + 'Body'
            lines += [f'class {body_type}(TypedDict, total=False):']
            for key, field in fields['fields'].items():
                if key.isidentifier() and not __import__('keyword').iskeyword(key):
                    typ = scalar.get(field['value'].get('type'), 'Any | None')
                    lines += [f'    {key}: {typ}  # Presence inferred from occurrence counts; optional for unseen behavior.']
            lines += ['    pass', '']
            body_type += ' | None'
        params = [f'{p}: {scalar.get(v["value"][0], "str")}' for p, v in endpoint['path_parameters'].items()]
        params += ['query: dict[str, Any] | None = None', 'headers: dict[str, str] | None = None', f'body: {body_type} = None']
        lines += [f'def {name}(*, ' + ', '.join(params) + ') -> Request:',
                  '    """Generated from inference, not a confirmed contract. Evidence: ' + ', '.join(endpoint['evidence_ids']) + '."""',
                  '    # Unknown fields remain optional; callers provide auth and query values explicitly.',
                  f'    path = {endpoint["path"]["value"]!r}']
        for param in endpoint['path_parameters']:
            lines += [f'    path = path.replace("{{{param}}}", quote(str({param}), safe=""))']
        lines += [f'    return {{"method": {endpoint["method"]["value"]!r}, "path": path, "query": dict(query or {{}}), "headers": dict(headers or {{}}), "body": body}}', '']
    return '\n'.join(lines)


def generated_tests(schema):
    cases = []
    for name, endpoint in names(schema):
        for row in schema['evidence']:
            if row['id'] not in endpoint['evidence_ids'] or row['kind'] == 'code':
                continue
            request = row['request']
            kwargs = {'query': request['query'], 'headers': request['headers'], 'body': request['body']}
            for index, segment in enumerate(endpoint['path']['value'].strip('/').split('/')):
                if segment.startswith('{'):
                    parameter = segment[1:-1]
                    value = request['path'].strip('/').split('/')[index]
                    kwargs[parameter] = int(value) if endpoint['path_parameters'][parameter]['value'] == ['integer'] else value
            cases.append({'function': name, 'kwargs': kwargs, 'expected': {k: request[k] for k in ['method', 'path', 'query', 'headers', 'body']}})
    return '\n'.join(['"""' + BANNER + '\nReplay checks only, not verification against a real API.\n"""',
                      'import importlib.util', 'import json', 'from pathlib import Path', 'import pytest',
                      'ROOT = Path(__file__).parent',
                      'spec = importlib.util.spec_from_file_location("inferred_client", ROOT / "client.py")',
                      'client = importlib.util.module_from_spec(spec)', 'spec.loader.exec_module(client)',
                      'CASES = json.loads(' + repr(json.dumps(cases, sort_keys=True)) + ')',
                      '@pytest.mark.parametrize("case", CASES)', 'def test_replay(case):',
                      '    assert getattr(client, case["function"])(**case["kwargs"]) == case["expected"]', '',
                      'def test_schema_consistency():', '    schema = json.loads((ROOT / "schema.json").read_text())',
                      '    ids = {row["id"] for row in schema["evidence"]}',
                      '    assert "INFERRED, NOT VERIFIED" in schema["banner"]',
                      '    def check(value):', '        if isinstance(value, dict):',
                      '            if "evidence_ids" in value:', '                assert value["evidence_ids"] and set(value["evidence_ids"]) <= ids',
                      '            for item in value.values(): check(item)',
                      '        elif isinstance(value, list):', '            for item in value: check(item)',
                      '    check(schema["endpoints"])', '    check(schema["conflicts"])', '    check(schema["unknowns"])', ''])


def test_bundle(schema, directory):
    from pathlib import Path
    root = Path(directory)
    write(root / 'schema.json', dump(schema))
    write(root / 'client.py', client(schema))
    write(root / 'test_replay.py', generated_tests(schema))
