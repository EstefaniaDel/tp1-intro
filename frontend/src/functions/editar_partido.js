const params = new URLSearchParams(window.location.search);
const id = params.get("id");
var id_torneo;

function request_error(error) {
  console.log("ERROR");
  console.log(error);
  Swal.fire({
    icon: 'error',
    title: 'Error',
    text: error
  });
}

function redireccion(data) {
  console.log(data);
  Swal.fire({
    icon: 'success',
    title: 'Éxito',
    text: 'Resultado modificado con éxito',
    customClass: {
      confirmButton: 'btn btn-primary' // Botón de aceptar
    }
  }).then(() => {
    window.location.href = `http://localhost/src/pages/ver_partidos?id=${id_torneo}`;
  });
}

function subir_resultado() {
  const datos = {
    id_partido: id,
    goles1: document.getElementById(1).value,
    goles2: document.getElementById(2).value,
  };
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

function crear_goles(id_goles) {
  select = document.createElement("select");
  select.id = id_goles;
  for (let i = 0; i <= 20; i++) {
    opcion = document.createElement("option");
    opcion.textContent = i;
    select.appendChild(opcion);
  }
  return select;
}
function mostrar_partido(partido) {
  id_torneo = partido.id_torneo;
  let plantilla = document.getElementById("partido");
  let fila1 = plantilla.insertRow(-1);
  let equipos = fila1.insertCell(0);
  let resultados = fila1.insertCell(1);
  equipos.innerHTML = "EQUIPOS";
  resultados.innerHTML = "RESULTADO";
  let fila2 = plantilla.insertRow(-1);
  let equipo1 = fila2.insertCell(0);
  let resultado1 = fila2.insertCell(1);
  equipo1.innerHTML = partido.equipo1;
  resultado1.appendChild(crear_goles(1));
  let fila3 = plantilla.insertRow(-1);
  let equipo2 = fila3.insertCell(0);
  let resultado2 = fila3.insertCell(1);
  equipo2.innerHTML = partido.equipo2;
  resultado2.appendChild(crear_goles(2));
}

fetch(`http://localhost:5000/ver_partido/${id}`)
  .then((res) => res.json())
  .then(mostrar_partido)
  .catch(request_error);
