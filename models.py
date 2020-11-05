from sqlalchemy import Table, Column, Integer, Date, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Receivers(Base):
    __tablename__ = 'receivers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address_part_1 = Column(String)
    address_part_2 = Column(String)

class Senders(Base):
    __tablename__ = 'senders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address_part_1 = Column(String)
    address_part_2 = Column(String)
    phone = Column(String)
    email = Column(String)
    siren = Column(String)
    bank_details_name = Column(String)
    bank_details_bank = Column(String)
    bank_details_iban = Column(String)
    bank_details_bic = Column(String)

class Bills(Base):
    __tablename__ = 'bills_with_number'

    id = Column(Integer, primary_key=True)
    number = Column(String)
    date = Column(Date)
    sender_id = Column(Integer, ForeignKey('senders.id'))
    receiver_id = Column(Integer, ForeignKey('receivers.id'))

class BillsWithoutNumber(Base):
    __tablename__ = 'bills'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    sender_id = Column(Integer, ForeignKey('senders.id'))
    receiver_id = Column(Integer, ForeignKey('receivers.id'))


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bill_id = Column(Integer, ForeignKey('bills_with_number.id'))
    quantity = Column(Integer)
    description = Column(String)
    unitary_price = Column(Float)
