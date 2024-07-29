from backend.app import db
from backend.app.models import Jugador, Gol, Resultado

def crear_jugadores(jugadores, id_equipo):
    for jugador in jugadores:
        nuevo_jugador = Jugador(goles=0, asistencias=0, id_equipo=id_equipo, nombre=jugador)
        db.session.add(nuevo_jugador)
    db.session.commit()

def crear_resultados(id_eq):
    nuevos_resultados = Resultado(victorias=0, derrotas=0, empates=0, goles=0, en_contra=0, id_equipo=id_eq)
    db.session.add(nuevos_resultados)
    db.session.commit()

def ver_jugadores(data_jugadores):
    jugadores = []
    for jugador in data_jugadores:
        jugadores.append({
            "id": jugador.id,
            "nombre": jugador.nombre,
            "goles": jugador.goles,
            "asistencias": jugador.asistencias
        })
    return jugadores

def victoria(equipo, gaf, gec):
    equipo.victorias += 1
    equipo.goles += int(gaf)
    equipo.en_contra += int(gec)

def derrota(equipo, gaf, gec):
    equipo.derrotas += 1
    equipo.goles += int(gaf)
    equipo.en_contra += int(gec)

def empate(equipo, gaf, gec):
    equipo.empates += 1
    equipo.goles += int(gaf)
    equipo.en_contra += int(gec)

def sumar_partido(equipo1, equipo2, goles1, goles2):
    if goles1 > goles2:
        victoria(equipo1, goles1, goles2)
        derrota(equipo2, goles2, goles1)
    elif goles2 > goles1:
        victoria(equipo2, goles2, goles1)
        derrota(equipo1, goles1, goles2)
    else:
        empate(equipo1, goles1, goles2)
        empate(equipo2, goles2, goles1)

def borrar_victoria(equipo, gaf, gec):
    equipo.victorias -= 1
    equipo.goles -= gaf
    equipo.en_contra -= gec

def borrar_derrota(equipo, gaf, gec):
    equipo.derrotas -= 1
    equipo.goles -= gaf
    equipo.en_contra -= gec

def borrar_empate(equipo, gaf, gec):
    equipo.empates -= 1
    equipo.goles -= gaf
    equipo.en_contra -= gec

def borrar_partido(equipo1, equipo2, goles1, goles2):
    if goles1 > goles2:
        borrar_victoria(equipo1, goles1, goles2)
        borrar_derrota(equipo2, goles2, goles1)
    elif goles2 > goles1:
        borrar_victoria(equipo2, goles2, goles1)
        borrar_derrota(equipo1, goles1, goles2)
    else:
        borrar_empate(equipo1, goles1, goles2)
        borrar_empate(equipo2, goles2, goles1)

def guardar_goleadores(goles, id_partido):
    goles_anteriores = Gol.query.filter_by(id_partido=id_partido).all()
    for gol in goles_anteriores:
        jugador = Jugador.query.get(gol.id_jugador)
        jugador.goles -= 1
        if gol.id_asistencia is not None:
            asistente = Jugador.query.get(gol.id_asistencia)
            asistente.asistencias -= 1
        db.session.delete(gol)
    for gol in goles:
        id_jugador = gol.get("goleador")
        jugador = Jugador.query.get(id_jugador)
        jugador.goles += 1
        nuevo_gol = Gol(id_jugador=id_jugador, id_equipo=jugador.id_equipo, id_partido=int(id_partido))
        if "asistente" in gol:
            id_asistente = gol.get("asistente")
            asistente = Jugador.query.get(id_asistente)
            asistente.asistencias += 1
            nuevo_gol.id_asistencia = id_asistente
        db.session.add(nuevo_gol)