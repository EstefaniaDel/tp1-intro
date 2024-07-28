## Readme
Trabajo Práctico 1 - Introducción al Desarrollo de Software (TB10) - FIUBA
Grupo: Tres Estrella
Integrantes: Estefanía , Nicolás , Joaquín Guerra

El proyecto consiste de una página web con su correspondiente frontend, backend e integración de base de datos, la cual permite crear y gestionar torneos de fútbol con sus respectivos equipos y los integrantes de los mismos. También permite el guardado de los goleadores y asistentes involucrados en los partidos, así como genera un calendario fecha a fecha para poder realizar el formato de liga "todos contra todos", tanto simple como doble.

## Requisitos para correr el proyecto
- Python
- Docker
- Docker-compose

## Correr

## Crear virtual enviroment
* Python -m venv venv
* source venv/bin/activate
* pip install -r requirements.txt

## Correr el proyecto con docker

* docker-compose up --build -d (-d es para no ver los logs)

* docker-compose down