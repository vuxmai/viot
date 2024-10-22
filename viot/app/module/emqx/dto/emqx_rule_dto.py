from typing import Literal

from pydantic import BaseModel


class RepublishArgsDto(BaseModel):
    topic: str
    payload: str
    qos: int
    retain: bool
    direct_dispatch: bool


class EmqxActionDto(BaseModel):
    function: Literal["republish"]
    args: RepublishArgsDto


class EmqxCreateRuleDto(BaseModel):
    id: str
    sql: str
    actions: list[EmqxActionDto]
    enable: bool


class EmqxUpdateRuleDto(BaseModel):
    sql: str
    actions: list[EmqxActionDto]
    enable: bool
