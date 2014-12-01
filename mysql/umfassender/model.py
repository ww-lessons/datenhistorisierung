# coding=utf-8

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from datetime import datetime


class ModelUtility():
    # Connectionstring ggf. anpassen siehe:
    # http://docs.sqlalchemy.org/en/rel_0_9/dialects/mysql.html
    db = create_engine('mysql+mysqlconnector://root:test1234@localhost:3306/historisierung_full')
    Base = declarative_base(db)
    SessionFactory = sessionmaker(bind=db)


class Permission(ModelUtility.Base):
    __tablename__ = 'tbl_role_permission'

    role_version_id = Column(Integer, ForeignKey('tbl_role_version.role_version_id'), primary_key=True)
    permission = Column(String(50), primary_key=True)


class RoleVersion(ModelUtility.Base):
    __tablename__ = 'tbl_role_version'

    role_version_id = Column(Integer, primary_key=True)
    rolename = Column(String(50), ForeignKey('tbl_role.rolename'))
    create_date = Column(DateTime, default=datetime.now())
    last_change_date = DateTime()
    last_changed_by = String(50)
    permissions = relationship("Permission", backref=backref('role_version'), cascade="all, delete, delete-orphan")
    role = relationship("RoleEntity", foreign_keys=[rolename], backref=backref('history'))


class RoleEntity(ModelUtility.Base):
    __tablename__ = 'tbl_role'

    rolename = Column(String(50), primary_key=True)
    create_date = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)
    future_version_id = Column(Integer, ForeignKey('tbl_role_version.role_version_id',
                                                   use_alter=True, name='fk_r_future_version_id'))
    current_version_id = Column(Integer, ForeignKey('tbl_role_version.role_version_id',
                                                    use_alter=True, name='fk_r_current_version_id'))
    future_version = relationship("RoleVersion", foreign_keys=[future_version_id],
                                  backref=backref('future_of'),
                                  #cascade="all, delete, delete-orphan",
                                  post_update=True)
    current_version = relationship("RoleVersion", foreign_keys=[current_version_id],
                                   backref=backref('current_of'),
                                   #cascade="all, delete, delete-orphan",
                                   post_update=True)


class UserVersion(ModelUtility.Base):
    __tablename__ = 'tbl_user_version'

    user_version_id = Column(Integer, primary_key=True)
    username = Column(String(50), ForeignKey('tbl_user.username'))
    create_date = Column(DateTime, default=datetime.now())
    description = Column(String(256))
    birthdate = Column(Date)
    assigned_rolename = Column(String(50), ForeignKey('tbl_role.rolename'))
    assigned_role = relationship("RoleEntity")
    user = relationship("UserEntity", foreign_keys=[username], backref=backref('history'))


class UserEntity(ModelUtility.Base):
    __tablename__ = 'tbl_user'

    username = Column(String(50), primary_key=True)
    create_date = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)
    future_version_id = Column(Integer,
                               ForeignKey('tbl_user_version.user_version_id',
                                          use_alter=True, name='fk_u_future_version_id'))
    current_version_id = Column(Integer,
                                ForeignKey('tbl_user_version.user_version_id',
                                           use_alter=True, name='fk_u_current_version_id'))
    future_version = relationship("UserVersion", foreign_keys=[future_version_id],
                                  backref=backref('future_of'),
                                  #cascade="all, delete, delete-orphan",
                                  post_update=True)
    current_version = relationship("UserVersion", foreign_keys=[current_version_id],
                                   backref=backref('current_of'),
                                   #cascade="all, delete, delete-orphan",
                                   post_update=True)