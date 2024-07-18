from flask_restx import fields

from extensions import api

# Szamla model
szamla_model = api.model("Szamla", {
    "id": fields.Integer,
    "ugyfel_id": fields.Integer,
    "egyenleg": fields.Integer
})

szamla_post_model = api.model("SzamlaLetrehozasa", {
    "ugyfel_id": fields.Integer,
    "egyenleg": fields.Integer
})

szamla_put_model = api.model("SzamlaModositasa", {
    "ugyfel_id": fields.Integer,
    "egyenleg": fields.Integer
})

# Ugyfel model
ugyfel_model = api.model("Register", {
    "id": fields.Integer,
    "nev": fields.String,
    "tel": fields.String,
    "email": fields.String,
    "szulido": fields.Date,
    "lakcim": fields.String,
    "admin": fields.Boolean,
    "szamlaszamok": fields.List(fields.Nested(szamla_model))
})

ugyfel_post_model = api.model("UgyfelLetrehozasa", {
    "nev": fields.String,
    "tel": fields.String,
    "email": fields.String,
    "szulido": fields.Date,
    "lakcim": fields.String,
    "admin": fields.Boolean,
    "jelszo": fields.String
})

ugyfel_put_model = api.model("UgyfelModositasa", {
    "nev": fields.String,
    "tel": fields.String,
    "email": fields.String,
    "szulido": fields.Date,
    "lakcim": fields.String,
    "admin": fields.Boolean
})

ugyfel_login_output_model = api.model("LoginOutput", {
    "Kulcs": fields.String,
    "nev": fields.String
})

ugyfel_login_model = api.model("Login",{
    "email": fields.String,
    "jelszo": fields.String
})

# Utalas_model
utalas_model = api.model("Utalas", {
    "id": fields.Integer,
    "osszeg": fields.Integer,
    "fogado_szamla": fields.Integer,
    "utalo_szamla": fields.Integer,
    "ido": fields.DateTime
})

utalas_post_model = api.model("UtalasLetrehozasa", {
    "osszeg": fields.Integer,
    "fogado_szamla": fields.Integer,
    "utalo_szamla": fields.Integer,
})

utalas_put_model = api.model("UtalasModositasa", {
    "osszeg": fields.Integer
})

# befizetes_model
befizetes_model = api.model("Befizetes", {
    "id": fields.Integer,
    "osszeg": fields.Integer,
    "szamla": fields.Integer,
    "ido": fields.DateTime
})

befizetes_post_model = api.model("BefizetesLetrehozasa", {
    "osszeg": fields.Integer,
    "szamla": fields.Integer,
})

befizetes_put_model = api.model("BefizetesModositasa", {
    "osszeg": fields.Integer
})

# Penzfelvetel model
penzfelvetel_model = api.model("Penzfelvetel", {
    "id": fields.Integer,
    "osszeg": fields.Integer,
    "szamla": fields.Integer,
    "ido": fields.DateTime
})

penzfelvetel_post_model = api.model("PenzfelvetelLetrehozasa", {
    "osszeg": fields.Integer,
    "szamla": fields.Integer
})

penzfelvetel_put_model = api.model("PenzfelvetelModositasa", {
    "osszeg": fields.Integer
})