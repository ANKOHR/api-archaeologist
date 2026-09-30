"""INFERRED, NOT VERIFIED. Schema is inferred from synthetic fixtures; unknowns are marked, not filled in.
Replay checks only, not verification against a real API.
"""
import importlib.util
import json
from pathlib import Path
import pytest
ROOT = Path(__file__).parent
spec = importlib.util.spec_from_file_location("inferred_client", ROOT / "client.py")
client = importlib.util.module_from_spec(spec)
spec.loader.exec_module(client)
CASES = json.loads('[{"expected": {"body": null, "headers": {"authorization": "Bearer fictional-token"}, "method": "GET", "path": "/inventory", "query": {}}, "function": "endpoint_1_get_inventory", "kwargs": {"body": null, "headers": {"authorization": "Bearer fictional-token"}, "query": {}}}, {"expected": {"body": null, "headers": {"authorization": "Bearer fictional-token"}, "method": "GET", "path": "/inventory", "query": {}}, "function": "endpoint_1_get_inventory", "kwargs": {"body": null, "headers": {"authorization": "Bearer fictional-token"}, "query": {}}}, {"expected": {"body": null, "headers": {"authorization": "Bearer fictional-token"}, "method": "GET", "path": "/orders", "query": {"include_archived": "true"}}, "function": "endpoint_2_get_orders", "kwargs": {"body": null, "headers": {"authorization": "Bearer fictional-token"}, "query": {"include_archived": "true"}}}, {"expected": {"body": null, "headers": {"authorization": "Bearer fictional-token"}, "method": "GET", "path": "/orders", "query": {}}, "function": "endpoint_2_get_orders", "kwargs": {"body": null, "headers": {"authorization": "Bearer fictional-token"}, "query": {}}}, {"expected": {"body": null, "headers": {"authorization": "Bearer fictional-token"}, "method": "GET", "path": "/orders/999", "query": {}}, "function": "endpoint_3_get_orders_param_2", "kwargs": {"body": null, "headers": {"authorization": "Bearer fictional-token"}, "param_2": 999, "query": {}}}, {"expected": {"body": null, "headers": {"authorization": "Bearer fictional-token"}, "method": "GET", "path": "/orders/101", "query": {}}, "function": "endpoint_3_get_orders_param_2", "kwargs": {"body": null, "headers": {"authorization": "Bearer fictional-token"}, "param_2": 101, "query": {}}}, {"expected": {"body": null, "headers": {"authorization": "Bearer fictional-token"}, "method": "GET", "path": "/orders/202", "query": {}}, "function": "endpoint_3_get_orders_param_2", "kwargs": {"body": null, "headers": {"authorization": "Bearer fictional-token"}, "param_2": 202, "query": {}}}, {"expected": {"body": {"quantity": 2, "sku": "FICTIONAL-A"}, "headers": {"authorization": "Bearer fictional-token"}, "method": "POST", "path": "/orders", "query": {}}, "function": "endpoint_4_post_orders", "kwargs": {"body": {"quantity": 2, "sku": "FICTIONAL-A"}, "headers": {"authorization": "Bearer fictional-token"}, "query": {}}}]')
@pytest.mark.parametrize("case", CASES)
def test_replay(case):
    assert getattr(client, case["function"])(**case["kwargs"]) == case["expected"]

def test_schema_consistency():
    schema = json.loads((ROOT / "schema.json").read_text())
    ids = {row["id"] for row in schema["evidence"]}
    assert "INFERRED, NOT VERIFIED" in schema["banner"]
    def check(value):
        if isinstance(value, dict):
            if "evidence_ids" in value:
                assert value["evidence_ids"] and set(value["evidence_ids"]) <= ids
            for item in value.values(): check(item)
        elif isinstance(value, list):
            for item in value: check(item)
    check(schema["endpoints"])
    check(schema["conflicts"])
    check(schema["unknowns"])
