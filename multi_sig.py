from stellar_sdk import Asset, Keypair, Network, Server, Signer, TransactionBuilder
import json
import requests


def create_coop():
    keypair = Keypair.random()

    print("Keypair generated successfully\n")

    print("Public: ", keypair.public_key)
    print("Secret: ", keypair.secret)

    url = "https://friendbot.stellar.org"
    response = requests.get(url, params={"addr": keypair.public_key})
    print("\nServer:\n", response)

    server = Server(horizon_url="https://horizon-testnet.stellar.org")
    root_keypair = Keypair.from_secret(keypair.secret)

    root_account = server.load_account(account_id=root_keypair.public_key)

    """secondary_public_key = input("Enter Public Key: ").upper()
    """
    """secondary_keypair = Keypair.from_secret(
    "SAV2G4KFDGJJS7DNXTQDKVBZ2QKLBLU7UFIB4FZXZMKSDS53JIIEHGPC")"""

    secondary_signer = Signer.ed25519_public_key(account_id=input("Enter Public Key: ").upper(), weight=1
                                                 )

    transaction = (
        TransactionBuilder(
            source_account=root_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
            .append_set_options_op(
            master_weight=1,
            low_threshold=1,
            med_threshold=2,
            high_threshold=2,
            signer=secondary_signer,
        )
            .set_timeout(30)
            .build()
    )

    transaction.sign(root_keypair)
    response = server.submit_transaction(transaction)
    print(json.dumps(response, indent=4))

create_coop()