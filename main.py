from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import config
from models import Base
from models import create_user, create_user_with_emails, show_users, fetch_user, delete_user
from models import show_addresses, add_addresses


engine = create_engine(
    url=config.SQLALCHEMY_URL,
    echo=config.SQLALCHEMY_ECHO,
)


def main():
    Base.metadata.create_all(bind=engine)
    #вот ета конструкция даёт нам возможность не писать после каждой функции комит что упрощает жизнь
    with Session(engine) as session:
        pass
        # delete_user(session, "bob")

        # create_user(
        #     session=session,
        #     name="John Brown",
        #     username="jbrown",
        # )

        # create_user(
        #     session=session,
        #     name="Bob White",
        #     username="bob",
        # )

        # create_user_with_emails(
        #     session=session,
        #     name="Michael Black",
        #     username="mbboy",
        #     emails=[
        #         "michaeln@example.com",
        #         "michael.black@example.gov",
        #     ]
        # )

        # user = fetch_user(session, "bob")
        # add_addresses(session, user, "bob@example.com")
        # show_addresses(session)


if __name__ == '__main__':
    main()
