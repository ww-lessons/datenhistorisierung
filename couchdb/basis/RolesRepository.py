# Controller-Klasse

__author__ = 'wiw39784'

from datetime import datetime

import couchdb
from model import Role


class RolesRepository():
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
        r.type = 'role'
        r.store(self.db)
        return r


    # Benutzer anhand des Namens mittels Schluesselzugriff ermitteln
    def get_role_by_name(self, rolename):
        r = Role.load(self.db, self.calculate_id(rolename))
        return r


    # Benutzer aktualisieren
    def update_role(self, role):
        r = Role.load(self.db, role.id)

        r.permissions = role.permissions
        r.last_change_date = datetime.now()
        r.last_changed_by = 'blubblub'

        r.store(self.db)


    # Benutzer loeschen
    def delete_role(self, rolename):
        del self.db[self.calculate_id(rolename)]


    # Eine Liste der Benutzer-Objekte erstellen
    def list_roles(self):
        map_function = "function(doc) { if(doc.type =='role') { emit(doc.rolename, doc); }}";
        return self.db.query(map_function)


    # Private Methode: IDs fuer Benutzer aus deren Benutzernamen berechnen
    @staticmethod
    def calculate_id(rolename):
        return 'role|' + rolename
