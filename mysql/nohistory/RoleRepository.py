# coding=utf-8

from model import ModelUtility, Role, Permission
from datetime import datetime


class RoleRepository():

    # Verbindung zur Datenbank initialisieren
    def __init__(self):
        self.db = ModelUtility.db
        ModelUtility.Base.metadata.create_all(self.db)
        self.session = ModelUtility.SessionFactory()

    # Benutzer anlegen
    def create_role(self, rolename, permissions=[]):
        r = Role(rolename=rolename)

        for permission in permissions:
            r.permissions.append(Permission(rolename=r.rolename, permission=permission))

        self.session.add(r)
        self.session.commit()
        return r

    # Benutzer anhand des Namens mittels Schluesselzugriff ermitteln
    def get_role_by_name(self, rolename):
        r = self.session.query(Role).filter(Role.rolename == rolename).first()
        return r

    # Benutzer aktualisieren
    def update_role(self, role, permissions):
        r = self.session.query(Role).filter(Role.rolename == role.rolename).first()

        r.permissions = []

        for permission in permissions:
            r.permissions.append(Permission(rolename=r.rolename, permission=permission))

        r.last_change_date = datetime.now()
        r.last_changed_by = 'blub'

        self.session.add(r)
        self.session.commit()

    # Benutzer loeschen
    def delete_role(self, rolename):
        r = self.session.query(Role).filter(Role.rolename == rolename).first()
        self.session.delete(r)
        self.session.commit()

    # Eine Liste der Benutzer-Objekte erstellen
    def list_roles(self):
        return self.session.query(Role).all()

