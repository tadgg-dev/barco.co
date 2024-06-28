from flask import Flask, g, render_template, request
from database.Conexion import Conexion
from classes.Cliente import Cliente
from classes.Envio import Envio

app = Flask(__name__)

DATABASE = 'database/barc_co.db'

def get_db():
    if 'db' not in g:
        g.db = Conexion(DATABASE)
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.Conexion.close()

def inicializar_datos():
    with get_db() as db:
        if not Cliente.tabla_clientes_envios_existe(db):
            Cliente.crear_tabla_clientes_envios(db)
            Cliente.agregar_cliente_envio(db, '43634567', 'Tadeo', 'Graziano', '42323232', 'tadegraziano@gmail.com', 'Argentino')
            Cliente.agregar_cliente_envio(db, '30433213', 'Pepe', 'Geroni', '10202020', 'pepe@gmail.com', 'Bolivia')
        
        if not Envio.tabla_envios_existe(db):
            Envio.crear_tabla_envios(db)
            Envio.agregar_envio(db, '2024-12-10', '2024-12-13', 10, 9990.00, 1, 1, 1)
            Envio.agregar_envio(db, '2024-06-07', '2024-06-13', 20, 19000.00, 1, 2, 1)

@app.route('/')
def index():
    inicializar_datos()
    return render_template('index.html')  

@app.route('/add_envio', methods=['GET', 'POST'])
def add_envio():
    return render_template('add_envio.html')

@app.route('/guardar_envio_nuevo', methods=['GET', 'POST'])
def guardar_envio_nuevo():
    if request.method == 'POST':

        
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        email = request.form['email']
        nacionalidad = request.form['nacionalidad']

        
        dni = request.form['dni']
        fecha_envio = request.form['fecha_envio']
        fecha_llegada = request.form['fecha_llegada']
        cantidad_contenedores = int(request.form['cantidad_contenedores'])
        costo = float(request.form['costo'])
        id_envio_gestor = 1
        id_barco = 1 

        cliente = Cliente.obtener_cliente_envio_por_dni(get_db(), dni)
        if cliente is None:
            Cliente.agregar_cliente_envio(get_db(), dni, nombre, apellido, telefono, email, nacionalidad)
        
        id_cliente = Cliente.obtener_cliente_envio_por_dni(get_db(), dni)[0]
        
        Envio.agregar_envio(get_db(), fecha_envio, fecha_llegada, cantidad_contenedores, costo, id_barco, id_cliente, id_envio_gestor)

        return render_template('index.html')
    return render_template('index.html')

@app.route('/view_envio', methods=['GET', 'POST'])
def view_envio():
       if request.method == 'POST':
        try:
            dni = int(request.form['dni'])
            numero_envio = int(request.form['numero_envio'])
        except ValueError:
             return render_template('view_envio.html', envio=None, cliente=None)

        envio = Envio.obtener_envio(get_db(), numero_envio)
        
        if envio is None:
            return render_template('view_envio.html', envio=None, cliente=None)
        
        cliente = Cliente.obtener_cliente_envio(get_db(), int(envio[4]))

        if dni != int(cliente[1]):
            return render_template('view_envio.html', envio=None, cliente=None)
        
        return render_template('view_envio.html', envio=envio, cliente=cliente)
    
    

@app.route('/edit_envio', methods=['GET', 'POST'])
def edit_envio():
    if request.method == 'POST':
        id_envio = request.form['id_envio']
        nombre_cliente = request.form['cliente']
        fecha_envio = request.form['fecha_envio']
        fecha_llegada = request.form['fecha_llegada']
        cantidad_contenedores = request.form['cantidad_contenedores']
        costo = request.form['costo']
        id_barco = request.form['id_barco']
        id_envio_gestor = request.form['id_envio_gestor']

        return render_template('edit_envio.html', id_envio= id_envio, nombre_cliente=nombre_cliente, fecha_envio=fecha_envio,fecha_llegada=fecha_llegada,cantidad_contenedores=cantidad_contenedores,costo=costo,id_barco=id_barco,id_envio_gestor=id_envio_gestor)
    return render_template('edit_envio.html',id_envio= None, nombre_cliente=None, fecha_envio=None,fecha_llegada=None,cantidad_contenedores=None,costo=None,id_barco=None,id_envio_gestor=None)

@app.route('/guardar_envio_nuevo', methods=['GET', 'POST'])
def guardar_envio_editado():
    if request.method == 'POST':
        try:
            id_envio = int(request.form['id_envio'])
            fecha_envio = request.form['fecha_envio']
            fecha_llegada = request.form['fecha_llegada']
            cantidad_contenedores = int(request.form['cantidad_contenedores'])
            costo = float(request.form['costo'])
            id_barco = request.form['id_barco']
            id_envio_gestor = request.form['id_envio_gestor']

            Envio.editar_envio(get_db(), id_envio, fecha_envio, fecha_llegada, cantidad_contenedores, costo, id_barco, id_envio_gestor)
            return render_template('index.html')

        except ValueError:
            return "Invalid input data: ", 400

    return render_template('index.html')

@app.route('/eliminar_envio', methods=['GET', 'POST'])
def eliminar_envio():
    if request.method == 'POST':
        id_envio = request.form['id_envio']
        Envio.eliminar_envio(get_db(),id_envio)

        return render_template('index.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
