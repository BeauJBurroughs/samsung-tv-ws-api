"""
SamsungTVWS - Samsung Smart TV WS API wrapper

Copyright (C) 2019 DSR! <xchwarze@gmail.com>

SPDX-License-Identifier: LGPL-3.0
"""

import logging
from typing import Any, Dict, Literal, Optional

import aiohttp

from . import connection, exceptions, helper

_LOGGING = logging.getLogger(__name__)

_REQUEST_METHODS = Literal["GET", "POST", "PUT", "DELETE"]


class SamsungTVAsyncRest(connection.SamsungTVWSBaseConnection):
    def __init__(
        self,
        host: str,
        *,
        session: aiohttp.ClientSession,
        port: int = 8001,
        timeout: Optional[float] = None,
    ) -> None:
        super().__init__(
            host,
            endpoint="",
            port=port,
            timeout=timeout,
        )
        self.session = session

    async def _rest_request(
        self, method: _REQUEST_METHODS, target: str
    ) -> Dict[str, Any]:
        timeout = aiohttp.ClientTimeout(self.timeout)
        url = self._format_rest_url(target)
        try:
            future = self.session.request(method, url, timeout=timeout, ssl=False)
            async with future as resp:
                return helper.process_api_response(await resp.text())
        except aiohttp.ClientConnectionError as err:
            raise exceptions.HttpApiError(
                "TV unreachable or feature not supported on this model."
            ) from err

    async def rest_device_info(self) -> Dict[str, Any]:
        _LOGGING.debug("Get device info via rest api")
        return await self._rest_request("GET", "")

    async def rest_app_status(self, app_id: str) -> Dict[str, Any]:
        _LOGGING.debug("Get app %s status via rest api", app_id)
        return await self._rest_request("GET", "applications/" + app_id)

    async def rest_app_run(self, app_id: str) -> Dict[str, Any]:
        _LOGGING.debug("Run app %s via rest api", app_id)
        return await self._rest_request("POST", "applications/" + app_id)

    async def rest_app_close(self, app_id: str) -> Dict[str, Any]:
        _LOGGING.debug("Close app %s via rest api", app_id)
        return await self._rest_request("DELETE", "applications/" + app_id)

    async def rest_app_install(self, app_id: str) -> Dict[str, Any]:
        _LOGGING.debug("Install app %s via rest api", app_id)
        return await self._rest_request("PUT", "applications/" + app_id)
