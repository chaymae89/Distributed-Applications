api_contract = [
    {
        "endpoint": "/api/v1/auth/login",
        "method": "POST",
        "input": '{"username": str, "password": str}',
        "output": '{"token": str, "expires_at": str, "user_id": str, "roles": [str]}',
        "errors": "400, 401, 429, 500",
        "idempotent": False,
        "security": "TLS, rate limiting strict, generic auth errors"
    },
    {
        "endpoint": "/api/v1/auth/verify",
        "method": "GET",
        "input": 'Authorization: Bearer <token>',
        "output": '{"valid": bool, "user_id": str, "roles": [str], "expires_at": str}',
        "errors": "401, 500",
        "idempotent": True,
        "security": "Token validation, X-Request-Id"
    },
    {
        "endpoint": "/api/v1/auth/logout",
        "method": "POST",
        "input": 'Authorization: Bearer <token>',
        "output": '{"message": "logout successful"}',
        "errors": "401, 500",
        "idempotent": True,
        "security": "Token invalidation, audit log"
    },
    {
        "endpoint": "/api/v1/documents",
        "method": "POST",
        "input": '{"title": str, "content": str, "tags": [str]}',
        "output": '{"id": str, "title": str, "created_at": str}',
        "errors": "400, 401, 403, 413, 429",
        "idempotent": False,
        "security": "AuthN + AuthZ, validation, max payload, Idempotency-Key"
    },
    {
        "endpoint": "/api/v1/documents",
        "method": "GET",
        "input": 'page, per_page, sort, order, tag',
        "output": '{"data": [...], "total": int, "page": int, "per_page": int}',
        "errors": "400, 401, 429",
        "idempotent": True,
        "security": "AuthN, forced pagination"
    },
    {
        "endpoint": "/api/v1/documents/{id}",
        "method": "GET",
        "input": 'id (UUID)',
        "output": '{"id": str, "title": str, "content": str}',
        "errors": "401, 403, 404",
        "idempotent": True,
        "security": "AuthN + AuthZ, UUID non predictable"
    },
    {
        "endpoint": "/api/v1/documents/{id}",
        "method": "PUT",
        "input": '{"title": str, "content": str, "tags": [str]}',
        "output": '{"id": str, "title": str, "updated_at": str}',
        "errors": "400, 401, 403, 404, 409",
        "idempotent": True,
        "security": "AuthN + AuthZ, optimistic locking"
    },
    {
        "endpoint": "/api/v1/documents/{id}",
        "method": "DELETE",
        "input": 'id (UUID)',
        "output": '204 No Content',
        "errors": "401, 403, 404",
        "idempotent": True,
        "security": "AuthN + AuthZ, audit log"
    },
    {
        "endpoint": "/api/v1/search",
        "method": "GET",
        "input": 'q, page, per_page, tag, date_from, date_to',
        "output": '{"results": [...], "total": int, "page": int}',
        "errors": "400, 401, 429, 500",
        "idempotent": True,
        "security": "AuthN, rate limiting, filtered results"
    }
]

print("=== TP 6.1 - Contrat d API ===")
for route in api_contract:
    print(f"{route['method']} {route['endpoint']} | idempotent={route['idempotent']}")