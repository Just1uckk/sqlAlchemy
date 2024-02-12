from sqlalchemy import create_engine,ForeignKey, select

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, session, Session, joinedload

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

class Base (DeclarativeBase):
    pass

class User (Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    addresses: Mapped[list["Address"]] = relationship(back_populates="user", uselist=True, lazy="selectin")

    def __repr__(self) -> str:
        return f'User: {self.id=}:{self.name=}:{self.age=}'

class Address (Base):
    __tablename__ = 'addresses'
    email: Mapped[str] = mapped_column(primary_key=True)
    user: Mapped["User"] = relationship(back_populates="addresses", uselist=False)
    user_fk: Mapped[int] = mapped_column(ForeignKey('users.id'))

    def __repr__(self) -> str:
        return f'Address: {self.email=}:{self.user_fk=}'

# class UserAdress(Base):
#     __tablename__ = 'user_address'
#     user_fk = mapped_column(ForeignKey('users.id'), primary_key=True)
#     address_fk = mapped_column(ForeignKey('addresses.email'), primary_key=True)
#
#     def __repr__(self) -> str:
#         return f'<UserAddress: {self.user_fk=}:{self.address_fk=}'

Base.metadata.create_all(engine)

session = Session(engine, expire_on_commit=True, autoflush=True)

user = User(id=1, name="Test1", age=30)
address1 = Address(email="test1@test.com")
address2 = Address(email="test2@test.com")
user.addresses.append(address1)
user.addresses.append(address2)
session.add(user)
session.commit()

user = session.scalar(select(User))

print(user.addresses)
