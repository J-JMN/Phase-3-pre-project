# freebie_app_project/models.py

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import func # For aggregate functions like min()


# --- Database Setup ---
DATABASE_FILE = './freebie_app.db'
engine = create_engine(f'sqlite:///{DATABASE_FILE}')
Session = sessionmaker(bind=engine)
Base = declarative_base()


# --- Define Models ---
class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    founding_year = Column(Integer, nullable=False)

    freebies = relationship('Freebie', back_populates='company', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}', founding_year={self.founding_year})>"

    # --- Company Specific Methods ---
    @property
    def devs(self):
        # We find all freebies given by this company, and then collect the unique devs from those freebies.
        # We use a set comprehension to ensure uniqueness.
        return list(set(freebie.dev for freebie in self.freebies))

    def give_freebie(self, dev_instance, item_name, value, session):
        """
        Creates a new Freebie instance associated with this company and the given dev.
        Requires an active session to add and commit the new freebie.
        """
        if not isinstance(dev_instance, Dev):
            raise TypeError("dev argument must be an instance of Dev class.")

        new_freebie = Freebie(
            item_name=item_name,
            value=value,
            company=self,  
            dev=dev_instance 
        )
        session.add(new_freebie)
        session.commit()
        return new_freebie # Return the newly created freebie

    @classmethod
    def oldest_company(cls, session):
        """
        Returns the Company instance with the earliest founding year.
        Requires an active session to query the database.
        """
        return session.query(cls).order_by(cls.founding_year.asc()).first()


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Dev has many Freebies
    freebies = relationship('Freebie', back_populates='dev', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Dev(id={self.id}, name='{self.name}')>"

    # --- Dev Specific Methods ---
    @property
    def companies(self):
        # We find all freebies collected by this dev, and then collect the unique companies from those freebies.
        return list(set(freebie.company for freebie in self.freebies))

    def received_one(self, item_name):
        """
        Accepts an item_name (string) and returns True if any of the freebies
        associated with the dev has that item_name, otherwise returns False.
        """
        for freebie in self.freebies:
            if freebie.item_name == item_name:
                return True
        return False

    def give_away(self, new_owner_dev, freebie_to_give, session):
        """
        Accepts a Dev instance (new_owner_dev) and a Freebie instance (freebie_to_give),
        changes the freebie's dev to be the given dev.
        The change only occurs if the freebie belongs to the dev who's giving it away (self).
        Requires an active session to commit the change.
        """
        if not isinstance(new_owner_dev, Dev):
            raise TypeError("new_owner_dev must be an instance of Dev class.")
        if not isinstance(freebie_to_give, Freebie):
            raise TypeError("freebie_to_give must be an instance of Freebie class.")

        # Check if the freebie actually belongs to the current dev (self)
        if freebie_to_give.dev_id == self.id:
            freebie_to_give.dev = new_owner_dev # Reassign the relationship
            session.add(freebie_to_give) 
            session.commit()
            print(f"'{freebie_to_give.item_name}' given away by {self.name} to {new_owner_dev.name}.")
            return True
        else:
            print(f"'{freebie_to_give.item_name}' does not belong to {self.name}. Cannot give away.")
            return False


class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)

    # Foreign Keys:
    dev_id = Column(Integer, ForeignKey('devs.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)

    # Freebie belongs to a Dev
    dev = relationship('Dev', back_populates='freebies')
    # Freebie belongs to a Company
    company = relationship('Company', back_populates='freebies')

    def __repr__(self):
        return f"<Freebie(id={self.id}, item_name='{self.item_name}', value={self.value}, dev_id={self.dev_id}, company_id={self.company_id})>"

    # --- Freebie Specific Methods ---

    def print_details(self):
        """
        Returns a string formatted as: {dev name} owns a {freebie item_name} from {company name}.
        """
        # Ensure relationships are loaded (lazy loading will handle this if not already)
        dev_name = self.dev.name if self.dev else "Unknown Dev"
        company_name = self.company.name if self.company else "Unknown Company"
        return f"{dev_name} owns a {self.item_name} from {company_name}."