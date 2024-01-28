from advanced_alchemy.exceptions import ConflictError
from litestar import Response, MediaType, Request
from litestar.exceptions import ValidationException, HTTPException, NotAuthorizedException
from sentry_sdk import capture_exception


def default_exception_handler(request: Request, exc: HTTPException) -> Response:
    if hasattr(exc, "detail"):
        detail = exc.detail
    elif exc:
        detail = exc
    else:
        detail = "Internal server error"
    status_code = exc.status_code if hasattr(exc, "status_code") else 500
    content = {
        "type": str(exc.__class__),
        "detail": detail,
        "status_code": status_code,
    }
    if hasattr(exc, "extra") and exc.extra:
        content.update({"extra": exc.extra})

    return Response(
        content=content,
        status_code=status_code,
    )


def not_found_exception_handler(request: Request, exc: HTTPException) -> Response:
    return Response(
        content={
            "type": str(exc.__class__),
            "detail": exc.detail,
            "status_code": 404,
        },
        status_code=404,
    )


def conflict_exception_handler(request: Request, exc: ConflictError) -> Response:
    return Response(
        content={
            "type": str(exc.__class__),
            "detail": "Item already exists",
            "status_code": 422,
        },
        status_code=422,
    )


def app_exception_handler(request: Request, exc: HTTPException) -> Response:
    capture_exception(exc)

    return default_exception_handler(request, exc)
