"""
Listas de Acuerdos, CRUD: the four basic operations (create, read, update, and delete) of data storage
"""
from datetime import datetime
from sqlalchemy.orm import Session
from api.listas_de_acuerdos import models, schemas


def get_listas_de_acuerdos(db: Session, autoridad_id: int = None):
    """ Consultar listas de acuerdos """
    listas_de_acuerdos = db.query(models.ListaDeAcuerdo)
    if autoridad_id:
        listas_de_acuerdos = listas_de_acuerdos.filter(models.ListaDeAcuerdo.autoridad_id == autoridad_id)
    return listas_de_acuerdos.filter(models.ListaDeAcuerdo.estatus == "A").order_by(models.ListaDeAcuerdo.fecha.desc()).limit(100).all()


def get_lista_de_acuerdo(db: Session, lista_de_acuerdo_id: int):
    """ Consultar una lista de acuerdos """
    return db.query(models.ListaDeAcuerdo).get(lista_de_acuerdo_id)


def new_lista_de_acuerdo(db: Session, esquema: schemas.ListaDeAcuerdoNew):
    """ Nueva lista de acuerdos """
    if esquema.fecha is None:
        esquema.fecha = datetime.now()
    if esquema.archivo is None:
        esquema.archivo = esquema.fecha.strftime("%Y-%m-%d") + "-lista-de-acuerdos.pdf"
    if esquema.descripcion is None:
        esquema.descripcion = "Lista de Acuerdo"
    if esquema.url is None:
        esquema.url = "https://storage.google.com/DEPOSITO/Listas de Acuerdos/DISTRITO/AUTORIDAD/YYYY/MM/" + esquema.archivo
    lista_de_acuerdo = models.ListaDeAcuerdo(**esquema.dict())
    db.add(lista_de_acuerdo)
    db.commit()
    db.refresh(lista_de_acuerdo)
    return lista_de_acuerdo
