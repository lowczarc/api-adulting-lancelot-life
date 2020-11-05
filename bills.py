import os
import uuid
import json
import datetime
import subprocess

from flask import Blueprint, request, abort, Response
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import create_engine

from models import Receivers, Senders, Bills, Products, BillsWithoutNumber

app = Blueprint('bills', __name__)

engine = create_engine(os.getenv('DB_URL'))

@app.route('/bills')
def bills_get_list():
  session = sessionmaker(bind=engine)()
  query = session.query(Bills, Receivers, Senders).select_from(Bills).join(Receivers, Senders, Products)

  receiver_filter = request.args.get('receiver', default=None, type=int)
  sender_filter = request.args.get('sender', default=None, type=int)

  if receiver_filter is not None:
    query = query.filter(Receivers.id == receiver_filter)

  if sender_filter is not None:
    query = query.filter(Senders.id == sender_filter)

  before_filter = request.args.get('before', default=None, type=str)

  if before_filter is not None:
    try:
      before = datetime.datetime.strptime(before_filter, "%Y-%m-%d")
    except ValueError:
      abort(400, "The parameter 'before' must be a valid ISO 8601 date")
    query = query.filter(Bills.date <= before)

  after_filter = request.args.get('after', default=None, type=str)

  if after_filter is not None:
    try:
      after = datetime.datetime.strptime(after_filter, "%Y-%m-%d")
    except ValueError:
      abort(400, "The parameter 'after' must be a valid ISO 8601 date")
    query = query.filter(Bills.date >= after)


  result = query.all()

  response = [dict(
      id=bill[0].id,
      number=bill[0].number,
      date=bill[0].date.isoformat(),
      sender=dict(
        id=bill[2].id,
        name=bill[2].name,
        url="{}/sender/{}".format(os.getenv('APP_URL'), bill[2].id),
      ),
      receiver=dict(
        id=bill[1].id,
        name=bill[1].name,
        url="{}/receiver/{}".format(os.getenv('APP_URL'), bill[1].id),
      ),
      url="{}/bill/{}".format(os.getenv('APP_URL'), bill[0].id),
      pdf="{}/bill/{}.pdf".format(os.getenv('APP_URL'), bill[0].id),
    ) for bill in result]

  return Response(
      json.dumps(response),
      mimetype='application/json'
  )

@app.route('/bill/<int:bill_id>')
def bill_get(bill_id):
  session = sessionmaker(bind=engine)()
  try:
    bill = session.query(Bills, Receivers, Senders).select_from(Bills).join(Receivers, Senders, Products).filter(Bills.id == bill_id).one()
  except NoResultFound:
    abort(404)

  products = session.query(Products).filter(Products.bill_id == bill_id).all()
  response = dict(
      id=bill[0].id,
      number=bill[0].number,
      date=bill[0].date.isoformat(),
      sender=dict(
        id=bill[2].id,
        name=bill[2].name,
        url="{}/sender/{}".format(os.getenv('APP_URL'), bill[2].id),
      ),
      receiver=dict(
        id=bill[1].id,
        name=bill[1].name,
        url="{}/receiver/{}".format(os.getenv('APP_URL'), bill[1].id),
      ),
      products=[dict(
        id=product.id,
          description=product.description,
          quantity=product.quantity,
          unitary_price=product.unitary_price,
      ) for product in products],
      total_price=sum([product.quantity * product.unitary_price for product in products]),
      pdf="{}/bill/{}.pdf".format(os.getenv('APP_URL'), bill[0].id),
  )
  return Response(
      json.dumps(response),
      mimetype='application/json'
  )

try:
    os.mkdir(os.getenv('PDF_TMP_DIR'))
except Exception:
    pass

@app.route('/bill/<int:bill_id>.pdf')
def bill_get_pdf(bill_id):
  session = sessionmaker(bind=engine)()
  try:
    session.query(Bills, Receivers, Senders).select_from(Bills).join(Receivers, Senders, Products).filter(Bills.id == bill_id).one()
  except NoResultFound:
    abort(404)

  pdf_path = os.getenv('PDF_TMP_DIR') + '/' + str(uuid.uuid1()) + '.pdf'

  command = "cd /tmp && sh $PDF_GENERATOR/generate_pdf.sh {} {}".format(bill_id, pdf_path)
  subprocess.check_call(command, shell=True)

  pdf = open(pdf_path, 'rb')
  string_pdf = pdf.read()
  pdf.close()

  os.remove(pdf_path)

  return Response(
      string_pdf,
      mimetype='application/pdf',
  )

@app.route('/bills', methods=['POST'])
def bill_post():
  try:
    session = sessionmaker(bind=engine)()

    sender_id = request.json['sender_id']
    receiver_id = request.json['receiver_id']
    products = request.json['products']

    bill = BillsWithoutNumber(date=datetime.datetime.now(), sender_id=sender_id, receiver_id=receiver_id)

    session.add(bill)
    session.flush()

    products = [Products(
      bill_id=bill.id,
      quantity=product['quantity'],
      description=product['description'],
      unitary_price=product['unitary_price'],
    ) for product in products]

    for product in products:
      session.add(product)
      session.flush()

    session.commit()
  except Exception:
    abort(400)

  return bill_get(bill.id)
