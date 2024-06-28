import sqlite3

class Conexion:
    def __init__(self, nombre_bd):
        self.conexion = sqlite3.connect(nombre_bd)
        self.cursor_sqlite = self.conexion.cursor()

    def execute(self, query, params=None):
        if params is None:
            params = []
        self.cursor_sqlite.execute(query, params)

    def commit(self):
        self.conexion.commit()

    def close(self):
        self.cursor_sqlite.close()
        self.conexion.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get_cursor(self):
        return self.cursor_sqlite
