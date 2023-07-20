import sqlalchemy
from sqlalchemy.orm import sessionmaker

from db.models import Base, Students


class DB:
    _path_to_db: str = 'test.db'

    def __init__(self):
        self.engine = sqlalchemy.create_engine(f'sqlite:///{self._path_to_db}')
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

        print('Database and table created')

    # def connector(self, method):
    #     def wrapper(*args):
    #         Session = sessionmaker(bind=self.engine)
    #
    #         with Session(bind=self.engine) as session:
    #             method(*args)
    #     return wrapper

    def add_student(self, name: str, age: int):

        with self.Session(bind=self.engine) as session:
            student = Students(name=name, age=age)
            session.add(student)
            session.commit()
            session.refresh(student)

        print(f'Student with id {student.id} and name {student.name} was successfully added')

    def get_all_students(self):

        with self.Session(bind=self.engine) as session:
            students = session.query(Students).all()

        return students

    def get_student_by_name(self, student_name: str):

        with self.Session(bind=self.engine) as session:
            students = session.query(Students).filter(Students.name == student_name).first()

        return students

    def update_student(self, id: int, name: str = None, age: int = None):

        with self.Session(bind=self.engine) as session:
            student = session.query(Students).filter(Students.id==id).first()

            if student:
                print(
                    f'Before change:\n'
                    f'ID: {student.id}\n'
                    f'Name: {student.name}\n'
                    f'Age: {student.age}\n'
                )

                if name:
                    student.name = name
                if age:
                    student.age = age

                session.commit()

                student = session.query(Students).filter(Students.id == id).first()

                print(f'After change:\n'
                      f'ID: {student.id}\n'
                      f'Name: {student.name}\n'
                      f'Age: {student.age}\n')

            else:
                print('Record not found.')

    def delete_by_id(self, id: int):

        with self.Session(bind=self.engine) as session:
            student = session.get(Students, id)

            if not student:
                print("Record not found")
                return False

            else:
                session.delete(student)
                session.commit()
                print('Student successfully deleted')
