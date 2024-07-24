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
    
#funcion de armado de cruces
def generar_fechas(id):
    cantidad_equipos = Partido.query.filter(Partido.id_torneo == id).count()
    equipos = list(range(1, cantidad_equipos+1))
    calendario = []

    for i in range(cantidad_equipos-1):
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
            partido = Partido(fecha=fecha_num+1, id_equipo1=match[0], id_equipo2=match[1])
            db.session.add(partido)
    db.session.commit()
if __name__ == '__main__':

    app.run(debug=True)