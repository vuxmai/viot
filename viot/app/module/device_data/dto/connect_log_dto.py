from datetime import datetime

from app.common.dto import BaseOutDto, PagingDto
from app.database.repository.pagination import Page

from ..constants import ConnectStatus
from ..model.connect_log import ConnectLog


class ConnectLogDto(BaseOutDto):
    ts: datetime
    connect_status: ConnectStatus
    ip: str
    keep_alive: int

    @classmethod
    def from_model(cls, connect_log: ConnectLog) -> "ConnectLogDto":
        return cls.model_validate(connect_log)


class PagingConnectLogDto(PagingDto[ConnectLogDto]):
    @classmethod
    def from_page(cls, page: Page[ConnectLog]) -> "PagingConnectLogDto":
        return cls(
            items=[ConnectLogDto.from_model(log) for log in page.items],
            total_items=page.total_items,
            page=page.page,
            page_size=page.page_size,
        )
