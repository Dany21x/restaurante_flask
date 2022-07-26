from app import db
'''

reserva = db.Table('reserva',
    db.Column('id_reserva', db.Integer, primary_key = True),
    db.Column('id_usuario_fk', db.Integer, db.ForeignKey('usuario.id_usuario')),
    db.Column('id_mesa_fk', db.Integer, db.ForeignKey('mesa.id_mesa')),
    db.Column('fecha_hora', db.DateTime)
)
'''

class Reserva(db.Model):
    id_reserva = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    id_mesa = db.Column(db.Integer, db.ForeignKey('mesa.id_mesa'))
    fecha_hora = db.Column(db.DateTime)
    #relacion_mesa = db.relationship('Mesa')

    def __str__(self):
        return(
            f'Id: {self.id_mesa}',
            f'Usuario: {self.id_usuario}',
            f'Mesa: {self.id_mesa}',
            f'Fecha: {self.fecha_hora}'
        )

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key = True)
    cedula = db.Column(db.Integer)
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))
    email = db.Column(db.String(250), unique = True)
    telefono = db.Column(db.Integer)
    #reservando = db.relationship('Mesa', secondary = reserva, backref = 'reserva')
    relacion_reserva = db.relationship('Reserva')

    def __str__(self):
        return(
            f'Id: {self.id_usuario}',
            f'Cedula: {self.cedula}',
            f'Nombre: {self.nombre}',
            f'Apellido: {self.apellido}',
            f'Email: {self.email}',
            f'Telefono: {self.telefono}'
        )

class Mesa(db.Model):
    id_mesa = db.Column(db.Integer, primary_key = True)
    disponible = db.Column(db.Boolean, default = True)

    def __str__(self):
        return(
            f'Id: {self.id_mesa}',
            f'Disponible: {self.disponible}'
        )

#'''