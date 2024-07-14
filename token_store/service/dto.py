import time
from enum import Enum
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class PermissionsEnum(str, Enum):

    read = "read"
    write = "write"
    delete = "delete"


class TokenDTO(BaseModel):

    id: UUID | None = None
    token: str
    expire_at: Annotated[int, Field(gt=0, description="The token expiration time", examples=[int(time.time())])]
    client_id: str
    instance_id: str
    account_id: str
    permissions: list[PermissionsEnum]


