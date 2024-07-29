from backend.app.utils import borrar_partido, crear_jugadores, crear_resultados, guardar_goleadores, sumar_partido, ver_jugadores
from flask import request, jsonify
from backend.app import app, db
from backend.app.models import Equipo, Jugador, Partido, Torneo, Gol
import logging

# CRUD para Torneos
@app.route('/torneos', methods=['GET'])
def obtener_torneos():
    try:
        torneos = Torneo.query.all()
        lista_torneos = [{"id": torneo.id, "nombre_torneo": torneo.nombre_torneo, "tipo_torneo": torneo.tipo_torneo, "cantidad_equipos": torneo.cantidad_equipos, "guardar_jugadores": torneo.guardar_jugadores, "goleadores": torneo.goleadores, "asistentes": torneo.asistentes} for torneo in torneos]
        return jsonify(lista_torneos)
    except Exception as e:
        logging.error(f"Error al obtener torneos: {e}")
        return jsonify({"Error": "Torneos no encontrados"}), 404

@app.route('/torneo/<int:torneo_id>', methods=['GET'])
def obtener_torneo(torneo_id):
    try:
        torneo = Torneo.query.get(torneo_id)
        if not torneo:
            return jsonify({"Error": "Torneo no encontrado"}), 404
        return jsonify({
            "id": torneo.id,
            "nombre_torneo": torneo.nombre_torneo,
            "tipo_torneo": torneo.tipo_torneo,
            "cantidad_equipos": torneo.cantidad_equipos,
            "guardar_jugadores": torneo.guardar_jugadores,
            "goleadores": torneo.goleadores,
            "asistentes": torneo.asistentes
        })
    except Exception as e:
        logging.error(f"Error al buscar el torneo: {e}")
        return jsonify({"Error": "Error al buscar el torneo"}), 500

@app.route('/torneo/', methods=['POST'])
def crear_torneo():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"Error": "No se proporcionaron datos"}), 400
        
        nombre_torneo = data.get('nombre_torneo')
        tipo_torneo = data.get('tipo_torneo')
        cantidad_equipos = data.get('cantidad_equipos')
        guardar_jugadores = data.get('guardar_jugadores', 0)
        goleadores = data.get('goleadores', 0)
        asistentes = data.get('asistentes', 0)
        
        if not nombre_torneo or not tipo_torneo or not cantidad_equipos:
            return jsonify({"Error": "Datos incompletos"}), 400
        
        nuevo_torneo = Torneo(nombre_torneo=nombre_torneo, tipo_torneo=tipo_torneo, cantidad_equipos=cantidad_equipos, guardar_jugadores=guardar_jugadores, goleadores=goleadores, asistentes=asistentes)
        db.session.add(nuevo_torneo)
        db.session.commit()
        
        return jsonify({"mensaje": "Torneo creado exitosamente", "id": nuevo_torneo.id}), 201
    except Exception as e:
        logging.error(f"Error al crear el torneo: {e}")
        return jsonify({"Error": "No se pudo crear el torneo"}), 500

@app.route('/torneo/<int:torneo_id>', methods=['PATCH'])
def update_torneo(torneo_id):
    try:
        torneo = Torneo.query.get_or_404(torneo_id)
        data = request.get_json()
        if 'nombre_torneo' in data:
            torneo.nombre_torneo = data['nombre_torneo']
        if 'tipo_torneo' in data:
            torneo.tipo_torneo = data['tipo_torneo']
        if 'cantidad_equipos' in data:
            torneo.cantidad_equipos = data['cantidad_equipos']
        if 'guardar_jugadores' in data:
            torneo.guardar_jugadores = data['guardar_jugadores']
        if 'goleadores' in data:
            torneo.goleadores = data['goleadores']
        if 'asistentes' in data:
            torneo.asistentes = data['asistentes']
        db.session.commit()
        return jsonify({"mensaje": "Torneo actualizado exitosamente"}), 200
    except Exception as e:
        logging.error(f"Error al actualizar el torneo: {e}")
        return jsonify({"Error": "No se pudo actualizar el torneo"}), 500

@app.route('/torneo/<int:torneo_id>', methods=['DELETE'])
def delete_torneo(torneo_id):
    try:
        torneo = Torneo.query.get_or_404(torneo_id)
        db.session.delete(torneo)
        db.session.commit()
        return jsonify({"mensaje": "Torneo eliminado exitosamente"}), 200
    except Exception as e:
        logging.error(f"Error al eliminar el torneo: {e}")
        return jsonify({"Error": "No se pudo eliminar el torneo"}), 500
    
@app.route('/torneo/<int:torneo_id>/goleadores', methods=['GET'])
def obtener_goleadores(torneo_id):
    try:
        jugadores = Jugador.query.join(Equipo).filter(Equipo.id_torneo == torneo_id).order_by(Jugador.goles.desc()).all()
        lista_goleadores = [{"id": jugador.id, "nombre": jugador.nombre, "goles": jugador.goles, "id_equipo": jugador.id_equipo} for jugador in jugadores]
        return jsonify(lista_goleadores)
    except Exception as e:
        logging.error(f"Error al obtener goleadores del torneo {torneo_id}: {e}")
        return jsonify({"Error": "No se pudieron obtener los goleadores"}), 500

# TODO: /torneos/<id>
@app.route('/ver_torneo/<int:id>', methods=['GET'])
def ver_torneo(id):
    try:
        lista_equipos = []
        for equipo in db.session.get(Torneo, id).equipos:
            resultados = equipo.resultados[0]
            lista_equipos.append({
                "nombre": equipo.nombre,
                "id": equipo.id,
                "puntos": resultados.victorias * 3 + resultados.empates,
                "victorias": resultados.victorias,
                "empates": resultados.empates,
                "derrotas": resultados.derrotas,
                "goles": resultados.goles,
                "en_contra": resultados.en_contra,
                "diferencia": resultados.goles - resultados.en_contra
            })
        return jsonify(lista_equipos)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/ver_torneos')
def ver_torneos():
    try:
        torneos = list(map(lambda x: {"id" : x.id, 
                                      "nombre" : x.nombre_torneo, 
                                      "jugadores_guardar" : x.guardar_jugadores, 
                                      "goleadores" : x.goleadores, 
                                      "asistentes" : x.asistentes, 
                                      "cantidad" : x.cantidad_equipos}, 
                                      db.session.query(Torneo).all()))
        return jsonify(torneos)
    except Exception as e:
        return jsonify({"error" : f"{e}"})
    
# CRUD para Equipo
@app.route('/equipos', methods=['GET'])
def obtener_equipos():
    try:
        equipos = Equipo.query.all()
        lista_equipos = [{"id": equipo.id, "nombre": equipo.nombre, "id_torneo": equipo.id_torneo} for equipo in equipos]
        return jsonify(lista_equipos)
    except Exception as e:
        logging.error(f"Error al obtener equipos: {e}")
        return jsonify({"Error": "Equipos no encontrados"}), 404

@app.route('/equipo/<int:equipo_id>', methods=['GET'])
def obtener_equipo(equipo_id):
    try:
        equipo = Equipo.query.get(equipo_id)
        if not equipo:
            return jsonify({"Error": "Equipo no encontrado"}), 404
        
        return jsonify({
            "id": equipo.id,
            "nombre": equipo.nombre,
            "id_torneo": equipo.id_torneo
        })
    except Exception as e:
        logging.error(f"Error al obtener equipo: {e}")
        return jsonify({"Error": "Equipo no encontrado"}), 404

@app.route('/equipo', methods=['POST'])
def nuevo_equipo():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"Error": "No se proporcionaron datos"}), 400
        
        nombre = data.get('nombre')
        id_torneo = data.get('id_torneo')

        if not nombre or not id_torneo:
            return jsonify({"Error": "Datos incompletos"}), 400
        
        nuevo_equipo = Equipo(nombre=nombre, id_torneo=id_torneo)
        db.session.add(nuevo_equipo)
        db.session.commit()
        return jsonify({"mensaje": "Equipo creado exitosamente"}), 201
    except Exception as e:
        logging.error(f"Error al crear el equipo: {e}")
        return jsonify({"Error": "No se pudo crear el equipo"}), 500

@app.route('/equipo/<int:equipo_id>', methods=['PATCH'])
def editar_equipo(equipo_id):
    try:
        equipo = Equipo.query.get_or_404(equipo_id)
        data = request.get_json()

        if 'nombre' in data:
            equipo.nombre = data['nombre']
        if 'id_torneo' in data:
            equipo.id_torneo = data['id_torneo']
        db.session.commit()
        return jsonify({"mensaje": "Equipo editado exitosamente"}), 200
    except Exception as e:
        logging.error(f"Error al editar el equipo: {e}")
        return jsonify({"Error": "No se pudo editar el equipo"}), 500

@app.route('/equipo/<int:equipo_id>', methods=['DELETE'])
def eliminar_equipo(equipo_id):
    try:
        equipo = Equipo.query.get_or_404(equipo_id)
        db.session.delete(equipo)
        db.session.commit()
        return jsonify({"mensaje": "Equipo eliminado exitosamente"}), 200
    except Exception as e:
        logging.error(f"Error al eliminar el equipo: {e}")
        return jsonify({"Error": "No se pudo eliminar el equipo"}), 500
    
# CRUD para Jugador

@app.route('/jugadores', methods=['GET'])
def obtener_jugadores():
    try:
        jugadores = Jugador.query.all()
        lista_jugadores = [{"id": jugador.id, "nombre": jugador.nombre, "goles": jugador.goles, "asistencias": jugador.asistencias, "id_equipo": jugador.id_equipo} for jugador in jugadores]
        return jsonify(lista_jugadores)
    except Exception as e:
        logging.error(f"Error al obtener jugadores: {e}")
        return jsonify({"Error": "Jugadores no encontrados"}), 404
    

@app.route('/jugadores/equipo', methods=['GET'])
def obtener_jugadores_equipo():
    try:
        id_equipo = request.args.get('id_equipo')
        if not id_equipo:
            return jsonify({"Error": "ID del equipo no proporcionado"}), 400
        
        jugadores = Jugador.query.filter_by(id_equipo=id_equipo).all()
        lista_jugadores = [{"id": jugador.id, "nombre": jugador.nombre, "goles": jugador.goles, "asistencias": jugador.asistencias, "id_equipo": jugador.id_equipo} for jugador in jugadores]
        return jsonify(lista_jugadores)
    except Exception as e:
        logging.error(f"Error al obtener jugadores del equipo: {e}")
        return jsonify({"Error": "Error al obtener jugadores del equipo"}), 500
    
@app.route('/jugadores/torneo', methods=['GET'])
def obtener_goleadores_torneo():
    try:
        id_torneo = request.args.get('id_torneo')
        if not id_torneo:
            return jsonify({"Error": "ID del torneo no proporcionado"}), 400

        jugadores = db.session.query(Jugador).join(Equipo).filter(Equipo.id_torneo == id_torneo).all()
        lista_jugadores = [{"id": jugador.id, "nombre": jugador.nombre, "goles": jugador.goles, "asistencias": jugador.asistencias, "id_equipo": jugador.id_equipo} for jugador in jugadores]
        return jsonify(lista_jugadores)
    except Exception as e:
        logging.error(f"Error al obtener goleadores del torneo: {e}")
        return jsonify({"Error": "Error al obtener goleadores del torneo"}), 500
    
@app.route('/jugador/', methods=['POST'])
def nuevo_jugador():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"Error": "No se proporcionaron datos"}), 400
        
        nombre = data.get('nombre')
        goles = data.get('goles', 0)
        asistencias = data.get('asistencias', 0)
        id_equipo = data.get('id_equipo')

        if not nombre or not id_equipo:
            return jsonify({"Error": "Datos incompletos"}), 400

        nuevo_jugador = Jugador(nombre=nombre, goles=goles, asistencias=asistencias, id_equipo=id_equipo)
        db.session.add(nuevo_jugador)
        db.session.commit()
        return jsonify({"mensaje": "Jugador creado exitosamente"}), 201
    except Exception as e:
        logging.error(f"Error al crear el jugador: {e}")
        return jsonify({"Error": "No se pudo crear el jugador"}), 500

@app.route('/jugador/<int:jugador_id>', methods=['PATCH'])
def editar_jugador(jugador_id):
    try:
        jugador = Jugador.query.get_or_404(jugador_id)
        data = request.get_json()
        if 'nombre' in data:
            jugador.nombre = data['nombre']
        if 'goles' in data:
            jugador.goles = data['goles']   
        if 'asistencias' in data:
            jugador.asistencias = data['asistencias']
        if 'id_equipo' in data:
            jugador.id_equipo = data['id_equipo']

        db.session.commit()
        return jsonify({"mensaje": "Jugador editado exitosamente"}), 200
    except Exception as e:
        logging.error(f"Error al editar el jugador: {e}")
        return jsonify({"Error": "No se pudo editar el jugador"}), 500

@app.route('/jugador/<int:jugador_id>', methods=['DELETE'])
def eliminar_jugador(jugador_id):
    try:
        jugador = Jugador.query.get_or_404(jugador_id)
        db.session.delete(jugador)
        db.session.commit()
        return jsonify({"mensaje": "Jugador eliminado exitosamente"}), 200
    except Exception as e:
        logging.error(f"Error al eliminar el jugador: {e}")
        return jsonify({"Error": "No se pudo eliminar el jugador"}), 500

@app.route('/crear_jugador/<id>', methods=["POST"])
def crear_jugador(id):
    jugador = request.json
    crear_jugadores([jugador], id)
    return jsonify(ver_jugadores(db.session.get(Equipo, id).jugadores))

@app.route('/ver_jugadores_doble/<id1>/<id2>')
def ver_jugadores_doble(id1, id2):
    try:
        jugadores1 = ver_jugadores(db.session.get(Equipo, id1).jugadores)
        jugadores2 = ver_jugadores(db.session.get(Equipo, id2).jugadores)
        return jsonify({"equipo1": jugadores1, "equipo2": jugadores2})
    except Exception as e:
        return jsonify({"error": "Jugadores no encontrados", "details": str(e)})

@app.route('/ver_fecha/<id>/<fecha>', methods=['GET'])
def ver_fecha(id, fecha):
    try:
        partidos = db.session.get(Torneo, id).partidos
        lista_partidos = []
        for partido in partidos:
            if partido.fecha == int(fecha):
                equipo1 = partido.equipo1
                equipo2 = partido.equipo2
                lista_partidos.append({
                    "equipo1": equipo1.nombre,
                    "equipo2": equipo2.nombre,
                    "id1": equipo1.id,
                    "id2": equipo2.id,
                    "goles1": partido.goles1,
                    "goles2": partido.goles2,
                    "id_partido": partido.id
                })
        return jsonify(lista_partidos)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/ver_extras/<id>', methods=['GET'])
def ver_extras(id):
    try:
        torneo = db.session.get(Torneo, id)
        if not torneo:
            logging.error(f"Torneo con ID {id} no encontrado")
            return jsonify({"error": "Torneo no encontrado"}), 404
        
        logging.info(f"Torneo con ID {id} encontrado: {torneo}")
        return jsonify({
            "cantidad": torneo.cantidad_equipos,
            "doble": torneo.tipo_torneo,
            "guardar": torneo.guardar_jugadores,
            "goleadores": torneo.goleadores,
            "asistentes": torneo.asistentes
        })
    except Exception as e:
        logging.error(f"Error al obtener extras del torneo: {e}")
        return jsonify({"error": "Error al obtener extras del torneo"}), 500

@app.route('/crear_equipo', methods=["POST"])
def crear_equipo():
    datos_equipo = request.json
    nuevo_equipo = Equipo(
        nombre=datos_equipo.get("nombre"),
        id_torneo=datos_equipo.get("torneo")
    )
    try:
        db.session.add(nuevo_equipo)
        db.session.commit()
        id_equipo = nuevo_equipo.id
        crear_resultados(id_equipo)
        jugadores = datos_equipo.get("jugadores")
        if jugadores:
            crear_jugadores(jugadores, id_equipo)
        return jsonify({"id_equipo": id_equipo})
    except Exception as e:
        return jsonify({"error": "Equipo no creado", "details": str(e)})

@app.route('/generar_fechas/<id>')
def generar_fechas(id):
    try:
        torneo = db.session.get(Torneo, id)
        cantidad_equipos = torneo.cantidad_equipos
        equipos = list(map(lambda x: x.id, torneo.equipos))
        calendario = []
        for _ in range(cantidad_equipos - 1):
            fecha = []
            mid = cantidad_equipos // 2
            L1 = equipos[:mid]
            L2 = equipos[mid:]
            L2.reverse()
            fecha.append(list(zip(L1, L2)))
            equipos.insert(1, equipos.pop())
            calendario.append(fecha)
        for fecha_num, partidos_fecha in enumerate(calendario):
            for match in partidos_fecha[0]:
                partido = Partido(id_torneo=id, fecha=fecha_num + 1, id_equipo1=match[0], id_equipo2=match[1])
                db.session.add(partido)
        if torneo.tipo_torneo == 2:
            calendario.reverse()
            for fecha_num, partidos_fecha in enumerate(calendario):
                for match in partidos_fecha[0]:
                    partido = Partido(id_torneo=id, fecha=len(calendario) + fecha_num + 1, id_equipo1=match[1], id_equipo2=match[0])
                    db.session.add(partido)
        db.session.commit()
        return jsonify(calendario)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/ver_partido/<int:id>', methods=['GET'])
def ver_partido(id):
    try:
        partido = db.session.get(Partido, id)
        equipo1 = partido.equipo1
        equipo2 = partido.equipo2
        return jsonify({
            "equipo1": equipo1.nombre,
            "equipo2": equipo2.nombre,
            "id1": equipo1.id,
            "id2": equipo2.id,
            "id_torneo": equipo1.id_torneo
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/ver_goles/<id>')
def ver_goles(id):
    try:
        goles = Gol.query.filter_by(id_partido=id).all()
        ret = []
        for gol in goles:
            jugador = db.session.get(Jugador, gol.id_jugador)
            ret.append({"goleador": jugador.nombre, "equipo": jugador.id_equipo})
        return jsonify(ret)
    except Exception as e:
        return jsonify({"error": "Goles no encontrados", "details": str(e)})


@app.route('/ver_equipo/<id>')
def ver_equipo(id):
    equipo = db.session.get(Equipo, id)
    jugadores = ver_jugadores(equipo.jugadores)
    partidos = []
    for partido in Partido.query.filter((Partido.id_equipo1 == equipo.id) | (Partido.id_equipo2 == equipo.id)):
        partidos.append({
            "id": partido.id,
            "equipo1": partido.equipo1.nombre,
            "equipo2": partido.equipo2.nombre,
            "goles1": partido.goles1,
            "goles2": partido.goles2
        })
    return jsonify({
        "id_torneo": equipo.id_torneo,
        "nombre": equipo.nombre,
        "jugadores": jugadores,
        "partidos": partidos
    })

@app.route('/editar_partido', methods=["PUT"])
def editar_partido():
    try:
        resultado_partido = request.json
        id_partido = resultado_partido.get("id_partido")
        partido = db.session.get(Partido, id_partido)
        goles1 = resultado_partido.get("goles1")
        goles2 = resultado_partido.get("goles2")
        equipo1 = db.session.get(Equipo, partido.id_equipo1).resultados[0]
        equipo2 = db.session.get(Equipo, partido.id_equipo2).resultados[0]
        if partido.goles1 is not None:
            borrar_partido(equipo1, equipo2, partido.goles1, partido.goles2)
        partido.goles1 = goles1
        partido.goles2 = goles2
        sumar_partido(equipo1, equipo2, goles1, goles2)
        if "goles" in resultado_partido:
            guardar_goleadores(resultado_partido.get("goles"), id_partido)
        db.session.commit()
        return jsonify({"message": "Partido editado exitosamente"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
if __name__ == '__main__':
    app.run(debug=True)
