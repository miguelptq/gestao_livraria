import sqlite3

#1 Ligar a base de dados
conn = sqlite3.connect('livraria.db')

#2 Criar um cursor
cursor = conn.cursor()

#3 Commando sql para criar a tabela
#id interger pk
#utilizador text not null unique
#password text not null

create_table_roles = '''
        CREATE TABLE IF NOT EXISTS roles(
            id INTEGER PRIMARY KEY,
            role_name VARCHAR(50) NOT NULL
        )
    '''
cursor.execute(create_table_roles)
insert_table_roles= '''
    INSERT INTO roles (role_name) VALUES
                ('Client'),
                ('Employer'),
                ('SuperAdmin');
'''
cursor.execute(insert_table_roles)
create_table_permissions = '''
        CREATE TABLE IF NOT EXISTS permissions (
            id INTEGER PRIMARY KEY,
            permission_name VARCHAR(50) NOT NULL
        )
    '''
cursor.execute(create_table_permissions)
insert_table_permissions = '''
    INSERT INTO PERMISSIONS (permission_name) VALUES
        ('Search Books'),
        ('Request Books'),
        ('Return Books'),
        ('Insert Books'),
        ('Remove Books'),
        ('Update Books'),
        ('Insert New Users'),
        ('List Users')
'''
cursor.execute(insert_table_permissions)
create_table_users = '''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            role_id INT DEFAULT 1,
            FOREIGN KEY (role_id) REFERENCES roles(id)
        );
    '''
cursor.execute(create_table_users)
insert_table_users = '''
    INSERT INTO users (username,password,email,role_id) VALUES
        ('admin', '4e7151c133a036376e3535ed5d68b895:50a5a898edad10aa2094f585f6c2185c5611ce67d537bf3f2e6279d287bd9a91','admin@gmail.com',3)
'''
cursor.execute(insert_table_users)

create_table_user_permissions ='''CREATE TABLE user_permissions (
        user_id INT,
        permission_id INT,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (permission_id) REFERENCES permissions(id),
        PRIMARY KEY (user_id, permission_id)
    )'''
cursor.execute(create_table_user_permissions)
insert_user_permissions =  """
    INSERT INTO user_permissions (user_id, permission_id)
        SELECT users.id, permissions.id
        FROM users
        JOIN roles ON users.role_id = roles.id
        JOIN permissions ON permissions.permission_name IN ('Search Books', 'Request Books', 'Return Books', 'Insert Books', 'Remove Books', 'Update Books', 'Insert New Users', 'Change User Permissions','List Users')
        WHERE roles.role_name = 'SuperAdmin';
        """
cursor.execute(insert_user_permissions)
#4 Executar o comando SQL com o cursor
tabela_livro = '''
    CREATE TABLE IF NOT EXISTS livro(
        isbn_livro TEXT PRIMARY KEY,
        nome_livro TEXT NOT NULL,
        desc_livro TEXT NOT NULL,
        ano_livro DATE NOT NULL
    )
'''
cursor.execute(tabela_livro)

tabela_autor = '''
    CREATE TABLE IF NOT EXISTS autor_livro(
        isbn_livro TEXT,
        nome_autor TEXT NOT NULL,
        FOREIGN KEY (isbn_livro) REFERENCES livro (isbn_livro)
    )
'''
cursor.execute(tabela_autor)

#5 Guardar com um commit
conn.commit()

#6 Fechar a ligação
conn.close()

print('guardado com sucesso')