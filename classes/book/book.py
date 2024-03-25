import sqlite3


class Book:
    def __init__(self, isbn_livro=None, nome_livro=None, desc_livro=None, ano_livro=None, borrowed=False, user_id=None):
        self._isbn_livro = isbn_livro
        self._nome_livro = nome_livro
        self._desc_livro = desc_livro
        self._ano_livro = ano_livro
        self._borrowed = borrowed
        self._user_id=user_id

    def get_isbn(self):
        return self._isbn_livro

    def set_isbn(self, isbn):
        self._isbn_livro = isbn

    def get_title(self):
        return self._nome_livro

    def set_title(self, title):
        self._nome_livro = title

    def get_desc(self):
        return self._desc_livro

    def set_desc(self, desc):
        self._desc_livro = desc

    def get_year(self):
        return self._ano_livro

    def set_year(self, year):
        self._ano_livro = year

    def get_borrowed(self):
        return self._borrowed

    def set_borrowed(self, borrowed):
        self._borrowed = borrowed

    def get_user_id(self):
        return self._user_id

    def set_user_id(self, user_id):
        self._user_id = user_id
    
    def create(self, authors = []):
        if not self._isbn_livro or not self._nome_livro or not self._desc_livro or not self._ano_livro or len(authors) == 0:
            return False, "Error: ISBN, Title, Description, Year and authors must be provided..","Red"

        # Ligar a Base de Dados
        conn = sqlite3.connect('livraria.db')

        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO livro (isbn_livro, nome_livro, desc_livro, ano_livro) VALUES (?, ?, ?, ?)", (self._isbn_livro, self._nome_livro, self._desc_livro, self._ano_livro)
            )
            for autor in authors:  # Iterate over all authors
                cursor.execute(
                    "INSERT INTO autor_livro (isbn_livro, nome_autor) VALUES (?, ?)", (self._isbn_livro, autor)
                )
            # Commit the transaction
            conn.commit()
            return True, f"The Book {self._nome_livro} was created successfully.", "Green"
        except sqlite3.IntegrityError:
            # User with the same name or email already exists
            return False, "Error: ISBN is already in use.","Red"
        finally:
            # Close the connection
            conn.close()
        
        
