from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import config
from models import Base, User, Address

engine = create_engine(
    url=config.SQLALCHEMY_URL,
    echo=config.SQLALCHEMY_ECHO,
)


def create_user(session: Session, name: str, username: str) -> User:
    user = User(
        name=name,
        username=username,
    )
    session.add(user)
    session.commit()

    return user


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


def fetch_user(session: Session, name: str) -> User | None:
    stmt = select(User).where(User.name == name)
    user: User | None = session.execute(stmt).scalar_one()
    return user


def main():
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:

        # create_user(
        #     session=session,
        #     name="Bob White",
        #     username="bob",
        # )
        #
        # create_user_with_emails(
        #     session=session,
        #     name="Michael Black",
        #     username="mbboy",
        #     emails=[
        #         "michaeln@example.com",
        #         "michael.black@example.gov",
        #     ]
        # )
        user = fetch_user(session, "Bob White")
        print("Bob White?", user)


if __name__ == '__main__':
    main()
