import asyncio
from db import DB


async def main():
    database = DB()

    # database.add_student(
    #     name='Мария Иванова',
    #     age=15
    # )

    # for student in database.get_all_students():
    #     print(f'{student.id}: {student.name}')

    # query_result = database.get_student_by_name(student_name='Мария Ежова')
    # print(f'{query_result.id}')

    # database.update_student(id=1, name='Виктория Зеленая')

    database.delete_by_id(3)

if __name__ == "__main__":
    asyncio.run(main())
