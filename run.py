from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)

# Crear las tablas dentro del contexto de la aplicación
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    clientes = Cliente.query.all()
    return render_template('index.html', clientes=clientes)

@app.route('/agregar', methods=['POST'])
def agregar_cliente():
    nombre = request.form.get('nombre')
    direccion = request.form.get('direccion')
    telefono = request.form.get('telefono')
    
    nuevo_cliente = Cliente(nombre=nombre, direccion=direccion, telefono=telefono)
    db.session.add(nuevo_cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente agregado correctamente'})

@app.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_cliente(id):
    cliente = Cliente.query.get(id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
        return jsonify({'message': 'Cliente eliminado correctamente'})
    return jsonify({'message': 'Cliente no encontrado'}), 404

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get(id)
    if request.method == 'POST':
        cliente.nombre = request.form.get('nombre')
        cliente.direccion = request.form.get('direccion')
        cliente.telefono = request.form.get('telefono')
        db.session.commit()
        return jsonify({'message': 'Cliente actualizado correctamente'})
    
    return render_template('editar.html', cliente=cliente)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
