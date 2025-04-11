from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Para permitir peticiones desde cualquier origen

@app.route('/location', methods=['POST'])
def receive_location():
    data = request.get_json()
    lat = data.get('lat')
    lon = data.get('lon')
    time = data.get('time', datetime.utcnow().isoformat())

    # Aquí puedes guardar en base de datos, enviar alerta, etc.
    print(f"[{time}] Ubicación recibida: lat={lat}, lon={lon}")

    return jsonify({'status': 'received'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
