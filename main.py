import fastapi
import sqlite3
from fastapi import applications, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Conexión a la base de datos SQLite
conn = sqlite3.connect('contactos.db')
cursor = conn.cursor()

# Crear tabla e insertar datos
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contactos';")
table_exists = cursor.fetchone()
if not table_exists:
    cursor.executescript('''
        CREATE TABLE contactos (
        email VARCHAR PRIMARY KEY,
        nombre TEXT,
        telefono TEXT
    );

    INSERT INTO contactos (email, nombre, telefono)
    VALUES ("juan@example.com", "Juan Pérez", "555-123-4567");

    INSERT INTO contactos (email, nombre, telefono)
    VALUES ("maria@example.com", "María García", "555-678-9012");
''')

conn.commit()
conn.close()

# Conexión a la base de datos SQLite
conn = sqlite3.connect('contactos.db')

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Reemplaza con la URL de tu aplicación frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

class Contacto(BaseModel):
    email: str
    nombre: str
    telefono: str

@app.post("/contactos")
async def crear_contacto(contacto: Contacto):
    """Crea un nuevo contacto."""
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contactos (email, nombre, telefono) VALUES (?, ?, ?)',
                   (contacto.email, contacto.nombre, contacto.telefono))
    conn.commit()
    return contacto

@app.get("/contactos")
async def obtener_contactos():
    """Obtiene todos los contactos."""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contactos')
    response = []
    for row in cursor:
        contacto = Contacto(email=row[0], nombre=row[1], telefono=row[2])
        response.append(contacto)
    return response

@app.get("/contactos/{email}")
async def obtener_contacto(email: str):
    """Obtiene un contacto por su email."""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contactos WHERE email = ?', (email,))
    row = cursor.fetchone()
    if row is not None:
        contacto = Contacto(email=row[0], nombre=row[1], telefono=row[2])
        return contacto
    else:
        return {"error": "Contacto no encontrado"}
    
@app.put("/contactos/{email}")
async def actualizar_contacto(email: str, contacto: Contacto):
    """Actualiza un contacto por su email."""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contactos WHERE email = ?', (email,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")

    cursor.execute('UPDATE contactos SET email = ?, nombre = ?, telefono = ? WHERE email = ?',
                   (contacto.email, contacto.nombre, contacto.telefono, email))
    conn.commit()
    return {"mensaje": "Contacto actualizado correctamente"}


@app.delete("/contactos/{email}")
async def eliminar_contacto(email: str):
    """Elimina un contacto."""
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contactos WHERE email = ?', (email,))
    conn.commit()
    return {"mensaje": "Contacto eliminado exitosamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
