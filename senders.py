import os
import json

from flask import Blueprint, abort, Response, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import create_engine

from models import Senders

app = Blueprint('senders', __name__)
engine = create_engine(os.getenv('DB_URL'))

@app.route('/senders')
def senders_get_list():
  session = sessionmaker(bind=engine)()
  result = session.query(Senders).all()

  response = [dict(
    id=sender.id,
    name=sender.name,
    address_part_1=sender.address_part_1,
    address_part_2=sender.address_part_2,
    phone=sender.phone,
    email=sender.email,
    siren=sender.siren,
    bank_details_name=sender.bank_details_name,
    bank_details_bank=sender.bank_details_bank,
    bank_details_iban=sender.bank_details_iban,
    bank_details_bic=sender.bank_details_bic,
    url="{}/sender/{}".format(os.getenv('APP_URL'), sender.id),
  ) for sender in result]

  return Response(
      json.dumps(response),
      mimetype='application/json'
  )

@app.route('/sender/<int:sender_id>')
def sender_get(sender_id):
  session = sessionmaker(bind=engine)()
  try:
    sender = session.query(Senders).filter(Senders.id == sender_id).one()
  except NoResultFound:
    abort(404)

  response = dict(
    id=sender.id,
    name=sender.name,
    address_part_1=sender.address_part_1,
    address_part_2=sender.address_part_2,
    phone=sender.phone,
    email=sender.email,
    siren=sender.siren,
    bank_details_name=sender.bank_details_name,
    bank_details_bank=sender.bank_details_bank,
    bank_details_iban=sender.bank_details_iban,
    bank_details_bic=sender.bank_details_bic,
    bills_url="{}/bills?sender={}".format(os.getenv('APP_URL'), sender.id),
  )

  return Response(
      json.dumps(response),
      mimetype='application/json'
  )

@app.route('/senders', methods=['POST'])
def sender_post():
  print(request.json)
  try:
    session = sessionmaker(bind=engine)()

    name = request.json['name']
    address_part_1 = request.json['address_part_1']
    address_part_2 = request.json['address_part_2']
    phone = request.json['phone']
    email = request.json['email']
    siren = request.json['siren']
    bank_details_name = request.json['bank_details_name']
    bank_details_bank = request.json['bank_details_bank']
    bank_details_iban = request.json['bank_details_iban']
    bank_details_bic = request.json['bank_details_bic']

    sender = Senders(
      name=name,
      address_part_1=address_part_1,
      address_part_2=address_part_2,
      phone=phone,
      email=email,
      siren=siren,
      bank_details_name=bank_details_name,
      bank_details_bank=bank_details_bank,
      bank_details_iban=bank_details_iban,
      bank_details_bic=bank_details_bic,
    )

    session.add(sender)
    session.flush()

    session.commit()
  except Exception:
    abort(400)

  return sender_get(sender.id)
