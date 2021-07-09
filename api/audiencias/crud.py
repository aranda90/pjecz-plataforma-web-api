"""
Audiencias, CRUD: the four basic operations (create, read, update, and delete) of data storage
"""
from datetime import datetime, date
from sqlalchemy.orm import Session

from api.audiencias.models import Audiencia
from api.autoridades.models import Autoridad
from api.distritos.models import Distrito


def get_audiencias(db: Session, autoridad_id: int = None, fecha: date = None, ano: int = None):
    """Consultar audiencias"""
    audiencias = db.query(Audiencia, Autoridad, Distrito).select_from(Audiencia).join(Autoridad).join(Distrito)
    if autoridad_id:
        audiencias = audiencias.filter(Audiencia.autoridad_id == autoridad_id)
    if fecha:
        desde = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=0, minute=0, second=0)
        hasta = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=23, minute=59, second=59)
        audiencias = audiencias.filter(Audiencia.tiempo >= desde).filter(Audiencia.tiempo <= hasta)
    elif ano is not None and 2000 <= ano <= date.today().year:
        audiencias = audiencias.filter(Audiencia.tiempo >= date(ano, 1, 1)).filter(Audiencia.tiempo <= date(ano, 12, 31))
    return audiencias.filter(Audiencia.estatus == "A").order_by(Audiencia.tiempo.desc()).limit(500).all()


def get_audiencia(db: Session, audiencia_id: int):
    """Consultar un audiencia"""
    return db.query(Audiencia).get(audiencia_id)
