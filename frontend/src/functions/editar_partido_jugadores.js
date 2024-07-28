const params = new URLSearchParams(window.location.search);
const id = params.get("id");
var jugadores;
var id_torneo;
var golesLocal = 0;
var golesVisitante = 0;

function request_error(error) {
  console.log("ERROR");
  console.log(error);
  alert(error);
}

function redireccion(data) {
  console.log(data);
  alert("Resultado modificado con exito!");
  window.location.href = `http://localhost/src/pages/ver_partidos?id=${id_torneo}`;
}

function subir_resultado() {
  var datos = {
    id_partido: id,
    goles1: golesLocal,
    goles2: golesVisitante,
    goles: [],
  };
  const goleadores1 = document.querySelectorAll(
    'select[name="goleadoresequipo1"]'
  );
  const asistentes1 = document.querySelectorAll(
    'select[name="asistentesequipo1"]'
  );
  for (let i = 0; i < goleadores1.length; i++) {
    var dic = {
      goleador: goleadores1[i].value,
      asistente: asistentes1[i].value,
    };
    datos.goles.push(dic);
  }
  const goleadores2 = document.querySelectorAll(
    'select[name="goleadoresequipo2"]'
  );
  const asistentes2 = document.querySelectorAll(
    'select[name="asistentesequipo2"]'
  );
  for (let i = 0; i < goleadores2.length; i++) {
    var dic = {
      goleador: goleadores2[i].value,
      asistente: asistentes2[i].value,
    };
    datos.goles.push(dic);
  }
  console.log(datos);
  fetch("http://localhost:5000/editar_partido", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(datos),
  })
    .then((res) => res.json())
    .then(redireccion)
    .catch(request_error);
}

function actualizar_gol() {
  let resultado = document.getElementById("resultado");
  resultado.innerHTML = `${golesLocal}-${golesVisitante}`;
}

function eliminar_gol(esLocal) {
  let select;
  if (esLocal) {
    select = document.getElementById("select_local");
    let longitud = select.rows.length;
    if (longitud > 0) {
      golesLocal -= 1;
      select.deleteRow(longitud - 1);
    }
  } else {
    select = document.getElementById("select_visitante");
    let longitud = select.rows.length;
    if (longitud > 0) {
      golesVisitante -= 1;
      select.deleteRow(longitud - 1);
    }
  }
  actualizar_gol();
}

function crear_select(equipo) {
  let select = document.createElement("select");
  select.name = `goleadores${equipo}`;
  for (let i = 0; i < jugadores[equipo].length; i++) {
    let jugador = jugadores[equipo][i];
    let option = document.createElement("option");
    option.textContent = jugador["nombre"];
    option.value = jugador["id"];
    select.appendChild(option);
  }
  return select;
}

function crear_select_asistencia(equipo) {
  let select = document.createElement("select");
  select.name = `asistentes${equipo}`;
  for (let i = 0; i < jugadores[equipo].length; i++) {
    let jugador = jugadores[equipo][i];
    let option = document.createElement("option");
    option.textContent = jugador["nombre"];
    option.value = jugador["id"];
    select.appendChild(option);
  }
  return select;
}

function agregar_gol(esLocal) {
  let select;
  let equipo;
  if (esLocal) {
    golesLocal += 1;
    select = document.getElementById("select_local");
    equipo = "equipo1";
  } else {
    golesVisitante += 1;
    select = document.getElementById("select_visitante");
    equipo = "equipo2";
  }
  let fila = select.insertRow(-1);
  let gol = fila.insertCell(0);
  let asistencia = fila.insertCell(1);
  gol.appendChild(crear_select(equipo));
  asistencia.appendChild(crear_select_asistencia(equipo));
  actualizar_gol();
}

function guardar(jugadores_equipos) {
  jugadores = jugadores_equipos;
}

function guardar_jugadores(equipo1, equipo2) {
  fetch(`http://localhost:5000/ver_jugadores_doble/${equipo1}/${equipo2}`)
    .then((res) => res.json())
    .then(guardar)
    .catch(request_error);
}
function mostrar_partido(partido) {
  guardar_jugadores(partido.id1, partido.id2);
  id_torneo = partido.id_torneo;
  let local = document.getElementById("local");
  let resultado = document.getElementById("resultados");
  let visitante = document.getElementById("visitante");
  let equipo1 = document.createElement("h3");
  let goles = document.createElement("h3");
  goles.id = "resultado";
  let equipo2 = document.createElement("h3");
  equipo1.innerHTML = partido.equipo1;
  equipo2.innerHTML = partido.equipo2;
  goles.innerHTML = `${golesLocal}-${golesVisitante}`;
  local.appendChild(equipo1);
  resultado.appendChild(goles);
  visitante.appendChild(equipo2);
  let tabla_select_l = document.createElement("table");
  let fila_l = tabla_select_l.insertRow(-1);
  let gol_l = fila_l.insertCell(0);
  let asistencia_l = fila_l.insertCell(1);
  gol_l.innerHTML = "Goles";
  asistencia_l.innerHTML = "Asistencia";
  tabla_select_l.id = "select_local";
  let tabla_select_v = document.createElement("table");
  let fila_v = tabla_select_v.insertRow(-1);
  let gol_v = fila_v.insertCell(0);
  let asistencia_v = fila_v.insertCell(1);
  gol_v.innerHTML = "Goles";
  asistencia_v.innerHTML = "Asistencia";
  tabla_select_v.id = "select_visitante";
  gol_l.classList.add("tabla_izq");
  gol_v.classList.add("tabla_izq");
  asistencia_l.classList.add("tabla_der");
  asistencia_v.classList.add("tabla_der");
  local.appendChild(tabla_select_l);
  visitante.appendChild(tabla_select_v);
}

fetch(`http://localhost:5000/ver_partido/${id}`)
  .then((res) => res.json())
  .then(mostrar_partido)
  .catch(request_error);
