"""
Autoridades v2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.safe_string import safe_string
from ...models.autoridades.models import Autoridad
from ..distritos.crud import get_distrito
from ..materias.crud import get_materia


def get_autoridades(
    db: Session,
    distrito_id: int = None,
    materia_id: int = None,
    organo_jurisdiccional: str = None,
    con_notarias: bool = False,
    para_glosas: bool = False,
) -> Any:
    """Consultar las Autoridades activas"""
    consulta = db.query(Autoridad)
    if distrito_id is not None:
        distrito = get_distrito(db, distrito_id)
        consulta = consulta.filter(Autoridad.distrito == distrito)
    if materia_id is not None:
        materia = get_materia(db, materia_id)
        consulta = consulta.filter(Autoridad.materia == materia)
    organo_jurisdiccional = safe_string(organo_jurisdiccional)
    if organo_jurisdiccional in Autoridad.ORGANOS_JURISDICCIONALES:
        consulta = consulta.filter(Autoridad.organo_jurisdiccional == organo_jurisdiccional)
    if con_notarias is False:
        consulta = consulta.filter(Autoridad.es_notaria == False)
    if para_glosas:
        consulta = consulta.filter(Autoridad.organo_jurisdiccional.in_(["PLENO O SALA DEL TSJ", "TRIBUNAL DE CONCILIACION Y ARBITRAJE"]))
    return consulta.filter(Autoridad.es_jurisdiccional == True).filter_by(estatus="A").order_by(Autoridad.clave)


def get_autoridad(db: Session, autoridad_id: int) -> Autoridad:
    """Consultar una Autoridad por su id"""
    autoridad = db.query(Autoridad).get(autoridad_id)
    if autoridad is None:
        raise IndexError("No existe ese autoridades")
    if autoridad.estatus != "A":
        raise ValueError("No es activo ese autoridades, está eliminado")
    return autoridad


def get_autoridad_from_clave(db: Session, autoridad_clave: str) -> Autoridad:
    """Consultar una Autoridad por su clave"""
    clave = safe_string(autoridad_clave)
    if clave == "":
        raise ValueError("No es valida la clave")
    autoridad = db.query(Autoridad).filter_by(clave=clave).first()
    if autoridad is None:
        raise IndexError("No existe ese autoridades")
    if autoridad.estatus != "A":
        raise ValueError("No es activa esa autoridad, está eliminada")
    return autoridad
