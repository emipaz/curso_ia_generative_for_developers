from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re
import jwt  # Para generar tokens
import datetime
from functools import wraps  # Para proteger rutas


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "supersecretkey"  # Clave para firmar los tokens
db = SQLAlchemy(app)


class User(db.Model):
    """
    Clase que representa un usuario en la base de datos.

    Atributos:
        id (int): Identificador único del usuario (clave primaria).
        username (str): Nombre de usuario único y no nulo.
        password (str): Contraseña del usuario, almacenada como una cadena.
        role (str): Rol del usuario en el sistema, puede ser "admin" o "user".
    """
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False) 
    role     = db.Column(db.String(10), nullable=False, default="user")  # "admin" o "user"

# El bloque 'with app.app_context():' se utiliza para crear un contexto de aplicación,
# lo que permite realizar operaciones que requieren acceso a la configuración de la aplicación
# y a la base de datos. Dentro de este contexto, se llama a db.create_all() para crear
# todas las tablas definidas en los modelos de la base de datos.
with app.app_context():
    db.create_all()


def create_admin_interactively():
    """
    Crea un usuario administrador de forma interactiva.

    Esta función verifica si ya existe un usuario con el rol de administrador en la base de datos. 
    Si no existe, solicita al usuario que ingrese un nombre de usuario y una contraseña. 
    Si el usuario no desea crear uno, se utilizan valores predeterminados ("admin" para el nombre de usuario 
    y la contraseña). La contraseña ingresada se cifra utilizando un hash antes de ser almacenada en la base de datos.

    Excepciones:
        Si ocurre un error al agregar el nuevo usuario a la base de datos, se imprime un mensaje de error.
    """
    with app.app_context():  # Necesitamos estar dentro del contexto de la app
        admin_user = User.query.filter_by(role="admin").first()
        if admin_user:
            print("El usuario administrador ya existe.")
        else:
            default=False
            if input("No hay un administrador desea crar uno s/n:").lower() == "s":
                username = input("Enter admin username: ")
                password = input("Enter admin password: ")
                default  = True
            else:
                username = "admin"
                password = "admin"
            try:
                hashed_password = generate_password_hash(password) # Generamos el hash de la contraseña
                new_admin = User(username=username, password=hashed_password, role="admin")
                db.session.add(new_admin)
                db.session.commit()
            except Exception as e:
                print("Error :", e)
                
            print(f"Admin user created with username '{username}'.")


# Función para validar y limpiar el username
def sanitize_username(username):
    """
    Si el nombre de usuario contiene caracteres sospechosos, devuelve None.
    """
    if re.search(r'[<>"/\'&]', username):
        return None
    return username

def token_required(f):
    """
    Decorador que verifica la presencia y validez de un token JWT en las solicitudes.

    Este decorador se utiliza para proteger rutas que requieren autenticación. 
    Extrae el token de la cabecera 'Authorization' de la solicitud y verifica su validez. 
    Si el token no está presente o es inválido, se devuelve un mensaje de error correspondiente 
    con el código de estado HTTP adecuado. Si el token es válido, se recupera el usuario actual 
    a partir del ID del usuario contenido en el token y se adjunta el rol del usuario a la solicitud.

    Args:
        f (function): La función que se va a decorar, que representa la ruta protegida.

    Returns:
        function: La función decorada que incluye la lógica de verificación del token.

    Raises:
        Exception: Si el token no es válido o si el usuario no se encuentra en la base de datos.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        
        try:
            token = token.split(" ")[1]  # Remover "Bearer"
            # decodificamos el token que hemos recibido de login
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # Buscamos el usuario en la base de datos
            current_user = User.query.get(data["user_id"])
            # Si el usuario no existe, devolvemos un error
            if not current_user:
                return jsonify({"message": "User not found"}), 404
            request.user_role = data["role"]  # Guardamos el rol en la petición
            print(f"User role from token: {request.user_role}")  # Debug
        except Exception as e:
            print(f"Token error: {e}")  # Debug
            return jsonify({"message": "Invalid token"}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    """
    Maneja la autenticación de usuarios y genera un token JWT.

    Esta función recibe las credenciales del usuario (nombre de usuario y contraseña) 
    a través de una solicitud POST. Verifica si el usuario existe en la base de datos 
    y si la contraseña proporcionada es correcta. Si las credenciales son válidas, 
    se genera un token JWT que contiene el ID del usuario, el nombre de usuario, 
    el rol del usuario y una fecha de expiración de 1 hora.

    Returns:
        json: Un objeto JSON que contiene el token JWT si las credenciales son válidas.
               En caso de credenciales inválidas, devuelve un mensaje de error con el código
               de estado HTTP 401.

    Raises:
        Exception: Si ocurre un error durante la verificación de credenciales o la generación del token.
    """
    data = request.get_json()
    print(data)  # Debug
    # Verificamos si el usuario existe y si la contraseña es correcta
    user = User.query.filter_by(username=data['username']).first()
    # Si el usuario no existe o la contraseña es incorrecta, devolvemos un error
    if not user or not check_password_hash(user.password, data['password']):
        print("No autorizado Invalid credentials")
        return jsonify({"message": "Invalid credentials"}), 401
    # Generamos un token JWT con la información del usuario
    token = jwt.encode({
        "user_id" : user.id,
        "user": user.username,
        "role": user.role, 
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    print("Token enviado") # Debug
    return jsonify({"token": token})


@app.route('/')
def home():
    """
    Ruta de inicio de la aplicación.
    """
    return "Welcome to the Security Testing Demo!"

@app.route('/users', methods=['GET'])
@token_required
def get_users(current_user):
    """
    Recupera la lista de todos los usuarios en la base de datos.

    Esta función maneja las solicitudes GET a la ruta '/users' y devuelve un 
    objeto JSON que contiene una lista de todos los usuarios registrados. 
    Cada usuario en la lista incluye su ID, nombre de usuario y rol. 
    La función requiere que el usuario esté autenticado mediante un token JWT, 
    que se verifica a través del decorador @token_required.

    Args:
        current_user (User): El usuario actual que realiza la solicitud, 
                              obtenido del token JWT.

    Returns:
        json: Un objeto JSON que contiene una lista de diccionarios, 
              donde cada diccionario representa un usuario y contiene 
              los campos 'id', 'username' y 'role'.
    
    Pendiente:
            que solo el admin pueda ver todos los usuarios
    
    """
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "role":user.role} for user in users])

@app.route('/user/<int:id>', methods=['GET'])
@token_required  # Aseguramos que se requiere un token para acceder a esta ruta
def get_user(current_user, id):
    """
    Recupera la información de un usuario específico por su ID.

    Esta función maneja las solicitudes GET a la ruta '/user/<id>' y devuelve 
    los detalles del usuario correspondiente al ID proporcionado en la URL. 
    La función verifica que el usuario actual tenga el rol de "admin" o que 
    el ID solicitado coincida con el ID del usuario autenticado. Si no se cumple 
    esta condición, se devuelve un mensaje de error con el código de estado HTTP 403.

    Args:
        current_user (User): El usuario actual que realiza la solicitud, 
                              obtenido del token JWT.
        id (int): El ID del usuario que se desea recuperar.

    Returns:
        json: Un objeto JSON que contiene los detalles del usuario, 
              incluyendo 'id', 'username' y 'role', si el usuario es encontrado.
              En caso de que el usuario no exista, se devuelve un mensaje de error 
              con el código de estado HTTP 404.
    """
    # Verificamos que el ID solicitado coincida con el ID del usuario en el token
    if current_user.role != "admin" and id != current_user.id:
        print(current_user.username , "Rechazado por solicitar solicitud indevida")
        return jsonify({"message": "Forbidden"}), 403
    user = User.query.get(id)
    if user:
        return jsonify({"id": user.id, "username": user.username, "role":user.role})
    return jsonify({"message": "User not found"}), 404

@app.route('/user', methods=['POST'])
def add_user():
    """
    Agrega un nuevo usuario a la base de datos.

    Esta función maneja las solicitudes POST a la ruta '/user' y permite la creación 
    de un nuevo usuario. Se espera que la solicitud contenga un JSON con el nombre 
    de usuario y la contraseña. La función valida que estos datos estén presentes 
    y no contengan caracteres sospechosos. La contraseña se cifra antes de ser 
    almacenada en la base de datos. Si la creación del usuario es exitosa, se 
    devuelve un mensaje de éxito junto con el ID del nuevo usuario y su nombre de 
    usuario.

    Returns:
        json: Un objeto JSON que indica el resultado de la operación. 
              Si el usuario se agrega correctamente, se devuelve un mensaje de éxito 
              con el ID, el nombre de usuario y el rol del nuevo usuario con un 
              código de estado HTTP 201. 
              En caso de errores de validación, se devuelve un mensaje de error 
              con un código de estado HTTP 400.

    Raises:
        Exception: Si ocurre un error durante la adición del usuario a la base de datos.
    """
    data = request.get_json()

    # Validar que los datos necesarios estén presentes
    if not data.get('username') or not data.get('password'):
        print("Faltan Datos")
        return jsonify({"message": "Username and password are required"}), 400
            
    # Validar username (no permitir caracteres sospechosos)
    if "'" in data['username'] or ";" in data['username'] or "--" in data['username']:
        print("username invalido")
        return jsonify({"message": "Invalid characters in username"}), 400

    # Encriptar contraseña antes de almacenarla
    hashed_password = generate_password_hash(data['password'])
    
    # new_user = User(username=data['username'], password=data['password'])
    # pasamos la contraseña
    clean_username = sanitize_username(data['username'])
    if clean_username is None:
        print("caracteres invalidos en el username")
        return jsonify({"message": "Invalid characters in username"}), 400

    #role = data.get("role", "user")  # Si no hay rol, asignamos "user"
    role = "user"
    try:
        new_user = User(username=clean_username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Error adding user"}), 500
    else:
        print(new_user.username , "Agregado correctamente")
        return jsonify({"message": "User added successfully", "id":new_user.id, "user_name":new_user.username, "rol":new_user.role}), 201

@app.route('/user/<int:id>', methods=['PUT'])
@token_required
def update_user(current_user, id):
    """
    Actualiza la información de un usuario específico.

    Esta función maneja las solicitudes PUT a la ruta '/user/<id>' y permite 
    la actualización de los detalles de un usuario existente. Solo los usuarios 
    con el rol de "admin" tienen permiso para realizar esta operación. La función 
    recibe un JSON con los nuevos datos del usuario, que incluyen el nombre de usuario, 
    la contraseña y el rol. Si el usuario es encontrado y actualizado exitosamente, 
    se devuelve un mensaje de éxito. Si el usuario no existe, se devuelve un mensaje 
    de error con el código de estado HTTP 404.

    Args:
        current_user (User): El usuario actual que realiza la solicitud, 
                              obtenido del token JWT.
        id (int): El ID del usuario que se desea actualizar.

    Returns:
        json: Un objeto JSON que indica el resultado de la operación. 
              Si el usuario se actualiza correctamente, se devuelve un mensaje de éxito. 
              En caso de que el usuario no exista, se devuelve un mensaje de error 
              con un código de estado HTTP 404. 
              Si el usuario no tiene permisos, se devuelve un mensaje de error 
              con un código de estado HTTP 403.

    Raises:
        Exception: Si ocurre un error durante la actualización del usuario en la base de datos.
    """
    print(f"Updating user {id} - Role: {request.user_role}")  # Debug
    
    if request.user_role != "admin":
        return jsonify({"message": "Forbidden"}), 403
    
    data = request.get_json()
    user = User.query.get(id)
    try:
        if user:
            user.username = data['username']
            user.password = generate_password_hash(data['password'])
            user.role = data.get("role", "user")
            db.session.commit()
            return jsonify({"message": "User updated successfully"})
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": "Error updating user"}), 500
    
@app.route('/user/<int:id>', methods=['DELETE'])
@token_required
def delete_user( current_user, id):
    """
    Elimina un usuario específico de la base de datos.

    Esta función maneja las solicitudes DELETE a la ruta '/user/<id>' y permite 
    la eliminación de un usuario existente. Solo los usuarios con el rol de "admin" 
    o el propio usuario pueden realizar esta operación. Si el usuario es encontrado 
    y eliminado exitosamente, se devuelve un mensaje de éxito. Si el usuario no existe, 
    se devuelve un mensaje de error con el código de estado HTTP 404.

    Args:
        current_user (User): El usuario actual que realiza la solicitud, 
                              obtenido del token JWT.
        id (int): El ID del usuario que se desea eliminar.

    Returns:
        json: Un objeto JSON que indica el resultado de la operación. 
              Si el usuario se elimina correctamente, se devuelve un mensaje de éxito. 
              En caso de que el usuario no exista, se devuelve un mensaje de error 
              con un código de estado HTTP 404. 
              Si el usuario no tiene permisos para realizar la eliminación, 
              se devuelve un mensaje de error con un código de estado HTTP 403.

    Raises:
        Exception: Si ocurre un error durante la eliminación del usuario en la base de datos.
    """
    # Verificamos si el usuario actual es admin o si es el propio usuario
    if current_user.role != "admin" and current_user.id != id:
        return jsonify({"message": "Forbidden"}), 403
    
    try:    
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully"})
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": "Error deleting user"}), 500


if __name__ == "__main__":
    create_admin_interactively()
    app.run(host="127.0.0.1", port=5001,debug=True)