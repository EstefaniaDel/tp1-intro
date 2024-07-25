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

if __name__ == '__main__':
    app.run(debug=True)