# coding=utf-8

from RolesRepository import RolesRepository

__author__ = 'wiw39784'

import unittest


DATABASE = 'demodb'
ROLENAME = 'MusterRole'


class RolesInObjectHistoryTests(unittest.TestCase):

    def test_create_role(self):
        repo = RolesRepository(DATABASE)
        role = repo.create_role(ROLENAME)
        self.assertEqual(role.rolename, ROLENAME)

    def test_list_roles(self):
        repo = RolesRepository(DATABASE)
        list = repo.list_roles()

        for item in list:
            print item

        self.assertEqual(2, len(list))

    def test_update_role_empty(self):
        repo = RolesRepository(DATABASE)
        role = repo.get_role_by_name(ROLENAME)

        role.permissions = []

        repo.update_role(role)

        role2 = repo.get_role_by_name(ROLENAME)
        self.assertEqual(role.id, role2.id)
        self.assertEqual(len(role.permissions), len(role2.permissions))

    def test_update_role(self):
        repo = RolesRepository(DATABASE)
        role = repo.get_role_by_name(ROLENAME)

        role.permissions.append("Beispielrecht 1")
        role.permissions.append("Beispielrecht 2")
        role.permissions.append("Beispielrecht 3")

        repo.update_role(role)

        role2 = repo.get_role_by_name(ROLENAME)
        self.assertEqual(role.id, role2.id)
        self.assertEqual(len(role.permissions), len(role2.permissions))

    def test_show_history(self):
        repo = RolesRepository(DATABASE)
        rolle = repo.get_role_by_name(ROLENAME)
        for version in rolle.previous_versions:
            print "{0} {1} {2} {3}".format(rolle.rolename, version.version_create_date, version.version_created_by,
                                           version.version_valid_until)

            for permission in version.permissions:
                print "Permission: {0}".format(permission)

    def test_xdelete_role(self):
        repo = RolesRepository(DATABASE)
        repo.delete_role("MusterRole")


if __name__ == '__main__':
    unittest.main()

