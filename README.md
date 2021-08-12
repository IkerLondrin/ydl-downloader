# Youtube Video Downloader (WIP)
-----------------------------------

Aplicación para descarga de videos de youtube realizada mediante el microframework de flask, utilizando la versión 3.6 de python.


## Instalación de librerías

Instalar las librerías referenciadas en el archivo ``requierements.txt`` mediante el comando ``pip install -r requirements.txt`` (se recomienda hacerlo en un entorno virtual, ya sea mediante virtualenv, anaconda o similares)

## Ejecutar la aplicación

Para ejecutar la aplicación, basta con situarse activar el entorno virtual con las librerías instaladas y ejecutar ``python /path-to/__init__.py``

## Notas

Al lanzar la aplicación, la pantalla de credenciales que se mostrará al usuario está sujeta a una conexión a una base de datos SQL. En caso de no tener una o querer cambiar el método de verificación de login, se puede cambiar el proceso de inicio de sesión modificando el código del endpoint ``@login`` del archivo ``__init__.py``


