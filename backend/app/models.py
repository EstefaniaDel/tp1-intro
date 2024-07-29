from backend.app import db

class Torneo(db.Model):
    __tablename__ = 'torneos'

    id = db.Column(db.Integer, primary_key=True)
    nombre_torneo = db.Column(db.String(100), nullable=False)
    tipo_torneo = db.Column(db.Integer, nullable=False)
    cantidad_equipos = db.Column(db.Integer, nullable=False)
    guardar_jugadores = db.Column(db.Integer, nullable=False)
    goleadores = db.Column(db.Integer, nullable=False)
    asistentes = db.Column(db.Integer, nullable=False)

    equipos = db.relationship('Equipo', backref='torneo', cascade='all, delete-orphan')
    partidos = db.relationship('Partido', backref='torneo', cascade='all, delete-orphan')

class Equipo(db.Model):
    __tablename__ = 'equipos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    id_torneo = db.Column(db.Integer, db.ForeignKey('torneos.id', ondelete='CASCADE'), nullable=False)

    resultados = db.relationship('Resultado', backref='equipo', cascade='all, delete-orphan')
    jugadores = db.relationship('Jugador', backref='equipo', cascade='all, delete-orphan')
    partidos_local = db.relationship('Partido', backref='equipo_local', foreign_keys='Partido.id_equipo1')
    partidos_visitante = db.relationship('Partido', backref='equipo_visitante', foreign_keys='Partido.id_equipo2')
class Resultado(db.Model):
    __tablename__ = 'resultados'

    id = db.Column(db.Integer, primary_key=True)
    victorias = db.Column(db.Integer, nullable=False, default=0)
    empates = db.Column(db.Integer, nullable=False, default=0)
    derrotas = db.Column(db.Integer, nullable=False, default=0)
    goles = db.Column(db.Integer, nullable=False, default=0)
    en_contra = db.Column(db.Integer, nullable=False, default=0)
    id_equipo = db.Column(db.Integer, db.ForeignKey('equipos.id', ondelete='CASCADE'), nullable=False)

class Jugador(db.Model):
    __tablename__ = 'jugadores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    goles = db.Column(db.Integer, nullable=False, default=0)
    asistencias = db.Column(db.Integer, nullable=False, default=0)
    id_equipo = db.Column(db.Integer, db.ForeignKey('equipos.id', ondelete='CASCADE'), nullable=False)

    goles_marcados = db.relationship('Gol', backref='goleador', foreign_keys='Gol.id_jugador')
    asistencias_dadas = db.relationship('Gol', backref='asistente', foreign_keys='Gol.id_asistencia')

class Partido(db.Model):
    __tablename__ = 'partidos'

    id = db.Column(db.Integer, primary_key=True)
    id_torneo = db.Column(db.Integer, db.ForeignKey('torneos.id', ondelete='CASCADE'), nullable=False)
    fecha = db.Column(db.Integer, nullable=False)
    id_equipo1 = db.Column(db.Integer, db.ForeignKey('equipos.id', ondelete='CASCADE'), nullable=False)
    id_equipo2 = db.Column(db.Integer, db.ForeignKey('equipos.id', ondelete='CASCADE'), nullable=False)
    goles1 = db.Column(db.Integer, default=None)
    goles2 = db.Column(db.Integer, default=None)

    goles = db.relationship('Gol', backref='partido', cascade='all, delete-orphan')
    equipo1 = db.relationship('Equipo', foreign_keys=[id_equipo1])
    equipo2 = db.relationship('Equipo', foreign_keys=[id_equipo2])

class Gol(db.Model):
    __tablename__ = 'goles'

    id = db.Column(db.Integer, primary_key=True)
    id_jugador = db.Column(db.Integer, db.ForeignKey('jugadores.id', ondelete='CASCADE'), nullable=False)
    id_asistencia = db.Column(db.Integer, db.ForeignKey('jugadores.id', ondelete='SET NULL'), nullable=True)
    id_equipo = db.Column(db.Integer, db.ForeignKey('equipos.id', ondelete='CASCADE'), nullable=False)
    id_partido = db.Column(db.Integer, db.ForeignKey('partidos.id', ondelete='CASCADE'), nullable=False)

