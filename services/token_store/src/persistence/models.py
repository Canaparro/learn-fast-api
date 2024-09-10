import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, configure_mappers, mapped_column, relationship
from sqlalchemy_continuum import make_versioned

from common.persistence.database import Base
from services.token_store.src.service.dto import PermissionsEnum

make_versioned(user_cls=None)


class TokenPermissionModel(Base):
    __tablename__ = "token_permission"
    __versioned__: dict[str, str] = {}

    name: Mapped[PermissionsEnum] = mapped_column(primary_key=True)
    token_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("token.id"), primary_key=True
    )
    token: Mapped["TokenModel"] = relationship(back_populates="permissions")


class TokenModel(Base):
    __tablename__ = "token"
    __versioned__: dict[str, str] = {}

    instance_id: Mapped[str] = mapped_column(index=True)
    client_id: Mapped[str] = mapped_column(index=True)
    account_id: Mapped[str] = mapped_column(index=True)
    token: Mapped[str]
    expire_at: Mapped[int]
    permissions: Mapped[list[TokenPermissionModel]] = relationship(
        TokenPermissionModel,
        back_populates="token",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default_factory=uuid.uuid4)


configure_mappers()
