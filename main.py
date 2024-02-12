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
    # uselist=False one-to-one relationship
    addresses: Mapped[list["Address"]] = relationship(back_populates="users", uselist=True, secondary="user_address")

    def __repr__(self) -> str:
        return f'User: {self.id=}:{self.name=}:{self.age=}'

class Address (Base):
    __tablename__ = 'addresses'
    email: Mapped[str] = mapped_column(primary_key=True)
    # uselist=False one-to-one relationship
    users: Mapped[list["User"]] = relationship(back_populates="addresses", uselist=True, secondary="user_address")
    # user_fk: Mapped[int] = mapped_column(ForeignKey('users.id'))

    def __repr__(self) -> str:
        return f'Address: {self.email=}'

class UserAdress(Base):
    __tablename__ = 'user_address'
    user_fk = mapped_column(ForeignKey('users.id'), primary_key=True)
    address_fk = mapped_column(ForeignKey('addresses.email'), primary_key=True)

    def __repr__(self) -> str:
        return f'<UserAddress: {self.user_fk=}:{self.address_fk=}'

Base.metadata.create_all(engine)

session = Session(engine, expire_on_commit=True, autoflush=True)

user1 = User(id=1, name="Test1", age=30)
user2 = User(id=2, name="Test2", age=20)
address1 = Address(email="test1@test.com")
address2 = Address(email="test2@test.com")
user1.addresses.append(address1)
user1.addresses.append(address2)
user2.addresses.append(address1)
user2.addresses.append(address2)
session.add(user1)
session.add(user2)
session.commit()

users = session.scalars(select(User)).all()
addresses = session.scalars(select(Address)).all()
user_secondary = session.scalars(select(UserAdress)).all()

print(users)
print(addresses)
print(user_secondary)
