class Cliente:

    @staticmethod
    def tabla_clientes_envios_existe(db):
        cursor = db.Conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clientes_envios'")
        return cursor.fetchone() is not None

    @staticmethod
    def crear_tabla_clientes_envios(conexion):
        conexion.execute(
            """CREATE TABLE IF NOT EXISTS clientes_envios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dni TEXT NOT NULL,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT,
            email TEXT NOT NULL,
            nacionalidad TEXT
            );""")
        conexion.commit()

    @staticmethod
    def agregar_cliente_envio(conexion, dni, nombre, apellido, telefono, email, nacionalidad):
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO clientes_envios (dni, nombre, apellido, telefono, email, nacionalidad)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (dni, nombre, apellido, telefono, email, nacionalidad))
        conexion.commit()

    @staticmethod
    def editar_cliente_envio(conexion, id, dni, nombre, apellido, telefono, email, nacionalidad):
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE clientes_envios
            SET dni = ?, nombre = ?, apellido = ?, telefono = ?, email = ?, nacionalidad = ?
            WHERE id = ?
        """, (dni, nombre, apellido, telefono, email, nacionalidad, id))
        conexion.commit()

    @staticmethod
    def mostrar_clientes_envios(conexion):
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientes_envios")
        return cursor.fetchall()

    @staticmethod
    def eliminar_cliente_envio(conexion, dni):
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes_envios WHERE dni=?", (dni,))
        conexion.commit()

    @staticmethod
    def obtener_cliente_envio(conexion, id):
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientes_envios WHERE id=?", (id,))
        return cursor.fetchone()
    
    @staticmethod
    def obtener_cliente_envio_por_dni(conexion, dni):
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientes_envios WHERE dni=?", (dni,))
        return cursor.fetchone()
