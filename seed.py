from app.database import Session
from app.models import Dev, Company, Freebie

session = Session()

# Clear previous records
session.query(Freebie).delete()
session.query(Company).delete()
session.query(Dev).delete()
session.commit()

# Seed data
c1 = Company(name="Google", founding_year=1998)
c2 = Company(name="Airbnb", founding_year=2008)
d1 = Dev(name="Alice")
d2 = Dev(name="Bob")

f1 = Freebie(item_name="Tote Bag", value=10, company=c1, dev=d1)
f2 = Freebie(item_name="Sticker Pack", value=5, company=c1, dev=d2)
f3 = Freebie(item_name="Notebook", value=8, company=c2, dev=d1)

session.add_all([c1, c2, d1, d2, f1, f2, f3])
session.commit()

print("Database seeded!")