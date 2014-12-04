from Role import Role
from RoleRepository import RoleRepository

repo = RoleRepository()
r1 = Role(rolename="Beispielrolle")
r1.permissions = ['Berechtigung 1']
role = repo.create_role(r1)