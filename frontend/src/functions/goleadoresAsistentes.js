const params = new URLSearchParams(window.location.search);
const id = params.get("id");
const constante_equipos = 10;
var jugadores = []

function request_error(error) {
    console.log("ERROR");
    console.log(error);
    alert(error);
}

function cambiar_seleccion(){
    let seleccion = document.getElementById("elegir_tabla").value
    let tabla = document.getElementById("tabla")
    tabla.innerHTML = ""
    let base = tabla.insertRow(-1)
    let nombre_celda = base.insertCell(0)
    let equipo_celda = base.insertCell(1)
    let seleccionar = base.insertCell(2)
    nombre_celda.innerHTML = "Nombre"
    equipo_celda.innerHTML = "Equipo"
    if (seleccion === "goleadores"){
        jugadores.sort(function(a,b){return b.goles-a.goles})
        seleccionar.innerHTML = "Goles"
        for (let i = 0; i<constante_equipos;i++){
            let fila = tabla.insertRow(-1)
            let nombre = fila.insertCell(0)
            let equipo = fila.insertCell(1)
            let goles = fila.insertCell(2)
            nombre.innerHTML = jugadores[i].nombre
            equipo.innerHTML = jugadores[i].equipo
            goles.innerHTML = jugadores[i].goles
        }
    } else{
        jugadores.sort(function(a,b){return b.asistencias-a.asistencias})
        seleccionar.innerHTML = "Asistencias"
        for (let i = 0; i<constante_equipos;i++){
            let fila = tabla.insertRow(-1)
            let nombre = fila.insertCell(0)
            let equipo = fila.insertCell(1)
            let asistencias = fila.insertCell(2)
            nombre.innerHTML = jugadores[i].nombre
            equipo.innerHTML = jugadores[i].equipo
            asistencias.innerHTML = jugadores[i].asistencias
        }
    }
}

function agregar_goleador(equipo){
    for (let i= 0; i<equipo.jugadores.length;i++ ){
        let jugador_actual = equipo.jugadores[i]
        var jugador = {
            nombre : jugador_actual.nombre,
            equipo : equipo.nombre,
            goles : jugador_actual.goles,
            asistencias : jugador_actual.asistencias
        }
        jugadores.push(jugador)
    }
    console.log(jugadores)
}

function buscar_equipos(equipos){
    for (let i = 0; i<equipos.length; i++){
        fetch(`http://localhost:5000/ver_equipo/${equipos[i].id}`)
        .then((res) => res.json())
        .then(agregar_goleador)
        .catch(request_error)
    }
}

function procesar(datos){
    fetch(`http://localhost:5000/ver_torneo/${id}`)
    .then((res) => res.json())
    .then(buscar_equipos)
    .catch(request_error)
    if (datos.guardar === 0 || (datos.goleadores == 0 && datos.asistentes ===0)){
        alert("Torneo sin equipos")
        window.location.href = `http://localhost/administrar_torneo?id=${id}`
    }
    let elegir_jugadores = document.getElementById("elegir_tabla")
    if (datos.goleadores === 1){
        let opcion = document.createElement("option")
        opcion.textContent = "goleadores"
        elegir_jugadores.appendChild(opcion)
    } 
    if (datos.asistentes === 1){
        let opcion = document.createElement("option")
        opcion.textContent = "asistentes"
        elegir_jugadores.appendChild(opcion)
    }
}

fetch(`http://localhost:5000/ver_extras/${id}`)
.then((res) => res.json())
.then(procesar)
.catch(request_error)