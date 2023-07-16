from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import config
from models import Base, User, Address

engine = create_engine(
    url=config.SQLALCHEMY_URL,
    echo=config.SQLALCHEMY_ECHO,
)


def create_user(session: Session, name: str, username: str):
    user = User(
        name=name,
        username=username,
    )


def main():
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        user = User(
            name = "John Smith",
            username="john",
            addresses=[
                Address(
                    email="john@example.com"
                ),
                Address(
                    email="john.smith@example.gov"
                ),
            ]
        )
        session.add(user)
        session.commit()


if __name__ == '__main__':
    main()
