from typing import TYPE_CHECKING, Iterable

from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, selectinload

from . import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str | None]

    addresses: Mapped[list["Address"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
       return f"User(id={self.id!r}, name={self.name!r}, username={self.username!r})"

    def __repr__(self) -> str:
        return str(self)


def create_user(session: Session, name: str, username: str) -> User:
    user = User(
        name=name,
        username=username,
    )
    session.add(user)
    session.commit()

def fetch_user(session: Session, name: str) -> User | None:
    stmt = select(User).where(User.name == name)
    user: User | None = session.execute(stmt).scalar_one()
    return user


def show_users(session: Session):
    stmt = select(User).options(
        selectinload(User.addresses),
    )
    users: Iterable[User] = session.scalars(stmt)
    for user in users:
        print("[+]", user)
        for address in user.addresses:  # type: Address
            print(" - @", address.email)
