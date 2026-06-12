---
name: add-error-code
description: Adds or updates application error codes in the FastAPI DDD template. Use when introducing a new API error, domain failure, exception mapping, or error response contract.
---

# Add Error Code

## Workflow

1. Read `app/shared/exceptions/error_code.py`.
2. Read `app/shared/exceptions/domains/{domain}/error_code.py` when the error is domain-specific.
3. Check existing names before adding a new code.
4. Add common codes to `ErrorCode` and domain-specific codes to `{Domain}ErrorCode`.
5. Use `(status_code, code, default_message)` for domain-specific error code values.
6. Put domain-specific error classes in `app/shared/exceptions/domains/{domain}/`.
7. Keep FastAPI handler registration in `app/shared/exceptions/handlers.py`.
8. Add or update tests for the response payload.

## Response Contract

```json
{
  "status": 400,
  "code": "ERROR_CODE",
  "message": "message"
}
```

## Rules

- Do not reuse removed error codes for a different meaning.
- Keep common codes in `ErrorCode`; keep domain-specific codes in `{Domain}ErrorCode`.
- Prefer domain-specific codes over generic messages when behavior differs.
- Keep user-facing messages stable once exposed through an API.
- Keep exception definitions centralized under `app/shared/exceptions/domains/{domain}/`.
