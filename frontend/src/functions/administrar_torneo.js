const params = new URLSearchParams(window.location.search);
const id = params.get("id");

function redireccion() {
  window.location.href = `http://localhost/src/pages/ver_partidos?id=${id}`;
}

function redireccion2() {
  window.location.href = `http://localhost/src/pages/goleadores_asistentes?id=${id}`;
}
function crear_link(nombre_equipo, id_equipo) {
  let nombre = document.createElement("a");
  nombre.href = `http://localhost/src/pages/administrar_equipo?id=${id_equipo}`;
  nombre.classList.add("link");
  nombre.innerText = nombre_equipo;
  return nombre;
}

function crearCelda(row, contenido) {
  let celda = row.insertCell();
  celda.classList.add("tabla-celda");
  celda.innerHTML = contenido;
  return celda;
}

function crear_tabla(equipos) {
  console.log("RESPUESTA DE LA API:", equipos); // Verifica la respuesta

  if (!Array.isArray(equipos)) {
    console.error("La respuesta de la API no es un array:", equipos);
    return;
  }

  var table = document.getElementById("tablaEquipos");
  table.innerHTML = "";

  console.log("Equipos a mostrar:", equipos);

  equipos.sort((a, b) => b.puntos - a.puntos);
  equipos.sort((a, b) => b.diferencia - a.diferencia);

  equipos.forEach((equipo, index) => {
    let row = table.insertRow(-1);

    crearCelda(row, index + 1);
    crearCelda(
      row,
      `<button type="button" class="btn btn-link" data-toggle="modal" data-target="#equipoModal" data-id="${equipo.id}">${equipo.nombre}</button>`
    );
    crearCelda(row, equipo.puntos);
    crearCelda(row, equipo.victorias + equipo.empates + equipo.derrotas);
    crearCelda(row, equipo.victorias);
    crearCelda(row, equipo.empates);
    crearCelda(row, equipo.derrotas);
    crearCelda(row, equipo.goles);
    crearCelda(row, equipo.en_contra);
    crearCelda(row, equipo.diferencia);
  });
}

function request_error(error) {
  console.log("ERROR");
  console.log(error);
  alert(error);
}

fetch(`http://localhost:5000/ver_torneo/${id}`)
  .then((res) => res.json())
  .then((data) => {
    console.log("Datos de la API:", data);
    crear_tabla(data);
  })
  .catch(request_error);

// Evento para cargar la información del equipo en el modal
$("#equipoModal").on("show.bs.modal", function (event) {
  var button = $(event.relatedTarget);
  var id_equipo = button.data("id");

  fetch(`http://localhost:5000/jugadores/equipo?id_equipo=${id_equipo}`)
    .then((res) => res.json())
    .then((jugadores) => {
      console.log("Datos de los jugadores:", jugadores);
      if (Array.isArray(jugadores)) {
        const tablaJugadores = $("#tablaJugadores");
        tablaJugadores.html("");

        jugadores.forEach((jugador, index) => {
          let row = document.createElement("tr");
          tablaJugadores.append(row);
          crearCelda(row, index + 1);
          crearCelda(row, jugador.nombre);
          crearCelda(row, jugador.goles);
          crearCelda(row, jugador.asistencias);
        });
      } else {
        console.error(
          "No se encontraron jugadores en la respuesta:",
          jugadores
        );
      }
    })
    .catch((error) => {
      console.error("Error al obtener los jugadores del equipo:", error);
    });
});
