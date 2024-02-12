from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, insert, select, or_
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
    result = conn.execute(
        insert(user_table),
        [
            {"first_name": "test1", "second_name": "test1 full"},
            {"first_name": "test2", "second_name": "test2 full"},
            {"first_name": "test3", "second_name": "test3 full"}
        ]
    )

with engine.begin() as conn:
    # c - columns
    result = conn.execute(
        # Default operation
        # select(user_table).where(user_table.c.name == "test1")

        # AND operation

        # select(user_table).where(
        #     user_table.c.name.startswith("test"),
        #     user_table.c.fullname.contains("3")
        # )

        # OR operation ( we can use _or or _and ... )
        # Also we can set columns user_table.c.id

        # select(user_table).where(
        #     or_(user_table.c.name.startswith("test2"),
        #     user_table.c.fullname.contains("3"))
        # )

        # IN operation
        select(user_table.c.id).where(
            user_table.c.id.in_([1,2])
        )
    )

# mappings => []
print(result.mappings().all())
