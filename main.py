from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, insert, select, or_, desc
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
# .label - set a key
with engine.begin() as conn:
    result = conn.execute(
        select(
            address_table.c.email_address.label('email'),
            (user_table.c.first_name + ' ' + user_table.c.second_name).label('full_name')
        ).where(
            user_table.c.id > 0
        )
        # ).join_from(user_table, address_table, user_table.c.id == address_table.c.user_id)
        .join(address_table, isouter=True)
        .order_by(
            # desc - back order
            # desc(user_table.c.id)
            # user_table.c.id.desc()
            # or by name of field
            "email"
        )
        # .group_by - grouping
        .group_by(
            "email"
        )
    )

    print(result.all())


