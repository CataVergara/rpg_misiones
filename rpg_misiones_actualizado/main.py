from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas, crud
from database import SessionLocal, engine
from tda_cola import ColaMisiones

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

colas = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/personajes", response_model=schemas.Personaje)
def crear_personaje(personaje: schemas.PersonajeCreate, db: Session = Depends(get_db)):
    nuevo = crud.crear_personaje(db, personaje)
    colas[nuevo.id] = ColaMisiones()
    return nuevo

@app.post("/misiones", response_model=schemas.Mision)
def crear_mision(mision: schemas.MisionCreate, db: Session = Depends(get_db)):
    return crud.crear_mision(db, mision)

@app.post("/personajes/{personaje_id}/misiones/{mision_id}")
def aceptar_mision(personaje_id: int, mision_id: int, db: Session = Depends(get_db)):
    personaje = crud.obtener_personaje(db, personaje_id)
    mision = crud.obtener_mision(db, mision_id)
    if not personaje or not mision:
        raise HTTPException(status_code=404, detail="Personaje o misión no encontrado")

    # 🔒 Asegurar que la cola exista
    if personaje_id not in colas:
        colas[personaje_id] = ColaMisiones()

    crud.aceptar_mision(db, personaje, mision)
    colas[personaje_id].enqueue(mision)
    return {"mensaje": "Misión aceptada"}

@app.post("/personajes/{personaje_id}/completar")
def completar_mision(personaje_id: int, db: Session = Depends(get_db)):
    personaje = crud.obtener_personaje(db, personaje_id)
    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    cola = colas.get(personaje_id)
    if cola is None or cola.is_empty():
        raise HTTPException(status_code=400, detail="No hay misiones en cola")

    mision = cola.dequeue()
    xp_ganada = mision.experiencia
    crud.completar_mision(db, personaje, mision)

    return {"mensaje": "Misión completada", "xp_ganada": xp_ganada}

@app.get("/personajes/{personaje_id}/misiones", response_model=List[schemas.Mision])
def listar_misiones(personaje_id: int):
    cola = colas.get(personaje_id)
    if cola:
        return cola.listar()
    return []
