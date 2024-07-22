from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Torneo(db.Model):
    __tablename__ = 'torneos'

    id = db.Column(db.Integer, primary_key=True)
    nombre_torneo = db.Column(db.String(100), nullable=False)
    tipo_torneo = db.Column(db.Integer, nullable=False)
    cantidad_equipos = db.Column(db.Integer,nullable = False)
    guardar_jugadores = db.Column(db.Integer,nullable = False)
    goleadores = db.Column(db.Integer,nullable = False)
    asistentes = db.Column(db.Integer,nullable = False)

    equipos = db.relationship('Equipo', backref='torneo', lazy=True)
    partidos = db.relationship('Partido', backref='torneo', lazy=True)

class Equipo(db.Model):
    __tablename__ = 'equipos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    id_torneo = db.Column(db.Integer, db.ForeignKey('torneos.id'), nullable=False)

    resultados = db.relationship('Resultado', backref='equipo', lazy=True)
    jugadores = db.relationship('Jugador', backref='equipo', lazy=True)
    goles = db.relationship('Gol', backref='equipo', lazy=True)

class Resultado(db.Model):
    __tablename__ = 'resultados'

    id = db.Column(db.Integer, primary_key=True)
    victorias = db.Column(db.Integer, nullable=False)
    empates = db.Column(db.Integer, nullable=False)
    derrotas = db.Column(db.Integer, nullable=False)
    goles = db.Column(db.Integer, nullable=False)
    en_contra = db.Column(db.Integer, nullable=False)
    id_equipo = db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)

class Jugador(db.Model):
    __tablename__ = 'jugadores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    goles = db.Column(db.Integer, nullable=False)
    asistencias = db.Column(db.Integer, nullable=False)
    id_equipo = db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)

    gol = db.relationship('Gol', backref='jugador', lazy=True)

class Partido(db.Model):
    __tablename__ = 'partidos'

    id = db.Column(db.Integer, primary_key=True)
    id_torneo = db.Column(db.Integer, db.ForeignKey('torneos.id'), nullable=False)
    fecha = db.Column(db.Integer, nullable=False)
    id_equipo1 = db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)
    id_equipo2 = db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)
    goles1 = db.Column(db.Integer)
    goles2 = db.Column(db.Integer)

    equipo1 = db.relationship('Equipo', foreign_keys=[id_equipo1])
    equipo2 = db.relationship('Equipo', foreign_keys=[id_equipo2])

class Gol(db.Model):
    __tablename__ = 'gol'

    id = db.Column(db.Integer, primary_key=True)
    id_jugador = db.Column(db.Integer, db.ForeignKey('jugadores.id'), nullable=False)
    id_equipo = db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)
    id_torneo = db.Column(db.Integer, db.ForeignKey('torneos.id'), nullable=False)

