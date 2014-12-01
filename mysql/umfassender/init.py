from model import ModelUtility, RoleEntity, RoleVersion
from datetime import datetime

db = ModelUtility.db
ModelUtility.Base.metadata.create_all(db)
session = ModelUtility.SessionFactory()

# Beispielrolle anlegen
r = RoleEntity(rolename="Beispielrolle")
r.create_date = datetime.now()
r.deleted = False

session.add(r)
session.commit()