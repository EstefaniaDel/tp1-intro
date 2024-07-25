from backend.app import db

class Torneo(db.Model):
    __tablename__ = 'torneos'

    id = db.Column(db.Integer, primary_key=True)
    nombre_torneo = db.Column(db.String(100), nullable=False)
    tipo_torneo = db.Column(db.Integer, nullable=False)

    equipos = db.relationship('Equipo', backref='torneo', lazy=True)
    partidos = db.relationship('Partido', backref='torneo', lazy=True)

class Equipo(db.Model):
    __tablename__ = 'equipos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    id_torneo = db.Column(db.Integer, db.ForeignKey('torneos.id'), nullable=False)

    # resultados = db.relationship('Resultado', backref='equipo', lazy=True)
    jugadores = db.relationship('Jugador', backref='equipo', lazy=True)
    # goles = db.relationship('Gol', backref='equipo', lazy=True)
    # asistentes = db.relationship('Asistente', backref='equipo', lazy=True)

# class Resultado(db.Model):
#     __tablename__ = 'resultados'

#     id = db.Column(db.Integer, primary_key=True)
#     victorias = db.Column(db.Integer, nullable=False)
#     empates = db.Column(db.Integer, nullable=False)
#     derrotas = db.Column(db.Integer, nullable=False)
#     goles = db.Column(db.Integer, nullable=False)
#     en_contra = db.Column(db.Integer, nullable=False)
#     id_equipo = db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)

class Jugador(db.Model):
    __tablename__ = 'jugadores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    goles = db.Column(db.Integer, nullable=True)
    asistencias = db.Column(db.Integer, nullable=False)
    id_equipo = db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)

    # goles = db.relationship('Gol', backref='jugador', lazy=True)
    asistentes = db.relationship('Asistente', backref='jugador', lazy=True)

class Partido(db.Model):
    __tablename__ = 'partidos'

    id = db.Column(db.Integer, primary_key=True)
    id_torneo = db.Column(db.Integer, db.ForeignKey('torneos.id'), nullable=False)
    id_equipo1 = db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)
    id_equipo2 = db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)

    equipo1 = db.relationship('Equipo', foreign_keys=[id_equipo1])
    equipo2 = db.relationship('Equipo', foreign_keys=[id_equipo2])
    asistentes = db.relationship('Asistente', backref='partido', lazy=True)

# class Gol(db.Model):
#     __tablename__ = 'goles'

#     id = db.Column(db.Integer, primary_key=True)
#     id_jugador = db.Column(db.Integer, db.ForeignKey('jugadores.id'), nullable=False)
#     id_equipo = db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)
#     id_torneo = db.Column(db.Integer, db.ForeignKey('torneos.id'), nullable=False)

# class ResultadoPartido(db.Model):
#     __tablename__ = 'resultado'

#     id = db.Column(db.Integer, primary_key=True)
#     id_partido = db.Column(db.Integer, db.ForeignKey('partidos.id'), nullable=False)
#     goles1 = db.Column(db.Integer)
#     goles2 = db.Column(db.Integer)

class Asistente(db.Model):
    __tablename__ = 'asistentes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    id_partido = db.Column(db.Integer, db.ForeignKey('partidos.id'), nullable=False)
    id_equipo = db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)
    id_jugador = db.Column(db.Integer, db.ForeignKey('jugadores.id'), nullable=False)

    equipo = db.relationship('Equipo', backref='asistentes', lazy=True)

# class Goleadores(db.Model):
#     __tablename__ = 'goleadores'

#     id = db.Column(db.Integer, primary_key=True)
#     id_jugador = db.Column(db.Integer, db.ForeignKey('jugadores.id'), nullable=False)
#     id_torneo = db.Column(db.Integer, db.ForeignKey('torneos.id'), nullable=False)
#     goles = db.Column(db.Integer, nullable=False)
