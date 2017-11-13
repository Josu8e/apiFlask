from flask import Flask, json, request, jsonify,url_for
import pyodbc

app = Flask(__name__)



server = '172.19.32.10'
database = 'ExplorandoMiPais'
username = 'infoTec'
password = '_1Nf0t3c'


#server = 'DESKTOP-DGU3E63'
#username = 'josue'
#password = '12345'


cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)



@app.route('/')
def index():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    return jsonify(output)

#---------------------------------------people

@app.route('/createPerson',methods=["POST"])
def craerPersona():
    try:
        dataDict = json.loads(data)
        nombre =dataDict["nombre"]
        correo = dataDict["correo"]
        contrasehna = dataDict["contrasehna"]
        cursor = cnxn.cursor()
        cursor.execute('insert into people(nombre,correo,contrasehna) values (?,?,?)',nombre,correo,contrasehna)
        cnxn.commit()
        return "succesfull"
    except pyodbc.Error as ex:
        return ex.args[1]

@app.route('/login/<correo>',methods = ["GET"])
def login(correo):
    try:
        cursor = cnxn.cursor();
        cursor.execute('select correo from people')
        rows = cursor.fetchall()
        for row in rows:
            if row.correo == correo:
                return 'True'
        return 'False'
    except pyodbc.Error as ex:
        return ex.args[1]


@app.route('/deletePerson/<correo>',methods = ["POST","GET"])
def deletePersona(correo):
    try:
        cursor = cnxn.cursor();
        cursor.execute("delete from people where correo = ?", correo)
        cnxn.commit();
        return 'succesfull'
    except pyodbc.Error as ex:
        return ex.args[1]


@app.route('/showPerson/<correo>',methods = ["GET"])
def showPerson(correo):


    try:
        cursor = cnxn.cursor();
        cursor.execute('select * from people where correo = ?',correo)
        row = cursor.fetchone()
        lista = []
        lista.append({"id":row[0],'correo':row[1],'nombre':row[2],'contrasehna':row[4]})
        return jsonify (lista)
    except pyodbc.Error as ex:
        return ex.args[0]


@app.route('/createExcursion',methods = ["POST"])
def crateExcursion():
    try:
        dataDict = json.loads(data)
        video = dataDict["video"]
        foto = dataDict["foto"]
        cupoMax = dataDict["cupoMax"]
        descripcion = dataDict["descripcion"]
        id_encargado = dataDict["idEncargado"]
        rangoCancelacion = dataDict["rangoCancelacion"]
        precio = dataDict["precio"]
        cursor = cnxn.cursor()
        cursor.execute('insert into excursions(video,foto,cupoMax,descripcion,encargado,rangoCancelacion,precio) values (?,?,?,?,?,?,?)',video,foto,cupoMax,descripcion,id_encargado,rangoCancelacion,precio)
        cnxn.commit()
        return 'succesfull'
    except pyodbc.Error as ex:
        return ex.args[0]


@app.route('/deleteExcursion/<id_excursion>',methods = ["POST","GET"])
def deleteExcursion(id_excursion):
    try:
        cursor = cnxn.cursor();
        cursor.execute("delete from excursions where id = ?", id_excursion)
        cnxn.commit();
        return 'succesfull'
    except pyodbc.Error as ex:
        return ex.args[1]


#---------------------------excursions
@app.route('/updateExcursion',methods = ["POST"])
def updateExcursions():
    try:
        dataDict = json.loads(data)
        video=dataDict["video"]
        foto=dataDict["foto"]
        cupoMax=dataDict["cupoMax"]
        descripcion=dataDict["descripcion"]
        id_encargado=dataDict["id_encargado"]
        rangoCancelacion=dataDict["rangoCancelacion"]
        id_excursion=dataDict["id_excursion"]
        cursor = cnxn.cursor()
        cursor.execute('update excursions set video = ?, foto = ?, cupoMax = ?, descripcion = ?, encargado = ?, rangoCancelacion =? where id = ?',video,foto,cupoMax,descripcion,id_encargado,rangoCancelacion,id_excursion)
        cnxn.commit();
        return 'succesfull'
    except pyodbc.Error as ex:
        return ex.args[1]



@app.route('/getAllExcursions',methods = ["POST","GET"])
def getAllExcursions():
    try:
        cursor = cnxn.cursor()
        cursor.execute('select * from excursions')
        rows = cursor.fetchall()
        lista = []
        for row in rows:
            lista.append({'id':row.id, 'video':row.video,'foto':row.foto,'cupoMax':row.cupoMax, 'descripcion':row.descripcion,'rangoCancelacion':row.rangoCancelacion})
        return jsonify(lista)
    except pyodbc.Error as ex:
        return ex.args[1]


@app.route('/getEncargadoExcursion/<idExcursion>',methods = ["GET"])
def getEncargadoExcursion(idExcursion):
    try:
        cursor = cnxn.cursor()
        cursor.execute('select p.correo,p.id,p.nombre from excursions as e inner join people as p on p.id = e.encargado where e.id = ?',idExcursion)
        row = cursor.fetchone()
        lista=[]
        lista.append({'correo': row[0],'id':row[1],'nombre':row[2]})
        return jsonify(lista)
    except pyodbc.Error as ex:
        return ex.args[1]


@app.route('/reservar/<idExcursion>/<idPer>',methods = ["POST","GET"])
def reservar(idExcursion,idPer):
    try:
        cursor = cnxn.cursor()
        cursor.execute('insert into excursions_people(excursions_id,people_id) values (?,?)',idExcursion,idPer)
        cnxn.commit();
        return "succesfull"
    except pyodbc.Error as ex:
        return ex.args[1]


@app.route('/misReservas/<idPer>',methods = ["POST","GET"])
def misReservas(idPer):
    try:
        cursor = cnxn.cursor();
        cursor.execute('select e.video,e.foto,e.descripcion,encargado from excursions as e inner join excursions_people as ep on e.id = ep.excursions_id inner join people as p on ep.people_id = p.id where p.id = ?',idPer)
        rows = cursor.fetchall()
        lista = []
        for row in rows:
            lista.append({'video': row.video, 'foto': row.foto, 'descripcion': row.descripcion, 'encargado': row.encargado})
        return jsonify(lista)
    except pyodbc.Error as ex:
        return ex.args[1]



@app.route('/cancelarReserva/<idExcursion>/<idPer>',methods = ["POST","GET"])
def cancelarReserva(idExcursion,idPer):
    try:
        cursor = cnxn.cursor()
        cursor.execute('delete excursions_people where excursions_id = ? and people_id = ?', idExcursion, idPer)
        cnxn.commit()
        return "succesfull"
    except pyodbc.Error as ex:
        return ex.args[1]


@app.route('/createActivity/<fechaInicio>/<fechaFinal>/<horaLlegada>/<horaSalida>',methods = ["POST","GET"])
def createActivity(fechaInicio,fechaFinal,horaLlegada,horaSalida):
    try:
        cursor = cnxn.cursor()
        cursor.execute('insert into activities (fechaInicio,fechafinal,horaLlegada,horaSalida) values (?,?,?,?)',fechaInicio,fechaFinal,horaLlegada,horaSalida)
        cnxn.commit()
        return "succesfull"
    except pyodbc.Error as ex:
        return ex.args[1]

@app.route('/unirActividadAExcursion/<id_excursion>/<id_activity>',methods = ["POST","GET"])
def unirActividadAExcursion(id_excursion,id_activity):
    try:
        cursor = cnxn.cursor()
        cursor.execute('insert into activities_excursions (excursions_id,activities_id) values (?,?)',id_excursion,id_activity)
        cnxn.commit()
        return "succesfull"
    except pyodbc.Error as ex:
        return ex.args[1]


@app.route('/activitiesByExcursions/<idExcursion>')
def activitiesByExcursions(idExcursion):
    try:
        cursor = cnxn.cursor()
        cursor.execute('select a.id,a.fechafinal,a.fechaInicio,a.horaLlegada,a.horaSalida from excursions as e inner join activities_excursions as ae on e.id = ae.excursions_id inner join activities as a on a.id = ae.activities_id where e.id = ?',idExcursion)
        rows = cursor.fetchall()
        lista = []
        for row in rows:
            lista.append({'id':row.id,'fechaInicio':row.fechaInicio,'fechafinal':row.fechafinal,'horaLlegada':row.horaLlegada,'horaSalida':row.horaSalida})
        return jsonify (lista)
    except pyodbc.Error as ex:
        return ex.args[1]

@app.route('/createPlace/<latitud>/<longitud>/<nombre>/<descripcion>/<services>', methods=["POST", "GET"])
def createPlace(latitud,longitud, nombre, descripcion, services):
    try:
        cursor = cnxn.cursor()
        cursor.execute('insert into places (latitud,longitud, nombre, descripcion, services) values (?,?,?,?,?)',latitud,longitud, nombre, descripcion, services)
        cnxn.commit()
        return "succesfull"
    except pyodbc.Error as ex:
        return ex.args[0]

@app.route('/unirLugar_a_Actividad/<id_lugar>/<id_activity>', methods=["POST", "GET"])
def unirLugar_a_Actividad(id_lugar, id_activity):
    try:
        cursor = cnxn.cursor()
        cursor.execute('insert into activities_places (activities_id,places_id) values (?,?)',id_activity,id_lugar)
        cnxn.commit()
        return "succesfull"
    except pyodbc.Error as ex:
        return ex.args[1]

@app.route('/placesByActivities/<idActivity>', methods=["POST", "GET"])
def placesByActivities(idActivity):
    try:
        cursor = cnxn.cursor()
        cursor.execute('select p.id,p.nombre,p.descripcion,p.services,p.latitud,p.longitud from activities as e inner join activities_places as ap on e.id = ap.activities_id inner join places as p on p.id = ap.places_id where e.id = ?',idActivity)
        rows = cursor.fetchall()
        lista = []
        for row in rows:
            lista.append({'id': row.id, 'nombre': row.nombre, 'descripcion': row.descripcion,'services': row.services, 'latitud': row.latitud,'longitud': row.latitud})
        return jsonify(lista)
    except pyodbc.Error as ex:
        return ex.args[1]

@app.route('/crearFoto', methods=["POST"])
def crearFoto():
    try:
        dataDict = json.loads(data)
        photo= dataDict["photo"]
        idLugar= dataDict["idLugar"]
        cursor = cnxn.cursor()
        cursor.execute('insert into photos (photo,place_id) values (?,?)',photo,idLugar)
        cnxn.commit()
        return "succesfull"
    except pyodbc.Error as ex:
        return ex.args[1]


@app.route('/createTheme', methods=["POST"])
def createTheme():
    try:
        data = request.data
        dataDict = json.loads(data)
        nombre = dataDict["nombre"]
        descripcion = dataDict["descripcion"]
        foto = dataDict["photo"]
        cursor = cnxn.cursor()
        cursor.execute('insert into themes (nombre,descripcion,foto) values (?,?,?)',nombre,descripcion,foto)
        cnxn.commit()
        return jsonify({"succesfull":True})
    except pyodbc.Error as ex:
        return ex.args[1]


@app.route('/getThemes/<idPersons>', methods=["GET"])
def getThemes(idPersons):
    try:
        cursor =  cnxn.cursor()
        cursor.execute('select * from themes as t left join theme_people as tp on t.id = tp.theme_id')
        lista = []
        rows = cursor.fetchall()
        for row in rows:
            idPersons = int (idPersons)
            if (idPersons == row.people_id):
                favorito = True
            else:
                favorito = False
            lista.append({"id": row.id, "nombre": row.nombre, "descripcion": row.descripcion, "foto": row.foto,"favorito": favorito})
        return jsonify(lista)
    except pyodbc.Error as ex:
        return ex.args[1]

@app.route('/setThemesPeople', methods=["POST"])
def setThemesPeople():
    try:
        data = request.data
        dataDict = json.loads(data)
        themeid = dataDict["theme_id"]
        peopleid = dataDict["people_id"]
        cursor = cnxn.cursor()
        cursor.execute('insert into theme_people(theme_id,people_id) values (?,?)', themeid,peopleid)
        cnxn.commit
        return jsonify({"succesful": True})
    except pyodbc.Error as ex:
        return ex.args[1]


@app.route('/getPlaces/<idPerson>')
def getPlaces(idPerson):
    try:
        cursor = cnxn.cursor()
        cursor.execute('select * from places as p left join people_places as pp on p.id = pp.place_id')
        lista = []
        rows = cursor.fetchall()
        for row in rows:
            idPerson = int(idPerson)
            favorito = False
            if (idPerson == row.people_id):
                favorito = True
            else:
                favorito = False
            a = place(row.id, row.latitud, row.longitud, row.nombre, row.descripcion, row.services, favorito)
            cursor2 = cnxn.cursor()
            cursor2.execute('select * from places as p inner join photos as ph on ph.place_id = p.id where place_id = ?', row.id)
            filas = cursor2.fetchall()
            photos = []
            for fila in filas:
                photos.append(fila.foto)
            a.add_photos(photos)
            lista.append({"id":a.id,"latitud":a.latitud,"longitud":a.longitud,"nombre":a.nombre,"descripcion":a.descripcion,"services":a.services,"favorito":a.favorito,"fotos":a.photos})
        return jsonify(lista)
    except pyodbc.Error as ex:
        return ex.args[1]


class place:
    def __init__(self,id,latitud,longitud,nombre,descripcion,services,favorito):
        self.id = id
        self.latitud = latitud
        self.longitud = longitud
        self.nombre = nombre
        self.descripcion = descripcion
        self.services = services
        self.photos = []
        self.favorito = favorito
    def add_photos(self,photos):
        self.photos = photos


#tiene que ir al final
if __name__  == '__main__':
    app.run(debug=True)
