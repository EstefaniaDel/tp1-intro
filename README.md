## Readme
### Trabajo Práctico 1 - Introducción al Desarrollo de Software (TB10) - FIUBA
### Grupo: Tres Estrellas ⭐ ⭐ ⭐ 
### *Integrantes: Estefanía, Nicolás, Joaquín Guerra*

El proyecto consiste en una página web con su correspondiente frontend, backend e integración de base de datos, la cual permite crear y gestionar torneos de fútbol con sus respectivos equipos y los integrantes de los mismos. También permite el guardado de los goleadores y asistentes involucrados en los partidos, así como genera un calendario fecha a fecha para poder realizar el formato de liga "todos contra todos", tanto simple como doble.

## Requisitos para correr el proyecto
- Linux
- Python
- Docker
- Docker-compose

## Pasos de Ejecucion
### Crear virtual enviroment
*Si se desea manipular el backend se debe dar uso a un entorno virtual*

- Crear un entorno virtual para la instalacion de paquetes 
```bash
Python -m venv venv
```
- Activar el entorno
```bash
source venv/bin/activate
```
- Instalar los paquetes
```bash
pip install -r requirements.txt
```

### Correr el proyecto con docker
*Primero se debera crear un archivo .env con los datos de la dabase de datos*
- Correr el docker compilando los paquetes necesario y armando las imagenes/servicios necesarios. **-d para evitar ver los logs en tiempo real**

```bash
docker-compose up --build -d 
```
- Para bajar el docker
```bash
docker-compose down
```