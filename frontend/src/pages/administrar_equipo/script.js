const params = new URLSearchParams(window.location.search);
const id = params.get("id");

function request_error(error) {
    console.log("ERROR");
    console.log(error);
    alert(error);
}

function base_table(partido){
    let cabecera = document.createElement("table");
    let fila =cabecera.insertRow(-1);
    let celda = fila.insertCell(0);
    celda.innerHTML = `Partido ${partido+1}`;
    return cabecera;
}

function subir_jugador(){
    let datos = document.getElementById("nuevo").value;
    document.getElementById("agregar jugador").innerHTML = "";
    document.getElementById("jugadores").innerHTML = "";
    fetch(`http://localhost:5000/crear_jugador/${id}`,{
    method: `POST`,
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(datos)
    })
    .then((res) => res.json())
    .then(crear_jugadores)
    .catch(request_error)
}

function agregar_jugador(){
    let agregar_jugador = document.getElementById("agregar jugador");
    if (agregar_jugador.innerHTML === ""){
        let input = document.createElement("input");
        input.placeholder = "Ingrese un jugador";
        input.id = "nuevo";
        agregar_jugador.appendChild(input);
        let boton = document.createElement("button");
        boton.textContent = "Guardar";
        boton.onclick = function() {subir_jugador();};
        agregar_jugador.appendChild(boton);
    }   
}

function crear_jugadores(jugadores){
    let div_jugadores = document.getElementById("jugadores");
    let fila = div_jugadores.insertRow(-1);
    let nombre = fila.insertCell(0);
    let goles = fila.insertCell(1);
    let asistencias = fila.insertCell(2);
    fila.insertCell(3);
    nombre.textContent = "Nombre";
    goles.textContent = "Goles";
    asistencias.textContent = "Asistencias";
    for( let i = 0; i<jugadores.length;i++){
        let nombre_jugador = fila_jugador.insertCell(0);
        let goles_jugador = fila_jugador.insertCell(1);
        let asistencias_jugador = fila_jugador.insertCell(2);
        let botones = fila_jugador.insertCell(3);
        nombre_jugador.textContent = jugadores[i].nombre;
        goles_jugador.textContent = jugadores[i].goles;
        asistencias_jugador.textContent = jugadores[i].asistencias;
        botones.appendChild(document,createElement("button"));
    }
    let div_boton = document.getElementById("agregar");
    let boton = document.createElement("button");
    boton.innerHTML = "agregar";
    boton.onclick = function() {agregar_jugador();};
    div_boton.appendChild(boton);   
}

function crear_tabla(partidos){
    partidos.sort(function(a,b){return (a.id) - (b.id)})
    let tablas = document.getElementById("partidos");
    for (let i = 0; i < partidos.length;i++){
        tablas.appendChild(base_tabla(i));
        let tabla = document.createElement("table");
        let partido = partidos[i];
        let fila = tabla.insertRow(-1);
        let nombre1 = fila.insertCell(0);
        let goles1 = fila.insertCell(1);
        let goles2 = fila.insertCell(2);
        let nombre2 = fila.insertCell(3);
        nombre1.innerHTML = partido.equipo1;
        goles1.innerHTML = partido.goles1;
        goles2.innerHTML = partido.goles2;
        nombre2.innerHTML = partido.equipo2;
        tablas.appendChild(tabla);
    }
}

function mostrar_equipo(equipo){
    let div_equipo = document.getElementById("equipo");
    div_equipo.innerHTML = equipo.nombre;
    crear_tabla(equipo.partido);
    if (equipo.jugadores.length !== 0){
        crear_jugadores(equipo.jugadores);
    }
}

fetch(`http://localhost:5000/ver_equipo/${id}`)
.then((res) => res.json())
.then(mostrar_equipo)
.catch(request_error)