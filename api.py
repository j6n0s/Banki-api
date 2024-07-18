from flask_restx import Resource, Namespace, abort
from flask_jwt_extended import jwt_required,  create_access_token, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from extensions import db
from db_models import Ugyfel, Szamla, Utalas, Befizetes, Penzfelvetel
from api_models import (ugyfel_model,
                        ugyfel_post_model,
                        ugyfel_put_model,
                        ugyfel_login_model,
                        ugyfel_login_output_model,
                        szamla_model,
                        szamla_post_model,
                        szamla_put_model,
                        utalas_model,
                        utalas_post_model,
                        utalas_put_model,
                        befizetes_model,
                        befizetes_post_model,
                        befizetes_put_model,
                        penzfelvetel_model,
                        penzfelvetel_post_model,
                        penzfelvetel_put_model)

autorizaciok = {
    "webKey": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

ns1 = Namespace("ugyfelek", authorizations=autorizaciok, description="Ugyfelek kezelese")
ns2 = Namespace("szamlak", authorizations=autorizaciok, description="Szamlak kezelese")
ns3 = Namespace("utalasok", authorizations=autorizaciok, description="Utalasok kezelese")
ns4 = Namespace("befizetesek", authorizations=autorizaciok, description="Befizetesek kezelese")
ns5 = Namespace("penzfelvetel", authorizations=autorizaciok, description="Penzfelvetele kezelese")
aut = Namespace("autentikacio", description="Autentikacio kezelese")


@aut.route("/regisztracio")
class Register(Resource):
    @aut.doc(security="webKey", description="Ugyfel regisztralasa")
    @aut.doc(responses={201: "Siker!", 409: "Ismetlodo email", 400: "Hibas formatum!"})
    @aut.expect(ugyfel_post_model)
    @aut.marshal_with(ugyfel_model)
    def post(self):
        if ("nev" in aut.payload and "tel" in aut.payload and
                "email" in aut.payload and "szulido" in aut.payload and
                "lakcim" in aut.payload and "admin" in aut.payload and
                "jelszo" in aut.payload):
            szulido_str = aut.payload["szulido"]
            if not Ugyfel.query.filter_by(email=aut.payload["email"]).first():
                try:
                    szulido_date = datetime.strptime(szulido_str, '%Y-%m-%d').date()
                    ugyfel = Ugyfel(nev=aut.payload["nev"], tel=aut.payload["tel"],
                                    email=aut.payload["email"], szulido=szulido_date,
                                    lakcim=aut.payload["lakcim"], admin=aut.payload["admin"],
                                    jelszo_hash=generate_password_hash(aut.payload["jelszo"]))
                    db.session.add(ugyfel)
                    db.session.commit()
                    return ugyfel, 201
                except:
                    abort(400, message="Hibas formatum")
            else:
                abort(409, message="Ismetlodo email")
        else:
            abort(400, message="Hibas formatum!")


@aut.route("/bejelentkezes")
class Login(Resource):
    @aut.doc(security="webKey", description="Bejelentkezes")
    @aut.doc(responses={200: "Siker!", 401: "Helytelen email vagy jelszo....", 400: "Hibas formatum!"})
    @aut.expect(ugyfel_login_model)
    @aut.marshal_with(ugyfel_login_output_model)
    def post(self):
        if "email" in aut.payload and "jelszo" in aut.payload:
            ugyfel = Ugyfel.query.filter_by(email=aut.payload["email"]).first()
            if ugyfel and check_password_hash(ugyfel.jelszo_hash, aut.payload["jelszo"]):
                return {"Kulcs": create_access_token(ugyfel), "nev": Ugyfel.query.filter_by(email=aut.payload["email"]).first().nev}, 200
            else:
                abort(401, message="Helytelen email vagy jelszo....")
        else:
            abort(400, message="Hibas formatum!")


@ns1.route("/")
class UgyfelekListApi(Resource):
    method_decorators = [jwt_required()]

    @ns1.doc(security="webKey")
    @ns1.doc(responses={200: "Siker!", 404: "Nem talalhato ugyfel"})
    @ns1.marshal_list_with(ugyfel_model)
    def get(self):
        #print(current_user.admin)
        #print(get_jwt_identity())
        if current_user.admin == True:
            ugyfel = Ugyfel.query.all()
        else:
            ugyfel = Ugyfel.query.get(current_user.id)
        if ugyfel:
            return ugyfel, 200
        else:
            abort(404, message="Nem talalhato ugyfel")


@ns1.route("/<int:id>")
class UgyfelekApi(Resource):
    method_decorators = [jwt_required()]

    @ns1.doc(security="webKey")
    @ns1.doc(responses={200: "Siker!", 404: "Nem talalhato ugyfel"})
    @ns1.marshal_with(ugyfel_model)
    def get(self, id):
        if current_user.admin == True:
            ugyfel = Ugyfel.query.get(id)
        else:
            ugyfel = Ugyfel.query.get(current_user.id)
        if ugyfel:
            return ugyfel, 200
        else:
            abort(404, message="Nem talahato ugyfel")

    @ns1.doc(security="webKey")
    @ns1.doc(responses={200: "Siker!", 400: "Hibas datum formatum! (%Y-%m-%d)",
                        404: "Nem talalhato ilyen ugyfel..."})
    @ns1.expect(ugyfel_put_model)
    @ns1.marshal_with(ugyfel_model)
    def put(self, id):
        if current_user.admin == True:
            ugyfel = Ugyfel.query.get(id)
        else:
            ugyfel = Ugyfel.query.get(current_user.id)
        if ugyfel:
            if "nev" in ns1.payload:
                ugyfel.nev = ns1.payload["nev"]
            if "tel" in ns1.payload:
                ugyfel.tel = ns1.payload["tel"]
            if "email" in ns1.payload:
                ugyfel.email = ns1.payload["email"]
            if "szulido" in ns1.payload:
                try:
                    szulido_str = ns1.payload["szulido"]
                    szulido_date = datetime.strptime(szulido_str, '%Y-%m-%d').date()
                    ugyfel.szulido = szulido_date
                except:
                    abort(400, message="Hibsa datum formatum! (%Y-%m-%d)")
            if "lakcim" in ns1.payload:
                ugyfel.lakcim = ns1.payload["lakcim"]
            db.session.commit()
            return ugyfel, 200
        else:
            abort(404, message="Nem talalhato ilyen ugyfel...")

    @ns1.doc(security="webKey")
    @ns1.doc(responses={204: "Sikeres torles!", 404: "Nem talalhato ilyen ugyfel..."})
    def delete(self, id):
        if current_user.admin == True:
            ugyfel = Ugyfel.query.get(id)
        else:
            ugyfel = Ugyfel.query.get(current_user.id)
        if ugyfel:
            szamlak_obj = Szamla.query.filter_by(ugyfel_id=ugyfel.id).all()
            if szamlak_obj is not []:
                for szamla in szamlak_obj:
                    db.session.delete(szamla)

            db.session.delete(ugyfel)
            db.session.commit()
            return 204
        else:
            abort(404, message="Nem talalhato ilyen ugyfel...")


@ns2.route("/")
class SzamlakListApi(Resource):
    method_decorators = [jwt_required()]

    @ns2.doc(security="webKey")
    @ns2.doc(responses={204: "Sikeres!", 404: "Nem talalhato szamla..."})
    @ns2.marshal_list_with(szamla_model)
    def get(self):
        if current_user.admin == True:
            szamla = Szamla.query.all()
        else:
            szamla = Szamla.query.filter_by(ugyfel_id=current_user.id).all()
        if szamla:
            return szamla
        else:
            abort(404, message="Nem talalhato szamla...")

    @ns2.doc(security="webKey")
    @ns2.doc(responses={201: "Sikeres!", 404: "Nem talalhato szamla...", 400: "Hibas formatum"})
    @ns2.expect(szamla_post_model)
    @ns2.marshal_with(szamla_model)
    def post(self):
        if (("ugyfel_id" in ns2.payload and "egyenleg" in ns2.payload)
                and (isinstance(ns2.payload["ugyfel_id"], int)
                     and isinstance(ns2.payload["egyenleg"], int))):
            ugyfel_id = ns2.payload["ugyfel_id"]
            egyenleg = ns2.payload["egyenleg"]
            if Ugyfel.query.get(ugyfel_id) is not None:
                if not Szamla.query.all():
                    id = 1000000000000000
                else:
                    szamlak_obj = Szamla.query.all()
                    szamlak_list = []
                    for szamla in szamlak_obj:
                        szamlak_list.append(szamla.id)
                    id = max(szamlak_list) + 1
                if current_user.admin == False:
                    ugyfel_id = current_user.id
                    egyenleg = 0
                szamla = Szamla(id=id, ugyfel_id=ugyfel_id,
                                egyenleg=abs(egyenleg))
                db.session.add(szamla)
                db.session.commit()
                return szamla, 201
            else:
                abort(404, message="Nem talalhato ilyen ugyfel")
        else:
            abort(400, message="Hibas formatum!")


@ns2.route("/<int:id>")
class SzamlakApi(Resource):
    method_decorators = [jwt_required()]

    @ns2.doc(security="webKey")
    @ns2.doc(responses={200: "Sikeres!", 404: "Nem talalhato szamla..."})
    @ns2.marshal_with(szamla_model)
    def get(self, id):
        szamla = Szamla.query.get(id)
        if szamla:
            if current_user.admin == False:
                szamlak = []
                szamlak_obj = Szamla.query.filter_by(ugyfel_id=current_user.id).all()

                for szamla in szamlak_obj:
                    szamlak.append(szamla.id)

                if id in szamlak:
                    return Szamla.query.get(id)
                else:
                    abort(404, message="Eleres megtagadva....")
            else:
                return szamla, 200
        else:
            abort(404, message="Nem talalhato ilyen szamla")

    @ns2.doc(security="webKey")
    @ns2.doc(responses={200: "Sikeres!", 404: "Nem talalhato ilyen szamla...", 400: "Hibas formatum!"})
    @ns2.expect(szamla_put_model)
    @ns2.marshal_with(szamla_model)
    def put(self, id):
        if ((("egyenleg" in ns2.payload and isinstance(ns2.payload["egyenleg"], int))
             or ("ugyfel_id" in ns2.payload) and isinstance(ns2.payload["ugyfel_id"], int))):
            if current_user.admin == True:
                szamla = Szamla.query.get(id)
                if szamla:
                    osszeg = abs(ns2.payload["egyenleg"])

                    if "egyenleg" in ns2.payload:
                        szamla.egyenleg = osszeg
                    if ("ugyfel_id" in ns2.payload and
                            Szamla.query.get(ns2.payload["ugyfel_id"] is not None)):
                        szamla.ugyfel_id = ns2.payload["uygfel_id"]

                        db.session.commit()
                        return szamla, 200
                else:
                    abort(404, message="Nem talalhato ilyen szamla...")
            else:
                abort(423, message="Jogosultsag megtagadva")
        else:
            abort(400, message="Hibas formatum!")

    @ns2.doc(security="webKey")
    @ns2.doc(responses={204: "Sikeres!", 404: "Nem talalhato ilyen szamla..."})
    def delete(self, id):
        if current_user.admin == True:
            szamla = Szamla.query.get(id)
        else:
            szamla = Szamla.query.get(current_user.id)
        if szamla:
            db.session.delete(szamla)
            db.session.commit()
            return {"Uzenet": "Sikeresen torolve!"}, 204
        else:
            abort(404, message="Nem talalhato ilyen szamla...")


@ns3.route("/")
class UtalasokListApi(Resource):
    method_decorators = [jwt_required()]

    @ns3.doc(security="webKey")
    @ns3.doc(responses={200: "Sikeres!", 404: "Nem talalhato utalas..."})
    @ns3.marshal_list_with(utalas_model)
    def get(self):
        if current_user.admin == True:
            utalas = Utalas.query.all()
        else:
            utalas = []
            szamlak = []
            szamlak_obj = Szamla.query.filter_by(ugyfel_id=current_user.id).all()

            for szamla in szamlak_obj:
                szamlak.append(szamla.id)

            for ut in szamlak:
                vizsg = Utalas.query.filter_by(utalo_szamla=ut).all()
                if vizsg:
                    for vg in vizsg:
                        utalas.append(vg)
        if utalas:
            return utalas, 200
        else:
            abort(404, message="Nem talalhato utalas...")

    @ns3.doc(security="webKey")
    @ns3.doc(responses={201: "Sikeres!", 404: "Nincs ilyen szamla", 400: "Hibas formatum!",
                        405: "Nincs eleg penz a szamlan", 423: "Eleres megtagadva"})
    @ns3.expect(utalas_post_model)
    @ns3.marshal_with(utalas_model)
    def post(self):
        if Szamla.query.get(ns3.payload["utalo_szamla"]) is None:
            abort(404, message="Utalo szamla nem talahato")
        if Szamla.query.get(ns3.payload["fogado_szamla"]) is None:
            abort(404, message="Fogado szamla nem talalhato")
        if not "osszeg" in ns3.payload and not isinstance(ns3.payload["osszeg"], int):
            abort(400, message="Hibas Formatum")

        utalo_szamla = ns3.payload["utalo_szamla"]

        if current_user.admin == False:
            szamlak = []
            szamlak_obj = Szamla.query.filter_by(ugyfel_id=current_user.id).all()

            for szamla in szamlak_obj:
                szamlak.append(szamla.id)

            if utalo_szamla not in szamlak:
                abort(423, message="Eleres megtagadva....")
        else:
            szamlak = []
            szamlak_obj = Szamla.query.all()

            for szamla in szamlak_obj:
                szamlak.append(szamla.id)

            if utalo_szamla not in szamlak:
                abort(404, message="Nincs ilyen szamla")

        osszeg = abs(ns3.payload["osszeg"])
        fogado_szamla = ns3.payload["fogado_szamla"]
        print(Szamla.query.get(ns3.payload["utalo_szamla"]).egyenleg - osszeg >= 0)
        if Szamla.query.get(ns3.payload["utalo_szamla"]).egyenleg - osszeg >= 0:

            utalas = Utalas(osszeg=osszeg,
                            fogado_szamla=fogado_szamla,
                            utalo_szamla=utalo_szamla,
                            ido=datetime.now())

            fogado_szamla = Szamla.query.get(ns3.payload["fogado_szamla"])
            fogado_szamla.egyenleg += osszeg

            utalo_szamla = Szamla.query.get(ns3.payload["utalo_szamla"])
            utalo_szamla.egyenleg -= osszeg

            db.session.add(utalas)
            db.session.commit()
            return utalas, 201
        else:
            print("alma")
            abort(405, message="Nincs eleg penz a szamlan")


@ns3.route("/<int:id>")
class UtalasokApi(Resource):
    method_decorators = [jwt_required()]

    @ns3.doc(security="webKey")
    @ns3.doc(responses={200: "Sikeres!", 404: "Utalas nem talalhato!",
                        423: "Elerese megtagadva"})
    @ns3.marshal_with(utalas_model)
    def get(self, id):
        if current_user.admin == True:
            utalas = Utalas.query.get(id)
        else:
            utalas = Utalas.query.get(id)
            szamlak = []
            szamlak_obj = Szamla.query.filter_by(ugyfel_id=current_user.id).all()

            for szamla in szamlak_obj:
                szamlak.append(szamla.id)

            if utalas.utalo_szamla not in szamlak:
                abort(423,message="Eleres megtagadva")
        if utalas:
            return utalas, 200
        else:
            abort(404, message="Utalas nem talalhato!")

    @ns3.doc(security="webKey")
    @ns3.doc(responses={200: "Sikeres!", 404: "Utalas nem talalhato!", 400: "Hibas formatum",
                        405: "Nincs eleg penz a szamlan"})
    @ns3.expect(utalas_put_model)
    @ns3.marshal_with(utalas_model)
    def put(self, id):
        if "osszeg" in ns3.payload:
            if current_user.admin == False:
                abort(423, message="Jogosultsag megtagadva!")
            utalas = Utalas.query.get(id)
            if utalas:
                jelenlegi_osszeg = ns3.payload["osszeg"]
                elozo_osszeg = utalas.osszeg

                if (elozo_osszeg > jelenlegi_osszeg and
                        Szamla.query.get(utalas.fogado_szamla).egyenleg -
                        (elozo_osszeg - jelenlegi_osszeg) >= 0):
                    osszeg = elozo_osszeg - jelenlegi_osszeg
                    utalas.osszeg = jelenlegi_osszeg

                    fogado_szamla = Szamla.query.get(utalas.fogado_szamla)
                    fogado_szamla.egyenleg -= osszeg

                    utalo_szamla = Szamla.query.get(utalas.utalo_szamla)
                    utalo_szamla.egyenleg += osszeg
                elif (elozo_osszeg < jelenlegi_osszeg and
                      Szamla.query.get(utalas.utalo_szamla).egyenleg -
                      (jelenlegi_osszeg - elozo_osszeg) >= 0):
                    osszeg = jelenlegi_osszeg - elozo_osszeg
                    utalas.osszeg = jelenlegi_osszeg

                    fogado_szamla = Szamla.query.get(utalas.fogado_szamla)
                    fogado_szamla.egyenleg += osszeg

                    utalo_szamla = Szamla.query.get(utalas.utalo_szamla)
                    utalo_szamla.egyenleg -= osszeg

                else:
                    abort(405, message="Nincs eleg penz a szamlan")

                db.session.commit()
                return utalas, 200
            else:
                abort(404, message="Utalas nem talalhato")
        else:
            abort(400, message="Hibás formatum")

    @ns3.doc(security="webKey")
    @ns3.doc(responses={204: "Sikeres torles!", 404: "Utalas nem talalhato",
                        423: "Jogosultsag megtagadva"})
    def delete(self, id):
        if current_user.admin == False:
            abort(423, message="Jogosultsag megtagadva!")
        utalas = Utalas.query.get(id)
        if utalas:
            db.session.delete(utalas)
            db.session.commit()
            return {"Uzenet": "Sikeresen torolve!"}, 204
        else:
            abort(404, "Utalas nem talalhato")


@ns4.route("/")
class BefizetesekListApi(Resource):
    method_decorators = [jwt_required()]

    @ns4.doc(security="webKey")
    @ns4.doc(responces={200: "Siker", 404: "Nem talalhato befizetes"})
    @ns4.marshal_list_with(befizetes_model)
    def get(self):
        if current_user.admin == True:
            befizetes = Befizetes.query.all()
        else:
            befizetes = []
            szamlak = []
            szamlak_obj = Szamla.query.filter_by(ugyfel_id=current_user.id).all()

            for szamla in szamlak_obj:
                szamlak.append(szamla.id)

            for szm in szamlak:
                vizsg = Befizetes.query.filter_by(szamla=szm).all()
                if vizsg:
                    for vg in vizsg:
                        befizetes.append(vg)
        if befizetes:
            return befizetes, 200
        else:
            abort(404, message="Nem talalhato utalas...")



        if Befizetes.query.all():
            if current_user.admin == False:
                befizetesek_list = []
                befizetesek_id = []
                ugyfel_szamlak_list = Szamla.query.filter_by(ugyfel_id=current_user.id).all()
                output = []

                for szamla in ugyfel_szamlak_list:
                    befizetesek_list.append(Befizetes.query.filter_by(szamla=szamla.id).all())
                print(befizetesek_list)
                if befizetesek_list is not []:
                    for befizetes in befizetesek_list:
                        for bf in befizetes:
                            befizetesek_id.append(bf.id)
                else:
                    abort(404, message="Nem talalhato ilyen befizetes")
                for befizetes in befizetesek_id:
                    output.append(Befizetes.query.get(befizetes))
                return output, 200
            else:
                return Befizetes.query.all(), 200
        else:
            abort(404, message="Nem talalhato ilyen befizetes")

    @ns4.doc(security="webKey")
    @ns4.doc(responces={200: "Siker", 404: "Szamla nem talalhato", 400: "Hibas formatum",
                        423: "Jogosultsag megtagadva"})
    @ns4.expect(befizetes_post_model)
    @ns4.marshal_with(befizetes_model)
    def post(self):
        if (("osszeg" in ns4.payload and isinstance(ns4.payload["osszeg"], int))
                and ("szamla" in ns4.payload and isinstance(ns4.payload["szamla"], int))):
            if Szamla.query.get(ns4.payload["szamla"]) is not None:
                osszeg = abs(ns4.payload["osszeg"])
                szamla = ns4.payload["szamla"]

                if current_user.admin == False:
                    try:
                        ugyfel_szamlak_obj = Szamla.query.filter_by(ugyfel_id=current_user.id).all()
                        ugyfel_szamlak = []

                        for u_szamla in ugyfel_szamlak_obj:
                            ugyfel_szamlak.append(u_szamla.id)

                        if szamla not in ugyfel_szamlak:
                            abort(423, message="Jogosultsag megtagadva")
                    except:
                        abort(404, "Az ugyfelnek nincs szamlaja")

                befizetes = Befizetes(osszeg=osszeg,
                                      szamla=szamla,
                                      ido=datetime.now())

                transfer = Szamla.query.get(szamla)
                transfer.egyenleg += osszeg

                db.session.add(befizetes)
                db.session.commit()
                return befizetes, 201
            else:
                abort(404, message="A szamla nem talalhato")
        else:
            abort(400, message="Hibás formatum")


@ns4.route("/<int:id>")
class BefizetesApi(Resource):
    method_decorators = [jwt_required()]

    @ns4.doc(security="webKey")
    @ns4.doc(responces={200: "Siker", 404: "Nem talalhato ilyen befizetes",
                        423: "Jogosultsag megtagadva"})
    @ns4.marshal_with(befizetes_model)
    def get(self, id):
        if Befizetes.query.get(id):
            if current_user.admin == False:
                befizetesek_list = []
                befizetesek_id = []
                ugyfel_szamlak_list = Szamla.query.filter_by(ugyfel_id=current_user.id).all()

                for szamla in ugyfel_szamlak_list:
                    befizetesek_list.append(Befizetes.query.filter_by(szamla=szamla.id).all())
                if befizetesek_list is not []:
                    for befizetes in befizetesek_list:
                        for bf in befizetes:
                            befizetesek_id.append(bf.id)
                else:
                    abort(423, message="Jogosultsag megtagadva")
                if id in befizetesek_id:
                    return Befizetes.query.get(id), 200
                else:
                    abort(423, message="Jogosultsag megtagadva")
            else:
                return Befizetes.query.get(id), 200
        else:
            abort(404, message="Nem talalhato ilyen befizetes")

    @ns4.doc(security="webKey")
    @ns4.doc(responces={200: "Siker", 404: "Nem talalhato ilyen befizetes",
                        400: "Hibas formatum", 405: "Nincs eleg penz a szamlan",
                        423: "Jogosultsag megtagadva"})
    @ns4.expect(befizetes_put_model)
    @ns4.marshal_with(befizetes_model)
    def put(self, id):
        if "osszeg" in ns4.payload and isinstance(ns4.payload["osszeg"], int):
            if Befizetes.query.get(id):
                if current_user.admin == False:
                        abort(423, message="Jogosultsag megtagadva")
                else:
                    befizetes = Befizetes.query.get(id)
                    elozo_osszeg = befizetes.osszeg
                    jelenlegi_osszeg = abs(ns4.payload["osszeg"])
                    szamla = Szamla.query.get(befizetes.szamla)

                    if (elozo_osszeg > jelenlegi_osszeg and
                            szamla.egyenleg - elozo_osszeg - jelenlegi_osszeg >= 0):
                        osszeg = elozo_osszeg - jelenlegi_osszeg
                        befizetes.osszeg -= osszeg
                        szamla.egyenleg -= osszeg
                    elif elozo_osszeg < jelenlegi_osszeg:
                        osszeg = jelenlegi_osszeg - elozo_osszeg
                        befizetes.osszeg += osszeg
                        szamla.egyenleg += osszeg
                    else:
                        abort(405, message="Nincs eleg penz a szamlan")

                    db.session.commit()
                    return befizetes, 200
            else:
                abort(404, message="Nem talalhato ilyen befizetes")

    @ns4.doc(security="webKey")
    @ns4.doc(responces={204: "Sikeres torles!", 404: "Nem talalhato ilyen befizetes",
                        423: "Jogosultsag megtagadva"})
    def delete(self, id):
        befizetes = Befizetes.query.get(id)
        if current_user.admin == False:
            abort(423, message="Jogosultsag megtagadva")
        if befizetes:
            db.session.delete(befizetes)
            db.session.commit()
            return {"Uzenet": "Sikeresen torolve!"}, 204
        else:
            abort(404, message="Nem talalhato ilyen befizetes")


@ns5.route("/")
class PenzfelvetelListApi(Resource):
    method_decorators = [jwt_required()]

    @ns5.doc(security="webKey")
    @ns5.doc(responses={200: "Sikeres!", 404: "Nem talalhato penzfelvetel..."})
    @ns5.marshal_list_with(penzfelvetel_model)
    def get(self):
        if Penzfelvetel.query.all():
            if current_user.admin == False:
                ugyfel_szamlak_obj = Szamla.query.filter_by(ugyfel_id=current_user.id).all()
                penzfelvetel_obj = []
                penzfelvetel = []
                for szamla in ugyfel_szamlak_obj:
                    penzfelvetel_obj.append(Penzfelvetel.query.filter_by(szamla=szamla.id).all())
                #Dekorator
                for i in penzfelvetel_obj:
                    for j in i:
                        penzfelvetel.append(j)
                if penzfelvetel:
                    return penzfelvetel, 200
                else:
                    abort(404, message="Nem talalhato penzfelvetel...")
            else:
                return Penzfelvetel.query.all(), 200
        else:
            abort(404, message="Nem talalhato penzfelvetel")

    @ns5.doc(security="webKey")
    @ns5.doc(responses={201: "Sikeres!", 404: "A szamla nem talalhato...",
                        400: "Hibas formatum!", 405: "Nincs eleg penz a szamlan!",
                        423: "Eleres megtagadva"})
    @ns5.expect(penzfelvetel_post_model)
    @ns5.marshal_with(penzfelvetel_model)
    def post(self):
        if (("osszeg" in ns5.payload and isinstance(ns5.payload["osszeg"], int))
                and ("szamla" in ns5.payload and isinstance(ns5.payload["szamla"], int))):
            szamla = ns5.payload["szamla"]
            if Szamla.query.get(szamla) is not None:
                if current_user.admin == False:
                    szamlak_obj = Szamla.query.filter_by(ugyfel_id=current_user.id).all()
                    szamlak = []

                    for u_szamla in szamlak_obj:
                        szamlak.append(u_szamla.id)

                    if szamla not in szamlak:
                        abort(423, message="Eleres megtagadva")

                osszeg = abs(ns5.payload["osszeg"])
                if Szamla.query.get(ns5.payload["szamla"]).egyenleg-osszeg>=0:
                    penzfelvetel = Penzfelvetel(szamla=ns5.payload["szamla"],
                                                osszeg=osszeg,
                                                ido=datetime.now())

                    penzlevonas = Szamla.query.get(ns5.payload["szamla"])
                    penzlevonas.egyenleg -= osszeg

                    db.session.add(penzfelvetel)
                    db.session.commit()
                    return penzfelvetel, 201
                else:
                    abort(405, message="Nincs eleg penz a szamlan!")
            else:
                abort(404, message="A szamla nem talalhato...")
        else:
            abort(400, message="Hibas formatum!")


@ns5.route("/<int:id>")
class PenzfelvetelApi(Resource):
    method_decorators = [jwt_required()]

    @ns5.doc(security="webKey")
    @ns5.doc(responses={200: "Sikeres!", 404: "Nem talalhato ilyen penzfelvetel"})
    @ns5.marshal_with(penzfelvetel_model)
    def get(self, id):
        if Penzfelvetel.query.get(id):
            if current_user.admin == False:
                penzfelvetel_list = []
                penzfelvetel_id = []
                ugyfel_szamlak_list = Szamla.query.filter_by(ugyfel_id=current_user.id).all()

                for szamla in ugyfel_szamlak_list:
                    penzfelvetel_list.append(Penzfelvetel.query.filter_by(szamla=szamla.id).all())
                if penzfelvetel_list is not []:
                    for befizetes in penzfelvetel_list:
                        for bf in befizetes:
                            penzfelvetel_id.append(bf.id)
                else:
                    abort(423, message="Jogosultsag megtagadva")
                if id in penzfelvetel_id:
                    return Befizetes.query.get(id), 200
                else:
                    abort(423, message="Jogosultsag megtagadva")
            else:
                return Befizetes.query.get(id), 200
        else:
            abort(404, message="Nem talalhato ilyen befizetes")

    @ns5.doc(security="webKey")
    @ns5.doc(responses={200: "Sikeres!", 404: "Nem talalhato ilyen penzfelvetel",
                        400: "Hibas formatum!", 405: "Nincs eleg penz a szamlan",
                        423: "Jogosultsag megtagadva"})
    @ns5.expect(penzfelvetel_put_model)
    @ns5.marshal_with(penzfelvetel_model)
    def put(self, id):
        if "osszeg" in ns5.payload and isinstance(ns5.payload["osszeg"], int):
            if current_user.admin == False:
                abort(423, message="Jogosultsag megtagadva")
            jelenlegi_osszeg = abs(ns5.payload["osszeg"])
            penzfelvetel = Penzfelvetel.query.get(id)
            if penzfelvetel:
                if Szamla.query.get(penzfelvetel.szamla) - jelenlegi_osszeg >= 0:
                    elozo_osszeg = penzfelvetel.osszeg- jelenlegi_osszeg
                    transfer = Szamla.query.get(penzfelvetel.szamla)

                    if elozo_osszeg > jelenlegi_osszeg:
                        transfer.egyenleg += elozo_osszeg-jelenlegi_osszeg
                    else:
                        transfer.egyenleg -= jelenlegi_osszeg-elozo_osszeg

                    penzfelvetel.osszeg = jelenlegi_osszeg
                    db.session.commit()
                    return penzfelvetel, 200
                else:
                    abort(405, "Nincs eleg penz a szamlan")
            else:
                abort(404, message="Nem talalhato ilyen penzfelvetel")
        else:
            abort(400, message="Hibas formatum!")

    @ns5.doc(security="webKey")
    @ns5.doc(responces={204: "Sikeres torles!", 404: "Nem talalhato ilyen penzfelvetel"})
    def delete(self, id):
        if current_user.admin == False:
            abort(423, message="Jogosultsag megtagadva")
        penzfelvetel = Penzfelvetel.query.get(id)
        if penzfelvetel:
            db.session.delete(penzfelvetel)
            db.session.commit()
            return {"Uzenet": "Sikeresen torolve!"}, 204
        else:
            abort(404, message="Nem talalhato ilyen penzfelvetel")

