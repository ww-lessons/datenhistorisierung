# coding=utf-8

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref


class ModelUtility():
    # Connectionstring ggf. anpassen siehe:
    # http://docs.sqlalchemy.org/en/rel_0_9/dialects/mysql.html
    db = create_engine('mysql+mysqlconnector://root:test1234@localhost:3306/historisierung_none')
    Base = declarative_base(db)
    SessionFactory = sessionmaker(bind=db)


class Permission(ModelUtility.Base):
    __tablename__ = 'tbl_role_permission'

    rolename = Column(String(50),
                      ForeignKey('tbl_role.rolename'),
                      primary_key=True)
    permission = Column(String(50), primary_key=True)


class Role(ModelUtility.Base):
    __tablename__ = 'tbl_role'

    rolename = Column(String(50), primary_key=True)
    last_change_date = Column(DateTime())
    last_changed_by = Column(String(50))
    permissions = relationship("Permission",
                               backref=backref('role'),
                               cascade="all, delete, delete-orphan")


class User(ModelUtility.Base):
    __tablename__ = 'tbl_user'

    username = Column(String(50), primary_key=True)
    description = Column(String(256))
    birthdate = Column(Date)
    assigned_rolename = Column(String(50), ForeignKey('tbl_role.rolename'))
    assigned_role = relationship("Role")