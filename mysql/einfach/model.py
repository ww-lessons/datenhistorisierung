# coding=utf-8

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from datetime import datetime


class ModelUtility():
    # Connectionstring ggf. anpassen siehe:
    # http://docs.sqlalchemy.org/en/rel_0_9/dialects/mysql.html
    db = create_engine('mysql+mysqlconnector://root:test1234@localhost:3306/historisierung_simple')
    Base = declarative_base(db)
    SessionFactory = sessionmaker(bind=db)
    NullTimeStamp = datetime.strptime("0001-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')


class Role(ModelUtility.Base):
    __tablename__ = 'tbl_role'

    rolename = Column(String(50), primary_key=True)
    valid_until = Column(DateTime(), default=ModelUtility.NullTimeStamp, primary_key=True)
    last_change_date = Column(DateTime())
    last_changed_by = Column(String(50))
    permissions = relationship("Permission", backref=backref('role'), cascade="all, delete, delete-orphan")


class Permission(ModelUtility.Base):
    __tablename__ = 'tbl_role_permission'

    rolename = Column(String(50), primary_key=True)
    valid_until = Column(DateTime(), default=ModelUtility.NullTimeStamp, primary_key=True)
    permission = Column(String(50), primary_key=True)

    __table_args__ = (ForeignKeyConstraint([rolename, valid_until],
                                           [Role.rolename, Role.valid_until]),
                      {})


class User(ModelUtility.Base):
    __tablename__ = 'tbl_user'

    username = Column(String(50), primary_key=True)
    valid_until = Column(DateTime(), default=ModelUtility.NullTimeStamp, primary_key=True)
    description = Column(String(256))
    birthdate = Column(Date)
    assigned_rolename = Column(String(50), ForeignKey('tbl_role.rolename'))
    assigned_role = relationship("Role")