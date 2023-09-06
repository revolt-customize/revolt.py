from __future__ import annotations

from typing import Union, TypedDict, cast
from dataclasses import dataclass, field


__all__ = (
    "Component",
    "ButtonComponent",
    "LineBreakComponent",
    "StatusComponent",
)


class ComponentPayload(TypedDict):
    type: str


class ButtonComponentPayload(ComponentPayload):
    label: str
    style: str
    enabled: bool


class LineBreakComponentPayload(ComponentPayload):
    pass


class StatusComponentPayload(ComponentPayload):
    label: str


@dataclass
class BaseComponent:
    type: str


@dataclass
class ButtonComponent(BaseComponent):
    type: str = field(default="button", init=False)
    label: str
    style: str
    enabled: bool


@dataclass
class LineBreakComponent(BaseComponent):
    type: str = field(default="line_break", init=False)


@dataclass
class StatusComponent(BaseComponent):
    type: str = field(default="status", init=False)
    label: str


Component = Union[ButtonComponent, LineBreakComponent, StatusComponent]


def component_factory(
    data: Union[
        ButtonComponentPayload, LineBreakComponentPayload, StatusComponentPayload
    ],
) -> Component:
    if data["type"] == "button":
        data = cast(ButtonComponentPayload, data)
        return ButtonComponent(
            label=data["label"], style=data["style"], enabled=data["enabled"]
        )
    elif data["type"] == "line_break":
        data = cast(LineBreakComponentPayload, data)
        return LineBreakComponent()
    elif data["type"] == "status":
        data = cast(StatusComponentPayload, data)
        return StatusComponent(label=data["label"])
    else:
        raise Exception
