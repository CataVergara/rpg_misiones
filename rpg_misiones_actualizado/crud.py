from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models, schemas
from fastapi import HTTPException

def crear_personaje(db: Session, personaje: schemas.PersonajeCreate):
    db_personaje = models.Personaje(nombre=personaje.nombre)
    db.add(db_personaje)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Ya existe un personaje con ese nombre")
    db.refresh(db_personaje)
    return db_personaje

def crear_mision(db: Session, mision: schemas.MisionCreate):
    db_mision = models.Mision(**mision.dict())
    db.add(db_mision)
    db.commit()
    db.refresh(db_mision)
    return db_mision

def obtener_personaje(db: Session, personaje_id: int):
    return db.query(models.Personaje).filter(models.Personaje.id == personaje_id).first()

def obtener_mision(db: Session, mision_id: int):
    return db.query(models.Mision).filter(models.Mision.id == mision_id).first()

def aceptar_mision(db: Session, personaje: models.Personaje, mision: models.Mision):
    if mision not in personaje.misiones:
        personaje.misiones.append(mision)
        db.commit()
        db.refresh(personaje)
    return personaje

def completar_mision(db: Session, personaje: models.Personaje, mision: models.Mision):
    if mision in personaje.misiones:
        personaje.experiencia += mision.experiencia
        personaje.misiones.remove(mision)
        db.commit()
        db.refresh(personaje)
    return personaje

def misiones_personaje(db: Session, personaje_id: int):
    personaje = obtener_personaje(db, personaje_id)
    if personaje:
        return personaje.misiones
    return []