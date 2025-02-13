import unittest
import requests
# import json

BASE_URL = "http://127.0.0.1:5001"

class FlaskAppTestCase(unittest.TestCase):
    """
    Clase de prueba para la aplicación Flask.

    Esta clase contiene pruebas unitarias para verificar la seguridad y 
    el comportamiento correcto de la aplicación Flask. Se utilizan 
    pruebas para detectar vulnerabilidades como inyecciones SQL, 
    ataques XSS, almacenamiento inseguro de contraseñas, 
    autenticación y autorización, referencias directas a objetos 
    inseguros y exposición de datos sensibles.
    """
    
    def get_auth_token(self, user):
        """
        Obtiene un token de autenticación para un usuario dado.

        Esta función realiza una solicitud de inicio de sesión para obtener 
        el token JWT del usuario. Se espera que el usuario tenga un nombre 
        de usuario y una contraseña válidos.

        Args:
            user (dict): Un diccionario que contiene el nombre de usuario 
                          y la contraseña del usuario.

        Returns:
            str: El token de autenticación obtenido de la respuesta JSON.

        Raises:
            AssertionError: Si la autenticación falla y el código de estado 
                            no es 200.
        """
        # Login para obtener el token (esto depende de cómo sea el login en tu app)
        response = requests.post(f"{BASE_URL}/login", json=user)  # Ajusta la ruta del login si es necesario
        self.assertEqual(response.status_code, 200, "Failed to authenticate")
        return response.json()['token']  # Asegúrate de que el campo del token sea el correcto
    
    def test_sql_injection(self):
        """
        Prueba para detectar vulnerabilidades de inyección SQL.

        Esta función intenta crear un usuario con un nombre de usuario que 
        contiene una carga útil de inyección SQL. Se espera que la 
        creación del usuario falle y no devuelva un código de estado 201.

        Raises:
            AssertionError: Si se detecta una vulnerabilidad de inyección SQL.
        """
        payload = {"username": "testuser'; DROP TABLE users; --", "password": "testpass"}
        response = requests.post(f"{BASE_URL}/user", json=payload)
        self.assertNotEqual(response.status_code, 201, "SQL Injection vulnerability detected")

    def test_xss(self):
        """
        Prueba para detectar vulnerabilidades de XSS.

        Esta función intenta crear un usuario con un nombre de usuario que 
        contiene un script malicioso. Se espera que la respuesta no contenga 
        el script, indicando que la aplicación es segura contra ataques XSS.

        Raises:
            AssertionError: Si se detecta una vulnerabilidad XSS.
        """
        payload = {"username": "<script>alert('XSS');</script>", "password": "testpass"}
        response = requests.post(f"{BASE_URL}/user", json=payload)
        self.assertNotIn("<script>", response.text, "XSS vulnerability detected")
    
    def test_insecure_password_storage(self):
        """
        Prueba para verificar el almacenamiento seguro de contraseñas.

        Esta función crea un nuevo usuario y verifica que la contraseña 
        no esté expuesta al obtener los detalles del usuario. Se espera 
        que la contraseña no aparezca en la respuesta.

        Raises:
            AssertionError: Si la contraseña se expone en la respuesta o 
                            si la recuperación del usuario falla.
        """
        payload = {"username": "testuser", "password": "testpass"}
        response = requests.post(f"{BASE_URL}/user", json=payload)
        # print(response.json())
        self.assertEqual(response.status_code, 201)

        # Obtener el ID del usuario
        user_id = response.json()["id"]
        auth_token = self.get_auth_token({"username": "testuser", "password": "testpass"})

        # 3. Realizar un GET al usuario con el token para asegurar que la contraseña no esté en la respuesta
        response = requests.get(f"{BASE_URL}/user/{user_id}", headers={"Authorization": f"Bearer {auth_token}"})
        self.assertEqual(response.status_code, 200, "Failed to retrieve user")
        # Verificar que la contraseña no esté en la respuesta
        response = requests.get(f"{BASE_URL}/user/{user_id}")
        self.assertNotIn("testpass", response.json().get("password", ""), "Insecure password storage detected")


    def test_authentication(self):
        """
        Prueba para verificar la autenticación.

        Esta función intenta acceder a la lista de usuarios sin un token 
        de autenticación. Se espera que la respuesta devuelva un código 
        de estado 401, indicando que la autenticación es necesaria.

        Raises:
            AssertionError: Si no se detecta la falta de autenticación.
        """
        response = requests.get(f"{BASE_URL}/users")
        self.assertEqual(response.status_code, 401, "No authentication detected")

    def test_authorization(self):
        """
        Prueba para verificar la autorización.

        Esta función intenta actualizar un usuario utilizando un token 
        de autenticación que no tiene los permisos necesarios. Se espera 
        que la respuesta devuelva un código de estado 403, indicando que 
        la autorización ha fallado.

        Raises:
            AssertionError: Si no se detecta la falta de autorización.
        """
        # Primero obtenemos el token de autenticación
        payload = {"username": "hacker", "password": "soyhacker"}
        response = requests.post(f"{BASE_URL}/user", json=payload)
        print(response.text)
        user_id = response.json()["id"]
        auth_token = self.get_auth_token({"username": "hacker", "password": "soyhacker"})

        # Intentamos hacer un PUT con el token de autenticación
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.put(f"{BASE_URL}/user/{user_id}", json={"username": "admin", "password": "hackedpass"}, headers=headers)
        print(response.text)
        self.assertEqual(response.status_code, 403, "No authorization detected")
    
    def test_insecure_direct_object_references(self):
        """
        Prueba para detectar referencias directas a objetos inseguras.

        Esta función crea un nuevo usuario y verifica que puede acceder 
        a su propia información. Luego intenta acceder a la información 
        de otro usuario, lo que debería estar prohibido. Se espera que 
        la respuesta devuelva un código de estado 403.

        Raises:
            AssertionError: Si se permite el acceso a la información de 
                            otro usuario.
        """
        # Crear un usuario normal
        payload = {"username": "testuser1", "password": "testpass"}
        response = requests.post(f"{BASE_URL}/user", json=payload)
        self.assertEqual(response.status_code, 201, "Failed to create user")

        # Obtener el ID del usuario creado
        user_id = response.json()["id"]

        # Iniciar sesión como ese usuario para obtener el token de autenticación
        auth_token = self.get_auth_token({"username": "testuser1", "password": "testpass"})

        # Intentar acceder al propio usuario
        response = requests.get(f"{BASE_URL}/user/{user_id}", headers={"Authorization": f"Bearer {auth_token}" ,
                                                                       "Accept": "application/json"})
        print(response.text)
        self.assertEqual(response.status_code, 200, "Failed to retrieve user")
        
        # Intentar acceder a la información de otro usuario (que no está autenticado)
        # En este caso, tratamos de acceder al usuario con un ID que no es el nuestro
        response = requests.get(f"{BASE_URL}/user/{user_id-1}", headers={"Authorization": f"Bearer {auth_token}" ,
                                                                       "Accept": "application/json}"})
        print(response.text)
        self.assertEqual(response.status_code, 403, "Insecure direct object reference detected")

    def test_data_exposure(self):
        """
        Prueba para detectar la exposición de datos sensibles.

        Esta función crea un usuario con rol de administrador y verifica 
        que al acceder a la lista de usuarios, no se expongan contraseñas 
        en la respuesta. Se espera que la respuesta devuelva un código 
        de estado 200.

        Raises:
            AssertionError: Si se detecta que las contraseñas están 
                            expuestas en la respuesta.
        """
        # Crear un usuario con rol de admin
        payload = {"username": "adminuser", "password": "adminpass", "role": "admin"}
        response = requests.post(f"{BASE_URL}/user", json=payload)
        self.assertEqual(response.status_code, 201, "Failed to create admin user")

        # Obtener el token de autenticación del admin
        auth_token = self.get_auth_token({"username": "adminuser", "password": "adminpass"})

        # Acceder a la lista de usuarios con el token de admin
        response = requests.get(f"{BASE_URL}/users", headers={"Authorization": f"Bearer {auth_token}", "Accept": "application/json"})
    
        # Verificar que no haya contraseñas expuestas en la respuesta
        users = response.json()
        for user in users:
            self.assertNotIn("password", user, "Sensitive data exposure detected")

        self.assertEqual(response.status_code, 200, "Failed to retrieve users")
    
if __name__ == '__main__':
    unittest.main()