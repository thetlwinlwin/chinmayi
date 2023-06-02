import hashlib
import json
from enum import Enum

import requests

from app.schema import lead_schema


class SuiteCrmMethod(Enum):
    login = "login"
    count = "get_entries_count"
    get_entries = "get_entry_list"


class SuiteCrm:
    def __init__(
        self,
        name,
        password,
        module_name,
        url,
    ) -> None:
        self._username = name
        self._password = password
        self._url = url
        self._module_name = module_name
        self._max_limit = 20
        self._session_id = self._get_session_id()

    def _call(self, method: str, arguments: dict) -> dict:
        args = {
            "method": method,
            "input_type": "json",
            "response_type": "json",
            "rest_data": json.dumps(arguments),
        }
        response = requests.get(self._url, args)

        if response.status_code != 200:
            raise Exception("something went wrong during fetching")
        return response.json()

    def _get_session_id(self):
        args = {
            "user_auth": {
                "user_name": self._username,
                "password": self._hashing_password(),
            },
        }
        return self._call(
            method=SuiteCrmMethod.login.value,
            arguments=args,
        )["id"]

    def _get_entries_count(self) -> int:
        args = {
            "session": self._session_id,
            "module_name": self._module_name,
            "query": "",
            "deleted": 0,
        }
        return self._call(
            SuiteCrmMethod.count.value,
            args,
        )

    def _get_entries(self) -> list[lead_schema.LeadCreate]:
        count = self._get_entries_count()["result_count"]
        data: list[lead_schema.LeadCreate] = []
        for i in range(0, int(count) + 1, self._max_limit):
            args = {
                "session": self._session_id,
                "module_name": self._module_name,
                "query": "",
                "order_by": "",
                "offset": i,
                "select_fields": ["first_name", "last_name", "phone_work"],
                "max_results": self._max_limit,
                "deleted": 0,
            }
            entry_response = self._call(
                SuiteCrmMethod.get_entries.value,
                args,
            )
            entry_response = entry_response["entry_list"]
            entry_results: list[lead_schema.LeadCreate] = list(
                map(
                    self._transform,
                    entry_response,
                )
            )
            data.extend(entry_results)
        return data

    @property
    def entries(self) -> list[lead_schema.LeadCreate]:
        return self._get_entries()

    def _transform(self, result: dict) -> lead_schema.LeadCreate:
        return lead_schema.LeadCreate(
            first_name=result["name_value_list"]["first_name"]["value"],
            last_name=result["name_value_list"]["last_name"]["value"],
            phone_work=str(result["name_value_list"]["phone_work"]["value"]),
        )

    def _hashing_password(self) -> str:
        return hashlib.md5(
            self._password.encode("utf-8"),
        ).hexdigest()
