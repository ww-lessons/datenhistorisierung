# coding=utf-8

import couchdb
from model import Role
from datetime import datetime


class RolesRepository():

    TYPE_KEY = 'role_inobject_hist'

    # Verbindung zur Datenbank initialisieren
    def __init__(self, db_name):
        server = couchdb.client.Server()

        if server.__contains__(db_name):
            self.db = server[db_name]
        else:
            self.db = server.create(db_name)


    # Benutzer anlegen
    def create_role(self, rolename, permissions=[]):
        r = Role(rolename=rolename, permissions=permissions)
        r.id = self.calculate_id(rolename)
        r.create_date = datetime.now()
        r.change_date = r.create_date
        r.created_by = "UNBEKANNT"
        r.type = self.TYPE_KEY
        r.store(self.db)
        return r


    # Benutzer anhand des Namens mittels Schluesselzugriff ermitteln
    def get_role_by_name(self, rolename):
        r = Role.load(self.db, self.calculate_id(rolename))
        return r


    # Benutzer aktualisieren
    def update_role(self, role):
        r = Role.load(self.db, role.id)

        # 1. Bisherigen Stand in die Historie schreiben
        r.previous_versions.append(
            permissions=r.permissions,
            version_create_date=r.change_date,
            version_created_by='UNBEKANNT',
            version_valid_until=datetime.now()
        )

        # 2. Daten aktualisieren
        r.permissions = role.permissions
        r.change_date = datetime.now()

        r.store(self.db)


    # Benutzer loeschen
    def delete_role(self, rolename):
        del self.db[self.calculate_id(rolename)]


    # Eine Liste der Benutzer-Objekte erstellen
    def list_roles(self):
        map_function = "function(doc) { if(doc.type =='"+self.TYPE_KEY+"') { emit(doc.rolename, doc); }}"
        return self.db.query(map_function)


    # Private Methode: IDs fuer Benutzer aus deren Benutzernamen berechnen
    def calculate_id(self, rolename):
        return '{0}|{1}'.format(self.TYPE_KEY, rolename)