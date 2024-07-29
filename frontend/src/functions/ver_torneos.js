function procesar(data) {
  console.log(data);
  const tablaTorneos = document.getElementById("tablaTorneos");
  for (let i = 0; i < data.length; i++) {
    let torneo = data[i];
    let fila = tablaTorneos.insertRow(-1);
    let nombre = fila.insertCell(0);
    nombre.innerHTML = torneo.nombre;
    let celda_cantidad = fila.insertCell(1);
    celda_cantidad.innerHTML = torneo.cantidad;
    let celda_guardar = fila.insertCell(2);
    celda_guardar.innerHTML = torneo.jugadores_guardar === 1 ? "SI" : "NO";
    let celda_goleadores = fila.insertCell(3);
    celda_goleadores.innerHTML = torneo.goleadores === 1 ? "SI" : "NO";
    let celda_asistentes = fila.insertCell(4);
    celda_asistentes.innerHTML = torneo.asistentes === 1 ? "SI" : "NO";
    let celda_botones = fila.insertCell(5);
    celda_botones.innerHTML = `
      <button type="button" class="btn btn-primary" onclick="editarTorneo(${torneo.id})">
        <i class="bi bi-pencil-square"></i> 
      </button>
      <button type="button" class="btn btn-danger" onclick="eliminarTorneo(${torneo.id})">
        <i class="bi bi-trash3-fill"></i> 
      </button>
    `;
  }
}

function editarTorneo(torneoId) {
  Swal.fire({
    title: "Ingrese el nuevo nombre del torneo:",
    input: "text",
    inputPlaceholder: "Nuevo nombre",
    showCancelButton: true,
    confirmButtonText: "Guardar",
    cancelButtonText: "Cancelar",
    customClass: {
      confirmButton: "btn btn-primary",
      cancelButton: "btn btn-secondary",
    },
  }).then((result) => {
    if (result.isConfirmed && result.value) {
      const nuevoNombre = result.value;
      fetch(`http://localhost:5000/torneo/${torneoId}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ nombre_torneo: nuevoNombre }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Error al actualizar el torneo");
          }
          return response.json();
        })
        .then((data) => {
          Swal.fire({
            title: "¡Actualizado!",
            text: data.mensaje,
            icon: "success",
            confirmButtonText: "Aceptar",
            customClass: {
              confirmButton: "btn btn-primary",
            },
          });
          mostrar_torneos();
        })
        .catch((error) => {
          console.error("Error:", error);
          Swal.fire({
            title: "Error",
            text: "No se pudo actualizar el torneo",
            icon: "error",
            confirmButtonText: "Aceptar",
            customClass: {
              confirmButton: "btn btn-danger",
            },
          });
        });
    }
  });
}

function eliminarTorneo(torneoId) {
  Swal.fire({
    title: "¿Estás seguro de que deseas eliminar este torneo?",
    text: "¡Esta acción no se puede deshacer!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Eliminar",
    cancelButtonText: "Cancelar",
    customClass: {
      confirmButton: "btn btn-danger",
      cancelButton: "btn btn-secondary",
    },
  }).then((result) => {
    if (result.isConfirmed) {
      fetch(`http://localhost:5000/torneo/${torneoId}`, {
        method: "DELETE",
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Error al eliminar el torneo");
          }
          return response.json();
        })
        .then((data) => {
          Swal.fire({
            title: "¡Eliminado!",
            text: data.mensaje,
            icon: "success",
            confirmButtonText: "Aceptar",
            customClass: {
              confirmButton: "btn btn-primary",
            },
          });
          mostrar_torneos();
        })
        .catch((error) => {
          console.error("Error:", error);
          Swal.fire({
            title: "Error",
            text: "No se pudo eliminar el torneo",
            icon: "error",
            confirmButtonText: "Aceptar",
            customClass: {
              confirmButton: "btn btn-danger",
            },
          });
        });
    }
  });
}

function request_error(error) {
  console.log("ERROR");
  console.log(error);
  alert(error);
}

function mostrar_torneos() {
  fetch(`http://localhost:5000/ver_torneos`)
    .then((res) => res.json())
    .then((data) => {
      const tablaTorneos = document.getElementById("tablaTorneos");
      tablaTorneos.innerHTML = "";

      procesar(data);
    })
    .catch(request_error);
}

mostrar_torneos();
