# coding=utf-8

from model import ModelUtility, RoleEntity, RoleVersion, Permission
from Role import Role
from datetime import datetime


class RoleRepository():

    # Verbindung zur Datenbank initialisieren
    def __init__(self):
        self.db = ModelUtility.db
        ModelUtility.Base.metadata.create_all(self.db)
        self.session = ModelUtility.SessionFactory()

    # Benutzer anlegen
    def create_role(self, role):
        # Prüfen, ob die Rolle bereits existiert
        exists = self.session.query(RoleEntity).filter(RoleEntity.rolename == role.rolename).count()

        # Prüfen, ob der Benutzer bereits als gelöscht existiert
        deleted = self.session.query(RoleEntity).filter(RoleEntity.rolename == role.rolename).\
            filter(RoleEntity.deleted).count()

        if deleted == 1:
            # Benutzerobjekt laden und wieder aktivieren
            r = self.session.query(RoleEntity).filter(RoleEntity.rolename == role.rolename).\
                filter(RoleEntity.deleted).first()
        elif exists == 0:
            # Benuter-Basisobjekt anlegen
            r = RoleEntity(rolename=role.rolename)
        else:
            # Ansonsten gibts den Benutzer schon in aktivem Zustand => Fehler!
            raise Exception("Der Rollenname {0} wird bereits verwendet".format(role.rolename))

        r.create_date = datetime.now()
        r.deleted = False

        r_version = RoleVersion(role=r)
        r_version.create_date = r.create_date
        r_version.last_change_date = datetime.now()
        r_version.last_changed_by = "unbekannt"
        r.future_version = r_version

        for permission in role.permissions:
            r_version.permissions.append(Permission(role_version=r_version, permission=permission))

        self.session.add(r)
        self.session.add(r_version)
        self.session.commit()

        return r

    # Eine Version freigeben und dabei eine neue future_version anlegen
    def commit(self, rolename):
        r = self.session.query(RoleEntity).filter(RoleEntity.rolename == rolename).\
            filter(RoleEntity.deleted == False).first()

        if r is None:
            raise Exception("Die Rolle {0} ist gelöscht oder existiert nicht".format(rolename))

        # Neue Rollenversion anlegen
        r_version = RoleVersion(role=r)
        r_version.create_date = datetime.now()
        r_version.last_change_date = datetime.now()
        r_version.last_changed_by = "unbekannt"
        for permission in r.future_version.permissions:
            r_version.permissions.append(Permission(role_version=r_version, permission=permission.permission))

        # Versionen weiterschalten
        r.current_version = r.future_version
        r.future_version = r_version

        # Speichern
        self.session.add(r)
        self.session.add(r.current_version)
        self.session.add(r_version)
        self.session.commit()

    # Rolle anhand des Namens mittels Schluesselzugriff ermitteln
    # (Current_Version)
    def get_role_by_name(self, rolename):
        r = self.session.query(RoleEntity).filter(RoleEntity.rolename == rolename).\
            filter(RoleEntity.deleted == False).first()

        if r is None:
            raise Exception("Die Rolle {0} ist gelöscht oder existiert nicht".format(rolename))

        role = Role(rolename=r.rolename)
        role.deleted = r.deleted
        role.create_date = r.create_date
        role.permissions = []

        for permission in r.current_version.permissions:
            role.permissions.append(permission.permission)

        return role

    # Rolle anhand des Namens mittels Schluesselzugriff ermitteln
    # (Future_Version)
    def get_role_future_version_by_name(self, rolename):
        r = self.session.query(RoleEntity).filter(RoleEntity.rolename == rolename).\
            filter(RoleEntity.deleted == False).first()

        if r is None:
            raise Exception("Die Rolle {0} ist gelöscht oder existiert nicht".format(rolename))

        role = Role(rolename=r.rolename)
        role.deleted = r.deleted
        role.create_date = r.create_date
        role.permissions = []

        for permission in r.future_version.permissions:
            role.permissions.append(permission.permission)

        return role

    # Benutzer aktualisieren
    def update_role(self, role):
        r = self.session.query(RoleEntity).filter(RoleEntity.rolename == role.rolename).\
            filter(RoleEntity.deleted == False).first()

        if r is None:
            raise Exception("Die Rolle {0} ist gelöscht oder existiert nicht".format(role.rolename))

        r.future_version.permissions = []

        for permission in role.permissions:
            r.future_version.permissions.append(Permission(role_version=r.future_version, permission=permission))

        r.future_version.last_change_date = datetime.now()
        r.future_version.last_changed_by = "unbekannt"

        self.session.add(r.future_version)
        self.session.commit()

    # Benutzer loeschen
    def delete_role(self, rolename):
        r = self.session.query(RoleEntity).filter(RoleEntity.rolename == rolename).\
            filter(RoleEntity.deleted == False).first()

        if r is None:
            raise Exception("Die Rolle {0} ist entweder bereits gelöscht oder existiert nicht".format(rolename))

        r.deleted = True
        self.session.delete(r.future_version)
        self.session.commit()

    # Eine Liste der Benutzer-Objekte erstellen
    def list_roles(self):
        roles = self.session.query(RoleEntity).filter(RoleEntity.deleted == False).all()

        result = []
        for role in roles:
            r = Role(rolename=role.rolename)
            r.create_date = role.create_date
            r.deleted = False
            r.permissions = []
            # wenn noch keine current_version existiert
            if role.current_version is None:
                for permission in role.future_version.permissions:
                    r.permissions.append(permission.permission)
            # ansonsten natürlich die current_version verwenden
            else:
                for permission in role.current_version.permissions:
                    r.permissions.append(permission.permission)

            result.append(r)

        return result

    # Historie einer Rolle auslesen
    def get_history(self, rolename):
        role = self.session.query(RoleEntity).filter(RoleEntity.rolename == rolename).\
            filter(RoleEntity.deleted == False).first()

        if role is None:
            raise Exception("Die Rolle {0} ist gelöscht oder existiert nicht".format(rolename))

        history = role.history
        result = []
        for version in history:
            r = Role(rolename=role.rolename, create_date=role.create_date, deleted=role.deleted)

            r.permissions = []
            for permission in version.permissions:
                r.permissions.append(permission.permission)
            result.append(r)

        return result
