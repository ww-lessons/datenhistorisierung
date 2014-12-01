# coding=utf-8

import unittest
import time

from RoleRepository import RoleRepository

ROLENAME = 'Musterrolle'


class SimpleHistoryMySQLTestCase(unittest.TestCase):
    def test_create_role(self):
        repo = RoleRepository()
        role = repo.create_role(ROLENAME)
        self.assertEqual(role.rolename, ROLENAME)

    def test_list_roles(self):
        repo = RoleRepository()
        list = repo.list_roles()

        for item in list:
            print item

        self.assertEqual(2, len(list))

    def test_update_role_empty(self):
        time.sleep(1)
        repo = RoleRepository()
        role = repo.get_role_by_name(ROLENAME)

        repo.update_role(role, [])

        role2 = repo.get_role_by_name(ROLENAME)
        self.assertEqual(len(role.permissions), len(role2.permissions))

    def test_update_role(self):
        repo = RoleRepository()
        role = repo.get_role_by_name(ROLENAME)

        permissions = ['Bespielrecht1', 'Beispielrecht2', 'Beispielrecht3']

        repo.update_role(role, permissions)

        role2 = repo.get_role_by_name(ROLENAME)
        self.assertEqual(len(role.permissions), len(role2.permissions))

    def test_get_history(self):
        repo = RoleRepository()
        role = repo.get_role_by_name(ROLENAME)
        history = repo.get_history(ROLENAME)

        print "History for Role {0}:{1}:".format(role.rolename, role.valid_until)
        for version in history:
            permissions = []
            for permission in version.permissions:
                permissions.append(permission.permission)
            print "    Version {0}:{1}:{2}".format(version.rolename, version.valid_until, permissions)

    def test_xdelete_role(self):
        repo = RoleRepository()
        repo.delete_role(ROLENAME)


if __name__ == '__main__':
    unittest.main()
