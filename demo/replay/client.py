"""INFERRED, NOT VERIFIED. Schema is inferred from synthetic fixtures; unknowns are marked, not filled in.
Request builders only. No real API verification or network calls.
"""
from typing import Any, TypedDict
from urllib.parse import quote

class Request(TypedDict):
    method: str
    path: str
    query: dict[str, Any]
    headers: dict[str, str]
    body: Any

def endpoint_1_get_inventory(*, query: dict[str, Any] | None = None, headers: dict[str, str] | None = None, body: Any | None = None) -> Request:
    """Generated from inference, not a confirmed contract. Evidence: ev-8495457c264eaa6b, ev-f54bfa7fa8030ae2."""
    # Unknown fields remain optional; callers provide auth and query values explicitly.
    path = '/inventory'
    return {"method": 'GET', "path": path, "query": dict(query or {}), "headers": dict(headers or {}), "body": body}

def endpoint_2_get_orders(*, query: dict[str, Any] | None = None, headers: dict[str, str] | None = None, body: Any | None = None) -> Request:
    """Generated from inference, not a confirmed contract. Evidence: ev-2c4ebea7f0e6687c, ev-7ad876f478cf8e8d."""
    # Unknown fields remain optional; callers provide auth and query values explicitly.
    path = '/orders'
    return {"method": 'GET', "path": path, "query": dict(query or {}), "headers": dict(headers or {}), "body": body}

def endpoint_3_get_orders_param_2(*, param_2: int, query: dict[str, Any] | None = None, headers: dict[str, str] | None = None, body: Any | None = None) -> Request:
    """Generated from inference, not a confirmed contract. Evidence: ev-4ad744c73477a194, ev-62536776afb6e0f1, ev-cd3277efe255bfa4, ev-efaf5bfe926a2350."""
    # Unknown fields remain optional; callers provide auth and query values explicitly.
    path = '/orders/{param_2}'
    path = path.replace("{param_2}", quote(str(param_2), safe=""))
    return {"method": 'GET', "path": path, "query": dict(query or {}), "headers": dict(headers or {}), "body": body}

class Endpoint4PostOrdersBody(TypedDict, total=False):
    quantity: int  # Presence inferred from occurrence counts; optional for unseen behavior.
    sku: str  # Presence inferred from occurrence counts; optional for unseen behavior.
    pass

def endpoint_4_post_orders(*, query: dict[str, Any] | None = None, headers: dict[str, str] | None = None, body: Endpoint4PostOrdersBody | None = None) -> Request:
    """Generated from inference, not a confirmed contract. Evidence: ev-7b297c1511b022ea, ev-def27801e0719916."""
    # Unknown fields remain optional; callers provide auth and query values explicitly.
    path = '/orders'
    return {"method": 'POST', "path": path, "query": dict(query or {}), "headers": dict(headers or {}), "body": body}
