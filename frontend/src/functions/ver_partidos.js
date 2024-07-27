const params = new URLSearchParams(window.location.search);
const id = params.get("id");

var mostrar_goleadores;

function volver(){
    window.location.href = `http://localhost:8000/src/pages/administrar_torneo?id=${id}`;
}

function base_tabla(partido){
    let cabecera = document.createElement("table");
    let fila = cabecera.insertRow(-1);
    let celda = fila.insertCell(0);
    celda.innerHTML = `Partido ${partido+1}`;
    return cabecera;
}

function editar_partido(id_partido){
    if (mostrar_goleadores === 0){
        window.location.href = `http://localhost:8000/src/pages/editar_partido?id=${id_partido}`;
    } else {
        window.location.href = `http://localhost:8000/src/pages/editar_partido_jugadores?id=${id_partido}`;
    }
}

function boton_editar_partido(id_partido){
    let boton = document.createElement("button");
    boton.textContent = "Editar partido";
    boton.onclick = function() { editar_partido(id_partido);};
    return boton;
}

function goleadores_equipo(goles){
    console.log(goles);
    for (let i= 0 ; i<goles.length;i++){
        let equipo = document.getElementById(goles[i].equipo);
        if(equipo !== null){
           equipo.innerHTML += `${goles[i].goleador} `; 
        } 
    }
}

function crear_tabla(partidos) {
    partidos.sort(function(a,b){return (a.id_partido) - (b.id_partido)});
    let base = document.getElementById("tablas");
    base.innerHTML = "";
    for (let i = 0 ; i< partidos.length;i++){
        let tablas = document.createElement("div");
        tablas.appendChild(base_tabla(i));
        let tabla = document.createElement("table");
        let partido = partidos[i];
        let fila = tabla.insertRow(-1);
        let nombre1 = fila.insertCell(0);
        let goles1 = fila.insertCell(1);
        let goles2 = fila.insertCell(2);
        let nombre2 = fila.insertCell(3);
        nombre1.innerHTML = partido.equipo1;
        nombre1.classList.add("nombres_equipos");
        goles1.innerHTML = partido.goles1;
        goles2.innerHTML = partido.goles2;
        nombre2.innerHTML = partido.equipo2;
        nombre2.classList.add("nombres_equipos");
        tablas.appendChild(tabla);
        if (mostrar_goleadores === 1){
            let goleadores = document.createElement("table");
            let fila_goleadores = goleadores.insertRow(-1);
            let golesLocal = fila_goleadores.insertCell(0);
            golesLocal.id = partido.id1;
            golesLocal.classList.add("nombres_equipos");
            let golesVisitante = fila_goleadores.insertCell(1);
            golesVisitante.id = partido.id2;
            golesVisitante.classList.add("nombres_equipos");
            tablas.appendChild(goleadores);

            fetch(`http://localhost:5000/ver_goles/${partido.id_partido}`)
            .then((res) => res.json())
            .then(goleadores_equipo)
            .catch(request_error)
        }
        tablas.appendChild(boton_editar_partido(partido.id_partido));
        base.appendChild(tablas);
    }
}

function buscar_fecha(fecha){
    fetch(`http://127.0.0.1:5000/ver_fecha/${id}/${fecha}`)
    .then((res) => res.json())
    .then(crear_tabla)
    .catch(request_error)
}

function crear_fechas(torneo){
    let fechas = document.getElementById("fechas");
    let cant_fechas;
    if(torneo.doble === 1){
        cant_fechas = torneo.cantidad-1;
    } else {
        cant_fechas = torneo.cantidad*2-2;  
    }
    for (let i = 1; i<=cant_fechas;i++){
        opcion = document.createElement("button");
        opcion.textContent = i;
        opcion.classList.add("botones");
        opcion.onclick = function() { buscar_fecha(i);};
        fechas.appendChild(opcion);
    }
    buscar_fecha(1);
}

function seleccionar_formato(extras){
    mostrar_goleadores = extras.goleadores;
    crear_fechas(extras);
}

function request_error(error) {
    console.log("ERROR");
    console.log(error);
    alert(error);
}

fetch(`http://localhost:5000/ver_extras/${id}`)
.then((res) => res.json())
.then(seleccionar_formato)
.catch(request_error)