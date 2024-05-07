import os

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/main', methods=['POST'])
def main():
    #name = request.form.get('name')

    #if name:
    #    print('Request for hello page received with name=%s' % name)
    #    return render_template('hello.html', name = name)
    #else:
    #    print('Request for hello page received with no name or blank name -- redirecting')
    #    return redirect(url_for('index'))
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_DDBB = os.getenv("DB_DDBB")
    #try:
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_DDBB)
    cursor = connection.cursor()

    print("conexión exitosa")
    mail = request.json['email']
    pasw = request.json['contrasena']

    sql = "select id, nombre, apellido, telefono, email, contrasena, fecha_nacimiento, genero, tipo_usuario, status from usuarios where email='"+mail+"';"
    cursor.execute(sql)
    resp = cursor.fetchone()
    print(str(resp))

    validacion = False
    if pasw == resp[5]:
        validacion= True

        retorno={
            "id":resp[0],
            "nombre":resp[1],
            "apellido":resp[2],
            "telefono":resp[3],
            "email":resp[4],
            "contrasena":resp[5],
            "fecha_nacimiento":resp[6],
            "genero":resp[7],
            "tipo_usuario":resp[8],
            "status":resp[9],
            "validacion":validacion
        }
    else:
        retorno = {           
        "detalle":"user inválido", 
        "validacion":validacion
    }
    return retorno


if __name__ == '__main__':
   app.run()
