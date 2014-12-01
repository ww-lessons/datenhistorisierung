# coding=utf-8

from model import UserEntity, UserVersion, ModelUtility
from User import User
from datetime import datetime


class UserRepository():
    # Verbindung zur Datenbank initialisieren
    def __init__(self):
        self.db = ModelUtility.db
        ModelUtility.Base.metadata.create_all(self.db)
        self.session = ModelUtility.SessionFactory()

    # Benutzer anlegen
    def create_user(self, user):
        # Prüfen, ob der Benutzer bereits existiert
        exists = self.session.query(UserEntity).filter(UserEntity.username == user.username).count()

        # Prüfen, ob der Benutzer bereits als gelöscht existiert
        deleted = self.session.query(UserEntity).filter(UserEntity.username == user.username).\
            filter(UserEntity.deleted).count()

        if deleted == 1:
            # Benutzerobjekt laden und wieder aktivieren
            u = self.session.query(UserEntity).filter(UserEntity.username == user.username).\
                filter(UserEntity.deleted).first()
        elif exists == 0:
            # Benuter-Basisobjekt anlegen
            u = UserEntity(username=user.username)
        else:
            # Ansonsten gibts den Benutzer schon in aktivem Zustand => Fehler!
            raise Exception("Der Benutzername {0} wird bereits verwendet".format(user.username))

        u.create_date = datetime.now()
        u.deleted = False

        # Erste Benutzerversion anlegen
        u_version = UserVersion(username=user.username)
        u_version.assigned_rolename = user.assigned_rolename
        u_version.create_date = u.create_date
        u_version.birthdate = user.birthdate
        u_version.description = user.description
        u.future_version = u_version

        self.session.add(u)
        self.session.add(u_version)
        self.session.commit()
        return u

    # Benutzer anhand des Namens mittels Schluesselzugriff ermitteln
    # (Veröffentlichter Zustand)
    def get_user_by_name(self, username):
        u = self.session.query(UserEntity).filter(UserEntity.username == username).\
            filter(UserEntity.deleted == False).first()

        user = User(username=u.username, create_date=u.create_date, deleted=u.deleted)

        if u.current_version != None:
            user.birthdate = u.current_version.birthdate
            user.assigned_rolename = u.current_version.assigned_rolename
            user.description = u.current_version.description

        return user

    # Benutzer anhand des Namens mittels Schluesselzugriff ermitteln
    # (Aktuellste unveröffentlichte Änderungen)
    def get_user_future_version_by_name(self, username):
        u = self.session.query(UserEntity).filter(UserEntity.username == username).\
            filter(UserEntity.deleted == False).first()

        user = User(username=u.username, create_date=u.create_date, deleted=u.deleted)

        if u.current_version is not None:
            user.birthdate = u.future_version.birthdate
            user.assigned_rolename = u.future_version.assigned_rolename
            user.description = u.future_version.description

        return user

    # Benutzer aktualisieren (aktualisiert den Inhalt der future_version)
    def update_user(self, user):
        u = self.session.query(UserEntity).filter(UserEntity.username == user.username).\
            filter(UserEntity.deleted == False).first()

        if u is None:
            raise Exception("Der Benutzer {0} ist gelöscht oder existiert nicht".format(user.username))

        # Benutzerversion aktualisieren
        u.future_version.assigned_rolename = user.assigned_rolename
        u.future_version.birthdate = user.birthdate
        u.future_version.description = user.description

        self.session.add(u.future_version)
        self.session.commit()

    # Eine Version freigeben und dabei eine neue Future_version anlegen
    def commit(self, username):
        u = self.session.query(UserEntity).filter(UserEntity.username == username).\
            filter(UserEntity.deleted == False).first()

        if u is None:
            raise Exception("Der Benutzer {0} ist gelöscht oder existiert nicht".format(username))

        # Neue Benutzerversion anlegen
        u_version = UserVersion(username=u.username)
        u_version.create_date = datetime.now()
        u_version.assigned_role_name = u.future_version.assigned_rolename
        u_version.birthdate = u.future_version.birthdate
        u_version.description = u.future_version.description

        # Versionen weiterschalten
        u.current_version = u.future_version
        u.future_version = u_version

        # Speichern
        self.session.add(u)
        self.session.add(u.current_version)
        self.session.add(u_version)
        self.session.commit()

    # Benutzer loeschen
    def delete_user(self, username):
        u = self.session.query(UserEntity).filter(UserEntity.username == username).\
            filter(UserEntity.deleted == False).first()

        if u is None:
            raise Exception("Der Benutzer {0} ist gelöscht oder existiert nicht".format(username))

        u.deleted = True
        future_version = u.future_version
        u.future_version = None

        self.session.delete(future_version)
        self.session.add(u)
        self.session.commit()

    # Historie eines Benutzers auslesen
    def get_history(self, username):
        user = self.session.query(UserEntity).filter(UserEntity.username == username).\
            filter(UserEntity.deleted == False).first()

        if user is None:
            raise Exception("Der Benutzer {0} ist gelöscht oder existiert nicht".format(username))

        history = user.history
        list = []
        for version in history:
            u = User(username=user.username, create_date=user.create_date, deleted=user.deleted)
            u.birthdate = version.birthdate
            u.assigned_rolename = version.assigned_rolename
            u.description = version.description
            list.append(u)

        return list

    # Eine Liste der Benutzer-Objekte erstellen
    def list_users(self):
        users = self.session.query(UserEntity).order_by(UserEntity.username).all()
        list = []

        for user in users:
            u = User(username=user.username, create_date=user.create_date, deleted=user.deleted)

            if user.current_version is not None:
                u.birthdate = user.current_version.birthdate
                u.assigned_rolename = user.current_version.assigned_rolename
                u.description = user.current_version.description

            list.append(u)

        return list
