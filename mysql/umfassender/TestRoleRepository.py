# coding=utf-8

import unittest
import time

from RoleRepository import RoleRepository
from Role import Role

ROLENAME = 'Musterrolle2'


class SimpleHistoryMySQLTestCase(unittest.TestCase):
    def test_1_create_role(self):
        repo = RoleRepository()
        r1 = Role(rolename=ROLENAME)
        r1.permissions = ['Berechtigung 1', 'Berechtigung 2', 'Berechtigung 3']
        role = repo.create_role(r1)
        self.assertEqual(role.rolename, ROLENAME)

    def test_2_commit(self):
        repo = RoleRepository()
        repo.commit(ROLENAME)

    def test_3_get_role_by_name(self):
        repo = RoleRepository()
        r = repo.get_role_by_name(ROLENAME)
        print "{0} {1} {2}".format(r.rolename, r.create_date, r.permissions)
        self.assertEqual(r.rolename, ROLENAME)
        self.assertEqual(r.permissions[0], 'Berechtigung 1')

    def test_1_get_role_future_version_by_name(self):
        repo = RoleRepository()
        r = repo.get_role_future_version_by_name(ROLENAME)
        print "{0} {1} {2}".format(r.rolename, r.create_date, r.permissions)
        self.assertEqual(r.rolename, ROLENAME)
        self.assertEqual(r.permissions[0], 'Berechtigung 1')

    # List Roles mit current_version
    def test_3_list_roles(self):
        repo = RoleRepository()
        role_list = repo.list_roles()

        for item in role_list:
            print "{0} {1}".format(item.rolename, item.deleted)

        self.assertGreaterEqual(len(role_list), 1)

    # List Roles mit future_version
    def test_1_list_roles(self):
        repo = RoleRepository()
        role_list = repo.list_roles()

        for item in role_list:
            print "{0} {1}".format(item.rolename, item.deleted)

        self.assertGreaterEqual(len(role_list), 1)

    def test_4_update_role_empty(self):
        time.sleep(1)
        repo = RoleRepository()
        role = repo.get_role_by_name(ROLENAME)
        role.permissions = []

        repo.update_role(role)
        repo.commit(ROLENAME)

        role2 = repo.get_role_by_name(ROLENAME)
        self.assertEqual(len(role.permissions), len(role2.permissions))

    def test_5_update_role(self):
        repo = RoleRepository()
        role = repo.get_role_by_name(ROLENAME)

        role.permissions = ['Bespielrecht1', 'Beispielrecht2', 'Beispielrecht3']

        repo.update_role(role)
        repo.commit(ROLENAME)

        role2 = repo.get_role_by_name(ROLENAME)
        self.assertEqual(len(role.permissions), len(role2.permissions))

    def test_6_get_history(self):
        repo = RoleRepository()
        role = repo.get_role_by_name(ROLENAME)
        history = repo.get_history(ROLENAME)

        print "History for Role {0}:{1}:".format(role.rolename, role.create_date)
        for version in history:
            print "    Version {0}:{1}:{2}".format(version.rolename, version.create_date, version.permissions)

    def test_9_delete_role(self):
        repo = RoleRepository()
        repo.delete_role(ROLENAME)


if __name__ == '__main__':
    unittest.main()
