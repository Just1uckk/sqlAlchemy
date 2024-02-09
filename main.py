from sqlalchemy import create_engine, Integer, String, ForeignKey, BigInteger, select
from sqlalchemy.orm import registry, declarative_base, as_declarative, sessionmaker, declared_attr, Mapped, \
    mapped_column, Session

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

# mapper_registry = registry()
# Base = mapper_registry.generate_base()

# Base = declarative_base()

@as_declarative()
class AbstractModel:
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    @classmethod
    @declared_attr
    def table_name(cls) -> str:
        return cls.__name__.lower()

class UserModel(AbstractModel):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column()
    fullname: Mapped[str] = mapped_column()

class AddressModel(AbstractModel):
    __tablename__ = "addresses"
    email = mapped_column(String, nullable=False)
    user_id = mapped_column(ForeignKey("users.id"))

with Session(engine) as session:
    with session.begin():
        AbstractModel.metadata.create_all(engine)
        user = UserModel(user_id=1, name='Adnry', fullname='Horpynych')
        session.add(user)
    with session.begin():
        res = session.execute(select(UserModel).where(UserModel.user_id == 1))
        user = res.scalar()
        print(user)