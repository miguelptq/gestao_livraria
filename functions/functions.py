import sqlite3


def list_permissions(user, role = None):
    
    if role is None:
        
        conn = sqlite3.connect('livraria.db')

        cursor = conn.cursor()
        cursor.execute("""SELECT p.permission_name 
                        FROM users u 
                        JOIN user_permissions up ON u.id = up.user_id 
                        JOIN permissions p ON up.permission_id = p.id WHERE u.id = ?""",(user['id'],))
        permissions = tuple(permission[0] for permission in cursor.fetchall())
    elif role == "Employer":
        permissions = ('Search Books','Request Books','Return Books')
    elif role  == "SuperAdmin":
        permissions = ('Search Books','Request Books','Return Books', 'Insert Books','Remove Books', 'Update Books', 'Insert New Users', 'List Users')
    return permissions

def get_role_id(role_name):
    conn = sqlite3.connect('livraria.db')

    cursor = conn.cursor()
    cursor.execute("""
        SELECT id from roles WHERE role_name = ?
    """, (role_name,))
    role_id = cursor.fetchone()
    return role_id[0]

def list_roles_depending_role(role_name):
    role_list =  {
        "SuperAdmin":{('Employer',1),('SuperAdmin',1),('Client',1)},
        "Employer": {('Employer', 0),('Client',1)}
    }
    return role_list[role_name]
    