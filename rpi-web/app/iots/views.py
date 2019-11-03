from flask import Blueprint

from .models import IoTs
from .schemas import IoTSchema
from .. import db, io

app = Blueprint('companies', __name__, url_prefix='/api/v1')


@app.route('/id/<iot_id>', methods=['GET'])
def get_iot_data(iot_id):
    iot = IoTs.query.filter_by(id=iot_id).first()
    if not iot:
        return io.not_found('Iot Data not found: ' + str(iot_id))
    return iot.to_dict()


@app.route('/date/<date>', methods=['GET'])
def get_iot_date_all(date):
    iot_all = IoTs.query.filter_by(date=date).all()
    if not iot_all:
        return io.not_found('Iot Data not found: ' + str(date))
    result = []
    for item in iot_all:
        result.append(item.to_dict())
    return result


@app.route('/device/<device>/date/<date>', methods=['GET'])
def get_iot_date_all_by_id(date, device):
    iot_all = IoTs.query.filter_by(device=device).filter_by(date=date).all()
    if not iot_all:
        return io.not_found('Iot Data not found: ' + str(date))
    result = []
    for item in iot_all:
        result.append(item.to_dict())
    return result


@app.route('/current', methods=['GET'])
def get_current_data():
    iot = IoTs.query.order_by(IoTs.timestamp.desc()).first()
    if not iot:
        return io.not_found('Iot Data not found ')
    return iot.to_dict()


@app.route('/iot', methods=['POST'])
@io.from_body('req', IoTSchema)
def insert_iot(req):
    print(req)
    iot = IoTs(req['hmt'], req['tmp'], req['ppm'], req['lx'], req['ld'], req['date'], req['time'], req['timestamp'], req['device'])
    db.session.add(iot)
    db.session.commit()
    return {"errors": "success"}
