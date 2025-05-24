from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    # One-to-many: company to freebies
    freebies = relationship("Freebie", back_populates="company")

    def give_freebie(self, dev, item_name, value):
        from .models import Freebie
        return Freebie(item_name=item_name, value=value, company=self, dev=dev)

    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()

    def __repr__(self):
        return f"<Company {self.name}, est. {self.founding_year}>"

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    freebies = relationship("Freebie", back_populates="dev")

    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, freebie, other_dev):
        if freebie in self.freebies:
            freebie.dev = other_dev

    def __repr__(self):
        return f"<Dev {self.name}>"

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)

    company_id = Column(Integer, ForeignKey('companies.id'))
    dev_id = Column(Integer, ForeignKey('devs.id'))

    company = relationship("Company", back_populates="freebies")
    dev = relationship("Dev", back_populates="freebies")

    def print_details(self):
        print(f"{self.dev.name} owns a {self.item_name} from {self.company.name}.")

    def __repr__(self):
        return f"<Freebie {self.item_name} (${self.value})>"