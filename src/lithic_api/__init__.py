from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from lithic_api.routers.transcription import router as transcription_router
from lithic_api.routers.upload import router as upload_router
from lithic_api.transcription import TranslationError

app = FastAPI()

app.include_router(transcription_router)
app.include_router(upload_router)


@app.exception_handler(TranslationError)
async def translation_error_handler(_: Request, exc: TranslationError) -> JSONResponse:
    """Default exeption handler for raised translation errors

    Args:
        _ (Request): The request
        exc (TranslationError): specific translation error

    Returns:
        JSONResponse: error response detailing the problem
    """
    return JSONResponse(status_code=400, content=jsonable_encoder({"detail": str(exc)}))


def main() -> None:
    print("Hello from lithic-api!")
