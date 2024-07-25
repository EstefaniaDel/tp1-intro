from flask import Flask, jsonify
from models import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://c0snick:Hola1234@localhost:5432/competencias'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/ver_torneo/<id>')
def ver_torneo(id):
    equipos = Equipo.query.filter_by(id_torneo=id).all()
    if equipos:
        lista_equipos =[]
        for equipo in equipos:
            resultados = Resultado.query.filter_by(id_equipo = equipo.id).first()
            lista_equipos.append({"nombre": equipo.nombre, 
                                  "victorias" : resultados.victorias, 
                                  "empates" : resultados.empates, 
                                  "derrotas" : resultados.derrotas,
                                  "goles" : resultados.goles,
                                  "en_contra" : resultados.en_contra} )
        return jsonify(lista_equipos)
    else:
        return jsonify({"error": "torneo no encontrado"}), 404
    
@app.route('/ver_fecha/<id>/<fecha>')
def ver_fecha(id,fecha):
    partidos = Partido.query.filter_by(id_torneo=id, fecha = fecha).all()
    if partidos:
        lista_partidos =[]
        for partido in partidos:
            equipo1 = Equipo.query.get(partido.id_equipo1)
            equipo2 = Equipo.query.get(partido.id_equipo2)
            lista_partidos.append({"equipo1": equipo1.nombre,
                                  "equipo2" : equipo2.nombre, 
                                  "goles1" : partido.goles1, 
                                  "goles2" : partido.goles2,
                                  "id_partido" : partido.id} )
        return jsonify(lista_partidos)
    else:
        return jsonify({"error": "torneo no encontrado"}), 404

@app.route('/cantidad_equipos/<id>')
def cantidad_equipos(id):
    try:
        torneo = Torneo.query.get(id)
        return jsonify({"cantidad": torneo.cantidad_equipos, "auxiliares" : torneo.guardar_jugadores})
    except:
        return jsonify({"error": "torneo no encontrado"}), 404

@app.route('/obtener_jugadores/<id>')
def obtener_jugadores(id):
    try:
        jugadores = Jugador.query.filter_by(id_equipo = id).all()
        return jsonify(jugadores)
    except:
        return jsonify({"error" : "jugadores no encontrados"})

@app.route('/ver_extras/<id>')
def ver_extras(id):
    try:
        torneo = db.session.get(Torneo,id)
        return jsonify({"cantidad": torneo.cantidad_equipos, "doble" : torneo.tipo_torneo, "guardar" : torneo.guardar_jugadores, "goleadores" : torneo.goleadores, "asistentes" : torneo.asistentes})
    except:
        return jsonify({"error": "torneo no encontrado"}), 404

def crear_jugadores(jugadores, id_equipo):
    for jugador in jugadores:
        nuevo_jugador = Jugador()
        nuevo_jugador.goles = 0
        nuevo_jugador.asistencias = 0
        nuevo_jugador.id_equipo = id_equipo
        nuevo_jugador.nombre = jugador
        db.session.add(nuevo_jugador)
    db.session.commit()

def crear_resultados(id_eq):
    nuevos_resultados = Resultado(victorias = 0, derrotas = 0, empates = 0, goles = 0, en_contra = 0, id_equipo = id_eq)
    db.session.add(nuevos_resultados)
    db.session.commit()

@app.route('/crear_equipo', methods = ["POST"])
def crear_equipo():
    datos_equipo = request.json
    nuevo_equipo = Equipo()
    nuevo_equipo.nombre = datos_equipo.get("nombre")
    nuevo_equipo.id_torneo = datos_equipo.get("torneo")
    try:
        db.session.add(nuevo_equipo)
        db.session.commit()
        id_equipo = nuevo_equipo.id
        crear_resultados(id_equipo)
        jugadores = datos_equipo.get("jugadores")
        if jugadores:
            crear_jugadores(jugadores,id_equipo)
        return jsonify({"id equipo" : id_equipo})
    except:
        return jsonify({"error": "equipo no creado"}), 404
    
@app.route('/generar_fechas/<id>')
def generar_fechas(id):
    try:
        torneo = db.session.get(Torneo,id)
        cantidad_equipos = torneo.cantidad_equipos
        equipos = list(map(lambda x : x.id,torneo.equipos))
        calendario = []
        for _ in range(cantidad_equipos-1):
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
                partido = Partido(id_torneo = id, fecha=fecha_num+1, id_equipo1=match[0], id_equipo2=match[1])
                db.session.add(partido)
        if torneo.tipo_torneo == 2:
            calendario.reverse()
            for fecha_num, partidos_fecha in enumerate(calendario):
                for match in partidos_fecha[0]:
                    partido = Partido(id_torneo = id, fecha=len(calendario)+fecha_num+1, id_equipo1=match[1], id_equipo2=match[0])
                    db.session.add(partido)
        db.session.commit()
        return jsonify(calendario)
    except Exception as e:
        return jsonify({"error":e})
if __name__ == '__main__':

    app.run(debug=True)