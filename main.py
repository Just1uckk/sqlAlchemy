from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, insert, select, or_, desc, \
    update, bindparam, delete
from sqlalchemy.dialects import postgresql, sqlite, mysql, oracle

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

metadata = MetaData()

user_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, unique=True, autoincrement=True),
    Column('first_name', String(30)),
    Column('second_name', String)
)

address_table = Table(
    'addresses',
    metadata,
    Column('id', Integer, primary_key=True, unique=True, autoincrement=True),
    Column('email_address', String(30)),
    Column('user_id', ForeignKey('users.id'))
)

metadata.create_all(engine)

with engine.begin() as conn:
    conn.execute(
        insert(user_table),
        [
            {"first_name": "test1", "second_name": "test1 full"},
            {"first_name": "test2", "second_name": "test2 full"},
            {"first_name": "test3", "second_name": "test3 full"}
        ]
    )
    conn.execute(
        insert(address_table),
        [
            {"email_address": "test1@gmail.com", "user_id": 1},
            {"email_address": "test2@gmail.com", "user_id": 2},
            {"email_address": "test3@gmail.com", "user_id": 3}
        ]
    )


with engine.begin() as conn:
    # Update Construction
    # stmt = update(user_table).where(user_table.c.first_name == bindparam("oldname")).values(first_name=bindparam("newname"))
    # conn.execute(
    #    stmt,
    #     [
    #         {"oldname": "test1", "newname": "New Test 1"}
    #     ]
    # )

    # Delete construction
    # From single table
    conn.execute(
        delete(user_table).where(user_table.c.id == 1)
    )

    # From others tables
    # delete_stmt = (
    #     delete(user_table)
    #     .where(user_table.c.id == address_table.c.user_id)
    #     .where (address_table.c.email_adress == 'test1@gmail.com')
    # )
    # conn.execute(
    #     delete_stmt
    # )


    print(conn.execute(select(user_table)).all())
