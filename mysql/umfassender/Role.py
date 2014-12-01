# coding=utf-8


class Role():
    def __init__(self, rolename, create_date=None,
                 deleted=False, permissions=[]):
        self.rolename = rolename
        self.create_date = create_date
        self.deleted = deleted
        self.permissions = permissions