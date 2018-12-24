import datetime
import json

import requests
from flask import render_template, redirect, request

from app import app

# Define value of Candycoin
cc = 0.25 # 1CandyCoin can buy 4 candies


#Define client and shop class
class Client:
    def __init__(self, name, balance, credit):
        self.name = name
        self.balance = balance
        self.credit = credit

class Shop:
    def __init__(self, name, balance, credit):
        self.name = name
        self.balance = balance
        self.credit = credit


# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

posts = []


def fetch_posts():
    #Fetch the chain from a blockchain node, parse data and store locally
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)

# Define client object and create a list of clients
clients = []

uter = Client(name="Uter", balance=100, credit=0)
milhouse = Client(name="Milhouse", balance=65, credit=0)
homer = Client(name="Homer", balance=230, credit=0)
winchester = Client(name="Winchester", balance=340, credit=0)
shop = Shop(name="Candy Shop", balance=3000, credit=5000)

clients.append(uter)
clients.append(milhouse)
clients.append(homer)
clients.append(winchester)
clients.append(shop)

def add_clients():

    return clients

@app.route('/')
def index():
    fetch_posts()
    add_clients()
    return render_template('index.html',
                           title='Blockchain Candy Shop',
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string,
                           clients=clients,)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    #Endpoint to create a new transaction
    payer = request.form["payer"]
    payee = request.form["payee"]
    amount = request.form["amount"]
    re = request.form["re"]

    post_object = {
        'payer': payer,
        'payee': payee,
        'amount': amount,
        're': re,
    }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
