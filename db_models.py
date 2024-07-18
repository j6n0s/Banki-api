from extensions import db


class Ugyfel(db.Model):
    __tablename__ = 'ugyfel'
    #__table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nev = db.Column(db.String(80))
    tel = db.Column(db.String(11))
    email = db.Column(db.String(80), unique=True)
    szulido = db.Column(db.Date)
    lakcim = db.Column(db.String(120))
    jelszo_hash = db.Column(db.String(40))
    admin = db.Column(db.Boolean)

    szamlaszamok = db.relationship("Szamla", back_populates="ugyfelek")


class Szamla(db.Model):
    __tablename__ = 'szamla'
    #__table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    ugyfel_id = db.Column(db.ForeignKey("ugyfel.id"))
    egyenleg = db.Column(db.Integer)

    ugyfelek = db.relationship("Ugyfel", back_populates="szamlaszamok")
    utalasok_fogado = db.relationship("Utalas", foreign_keys="[Utalas.fogado_szamla]", back_populates="fogado")
    utalasok_utatlo = db.relationship("Utalas", foreign_keys="[Utalas.utalo_szamla]", back_populates="utalo")
    befizetes = db.relationship("Befizetes", back_populates="szamlaszamok")
    penzfelvetel = db.relationship("Penzfelvetel", back_populates="szamlaszamok")


class Utalas(db.Model):
    __tablename__ = 'utalas'
    #__table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    osszeg = db.Column(db.Integer)
    fogado_szamla = db.Column(db.ForeignKey("szamla.id"))
    utalo_szamla = db.Column(db.ForeignKey("szamla.id"))
    ido = db.Column(db.DateTime)

    fogado = db.relationship("Szamla", foreign_keys=[fogado_szamla], back_populates="utalasok_fogado")
    utalo = db.relationship("Szamla", foreign_keys=[utalo_szamla], back_populates="utalasok_utatlo")


class Befizetes(db.Model):
    __tablename__ = 'befizetes'
    #__table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    osszeg = db.Column(db.Integer)
    szamla = db.Column(db.ForeignKey("szamla.id"))
    ido = db.Column(db.DateTime)

    szamlaszamok = db.relationship("Szamla", back_populates="befizetes")


class Penzfelvetel(db.Model):
    __tablename__ = 'penzfelvetel'
    #__table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    osszeg = db.Column(db.Integer)
    szamla = db.Column(db.ForeignKey("szamla.id"))
    ido = db.Column(db.DateTime)

    szamlaszamok = db.relationship("Szamla", back_populates="penzfelvetel")


'''
sqlite3 adatbázis létrehozása:
Flask shell-ben:
(parancs: flask shell)
from db_models import *
db.create_all()
exit()
'''