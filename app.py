# AUTOR:
#  MORENO LAINES ANGEL ROBERTO: Backend
#  SUÁREZ JUÁREZ ALDAIR ALEXIS: Frontend
# FECHA: 8 DE MAYO DEL 2021
# el programa funcion es cribiendo en la terminal "python app.py"
# este programa cuenta con un indice y para poder buscar frases se debe contar con una cuenta y caso 
# de que no se cuente con una entonces tendremos que crear una, una vez hecho, nos aparecera un nav donde
# estaran situados unos botones que nos permitiran navegar en el servidor creado
# en la busqueda de frases podemos buscar cualquier frase celebre como "todos estos momentos se perderan en el tiempo, como lagrimas bajo la lluvia"
# junto con su limite de distancia para la busqueda, al momento de que aparezca las frases habra un checkbox que 
# nos permitira elegir la frase deseada para guardarla en nuestra cuenta, donde podremos eliminar de nuestras frases
# favoritas las que no querramos mediante un checkbox.  

from flask import Flask, render_template, request, session
from werkzeug.utils import redirect
import secrets
import json
import frases
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
archivo='./static/dicc_y_frases/frases_celebres.csv'
with open("./static/dicc_y_frases/dict_usuarios.json","r") as fh:
    dic_usuario = json.load(fh)


#menu principal
@app.route("/")
def index(): #index o root o home page
    if 'email' in session:
        user = dic_usuario[session['email']]
        usuario=user['username']
        return render_template("index.html", username=usuario)
    return render_template("index.html")
#pagina logout

@app.route('/frasesfav',methods=['GET','POST'])
def frasesfav():
    error=None
    diccionario=dic_usuario[session['email']]
    lista=diccionario['lista']
    if request.method=='POST':
        lista_frases=request.form.getlist('checkbox')
        dic_lista=dict()
        nueva_lista=list()
        i=0
        for n in lista:
            dic_lista[i]=n
            i+=1

        for n in lista_frases:
            i=int(n)
            del dic_lista[i]

        if dic_lista!=None:
            for k,v in dic_lista.items():
                
                nueva_lista.append(v)
        

        diccionario=dic_usuario[session['email']]
        lista=diccionario['lista']
        del dic_usuario[session['email']]
        
        diccionario['lista']=nueva_lista
        dic_usuario[session['email']]=diccionario

        with open("./static/dicc_y_frases/dict_usuarios.json","w") as usuariosjson:
            json.dump(dic_usuario, usuariosjson)
        return redirect('/frasesfav')
    else:
        return render_template('frasesfav.html',error=None,listas=lista)

@app.route('/busqueda',methods=['GET','POST'])
def busqueda():
    error=None
    if request.method=='POST':
        lista_frases=list()
        dic_listas=dict()
        lista=request.form.getlist('checkbox')
        distancias=frases.buscar_frases(archivo, request.form['frase'], int(request.form['limite']))
        i=0
        for n in distancias:
            dic_listas[i]=n
            i+=1
        if lista!=None:

            for n in lista:
                i=int(n)
                lista_frases.append(dic_listas[i])

            diccionario=dic_usuario[session['email']]
            del dic_usuario[session['email']]
            if diccionario['lista']==None:
                diccionario['lista']=lista_frases
                dic_usuario[session['email']]=diccionario
            else:
                nueva_lista=list()
                nueva_lista=diccionario['lista']
                for l in lista_frases:
                    
                    nueva_lista.append(l)
                diccionario['lista']=nueva_lista
                dic_usuario[session['email']]=diccionario
            with open("./static/dicc_y_frases/dict_usuarios.json","w") as usuariosjson:
                json.dump(dic_usuario, usuariosjson)
            
    
        return render_template('busqueda.html',error=None,listas=distancias)
    else:
        return render_template('busqueda.html',error=None,listas=None)

@app.route("/logout")
def logout():
    if 'email' in session:
        session.pop('email', None)
        return redirect('/')

@app.route('/login', methods=['GET','POST']) # GET---> info de ida del server hacia el navegador
def login():                                 # POST --> info de regreso del navegador al server
    error = None
    dicc_user=dict()
    if request.method == 'POST':
        email = request.form['email']
        #validamos el correo si existe
        if (request.form['email'] in dic_usuario):
            username = dic_usuario[request.form['email']]['username'] 
            # password = dic_usuario[request.form['email']]['password']   
            # Obtener el hash de la contraseña ingresada y validar que sea la misma que tenemos registrada
            dicc_user=dic_usuario[email]
            if (str(request.form['password']) == dicc_user["password"]):   
                session['email'] = email
                return redirect('/')
            else:
                return render_template('login.html', error='Password incorrecto')
        else:
                return render_template('login.html', error='email incorrecto')
    else:   
        return render_template('login.html', error=None)
@app.route('/register', methods=['GET','POST'])
def registro():
    error=None
    if request.method == 'POST':
        email = request.form['email']
        # Validar que el email ingresado en el formulario de registro no esté registrado previamente
        if (request.form['email'] not in dic_usuario):
            # Obtener el nombre de usuario ingresada en el formulario
            username = request.form['username']
            password = request.form['password']
            # Validar que el email ingresado en el formulario de registro no esté registrado previamente
            dic_usuario[email] ={'username': username, 'password': password, 'lista': None}
            #actualizar el archivo json del diccionario de usuarios
            with open("./static/dicc_y_frases/dict_usuarios.json","w") as usuariosjson:
                json.dump(dic_usuario, usuariosjson)
            # Iniciar sesión con el usuario recien registrado y redireccionar al index
            session['email'] = email
            return redirect('/')
        else:
            return render_template('register.html', error='El email ya existe')
    else:   
        return render_template('register.html', error=None)

@app.route('/modificar',methods=['GET','POST'])
def update():
    error = None
    dicc_user=dict()
    if request.method=='POST':
        dicc_user=dic_usuario[session['email']]
        del dic_usuario[session['email']]
        del dicc_user['username']
        del dicc_user['password']
        dicc_user['username']=request.form['username2']
        dicc_user['password']=request.form['password2']
        dic_usuario[request.form['email2']]=dicc_user
        with open("./static/dicc_y_frases/dict_usuarios.json","w") as usuariosjson:
            json.dump(dic_usuario, usuariosjson)
        return redirect('/modificar')
    else:
        dicc_user=dic_usuario[session['email']]
        email=session['email']
        user=dicc_user['username']
        password=dicc_user['password']   
        return render_template('update.html', error=None,email1=email,username1=user,password1=password)

if __name__ == "__main__":
    app.run(debug =True, port=8000 )