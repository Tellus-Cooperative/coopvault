import json
from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder


def create_account():
    import requests

    from stellar_sdk import Keypair

    keypair = Keypair.random()
    url = "https://friendbot.stellar.org"
    _response = requests.get(url, params={"addr": keypair.public_key})
    return keypair


example_keypair = create_account()
source_secret_key = example_keypair.secret
source_keypair = Keypair.from_secret(source_secret_key)
source_public_key = source_keypair.public_key

receiver_public_key = example_keypair.public_key

server = Server(horizon_url="https://horizon-testnet.stellar.org")

source_account = server.load_account(source_public_key)

base_fee = 100

transaction = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
        .add_text_memo("TEST PAYMENT")

        .append_payment_op(receiver_public_key, Asset.native(), "350.1234567")
        .set_timeout(30)
        .build()
)

transaction.sign(source_keypair)

print(transaction.to_xdr())

response = server.submit_transaction(transaction)
print(json.dumps(response, indent=4))
