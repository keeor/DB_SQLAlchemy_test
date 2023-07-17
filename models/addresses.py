from typing import TYPE_CHECKING, Iterable

from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, joinedload

from . import Base
from . import User

if TYPE_CHECKING:
    from .users import User


class Address(Base):
    __tablename__ = "addresses"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")


def add_addresses(session: Session, user: User, *emails: str) -> None:
    user.addresses = [
        Address(email=email)
        for email in emails
    ]
    session.commit()


def show_addresses(session: Session):
    stmt = select(Address).options(
        joinedload(Address.user)
    )
    addresses: Iterable[Address] = session.scalars(stmt)
    for address in addresses:
        print("[@]", address.email)
        print(" +", address.user)


def create_user_with_emails(
        session: Session,
        name: str,
        username: str,
        emails: list[str]
) -> User:
    addresses = [

        Address(email=email)
        for email in emails
    ]
    user = User(
        name=name,
        username=username,
        addresses=addresses,
    )
    session.add(user)

    session.commit()

    return user
