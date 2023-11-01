from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3  # Importa la biblioteca sqlite3
from pydantic import BaseModel  # Importa la biblioteca pydantic
import os
from fastapi.staticfiles import StaticFiles
import mysql.connector

app = FastAPI()



# Configuración de CORS para permitir acceso desde el puerto 8080
mysql_conn = mysql.connector.connect(
    host="cxmgkzhk95kfgbq4.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",  # Cambia esto por la URL o dirección IP de tu servidor MySQL
    user="mvvs08b6ffqn1u3k",  # Usuario de MySQL
    password="bs57pdwk1l1l7dlm",  # Contraseña de MySQL
    port="3306",
    database="ynbydh91h8238fjo" # Nombre de la base de datos MySQL
   
)



db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dbcontactos', 'contactos.db')
sql_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dbcontactos', 'contactos.sql')

if not os.path.exists(db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        with open(sql_file_path, 'r') as sql_file:
            cursor.executescript(sql_file.read())

class Contacto(BaseModel):
    email: str
    nombre: str
    telefono: str

# Rutas para las operaciones CRUD
@app.post("/contactos")
async def crear_contacto(contacto: Contacto):
    """Crea un nuevo contacto."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO contactos (email, nombre, telefono) VALUES (?, ?, ?)',
                       (contacto.email, contacto.nombre, contacto.telefono))
        conn.commit()
    return contacto

@app.get("/contactos")
async def obtener_contactos():
    """Obtiene todos los contactos."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contactos')
        response = []
        for row in cursor.fetchall():
            contacto = Contacto(email=row[0], nombre=row[1], telefono=row[2])
            response.append(contacto)
    return response

@app.get("/contactos/{email}")
async def obtener_contacto(email: str):
    """Obtiene un contacto por su email."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contactos WHERE email = ?', (email,))
        row = cursor.fetchone()
        if row:
            contacto = Contacto(email=row[0], nombre=row[1], telefono=row[2])
            return contacto
        return None

@app.put("/contactos/{email}")
async def actualizar_contacto(email: str, contacto: Contacto):
    """Actualiza un contacto."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE contactos SET nombre = ?, telefono = ? WHERE email = ?',
                       (contacto.nombre, contacto.telefono, email))
        conn.commit()
    return contacto

@app.delete("/contactos/{email}")
async def eliminar_contacto(email: str):
    """Elimina un contacto."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM contactos WHERE email = ?', (email,))
        conn.commit()
    return {"message": "Contacto eliminado correctamente"}