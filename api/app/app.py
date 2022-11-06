############################################### API ################################################# 
##-------------------------------------------------------------------------------------------------## 
##-------------------------------------------------------------------------------------------------## 
##--------------------------------------------- By ------------------------------------------------## 
##------------------------------------- Salvador Mellado ------------------------------------------## 
##-------------------------------------------------------------------------------------------------## 
##-------------------------------------------------------------------------------------------------## 
############################################### API ################################################# 

#TODO: Hacer uso de las consultas multitablas
#TODO: Hacer Pruebas unitarias
#TODO: Optimizar codigo
#TODO: Refactorizar codigo
#TODO: Proteger Rutas
#TODO: Crear login para proteger documentación
#TODO: Mejorar documentación


# Micro Framework Flask
from flask import Flask
from flask import render_template
from flask import jsonify
# from flask import request
from flask_cors import CORS, cross_origin



# Extensión para la base de datos
from flask_mysqldb import MySQL
from sqlite3 import DatabaseError



# Extensión para las variable de entorno
from decouple import config



# Modelos
from models.sensores import Dispositivo, Medicion_dht, Medicion_nova, Medicion_uv



import secrets



# Aplicación
app = Flask(__name__) 
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


#configuraciones
app.secret_key = secrets.token_hex() 

app.config['CORS_HEADERS'] = 'Content-Type'

app.config["ENV"] = config("FLASK_ENTORNO")
app.config["DEBUG"] = config("FLASK_DEBUG")

app.config["MYSQL_HOST"] = config("MYSQL_HOST")
app.config["MYSQL_USER"] = config("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = config("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = config("MYSQL_DB_NAME")
app.config["MYSQL_PORT"] = int(config("MYSQL_PORT")) 



# Instancias u Objetos
mysql = MySQL(app)

    

# Lista de titulos para los templates
lista_titulos = ["Inicio", "Login", "Documentación"] 
# Diccionario con las rutas de la api
diccionario_de_rutas = {
    "inicio": "/",
    # "login": "/iniciar_sesion",
    "sobre nosotros": "/sobre-nosotros",
    # "datos sensores": "/listar_datos_sensores"
}



# Rutas
@app.route('/')
def index():
    titulo = lista_titulos[2]
    return render_template("index.html", titulo=titulo, rutas=diccionario_de_rutas)



@app.route('/listar_datos_sensores', methods=['GET'])
@cross_origin()
def listar_datos_sensores() -> dict:
    """Retorna un objeto `JSON` con los ultimo datos registrados de los sensores en la base de datos.
    
        Parameters:
            No hay parametros
            
        ----------------------
        
        Returns:
        
            JSON: `{'dht22': {'humedad': 12.3, ...}, 'nova': {...}, 'uv': {...} }`
        
        ----------------------
        
        Error:
            JSON: `{'error': str}`
    """
    # TODO: usar consulta multi tabla
    
    
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT idmediciones, humedad, temperatura, fecha, hora, dispositivo_ubicacion FROM mediciones_dht ORDER BY idmediciones DESC LIMIT 1"
        cursor.execute(sql, )
        datos = cursor.fetchall()

        diccionario_datos = {}
        lista_datos_dht = []
        lista_datos_uv = []
        lista_datos_nova = []
               
        for dato in datos:
            registro_dht = Medicion_dht(dato[0], dato[1], dato[2], str(dato[3]), str(dato[4]), dato[5])
            lista_datos_dht.append(registro_dht.__dict__)
            
        sql = "SELECT idmediciones_nova, pm_dos_punto_cinco, pm_diez, fecha, hora, dispositivo_ubicacion FROM mediciones_nova ORDER BY idmediciones_nova DESC LIMIT 1"
        cursor.execute(sql, )
        datos = cursor.fetchall()
        
        for dato in datos:
            registro_nova = Medicion_nova(dato[0], dato[1], dato[2], str(dato[3]), str(dato[4]), dato[5])
            lista_datos_nova.append(registro_nova.__dict__)


        sql = "SELECT idmediciones_uv, radiacion_uv, fecha, hora, dispositivo_ubicacion FROM mediciones_uv ORDER BY idmediciones_uv DESC LIMIT 1"
        cursor.execute(sql, )
        datos = cursor.fetchall()
        
        for dato in datos:
            registro_uv = Medicion_uv(dato[0], dato[1], str(dato[2]), str(dato[3]), dato[4])
            lista_datos_uv.append(registro_uv.__dict__)
        
        diccionario_datos["dht22"] = lista_datos_dht
        diccionario_datos["nova"] = lista_datos_nova
        diccionario_datos["uv"] = lista_datos_uv
        

        return jsonify(diccionario_datos)
    except Exception as e:
        return jsonify({"Error": f"{e}"})
    


@app.route('/listar_dato/<string:sensor>')
@cross_origin()
def listar_dato(sensor) -> dict:
    """
    """
    cursor = mysql.connection.cursor()
    sql = None
    
    if sensor == "dht22":
        sql = "SELECT idmediciones, humedad, temperatura, fecha, hora, dispositivo_ubicacion FROM mediciones_dht ORDER BY idmediciones DESC LIMIT 1"
        cursor.execute(sql, )
        datos = cursor.fetchall()
        objeto_dht = Medicion_dht(datos[0][0], datos[0][1], datos[0][2], str(datos[0][3]), str(datos[0][4]), datos[0][5])
        
        return jsonify(objeto_dht.__dict__)
        
    elif sensor == "uv":
        sql = "SELECT idmediciones_uv, radiacion_uv, fecha, hora, dispositivo_ubicacion FROM mediciones_uv ORDER BY idmediciones_uv DESC LIMIT 1"
        cursor.execute(sql, )
        datos = cursor.fetchall()
        objeto_uv = Medicion_uv(datos[0][0], datos[0][1], str(datos[0][2]), str(datos[0][3]), datos[0][4])
        
        return jsonify(objeto_uv.__dict__)
    
    elif sensor == "nova":
        sql = "SELECT idmediciones_nova, pm_dos_punto_cinco, pm_diez, fecha, hora, dispositivo_ubicacion FROM mediciones_nova ORDER BY idmediciones_nova DESC LIMIT 1"
        cursor.execute(sql, )
        datos = cursor.fetchall()
        objeto_nova = Medicion_nova(datos[0][0], datos[0][1], datos[0][2], str(datos[0][3]), str(datos[0][4]), datos[0][5])
        
        return jsonify(objeto_nova.__dict__)
    else:
        return jsonify({"Error": "No se pudo completar la solicitud"})



@app.route('/listar_ultimos_registros_dht')
@cross_origin()
def listar_ultimos_resgistros_dht():
    cursor = mysql.connection.cursor()
    sql = "SELECT idmediciones, humedad, temperatura, fecha, hora, dispositivo_ubicacion FROM mediciones_dht ORDER BY idmediciones DESC LIMIT 10"
    cursor.execute(sql, )
    datos = cursor.fetchall()
    
    lista_mediciones_dht = []

    for dato in datos:
        medicion_dht = Medicion_dht(dato[0], dato[1], dato[2], str(dato[3]), str(dato[4]), dato[5])
        lista_mediciones_dht.append(medicion_dht.__dict__)
        
    return jsonify(lista_mediciones_dht)



@app.route('/listar_ultimos_registros_uv')
@cross_origin()
def listar_ultimos_registros_uv():
    cursor = mysql.connection.cursor()
    sql = "SELECT idmediciones_uv, radiacion_uv, fecha, hora, dispositivo_ubicacion FROM mediciones_uv ORDER BY idmediciones_uv DESC LIMIT 10"
    cursor.execute(sql, )
    datos = cursor.fetchall()
    
    lista_mediciones_uv = []
    
    for dato in datos:
        medicion_uv = Medicion_uv(dato[0], dato[1], str(dato[2]), str(dato[3]), dato[4])
        lista_mediciones_uv.append(medicion_uv.__dict__)
        
    return jsonify(lista_mediciones_uv)



@app.route('/listar_ultimos_registros_nova')
@cross_origin()
def listar_ultimos_registros_nova():
    cursor = mysql.connection.cursor()
    sql = "SELECT idmediciones_nova, pm_dos_punto_cinco, pm_diez, fecha, hora, dispositivo_ubicacion FROM mediciones_nova ORDER BY idmediciones_nova DESC LIMIT 10"
    cursor.execute(sql, )
    datos = cursor.fetchall()
    
    lista_mediciones_nova = []
    
    for dato in datos:
        medicion_nova = Medicion_nova(dato[0], dato[1], dato[2], str(dato[3]), str(dato[4]), dato[5])
        lista_mediciones_nova.append(medicion_nova.__dict__)
        
    return jsonify(lista_mediciones_nova)


    
@app.route('/listar_dispositivos')
@cross_origin()
def listar_dispositivos(): 
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM dispositivo"
        cursor.execute(sql, )
        datos = cursor.fetchall()

        lista_dispositivos = []
        
        for dato in datos:
            objeto_dispositivo = Dispositivo(dato[0], dato[1])
            lista_dispositivos.append(objeto_dispositivo.__dict__)
            
        return jsonify(lista_dispositivos)
        
    except Exception as e:
        return jsonify({"Error": f"{e}"})








# Rutas de errores
@app.errorhandler(404)
def error_pagina_no_encontrada(error):
    titulo = 404
    return render_template("/error/404.html", titulo=titulo), 404

@app.errorhandler(DatabaseError)
def error_conexion_db(error):
    titulo = 500
    return render_template("/error/500.html", titulo=titulo), 500
    




if __name__ == "__main__":
    app.run(port=8082)
    # app.run(port=5001) # Cambiar en caso de conflictos