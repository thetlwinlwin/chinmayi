import requests

from app.core import exceptions as exc
from app.schema import crypto_schema

from ..config import all_currencies as currency_list


class Crypto:
    def __init__(
        self,
        crypto_api_key: str,
        base_url: str,
    ) -> None:
        self._base_url = base_url
        self._headers = {
            "X-CoinAPI-Key": crypto_api_key,
        }

    def _call(self, url: str, args: dict | None = None) -> dict | list[dict]:
        try:
            res = requests.get(url, headers=self._headers, params=args)
            match res.status_code:
                case 400 | 401 | 403 | 550:
                    raise exc.BadRequest()
                case 429:
                    raise exc.TooManyRequest()
            return res.json()
        except:
            raise exc.BadRequest()

    def get_rate(
        self, crypto: currency_list.CryptoList, to: currency_list.CurrencyList
    ) -> crypto_schema.CryptoToCurrency:
        url = f"{self._base_url}/{crypto.value}/{to.value}/"
        return self._call(url)

    def get_rate_history(
        self,
        crypto: currency_list.CryptoList,
        to: currency_list.CurrencyList,
        time_args: crypto_schema.TimeConfigBody,
    ) -> list[crypto_schema.CryptoHistoryCreate]:
        url = f"{self._base_url}/{crypto.value}/{to.value}/history"
        return self._call(url, time_args.get_args)
