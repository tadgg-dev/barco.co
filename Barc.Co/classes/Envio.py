class Envio:

    @staticmethod
    def tabla_envios_existe(db):
        cursor = db.Conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='envios'")
        return cursor.fetchone() is not None

    @staticmethod
    def crear_tabla_envios(conexion):
        conexion.execute(
            """CREATE TABLE IF NOT EXISTS envios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_envio TEXT NOT NULL,
            fecha_llegada TEXT NOT NULL,
            cantidad_contenedores INTEGER NOT NULL,
            costo REAL NOT NULL,
            id_barco INTEGER NOT NULL,
            id_cliente INTEGER NOT NULL,
            id_gestor_envio INTEGER NOT NULL
            );""")
        conexion.commit()

    @staticmethod
    def agregar_envio(conexion, fecha_envio, fecha_llegada, cantidad_contenedores, costo, id_barco, id_cliente, id_gestor_envio):
        conexion.execute("""
            INSERT INTO envios (fecha_envio, fecha_llegada, cantidad_contenedores, costo, id_barco, id_cliente, id_gestor_envio)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (fecha_envio, fecha_llegada, cantidad_contenedores, costo, id_barco, id_cliente, id_gestor_envio))
        conexion.commit()

    @staticmethod
    def editar_envio(conexion, id, fecha_envio, fecha_llegada, cantidad_contenedores, costo, id_barco, id_gestor_envio):
        conexion.execute("""
            UPDATE envios
            SET fecha_envio = ?, fecha_llegada = ?, cantidad_contenedores = ?, costo = ?, id_barco = ?, id_gestor_envio = ?
            WHERE id = ?
        """, (fecha_envio, fecha_llegada, cantidad_contenedores, costo, id_barco, id_gestor_envio, id))
        conexion.commit()

    @staticmethod
    def mostrar_envios(conexion):
        cursor = conexion.get_cursor()
        cursor.execute("SELECT * FROM envios")
        return cursor.fetchall()

    @staticmethod
    def eliminar_envio(conexion, id):
        conexion.execute("DELETE FROM envios WHERE id=?", (id,))
        conexion.commit()

    @staticmethod
    def obtener_envio(conexion, id):
        cursor = conexion.get_cursor()
        cursor.execute("SELECT * FROM envios WHERE id=?", (id,))
        return cursor.fetchone()
