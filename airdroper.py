import fontstyle
import json
import requests
import time
import datetime
from stellar_sdk import *


def welcome():
    welcome_text = fontstyle.apply("Welcome to Tellus' Airdrop v.0.2\n", 'BOLD/purple/CYAN_BG')
    print(welcome_text)
    main_menu()


def main_menu():
    print("Main Menu\n (A) Schedule Airdrop\n (B) Else")
    answer = input().upper()
    if answer == "A":
        payment()
    elif answer == "B":
        pass


def payment():
    source_secret_key = "SBZPHIQI4GRLVLUAGEFW4U5RXDGSDG6HM4TN677GHTENCS6IQNSB33C2"
    source_keypair = Keypair.from_secret(source_secret_key)
    source_public_key = source_keypair.public_key

    receiver_public_key = input("Enter Public Key: ").upper()
    print(receiver_public_key)
    check_address = input("\nIs this correct? Y/N :").upper()
    if check_address == "Y":
        print("\nPublic Key entered successfully\n")

    server = Server(horizon_url="https://horizon-testnet.stellar.org")

    source_account = server.load_account(source_public_key)

    base_fee = 100

    transaction = (
        TransactionBuilder(
            source_account=source_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        )
            .add_text_memo("Tellus Test Airdrop")
            .append_payment_op(receiver_public_key, Asset.native(), "69.420")
            .set_timeout(30)
            .build()
    )

    transaction.sign(source_keypair)

    print("XDR:")
    print(transaction.to_xdr())

    response = server.submit_transaction(transaction)
    print(json.dumps(response, indent=4))


welcome()
