from models import Company, Dev, Freebie, Session, engine, Base
import ipdb

print("Entering debug session. Models (Company, Dev, Freebie), Session, engine, Base are available.")
print("Use 'session = Session()' to create a new session.")
print("Remember to use 'session.commit()' to save changes or 'session.rollback()' on error.")
ipdb.set_trace()