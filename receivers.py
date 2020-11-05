import os
import json

from flask import Blueprint, abort, Response, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import create_engine

from models import Receivers

app = Blueprint('receivers', __name__)
engine = create_engine(os.getenv('DB_URL'))

@app.route('/receivers')
def receivers_get_list():
  session = sessionmaker(bind=engine)()
  result = session.query(Receivers).all()

  response = [dict(
    id=receiver.id,
    name=receiver.name,
    address_part_1=receiver.address_part_1,
    address_part_2=receiver.address_part_2,
    url="{}/receiver/{}".format(os.getenv('APP_URL'), receiver.id),
  ) for receiver in result]

  return Response(
      json.dumps(response),
      mimetype='application/json'
  )

@app.route('/receiver/<int:receiver_id>')
def receiver_get(receiver_id):
  session = sessionmaker(bind=engine)()
  try:
    receiver = session.query(Receivers).filter(Receivers.id == receiver_id).one()
  except NoResultFound:
    abort(404)

  response = dict(
    id=receiver.id,
    name=receiver.name,
    address_part_1=receiver.address_part_1,
    address_part_2=receiver.address_part_2,
    bills_url="{}/bills?receiver={}".format(os.getenv('APP_URL'), receiver.id),
  )

  return Response(
      json.dumps(response),
      mimetype='application/json'
  )

@app.route('/receivers', methods=['POST'])
def receiver_post():
  print(request.json)
  try:
    session = sessionmaker(bind=engine)()

    name = request.json['name']
    address_part_1 = request.json['address_part_1']
    address_part_2 = request.json['address_part_2']

    receiver = Receivers(
      name=name,
      address_part_1=address_part_1,
      address_part_2=address_part_2,
    )

    session.add(receiver)
    session.flush()

    session.commit()
  except Exception:
    abort(400)

  return receiver_get(receiver.id)
