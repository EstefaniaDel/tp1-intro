function boton_editar() {
  let editar = document.createElement("button");
  editar.textContent = "+";
  editar.classList.add("botones");
  return editar;
}

function boton_eliminar() {
  let borrar = document.createElement("button");
  borrar.textContent = "Edit";
  borrar.classList.add("botones");
  return borrar;
}

function procesar(data) {
  console.log(data);
  for (let i = 0; i < data.length; i++) {
    let torneo = data[i];
    let tabla = document.getElementById("tabla");
    let fila = tabla.insertRow(-1);
    let nombre = fila.insertCell(0);
    nombre.innerHTML = torneo.nombre;
    let celda_cantidad = fila.insertCell(1);
    celda_cantidad.innerHTML = torneo.cantidad;
    let celda_guardar = fila.insertCell(2);
    if (torneo.jugadores_guardar === 1) {
      celda_guardar.innerHTML = "SI";
    } else {
      celda_guardar.innerHTML = "NO";
    }
    let celda_goleadores = fila.insertCell(3);
    if (torneo.goleadores === 1) {
      celda_goleadores.innerHTML = "SI";
    } else {
      celda_goleadores.innerHTML = "NO";
    }
    let celda_asistentes = fila.insertCell(4);
    if (torneo.asistentes === 1) {
      celda_asistentes.innerHTML = "SI";
    } else {
      celda_asistentes.innerHTML = "NO";
    }
    let celda_botones = fila.insertCell(5);
    celda_botones.appendChild(boton_eliminar());
    celda_botones.appendChild(boton_editar());
  }
}

function request_error(error) {
  console.log("ERROR");
  console.log(error);
  alert(error);
}

function mostrar_torneos() {
  fetch(`http://localhost:5000/ver_torneos`)
    .then((res) => res.json())
    .then(procesar)
    .catch(request_error);
}

mostrar_torneos();
