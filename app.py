from flask import Flask, render_template, redirect, url_for, request
from flask_migrate import Migrate
from datetime import date

from database import db
from models import Usuario, Reserva, Mesa
from forms import UsuarioForm, ReservaForm, FechaForm

app = Flask(__name__)

#Configuracion de la bd
USER_DB = 'root'
PASS_DB = ''
URL_DB = 'localhost'
NAME_DB = 'restaurante_flask_db'
PORT_DB = 3307
FULL_URL_DB = f'mysql+pymysql://{USER_DB}:{PASS_DB}@{URL_DB}:{PORT_DB}/{NAME_DB}?charset=utf8mb4'


app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Inicializacion del objeto db de sqlalchemy
db.init_app(app)

#Configurar flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

app.config['SECRET_KEY'] = 'SecretKey.32'

@app.route('/')
@app.route('/index.html')
def inicio():
    return render_template('index.html')

@app.route('/registrar', methods=['GET','POST'])
def registrar():
    usuario = Usuario()
    usuarioForm = UsuarioForm(obj=usuario)

    if request.method == 'POST':
        if usuarioForm.validate_on_submit():
            usuarioForm.populate_obj(usuario)

            db.session.add(usuario)
            db.session.commit()
            return redirect(url_for('inicio'))

    return render_template('registrar.html', formulario = usuarioForm)

@app.route('/reservar',  methods=['GET','POST'])
def reservar():
    reserva = Reserva()
    usuario = Usuario()
    mesa = Mesa()
    reservaForm = ReservaForm(obj=reserva)
    reservaForm.id_usuario.choices = [(usuario.id_usuario, usuario.cedula) for usuario in Usuario.query.all()]
    reservaForm.id_mesa.choices = [(mesa.id_mesa, mesa.id_mesa) for mesa in Mesa.query.all()]

    if request.method == 'POST':
        print(reservaForm.errors)

        if reservaForm.validate_on_submit():

            reservaForm.populate_obj(reserva)
            print(f'insertando {reservaForm.id_mesa.data}')

            db.session.add(reserva)
            db.session.commit()

            mesa = Mesa.query.get(reservaForm.id_mesa.data)
            mesa.disponible = 0
            db.session.commit()

            return redirect(url_for('inicio'))

    return render_template('reservar.html', formulario = reservaForm)
#'''

#'''

'''
@app.route('/verDisponibilidad')
def verDisponibilidad():
    mesas = Mesa.query.order_by('id_mesa').filter_by(disponible='1')
    return render_template('verDisponibilidad.html', mesas = mesas)
'''

@app.route('/verDisponibilidad/<fecha_hora>', methods=['GET','POST'])
def verDisponibilidad(fecha_hora):
    #mesas = Mesa.query.order_by('id_mesa').filter_by(disponible='1')
    fecha_hora_consultada1 = date(2022, 7, 15)
    fecha_hora_consultada = date(2022,7,2)
    print(Reserva.query.filter(Reserva.fecha_hora.between('2022-07-17','2022-07-26')))
    print(str(Reserva.query.filter(Reserva.fecha_hora.between(fecha_hora_consultada1,fecha_hora_consultada))))
    mesas_ocupadas = Reserva.query.filter(Reserva.fecha_hora.between(fecha_hora_consultada1,fecha_hora_consultada)).all()
    print(mesas_ocupadas)

    return render_template('verDisponibilidad.html', mesas = mesas_ocupadas)


@app.route('/seleccionarFecha', methods=['GET','POST'])
def seleccionarFecha():
    fechaForm = FechaForm()

    if request.method == 'POST':
        print(fechaForm.errors)
        if fechaForm.validate_on_submit():

            print('valido')
            fecha_hora = request.form['fecha_hora']
            return redirect(url_for('verDisponibilidad', fecha_hora=fecha_hora))
        else:
            print('no valido')
    return render_template('seleccionarFecha.html', formulario = fechaForm)

@app.route('/verReservas')
def verReservas():
    resultados = db.session.query(Reserva,Usuario).join(Usuario, Usuario.id_usuario == Reserva.id_usuario).\
                order_by(Reserva.fecha_hora.desc(), Reserva.id_mesa).all()
    print(resultados)
    return render_template('verReservas.html', resultados = resultados)

@app.route('/anular/<int:id_reserva>')
def anular(id_reserva):
    reserva = Reserva.query.get_or_404(id_reserva)
    db.session.delete(reserva)
    db.session.commit()
    return redirect(url_for('verReservas'))

if (__name__ == "__main__"):
    app.run(debug=True)