#!/usr/bin/python3

# WARNING: This file (and honestly all my pdf generator) is super hacky/messy
#          and I don't really care. I did this a while ago and it still works,
#          I'll remake it if I ever need to. And since it's a personnal project
#          nobody can tell me what to do 😈

import psycopg2
import yaml
import os
import sys
import functools
import operator
import psycopg2.extras

from urllib.parse import urlparse

if len(sys.argv) < 2:
    sys.exit(-1)

id = sys.argv[1]

def add_space_every(string, every):
    return ' '.join([string[i:i+every] for i in range(0, len(string), every)])

result = urlparse(os.getenv('DB_URL'))

username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

conn = psycopg2.connect(
    database = database,
    user = username,
    password = password,
    host = hostname
)
cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

cur.execute("""
SELECT
    bills.id as id,
    bills.number as number,
    bills.date as date,
    senders.name as sender_name,
    senders.address_part_1 as sender_address_part_1,
    senders.address_part_2 as sender_address_part_2,
    senders.phone as sender_phone,
    senders.email as sender_email,
    senders.siren as sender_siren,
    receivers.name as receiver_name,
    receivers.address_part_1 as receiver_address_part_1,
    receivers.address_part_2 as receiver_address_part_2,
    senders.bank_details_name as sender_bank_details_name,
    senders.bank_details_bank as sender_bank_details_bank,
    senders.bank_details_iban as sender_bank_details_iban,
    senders.bank_details_bic as sender_bank_details_bic
FROM
    bills_with_number AS bills
    JOIN senders
        ON senders.id = bills.sender_id
    JOIN receivers
        ON receivers.id = bills.receiver_id
WHERE
    bills.id = %s""", (id,))

res = dict(cur.fetchone())

bill = {
    'number': res['number'],
    'date': res['date'].strftime("%d/%m/%Y"),
    'sender': {
        'name': res['sender_name'],
        'address_part_1': res['sender_address_part_1'],
        'address_part_2': res['sender_address_part_2'],
        'phone': res['sender_phone'],
        'email': res['sender_email'],
        'siren': add_space_every(res['sender_siren'], 3),
    },
    'receiver': {
        'name': res['receiver_name'],
        'address_part_1': res['receiver_address_part_1'],
        'address_part_2': res['receiver_address_part_2'],
    },
    'bank_details': {
        'name': res['sender_bank_details_name'],
        'bank': res['sender_bank_details_bank'],
        'iban': add_space_every(res['sender_bank_details_iban'], 4),
        'bic': res['sender_bank_details_bic'],
    }
}

cur.execute("""
SELECT * FROM
    products
WHERE
    bill_id = %s""", (id,))

bill['products'] = [{
    'quantity': row['quantity'],
    'description': row['description'],
    'unitary_price': str(row['unitary_price']),
    'total_price': str(row['unitary_price'] * row['quantity'])
    } for row in cur.fetchall()]

bill['total_price'] = "{0:.2f}".format(functools.reduce(operator.add, [float(elem['total_price']) for elem in bill['products']]))

print(yaml.dump(bill, allow_unicode=True))

cur.close()
conn.close()

