import logging
from typing import Annotated

from classy_fastapi import post
from fastapi import Body
from injector import inject

from app.common.controller import Controller
from app.common.fastapi.serializer import JSONResponse
from app.database.dependency import DependSession

from ..dto.emqx_auth_dto import EmqxAuthenRequestDto, EmqxAuthenResponseDto
from ..dto.emqx_event_dto import DeviceConnectedEventDto, DeviceDisconnectedEventDto
from ..service.emqx_auth_service import EmqxDeviceAuthService
from ..service.emqx_event_service import EmqxEventService

logger = logging.getLogger(__name__)


class EmqxDeviceController(Controller):
    @inject
    def __init__(
        self,
        emqx_device_authen_service: EmqxDeviceAuthService,
        emqx_event_service: EmqxEventService,
    ) -> None:
        super().__init__(
            prefix="/emqx",
            tags=["EMQX Auth"],
            dependencies=[DependSession],
        )
        self._emqx_device_authen_service = emqx_device_authen_service
        self._emqx_event_service = emqx_event_service

    @post(
        "/auth",
        summary="Authenticate a device with EMQX",
        status_code=200,
        responses={200: {"model": EmqxAuthenResponseDto}},
    )
    async def authenticate(
        self, *, body: Annotated[EmqxAuthenRequestDto, Body(...)]
    ) -> JSONResponse[EmqxAuthenResponseDto]:
        """
        Authenticate a device with EMQX.

        https://docs.emqx.com/en/emqx/v5.8/access-control/authn/http.html#post-request

        From documentation we need to return a response with:
        - `Status code` should be 200 and result should be `allow`, `deny`
        to prevent continue authentication chain.
        - All exceptions will be caught in controller and return result `deny` with status code 200.
        """

        try:
            return JSONResponse(
                content=await self._emqx_device_authen_service.authenticate(request_dto=body)
            )
        except Exception as e:
            logger.warning(f"Failed to authenticate device: {e}")
            return JSONResponse(content=EmqxAuthenResponseDto(result="deny"))

    @post(
        "/events/device-connected",
        summary="Event device connected from EMQX",
        status_code=200,
    )
    async def event_connected(
        self, *, body: Annotated[DeviceConnectedEventDto, Body(...)]
    ) -> JSONResponse[None]:
        """Event device connected from EMQX."""
        await self._emqx_event_service.handle_device_connected(event=body)
        return JSONResponse.no_content()

    @post(
        "/events/device-disconnected",
        summary="Event device disconnected from EMQX",
        status_code=200,
    )
    async def event_disconnected(
        self, *, body: Annotated[DeviceDisconnectedEventDto, Body(...)]
    ) -> JSONResponse[None]:
        """Event device disconnected from EMQX."""
        await self._emqx_event_service.handle_device_disconnected(event=body)
        return JSONResponse.no_content()
