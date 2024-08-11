import uuid

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship, configure_mappers
from sqlalchemy_continuum import make_versioned

from token_store.persistence.database import Base
from token_store.service.dto import PermissionsEnum

make_versioned(user_cls=None)


class TokenPermissionModel(Base):
    __tablename__ = "token_permission"
    __versioned__ = {}

    name: Mapped[PermissionsEnum] = mapped_column(Enum(PermissionsEnum), primary_key=True, name="token_permission_enum")
    token_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("token.id"), primary_key=True)
    token: Mapped["TokenModel"] = relationship(back_populates="permissions")


class TokenModel(Base):
    __versioned__ = {}
    __tablename__ = "token"

    instance_id: Mapped[str] = mapped_column(index=True)
    client_id: Mapped[str] = mapped_column(index=True)
    account_id: Mapped[str] = mapped_column(index=True)
    token: Mapped[str]
    expire_at: Mapped[int]
    permissions: Mapped[list[TokenPermissionModel]] = relationship(
        TokenPermissionModel,
        back_populates="token",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default_factory=uuid.uuid4)


configure_mappers()
