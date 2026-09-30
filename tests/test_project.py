import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

from aar.core import BANNER, CodeExampleError, EvidenceError, MalformedCaptureError, capture, dump, fixtures, infer, ingest, write
from aar.generate import client, generated_tests, markdown, report, test_bundle as make_bundle


@pytest.fixture
def remains(tmp_path):
    fixtures(tmp_path / 'remains')
    return tmp_path / 'remains'


@pytest.fixture
def schema(remains):
    return infer(ingest(remains))


def endpoint(schema, method, path):
    return next(e for e in schema['endpoints'] if e['method']['value'] == method and e['path']['value'] == path)


def test_ingest(remains):
    records = ingest(remains)['records']
    assert len(records) == 10
    assert all(r['synthetic'] for r in records)
    assert {r['kind'] for r in records} == {'traffic', 'error', 'code'}
    row = next(r for r in records if r['request']['query'])
    assert row['request']['query'] == {'include_archived': 'true'}
    assert row['response']['status'] == 200


@pytest.mark.parametrize('value', [{}, {'request': {}}, {'request': {'method': 'NO', 'path': '/'}},
    {'request': {'method': 'GET', 'path': 'relative'}},
    {'request': {'method': 'GET', 'path': '/', 'headers': []}},
    {'request': {'method': 'GET', 'path': '/'}, 'response': {'status': '200'}},
    {'request': {'method': 'GET', 'path': '/'}, 'response': {'status': 700}}])
def test_malformed_capture(value):
    with pytest.raises(MalformedCaptureError, match='broken.json'):
        capture(value, 'broken.json')


def test_invalid_json(tmp_path):
    write(tmp_path / 'bad.json', '{')
    with pytest.raises(MalformedCaptureError):
        ingest(tmp_path)


def test_invalid_code(tmp_path):
    write(tmp_path / 'bad.py', 'def broken(')
    with pytest.raises(CodeExampleError):
        ingest(tmp_path)


def test_empty(tmp_path):
    with pytest.raises(EvidenceError, match='NoEvidenceError'):
        ingest(tmp_path)


def test_safe_code_extraction(tmp_path):
    write(tmp_path / 'calls.py', '"""SYNTHETIC"""\nrequests.get(dynamic)\nrequests.get("/known", params={"page": 2})\nother.get("/ignore")\n')
    rows = ingest(tmp_path)['records']
    assert len(rows) == 1
    assert rows[0]['request']['query'] == {'page': 2}
    assert rows[0]['response'] is None


def test_path_and_query(schema):
    e = endpoint(schema, 'GET', '/orders/{param_2}')
    assert e['path_parameters']['param_2']['value'] == ['integer']
    q = endpoint(schema, 'GET', '/orders')['query_parameters']['include_archived']
    assert q['confidence'].startswith('low:')
    assert q['required']['value'] == 'unknown'


def test_conflict(schema):
    conflict = next(c for c in schema['conflicts'] if c['endpoint'] == 'GET /inventory')
    assert {v['value']['fields']['available']['type'] for v in conflict['variants']} == {'boolean', 'string'}
    e = endpoint(schema, 'GET', '/inventory')
    assert e['responses']['200']['shape']['value']['state'] == 'conflicting'


def test_optional_counts(schema):
    fields = endpoint(schema, 'GET', '/orders/{param_2}')['responses']['200']['shape']['value']['fields']
    assert fields['id']['required']['value'] is True
    assert fields['note']['required']['value'] is False
    assert '1/2' in fields['note']['required']['confidence']


def test_auth_and_status(schema):
    e = endpoint(schema, 'GET', '/orders/{param_2}')
    assert set(e['responses']) == {'200', '404'}
    assert e['auth'][0]['value'] == {'scheme': 'bearer', 'header': 'authorization', 'required': 'unknown'}


def test_unknown_auth_and_code_response(tmp_path):
    write(tmp_path / 'only.py', '"""SYNTHETIC"""\nrequests.get("/health", headers={"Authorization": "Custom xyz"})\n')
    e = infer(ingest(tmp_path))['endpoints'][0]
    assert e['auth'][0]['value'] == 'unknown'
    assert e['responses'] == {}
    assert e['request_shape']['value'] == 'unknown'


def test_docs(schema):
    doc = markdown(schema)
    for e in schema['endpoints']:
        assert f"{e['method']['value']} {e['path']['value']}" in doc
        for i in e['evidence_ids']:
            assert f'[{i}](#{i})' in doc
            assert f'id="{i}"' in doc
    assert 'Unknown' in doc and 'conflicting' in doc and BANNER in doc


@pytest.mark.parametrize('fmt', ['md', 'json'])
def test_report(schema, fmt):
    text = report(schema, fmt)
    assert BANNER in text
    if fmt == 'json':
        data = json.loads(text)
        assert data['conflicts'] and data['unknowns'] and data['endpoint_catalogue']


def test_client_import_and_typed_request(schema, tmp_path):
    write(tmp_path / 'client.py', client(schema))
    spec = importlib.util.spec_from_file_location('client_under_test', tmp_path / 'client.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.endpoint_3_get_orders_param_2(param_2=101)
    assert result == {'method': 'GET', 'path': '/orders/101', 'query': {}, 'headers': {}, 'body': None}
    assert 'inference' in module.endpoint_3_get_orders_param_2.__doc__
    assert 'TypedDict' in client(schema) and 'optional' in client(schema)


def test_generated_suite(schema, tmp_path):
    make_bundle(schema, tmp_path / 'bundle')
    result = subprocess.run([sys.executable, '-m', 'pytest', '-q', str(tmp_path / 'bundle')], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert '9 passed' in result.stdout


def test_determinism(remains, tmp_path):
    fixtures(tmp_path / 'second')
    for path in remains.iterdir():
        assert path.read_bytes() == (tmp_path / 'second' / path.name).read_bytes()
    a, b = infer(ingest(remains)), infer(ingest(tmp_path / 'second'))
    assert dump(a) == dump(b)
    for generate in [markdown, client, generated_tests]:
        assert generate(a).encode() == generate(b).encode()
    for fmt in ['md', 'json']:
        assert report(a, fmt) == report(b, fmt)


def test_cli_end_to_end(tmp_path):
    def run(*args):
        result = subprocess.run([sys.executable, '-m', 'aar', *map(str, args)], cwd=tmp_path, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        assert BANNER in result.stdout
    run('fixtures', '--out', 'remains')
    run('ingest', 'remains')
    run('infer')
    run('docs')
    run('client', '--lang', 'python')
    run('tests')
    run('report')
    run('report', '--format', 'json', '--out', 'report.json')
    assert (tmp_path / 'reference.md').exists()
    assert BANNER in (tmp_path / 'report.md').read_text()
    result = subprocess.run([sys.executable, '-m', 'pytest', '-q', str(tmp_path / 'replay')], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_cli_named_error(tmp_path):
    write(tmp_path / 'broken.json', '{}')
    result = subprocess.run([sys.executable, '-m', 'aar', 'ingest', str(tmp_path)], capture_output=True, text=True)
    assert result.returncode == 2
    assert 'MalformedCaptureError' in result.stderr


def test_no_em_dash():
    root = Path(__file__).parents[1]
    for folder in [root / 'aar', root / 'tests']:
        for path in folder.glob('*.py'):
            assert chr(0x2014) not in path.read_text(encoding='utf-8')


@pytest.mark.parametrize('header,value,scheme', [('Authorization', 'Basic fictional', 'basic'), ('X-API-Key', 'fictional', 'api-key')])
def test_declared_auth(header, value, scheme):
    r = capture({'synthetic': True, 'request': {'method': 'GET', 'path': '/x', 'headers': {header: value}}}, 'x')
    assert infer({'records': [r]})['endpoints'][0]['auth'][0]['value']['scheme'] == scheme


def test_query_type_conflict():
    records = [capture({'synthetic': True, 'request': {'method': 'GET', 'path': '/x', 'query': {'q': value}}}, str(value)) for value in [1, 'abc']]
    schema = infer({'records': records})
    assert schema['conflicts'][0]['variants'] == ['integer', 'string']


def test_nested_shape_conflict():
    records = [capture({'synthetic': True, 'request': {'method': 'POST', 'path': '/x', 'body': {'items': [{'x': value}]}}}, str(value)) for value in [1, 'abc']]
    assert infer({'records': records})['conflicts'][0]['location'] == 'request'


def test_uuid_and_constant_rules():
    records = [capture({'synthetic': True, 'request': {'method': 'GET', 'path': path}}, path)
               for path in ['/users/12345678-abcd-abcd-abcd-123456789abc', '/users/current']]
    paths = {e['path']['value'] for e in infer({'records': records})['endpoints']}
    assert paths == {'/users/{param_2}', '/users/current'}


def test_empty_array_unknown_items():
    row = capture({'synthetic': True, 'request': {'method': 'POST', 'path': '/x', 'body': []}}, 'empty-array')
    shape = infer({'records': [row]})['endpoints'][0]['request_shape']['value']
    assert shape['items']['value'] == 'unknown'


def test_missing_and_null_distinct():
    row = capture({'synthetic': True, 'request': {'method': 'POST', 'path': '/x', 'body': None}}, 'null')
    assert row['request']['body_known']
    assert infer({'records': [row]})['endpoints'][0]['request_shape']['value']['type'] == 'null'
