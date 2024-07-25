from flask import request, jsonify
from backend.app import app, db
from backend.app.models import Asistente, Equipo, Jugador, Partido, Torneo
import logging

# CRUD para Torneos
@app.route('/torneos', methods=['GET'])
def obtener_torneos():
    try:
        torneos = Torneo.query.all()
        lista_torneos = [{"id": torneo.id, "nombre_torneo": torneo.nombre_torneo, "tipo_torneo": torneo.tipo_torneo} for torneo in torneos]
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
            "tipo_torneo": torneo.tipo_torneo
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
        
        if not nombre_torneo or not tipo_torneo:
            return jsonify({"Error": "Datos incompletos"}), 400
        
        nuevo_torneo = Torneo(nombre_torneo=nombre_torneo, tipo_torneo=tipo_torneo)
        db.session.add(nuevo_torneo)
        db.session.commit()
        
        return jsonify({"mensaje": "Torneo creado exitosamente"}), 201
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

@app.route('/equipo/nuevo', methods=['POST'])
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
        # equipo.nombre = request.form['nombre']
        # equipo.id_torneo = request.form['id_torneo']
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

@app.route('/jugador/<int:jugador_id>', methods=['GET'])
def obtener_jugador(jugador_id):
    try:
        jugador = Jugador.query.get(jugador_id)
        if not jugador:
            return jsonify({"Error": "Jugador no encontrado"}), 404
        return jsonify({
            "id": jugador.id,
            "nombre": jugador.nombre,
            "goles": jugador.goles,
            "asistencias": jugador.asistencias,
            "id_equipo": jugador.id_equipo
        })
    except Exception as e:
        logging.error(f"Error al obtener jugador: {e}")
        return jsonify({"Error": "Jugador no encontrado"}), 404

@app.route('/jugador/nuevo', methods=['POST'])
def nuevo_jugador():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"Error": "No se proporcionaron datos"}), 400
        
        nombre = data.get('nombre')
        goles = data.get('goles', 0)
        asistencias = data.get('asistencias')
        id_equipo = data.get('id_equipo')

        if not nombre or not asistencias or not id_equipo:
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
    
if __name__ == '__main__':
    app.run(debug=True)