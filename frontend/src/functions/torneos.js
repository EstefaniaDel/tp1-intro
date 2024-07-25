document.addEventListener('DOMContentLoaded', function() {
    // Funcionalidad para crear un torneo
    const crearTorneoForm = document.getElementById('crearTorneoForm');
    if (crearTorneoForm) {
        crearTorneoForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const nombreTorneo = document.getElementById('nombreTorneo').value;
            const tipoTorneo = document.getElementById('tipoTorneo').value;
            
            fetch('http://localhost:5000/torneo/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    nombre_torneo: nombreTorneo,
                    tipo_torneo: tipoTorneo
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.Error) {
                    alert(data.Error);
                } else {
                    alert(data.mensaje);
                    crearTorneoForm.reset();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("Error al crear el torneo");
            });
        });
    }

    // Funcionalidad para ver torneos
    const torneosList = document.getElementById('torneosList');
    if (torneosList) {
        fetch('http://localhost:5000/torneos')
            .then(response => response.json())
            .then(data => {
                data.forEach(torneo => {
                    const li = document.createElement('li');
                    li.className = 'list-group-item d-flex justify-content-between align-items-center';
                    li.textContent = `Nombre: ${torneo.nombre_torneo}, Tipo: ${torneo.tipo_torneo}`;
                    
                    const editButton = document.createElement('a');
                    editButton.href = `editar_torneo.html?id=${torneo.id}`;
                    editButton.textContent = 'Editar';
                    editButton.className = 'btn btn-warning btn-sm';
                    li.appendChild(editButton);

                    torneosList.appendChild(li);
                });
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
