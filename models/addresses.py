from typing import TYPE_CHECKING, Iterable

from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, joinedload

from . import Base
from . import User

# Ето вроде как решает проблему циклического импорта, но я не уверен... именно ли ето оно делает
if TYPE_CHECKING:
    from .users import User


class Address(Base):
    __tablename__ = "addresses"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="addresses")


# Добавление адреса к данным микрочелика, можно задать по юзернейму
# но сейчас будет работать только если перед ним юзать функцию fetch_user()
def add_addresses(session: Session, user: User, *emails: str) -> None:
    user.addresses = [
        Address(email=email)
        for email in emails
    ]
    session.commit()


# Выборка адресов всех юзеров
def show_addresses(session: Session):
    stmt = select(Address).options(
        # Делаем выборку всего одним запросом благодаря джоинлоад
        joinedload(Address.user)
    )
    addresses: Iterable[Address] = session.scalars(stmt)
    for address in addresses:
        print("[@]", address.email)
        print(" +", address.user)


# Создаём юзера с емейлом (тоже нету проверки на уникальность username потом добавлю обязательно)
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
