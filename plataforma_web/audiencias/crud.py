"""
Audiencias, CRUD: the four basic operations (create, read, update, and delete) of data storage
"""
from datetime import datetime, date
from sqlalchemy.orm import Session

from plataforma_web.audiencias.models import Audiencia
from plataforma_web.autoridades.crud import get_autoridad
from plataforma_web.autoridades.models import Autoridad
from plataforma_web.distritos.models import Distrito


def get_audiencias(db: Session, autoridad_id: int = None, fecha: date = None, ano: int = None):
    """Consultar audiencias"""
    audiencias = db.query(Audiencia, Autoridad, Distrito).select_from(Audiencia).join(Autoridad).join(Distrito)
    if autoridad_id:
        autoridad = get_autoridad(db, autoridad_id=autoridad_id)
        audiencias = audiencias.filter(Audiencia.autoridad == autoridad)
    if fecha:
        desde = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=0, minute=0, second=0)
        hasta = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=23, minute=59, second=59)
        audiencias = audiencias.filter(Audiencia.tiempo >= desde).filter(Audiencia.tiempo <= hasta)
    elif ano is not None and 2000 <= ano <= date.today().year:
        audiencias = audiencias.filter(Audiencia.tiempo >= date(ano, 1, 1)).filter(Audiencia.tiempo <= date(ano, 12, 31))
    return audiencias.filter(Audiencia.estatus == "A").order_by(Audiencia.tiempo.desc()).limit(500).all()


def get_audiencia(db: Session, audiencia_id: int):
    """Consultar un audiencia"""
    audiencia = db.query(Audiencia).get(audiencia_id)
    if audiencia is None:
        raise IndexError
    if audiencia.estatus != "A":
        raise ValueError("No es activa la audiencia, está eliminada")
    return audiencia
