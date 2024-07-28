const params = new URLSearchParams(window.location.search);
const id_equipo = params.get("id_equipo");

function crearCelda(row, contenido) {
    let celda = row.insertCell();
    celda.classList.add("tabla-celda");
    celda.innerHTML = contenido;
    return celda;
}

function crear_tabla(jugadores) {
    console.log("RESPUESTA DE LA API:", jugadores); 

    if (!Array.isArray(jugadores)) {
        console.error("La respuesta de la API no es un array:", jugadores);
        return;
    }

    var table = document.getElementById("tablaCuerpo"); 
    table.innerHTML = ""; 

    console.log("Jugadores a mostrar:", jugadores);

    jugadores.forEach((jugador, index) => {
        let row = table.insertRow(-1);
        
        crearCelda(row, index + 1); 
        crearCelda(row, jugador.nombre);
        crearCelda(row, jugador.goles);
        crearCelda(row, jugador.asistencias);
    });
}

function request_error(error) {
    console.log("ERROR");
    console.log(error);
    alert(error);
}

fetch(`http://localhost:5000/jugadores`)
    .then(res => res.json())
    .then(data => {
        console.log("Datos de la API:", data); 
        if (Array.isArray(data)) {
            
            const jugadores_equipo = data.filter(jugador => 
                jugador.id_equipo == id_equipo && 
                (jugador.goles > 0 || jugador.asistencias > 0)
            );
            console.log("Jugadores filtrados:", jugadores_equipo);
            crear_tabla(jugadores_equipo);
        } else {
            console.error("No se encontraron jugadores en la respuesta:", data);
        }
    })
    .catch(request_error);
