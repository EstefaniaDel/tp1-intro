var cantidad_equipos;
var equipo_actual;
var jugadores_guardar;

const params = new URLSearchParams(window.location.search);
const id = params.get("id");

if (id === null) {
  window.location.href = "http://localhost:8000/crear_torneo";
}

function request_error(error) {
  console.log("ERROR");
  console.log(error);
  alert(error);
}

function equipo_creado(data){
  console.log(data);
}

function agregar_jugador(){
  jugadores = document.getElementById("jugadores");
  let div = document.createElement("div");
  let ingrese = document.createElement("h4");
  ingrese.textContent = "Ingrese un jugador";
  let input = document.createElement("input");
  input.name = 'nombres';
  input.placeholder = 'ingrese el nombre del jugador';
  div.appendChild(ingrese);
  div.appendChild(input);
  jugadores.appendChild(div);
}

function subir_equipo(datos){
  fetch("http://localhost:5000/crear_equipo" ,{
    method: 'POST',
    headers: {
    'Content-Type': 'application/json'
  },
    body: JSON.stringify(datos)
  })
  .then((res) => res.json())
  .then(equipo_creado)
  .catch(request_error)
}

function cruces_creados(data){
  console.log(data);
}

function crear_cruces(){
  fetch(`http://localhost:5000/generar_fechas/${id}`)
  .then((res) => res.json())
  .then(cruces_creados)
  .catch(request_error)
}

function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}

function verificar_caso(){
  if (equipo_actual<=cantidad_equipos){
    let nombre_equipo = document.getElementById("nombre");
    nombre_equipo.value = "";
    mostrar();
  } else{
    sleep(500);
    crear_cruces();
    alert("equipos creados con exito");
    window.location.href = `http://localhost:8000/administrar_torneo?id=${id}`;
  }
}

function actualizar(){
  equipo_actual += 1;
  var datos = {
    nombre : document.getElementById("nombre").value,
    torneo : id,
    guardar : jugadores_guardar,
    jugadores : []
  };
  if (jugadores_guardar == 1){
    const nombres = document.querySelectorAll('input[name="nombres"]');
    for (let i = 0; i<nombres.length;i++){
      datos.jugadores.push(nombres[i].value);      
    }
  }
  subir_equipo(datos);
  verificar_caso();
}

function mostrar(){
  titulo = document.getElementById("numero_equipo")
  titulo.innerText = "equipo " + String(equipo_actual);
  if (jugadores_guardar == 1){
    jugadores = document.getElementById("jugadores");
    jugadores.innerHTML = "";
    for (let i = 0; i<5;i++){
      agregar_jugador();
    }
    agregar = document.getElementById("boton");
    agregar.innerHTML = "";
    boton = document.createElement("button");
    boton.classList.add("botones");
    boton.onclick = function() {agregar_jugador();};
    boton.textContent = "+";
    agregar.appendChild(boton);
  }
}

function procesar(data){
  cantidad_equipos = data.cantidad;
  equipo_actual = 1;
  jugadores_guardar = data.guardar;
  mostrar();
}

fetch(`http://localhost:5000/ver_extras/${id}`)
.then((res) => res.json())
.then(procesar)
.catch(request_error)