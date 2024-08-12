from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coordenadas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Coordenada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    androidId = db.Column(db.String(50), nullable=False)

@app.route('/api/location', methods=['POST', 'GET'])
def manejar_coordenadas():
    if request.method == 'POST':
        datos = request.json
        if 'latitude' in datos and 'longitude' in datos and 'androidId' in datos:
            nueva_coordenada = Coordenada(
                latitude=datos['latitude'],
                longitude=datos['longitude'],
                androidId=datos['androidId']
            )
            
            try:
                db.session.add(nueva_coordenada)
                db.session.commit()
                return jsonify({'mensaje': 'Coordenadas agregadas correctamente'}), 200
            except SQLAlchemyError:
                db.session.rollback()
                return jsonify({'error': 'Error al guardar las coordenadas'}), 500
        else:
            return jsonify({'error': 'Datos de coordenadas incompletos'}), 400
    
    elif request.method == 'GET':
        try:
            coordenadas = Coordenada.query.all()
            return jsonify([
                {
                    'latitude': c.latitude,
                    'longitude': c.longitude,
                    'androidId': c.androidId
                } for c in coordenadas
            ]), 200
        except SQLAlchemyError:
            return jsonify({'error': 'Error al obtener las coordenadas'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8001)
