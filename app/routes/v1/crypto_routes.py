from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.core import config
from app.core import crypto as crypto_core
from app.db.models import crypto as service
from app.schema import crypto_schema

crypto_router = APIRouter(
    tags=["crypto"],
    prefix="/api/v1/crypto",
)


@crypto_router.post(
    "/current",
    description="Get directly from coinAPI",
    response_model=crypto_schema.CryptoToCurrency,
)
def get_data(
    crypto: config.CryptoList,
    currency: config.CurrencyList,
):
    crypto_obj = crypto_core.Crypto(
        base_url=config.app_settings.crypto_base_url,
        crypto_api_key=config.app_settings.crypto_api_key,
    )
    return crypto_obj.get_rate(
        crypto=crypto,
        to=currency,
    )


@crypto_router.post(
    "/save-all",
    response_model=list[crypto_schema.CryptoHistoryCreate],
)
def save_all_leads(
    crypto: config.CryptoList,
    currency: config.CurrencyList,
    time_args: crypto_schema.TimeConfigBody,
    crypto_crud: service.get_crypto_crud = Depends(service.get_crypto_crud),
):
    crypto_obj = crypto_core.Crypto(
        base_url=config.app_settings.crypto_base_url,
        crypto_api_key=config.app_settings.crypto_api_key,
    )

    return crypto_obj.get_rate_history(
        crypto=crypto,
        to=currency,
        time_args=time_args,
    )
