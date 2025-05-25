from models import Company, Dev, Freebie, Session, engine, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

print("--- Seeding Database ---")

# Get a session
session = Session()

# Clear existing data for a fresh start each time you run seed.py
session.query(Freebie).delete()
session.query(Company).delete()
session.query(Dev).delete()
session.commit()
print("Existing data cleared.")

# --- Create Companies ---
comp_a = Company(name="TechCorp", founding_year=2005)
comp_b = Company(name="InnovateLabs", founding_year=2010)
comp_c = Company(name="GadgetFlow", founding_year=2008)
comp_d = Company(name="FutureBytes", founding_year=2002) # Older company
session.add_all([comp_a, comp_b, comp_c, comp_d])
session.commit()
print("Companies created.")

# --- Create Devs ---
dev_Jason = Dev(name="Jason")
dev_Dan = Dev(name="Dan")
dev_Charlie = Dev(name="Charlie")
session.add_all([dev_Jason, dev_Dan, dev_Charlie])
session.commit()
print("Devs created.")

# Retrieve instances from the session after commit to ensure they are 'fresh'
Jason_from_db = session.query(Dev).filter_by(name="Jason").first()
Dan_from_db = session.query(Dev).filter_by(name="Dan").first()
Charlie_from_db = session.query(Dev).filter_by(name="Charlie").first()
techcorp_from_db = session.query(Company).filter_by(name="TechCorp").first()
innovatelabs_from_db = session.query(Company).filter_by(name="InnovateLabs").first()
gadgetflow_from_db = session.query(Company).filter_by(name="GadgetFlow").first()
futurebytes_from_db = session.query(Company).filter_by(name="FutureBytes").first()


# --- Create Freebies and link them ---
# Using the give_freebie method for Companies
print("\n--- Creating Freebies using give_freebie method ---")
freebie1 = techcorp_from_db.give_freebie(Jason_from_db, "T-Shirt", 25, session)
freebie2 = innovatelabs_from_db.give_freebie(Dan_from_db, "Sticker Pack", 5, session)
freebie3 = techcorp_from_db.give_freebie(Charlie_from_db, "Water Bottle", 15, session)
freebie4 = gadgetflow_from_db.give_freebie(Jason_from_db, "Pen Set", 10, session)
freebie5 = futurebytes_from_db.give_freebie(Dan_from_db, "Notebook", 12, session)
freebie6 = techcorp_from_db.give_freebie(Jason_from_db, "USB Drive", 30, session) # Jason gets another freebie from TechCorp


print("\n--- Testing Relationship Attributes and Methods ---")

# Re-query all to ensure relationships are loaded fresh
session.close() # Close session to ensure objects are reloaded if needed
session = Session() # Open a new session

# Get fresh instances for testing
Jason = session.query(Dev).filter_by(name="Jason").first()
Dan = session.query(Dev).filter_by(name="Dan").first()
Charlie = session.query(Dev).filter_by(name="Charlie").first()
techcorp = session.query(Company).filter_by(name="TechCorp").first()
innovatelabs = session.query(Company).filter_by(name="InnovateLabs").first()
gadgetflow = session.query(Company).filter_by(name="GadgetFlow").first()
futurebytes = session.query(Company).filter_by(name="FutureBytes").first()

print(f"\nJason freebies: {[f.item_name for f in Jason.freebies]}")
print(f"Jason companies: {[c.name for c in Jason.companies]}")
print(f"Dan freebies: {[f.item_name for f in Dan.freebies]}")
print(f"Dan companies: {[c.name for c in Dan.companies]}")
print(f"\nTechCorp's freebies: {[f.item_name for f in techcorp.freebies]}")
print(f"TechCorp's devs: {[d.name for d in techcorp.devs]}")
print(f"\nInnovateLabs's freebies: {[f.item_name for f in innovatelabs.freebies]}")
print(f"InnovateLabs's devs: {[d.name for d in innovatelabs.devs]}")


print("\n--- Testing Freebie.print_details() ---")
# Get a freebie instance (e.g., the T-Shirt)
tshirt_freebie = session.query(Freebie).filter_by(item_name="T-Shirt").first()
if tshirt_freebie:
    print(tshirt_freebie.print_details())

print("\n--- Testing Company.oldest_company() ---")
oldest_company = Company.oldest_company(session)
if oldest_company:
    print(f"Oldest company: {oldest_company.name} founded in {oldest_company.founding_year}")


print("\n--- Testing Dev.received_one() ---")
print(f"Jason received 'T-Shirt'? {Jason.received_one('T-Shirt')}")
print(f"Dan received 'Notebook'? {Dan.received_one('Notebook')}")
print(f"Charlie received 'Sticker Pack'? {Charlie.received_one('Sticker Pack')}") # Charlie should not have this


print("\n--- Testing Dev.give_away() ---")
usb_freebie = session.query(Freebie).filter_by(item_name="USB Drive").first()
if usb_freebie and Jason and Dan:
    print(f"Before give away: {usb_freebie.print_details()}")
    Jason.give_away(Dan, usb_freebie, session) 
    session.refresh(usb_freebie) 
    print(f"After give away: {usb_freebie.print_details()}")

    non_Jason_freebie = session.query(Freebie).filter_by(item_name="Notebook").first()
    if non_Jason_freebie:
        Jason.give_away(Charlie, non_Jason_freebie, session) 


session.close()
print("\n--- Seeding complete. ---")