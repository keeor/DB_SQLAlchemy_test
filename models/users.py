from typing import TYPE_CHECKING, Iterable

from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, selectinload

from . import Base

# Ето вроде как решает проблему циклического импорта, но я не уверен... именно ли ето оно делает
if TYPE_CHECKING:
    from . import Address


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str | None] = mapped_column(String(15), unique=True)
    addresses: Mapped[list["Address"]] = relationship(
        "Address",
        back_populates="user",
        cascade="all, delete, delete-orphan"
    )

    # то ето такое я пока не понял, в гайде сказали нужно...
    def __str__(self) -> str:
       return f"User(id={self.id!r}, name={self.name!r}, username={self.username!r})"

    def __repr__(self) -> str:
        return str(self)


# Создаем обычного юзера, без адреса (юзернейм должен быть уникален, но пока проверки на ето нету)
def create_user(session: Session, name: str, username: str) -> User:
    user = User(
        name=name,
        username=username,
    )
    session.add(user)
    session.commit()


# Ето вроде как просто запрос на поиск юзера, хз зачем сделал, было в гайде)
def fetch_user(session: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    user: User | None = session.execute(stmt).scalar_one()
    return user


# Функция показа юзера (вывод в комм. строку)
def show_users(session: Session):
    stmt = select(User).options(
        selectinload(User.addresses),
        # selectinload юзаем дл того что-бы уменьшить кол-во запросов sql
        # (так получается одним запросом всё что нужно вывести)
    )
    users: Iterable[User] = session.scalars(stmt)
    for user in users:
        print("[+]", user)
        for address in user.addresses:  # type: Address
            print(" - @", address.email)


# Хуйня кривая но работает, делаем запрос на посик user по username и вытягиваем его id
# id нужен для удаления из других таблиц ибо так прописаны связи
# PS. нейминг у меня страдает)
def delete_user(session: Session, username: str):
    stmt = select(User).where(User.username == username)
    x = session.execute(stmt).scalar_one()
    y = session.query(User).get(x.id)
    session.delete(y)
    session.commit()


def update_user_name(session: Session, username: str, name: str):
    usr = session.query(User).filter(User.username == username).first()
    if usr is not None:
        usr.name = name
        session.commit()
    else:
        print("!User not found!")
