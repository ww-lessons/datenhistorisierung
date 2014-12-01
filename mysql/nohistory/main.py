# coding=utf-8

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

#
# Vor dem Durchlauf des Skripts manuell die Tabellen löschen:
# drop table `historisierung_none`.`tbl_role_permission`;
# drop table `historisierung_none`.`tbl_user`;
# drop table `historisierung_none`.`tbl_role`;
#

#db = create_engine('mysql+mysqlconnector://demo:demo@localhost:3306/historisierung_none')
db = create_engine('mysql+mysqlconnector://root:test1234@localhost:3306/historisierung_none')
Base = declarative_base(db)
SessionFactory = sessionmaker(bind=db)


class Permission(Base):
    __tablename__ = 'tbl_role_permission'

    rolename = Column(String(50), ForeignKey('tbl_role.rolename'), primary_key=True)
    permission = Column(String(50), primary_key=True)
    role = relationship("Role", backref=backref('permissions'))


class Role(Base):
    __tablename__ = 'tbl_role'

    rolename = Column(String(50), primary_key=True)
    last_change_date = DateTime()
    last_changed_by = String(50)


class User(Base):
    __tablename__ = 'tbl_user'

    username = Column(String(50), primary_key=True)
    description = Column(String(256))
    birthdate = Column(Date)
    assigned_role_name = Column(String(50), ForeignKey('tbl_role.rolename'))
    assigned_role = relationship("Role")


Base.metadata.create_all(db)

session = SessionFactory()
u = User(username='Musteruser.Max', birthdate='2000-01-01')
session.add(u)

r = Role(rolename='Beispielrolle')
session.add(r)

session.commit()

u.assigned_role = r

session.commit()

p1 = Permission(rolename=r.rolename, permission='Recht1')
session.add(p1)
p2 = Permission(rolename=r.rolename, permission='Recht2')
session.add(p2)
p3 = Permission(rolename=r.rolename, permission='Recht3')
session.add(p3)

session.commit()

print "Version 1: "
for perm in r.permissions:
    print "{0} {1}".format(perm.rolename, perm.permission)

p1 = Permission(role=r, permission='Recht4')
session.add(p1)
p2 = Permission(role=r, permission='Recht5')
session.add(p2)
p3 = Permission(role=r, permission='Recht6')
session.add(p3)

session.commit()

print "\nVersion 2: "
for perm in r.permissions:
    print "{0} {1}".format(perm.rolename, perm.permission)