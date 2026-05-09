Popayán Activa
Sistema web para la gestión de denuncias ciudadanas desarrollado con Django y Docker.

Descripción
Popayán Activa es una plataforma que permite a los ciudadanos registrar denuncias, realizar seguimiento de casos y visualizar el estado de las solicitudes de manera transparente.

Tecnologías utilizadas
Python 3
Django
SQLite / SQL Server
Docker
Bootstrap 5
Funcionalidades
Registro de denuncias ciudadanas
Gestión de estados de denuncias
Seguimiento de casos
Geolocalización
Panel administrativo
Filtros por estado y usuario
Estructura del proyecto
popayanactiva/
│
├── denuncias/
├── popayanactiva/
├── templates/
├── static/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py
Instalación local
1. Clonar el repositorio
git clone https://github.com/TU-USUARIO/popayanactiva.git
cd popayanactiva
2. Crear entorno virtual
python -m venv venv
3. Activar entorno virtual

Windows:
venv\Scripts\activate

Linux/Mac:
source venv/bin/activate
4. Instalar dependencias
pip install -r requirements.txt
5. Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate
6. Ejecutar servidor
python manage.py runserver

Abrir en navegador:
http://127.0.0.1:8000/
Ejecución con Docker
Construir contenedores
docker compose build
Levantar servicios
docker compose up
Ejecutar migraciones dentro del contenedor
docker compose exec web python manage.py migrate
Acceder al proyecto
http://localhost:8000/
Variables importantes

Configurar en settings.py:
DEBUG = True
ALLOWED_HOSTS = ['*']
Base de datos

El proyecto puede funcionar con:
SQLite (desarrollo)
SQL Server
PostgreSQL

Autor
Proyecto desarrollado para trabajo académico UNAD 2026.
Licencia
Proyecto de uso académico y educativo.
