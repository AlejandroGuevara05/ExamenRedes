import requests
from cryptography.fernet import Fernet

# Genera el token de encriptación
response = requests.get('http://127.0.0.1:3000/generate_token')
encryption_key = response.json()['encryption_key']

cipher_suite = Fernet(encryption_key)

# Carga una imagen para cifrarla
image_path = '/Users/alejandroguevara/Documents/ITESM/Integración de Seguridad Informática en Redes y Sistemas de Software/Ciberseguridad/sergio.jpeg'  # Cambia a tu archivo de imagen
with open(image_path, 'rb') as img_file:
    image_data = img_file.read()

# Cifra la imagen
encrypted_image = cipher_suite.encrypt(image_data)

# Enviar la imagen cifrada al servidorpi
response = requests.post(
    'http://127.0.0.1:3000/upload_encrypted_image', 
    files={'image': encrypted_image}
)

print(response.json())