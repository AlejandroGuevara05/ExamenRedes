from flask import Flask, request, jsonify, send_file
import datetime
from cryptography.fernet import Fernet
import os
import base64

app = Flask(__name__)
encryption_key = None
cipher_suite = None

@app.route("/generate_token", methods=['GET']) 
def generate_token():
    global encryption_key, cipher_suite
    encryption_key = Fernet.generate_key()
    cipher_suite = Fernet(encryption_key)
    return jsonify({'encryption_key': encryption_key.decode()})

@app.route("/upload_encrypted_image", methods=['POST'])
def upload_encrypted_image():
    if cipher_suite is None:
        return jsonify({'error': 'No se ha generado un token'}), 400

    # Obtiene la imagen encriptada del cliente
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No se proporcionó un archivo'}), 400
    
    encrypted_image = file.read()  # Obtiene los bytes del archivo
    
    # Desencripta la imagen
    decrypted_image = cipher_suite.decrypt(encrypted_image)

    # Guarda la imagen desencriptada en un archivo temporal
    image_path = "decrypted_image.png"
    with open(image_path, 'wb') as img_file:
        img_file.write(decrypted_image)
    
    return jsonify({'message': 'Imagen desencriptada', 'image_path': image_path})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)