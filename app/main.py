from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core import exceptions as exc
from app.routes import v1


def validation_exception_handler(request: Request, exc: RequestValidationError):
    """ReWrite the pydantic request model error into simple one line."""

    error_message = ""
    for i in exc.errors():
        error_message = i.get("msg")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": error_message},
    )


app = FastAPI(
    exception_handlers={
        exc.AppExceptionBase: exc.handler,
        RequestValidationError: validation_exception_handler,
    },
)

app.include_router(v1.suite_crm_router)
app.include_router(v1.crypto_router)


@app.get("/", response_model=None)
def read_root():
    return {"hello": "world"}
