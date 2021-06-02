from enum import Enum
from typing import Any, Dict, Optional, Type

import validators
from pydantic import constr, root_validator
from pydantic.dataclasses import dataclass


class EndpointType(str, Enum):
    UDPServer = "udpin"
    UDPClient = "udpout"
    TCPServer = "tcpin"
    TCPClient = "tcpout"
    Serial = "serial"


@dataclass
class Endpoint:
    name: constr(strip_whitespace=True, min_length=3, max_length=50)  # type: ignore
    owner: constr(strip_whitespace=True, min_length=3, max_length=50)  # type: ignore

    connection_type: str
    place: str
    argument: Optional[int] = None

    persistent: Optional[bool] = False
    protected: Optional[bool] = False

    @root_validator
    @classmethod
    def is_mavlink_endpoint(cls: Type["Endpoint"], values: Any) -> Any:
        connection_type, place, argument = (values.get("connection_type"), values.get("place"), values.get("argument"))

        if connection_type in [
            EndpointType.UDPServer,
            EndpointType.UDPClient,
            EndpointType.TCPServer,
            EndpointType.TCPClient,
        ]:
            if not (validators.domain(place) or validators.ipv4(place) or validators.ipv6(place)):
                raise ValueError(f"Invalid network address: {place}")
            if not argument in range(1, 65536):
                raise ValueError(f"Ports must be in the range 1:65535. Received {argument}.")
            return values

        if connection_type == EndpointType.Serial.value:
            if not place.startswith("/") or place.endswith("/"):
                raise ValueError(f"Bad serial address: {place}. Make sure to use an absolute path.")
            if not argument in VALID_SERIAL_BAUDRATES:
                raise ValueError(f"Invalid serial baudrate: {argument}. Valid option are {VALID_SERIAL_BAUDRATES}.")
            return values

        raise ValueError(
            f"Invalid connection_type: {connection_type}. Valid types are: {[e.value for e in EndpointType]}."
        )

    def __str__(self) -> str:
        return ":".join([self.connection_type, self.place, str(self.argument)])

    def as_dict(self) -> Dict[str, Any]:
        return dict(filter(lambda field: field[0] != "__initialised__", self.__dict__.items()))

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise NotImplementedError
        return str(self) == str(other)


VALID_SERIAL_BAUDRATES = [
    3000000,
    2000000,
    1000000,
    921600,
    570600,
    460800,
    257600,
    250000,
    230400,
    115200,
    57600,
    38400,
    19200,
    9600,
]
