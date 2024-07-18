# Szamla model
szamla_post_model_params = {
    "ugyfel_id": "ugyfel megadasa",
    "egyenleg": {
        "description": "start egyenleg megadasa",
        "type": "integer"
    }
}

szamla_put_model_params = {
    "ugyfel_id": "ugyfel megadasa",
    "egyenleg": {
        "description": "start egyenleg megadasa",
        "type": "integer"
    }
}

# Ugyfel model
ugyfel_post_model_params = {
    "nev": "nev megadasa",
    "tel": "relefonszam megadasa",
    "email": "email megadasa",
    "szulido": {
        "description": "szuletesi ido megadasa",
        "type": "date"
    },
    "lakcim": "laskcim megadasa",
    "admin": {
        "description": "rendszergazda (True / False)",
        "type": "bool"
    },
    "jelszo": "jelszo megadasa"
}

ugyfel_put_model_params = {
    "nev": "nev megadasa",
    "tel": "relefonszam megadasa",
    "email": "email megadasa",
    "szulido": {
        "description": "szuletesi ido megadasa",
        "type": "date"
    },
    "lakcim": "laskcim megadasa"
}

ugyfel_login_model_params = {
    "email": "email megadasa",
    "jelszo": "jelszo megadasa"
}

# Utalas_model
utalas_post_model_params = {
    "osszeg": {
        "description": "osszeg megadasa",
        "type": "integer"
    },
    "fogado_szamla": {
        "description": "fogado szamla megadasa",
        "type": "integer"
    },
    "utalo_szamla": {
        "description": "utalo szamla megadasa",
        "type": "integer"
    }
}

utalas_put_model_params = {
    "osszeg": {
        "description": "osszeg megadasa",
        "type": "integer"
    }
}

# befizetes_model
befizetes_post_model_params = {
    "osszeg": {
        "description": "osszeg megadasa",
        "type": "integer"
    },
    "szamla": {
        "description": "szamla megadasa",
        "type": "integer"
    },
}

befizetes_put_model_params = {
    "osszeg": {
        "description": "osszeg megadasa",
        "type": "integer"
    }
}

# Penzfelvetel model
penzfelvetel_post_model_params = {
    "osszeg": {
        "description": "osszeg megadasa",
        "type": "integer"
    },
    "szamla": {
        "description": "szamla megadasa",
        "type": "integer"
    }
}

penzfelvetel_put_model_params = {
    "osszeg": {
        "description": "osszeg megadasa",
        "type": "integer"
    }
}