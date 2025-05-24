from app.database import Session
from app.models import Dev, Company, Freebie

session = Session()

# 🧠 Check before inserting to avoid duplication
def get_or_create(model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        params = {**kwargs}
        if defaults:
            params.update(defaults)
        instance = model(**params)
        session.add(instance)
        session.commit()
        return instance

# Seed devs
d1 = get_or_create(Dev, name="Alice")
d2 = get_or_create(Dev, name="Bob")
d3 = get_or_create(Dev, name="Charlie")  
d4 = get_or_create(Dev, name="Diana")
d5 = get_or_create(Dev, name="Eve")
d6 = get_or_create(Dev, name="Frank")
d7 = get_or_create(Dev, name="Grace")

# Seed companies
c1 = get_or_create(Company, name="Google", defaults={"founding_year": 1998})
c2 = get_or_create(Company, name="Airbnb", defaults={"founding_year": 2008})
c3 = get_or_create(Company, name="OpenAI", defaults={"founding_year": 2015})  
c4 = get_or_create(Company, name="Meta", defaults={"founding_year": 2004})
c5 = get_or_create(Company, name="Microsoft", defaults={"founding_year": 1975})
c6 = get_or_create(Company, name="Amazon", defaults={"founding_year": 1994})
c7 = get_or_create(Company, name="Apple", defaults={"founding_year": 1976})

# Seed freebies with logic to prevent duplicates
def create_freebie(item_name, value, company, dev):
    existing = session.query(Freebie).filter_by(
        item_name=item_name,
        company_id=company.id,
        dev_id=dev.id
    ).first()
    if not existing:
        f = Freebie(item_name=item_name, value=value, company=company, dev=dev)
        session.add(f)
        session.commit()

create_freebie("Tote Bag", 10, c1, d1)
create_freebie("Sticker Pack", 5, c1, d2)
create_freebie("Notebook", 8, c2, d1)
create_freebie("Laptop Skin", 20, c3, d3)  
create_freebie("T-Shirt", 15, c4, d4)
create_freebie("Mug", 12, c5, d5)
create_freebie("Water Bottle", 10, c6, d6)
create_freebie("Headphones", 50, c7, d7)

print("Database updated with new unique data!")
