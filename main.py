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
    addresses: Mapped[list["Address"]] = relationship(back_populates="user", uselist=True)

    def __repr__(self) -> str:
        return f'User: {self.id=}:{self.name=}:{self.age=}'

class Address (Base):
    __tablename__ = 'addresses'
    email: Mapped[str] = mapped_column(primary_key=True)
    # uselist=False one-to-one relationship
    user: Mapped["User"] = relationship(back_populates="addresses", uselist=False)
    user_fk: Mapped[int] = mapped_column(ForeignKey('users.id'))

    def __repr__(self) -> str:
        return f'Address: {self.email=}:{self.user_fk=}'

Base.metadata.create_all(engine)

session = Session(engine, expire_on_commit=True, autoflush=True)

user = User(id=1, name="Test", age=30)
address1 = Address(email="test1@test.com")
address2 = Address(email="test2@test.com")
user.addresses.append(address1)
user.addresses.append(address2)
session.add(user)
session.commit()

user = session.scalar(select(User))

print(user)
print(user.addresses)
