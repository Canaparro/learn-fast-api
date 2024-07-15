from uuid import UUID, uuid4

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship, MappedAsDataclass


class Base(AsyncAttrs, MappedAsDataclass, DeclarativeBase):
    pass


association_table = Table(
    "association_table",
    Base.metadata,
    Column("token_id", ForeignKey("token.id"), primary_key=True),
    Column("permission_id", ForeignKey("permission.id"), primary_key=True),
)


class PermissionModel(Base):
    __tablename__ = "permission"

    name: Mapped[str] = mapped_column(index=True)
    id: Mapped[str] = mapped_column(primary_key=True, default_factory=uuid4)


class TokenModel(Base):
    __tablename__ = "token"

    instance_id: Mapped[str] = mapped_column(index=True)
    client_id: Mapped[str] = mapped_column(index=True)
    account_id: Mapped[str] = mapped_column(index=True)
    token: Mapped[str]
    expire_at: Mapped[int]
    permissions: Mapped[list[PermissionModel]] = relationship(
        secondary="association_table", default_factory=list
    )
    id: Mapped[str] = mapped_column(primary_key=True, default_factory=uuid4)
