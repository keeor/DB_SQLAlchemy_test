from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import config
from models import Base, create_user, create_user_with_emails, show_users, fetch_user, show_addresses, add_addresses

engine = create_engine(
    url=config.SQLALCHEMY_URL,
    echo=config.SQLALCHEMY_ECHO,
)


def main():
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        # create_user(
        #     session=session,
        #     name="John Brown",
        #     username="jbrown",
        # )
        #
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
        # user = fetch_user(session, "Bob White")
        # print("Bob White?", user)
        # add_addresses(session, user, "bob@example.com")
        # show_addresses(session)


if __name__ == '__main__':
    main()
