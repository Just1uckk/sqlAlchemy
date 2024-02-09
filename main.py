from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, insert
from sqlalchemy.dialects import postgresql, sqlite, mysql, oracle

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

metadata = MetaData()

user_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, unique=True, autoincrement=True),
    Column('name', String(30)),
    Column('fullname', String)
)

address_table = Table(
    'addresses',
    metadata,
    Column('id', Integer, primary_key=True, unique=True, autoincrement=True),
    Column('email_address', String(30)),
    Column('user_id', ForeignKey('users.id'))
)

metadata.create_all(engine)

stmt = insert(user_table).values(name='Test', fullname='Test Test')
# print(stmt.compile(engine, sqlite.dialect()))
# print(stmt.compile(engine, postgresql.dialect()))
# print(stmt.compile(engine, mysql.dialect()))
# print(stmt.compile(engine, oracle.dialect()))

stmt_wo_values = insert(user_table)

sqlite_stmt = stmt_wo_values.compile(engine, sqlite.dialect())
postgresql_stmt = stmt_wo_values.compile(engine, postgresql.dialect())

with engine.begin() as conn:
    result = conn.execute(
        stmt_wo_values,
        [
            {"name": "test1", "fullname": "test1 full"},
            {"name": "test2", "fullname": "test2 full"},
            {"name": "test3", "fullname": "test3 full"}
         ]
    )