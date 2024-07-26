const params = new URLSearchParams(window.location.search);
const id = params.get("id");

function redireccion(){
  window.location.href = `http://localhost:8000/ver_partidos?id=${id}`;
}

function crear_link(nombre_equipo,id_equipo){
  let nombre = document.createElement("a");
  nombre.href = `http://localhost:8000/administrar_equipos?id=${id_equipo}`;
  nombre.classList.add("link");
  nombre.innerText = nombre_equipo;
  return nombre;
}

function crear_tabla(equipos) {
  var table = document.getElementById("myTable");
  equipos.sort(function(a,b){return a.diferencia>b.diferencia?-1:1});
  equipos.sort(function(a,b){return (b.puntos) - (a.puntos)});
  for (let i = 0 ; i< equipos.length;i++){
  var equipo = equipos[i];
  var row = table.insertRow(-1);
  var nombre = row.insertCell(0);
  var puntos = row.insertCell(1);
  var jugados = row.insertCell(2);
  var ganados = row.insertCell(3);
  var empatados = row.insertCell(4);
  var perdidos = row.insertCell(5);
  var goles = row.insertCell(6);
  var contra = row.insertCell(7);
  var diferencia = row.insertCell(8);
  nombre.appendChild(crear_link(equipo.nombre,equipo.id));
  puntos.innerHTML = equipo.puntos;
  jugados.innerHTML = equipo.victorias + equipo.empates + equipo.derrotas;
  ganados.innerHTML = equipo.victorias;
  empatados.innerHTML = equipo.empates;
  perdidos.innerHTML = equipo.derrotas;
  goles.innerHTML = equipo.goles;
  contra.innerHTML = equipo.en_contra;
  diferencia.innerHTML = equipo.diferencia;
}
}

function request_error(error) {
  console.log("ERROR");
  console.log(error);
  alert(error);
}

fetch(`http://127.0.0.1:5000/ver_torneo/${id}`)
.then((res) => res.json())
.then(crear_tabla)
.catch(request_error)