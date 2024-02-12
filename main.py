from sqlalchemy import create_engine,ForeignKey, select

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, session, Session

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

class Base (DeclarativeBase):
    pass

class User (Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    # uselist=False one-to-one relationship
    address: Mapped["Address"] = relationship(back_populates="user",uselist=False)

    def __repr__(self) -> str:
        return f'User: {self.id=}:{self.name=}:{self.age=}'

class Address (Base):
    __tablename__ = 'addresses'
    email: Mapped[str] = mapped_column(primary_key=True)
    # uselist=False one-to-one relationship
    user: Mapped["User"] = relationship(back_populates="address", uselist=False)
    user_fk: Mapped[int] = mapped_column(ForeignKey('users.id'))

    def __repr__(self) -> str:
        return f'Address: {self.email=}:{self.user_fk=}'

Base.metadata.create_all(engine)

session = Session(engine, expire_on_commit=True, autoflush=False)

user = User(id=1, name="Test", age=30)
address = Address(email="test@test.com")
user.address = address
session.add(user)
session.commit()

users = session.scalars(select(User)).all()
address = session.scalars(select(Address)).all()

print(users)
print(address)
