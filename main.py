import fontstyle
import json
import requests
import time
import datetime
from stellar_sdk import *


def welcome():
    welcome_text = fontstyle.apply("Welcome to Tellus' Airdrop v.0.3.1\n", 'BOLD/purple/CYAN_BG')
    print(welcome_text)
    main_menu()


def main_menu():
    print("Main Menu\n (A) Schedule Airdrop\n (B) Create test account\n (C) Create test Cooperative Vault")
    answer = input().upper()
    if answer == "A":
        payment()
    if answer == "B":
        main_menu()
    if answer == "C":
        create_coop()
    else:
        create_account()


def back_to_menu():
    answer = input("\nGo back to Main Menu? Y/N\n").upper()
    if answer == "Y":
        welcome()
    elif answer:
        pass


def create_account():
    keypair = Keypair.random()

    print("🔐 Keypair generated successfully\n")
    print("Public: ", keypair.public_key)
    print("Secret: ", keypair.secret)

    url = "https://friendbot.stellar.org"
    response = requests.get(url, params={"addr": keypair.public_key})
    print("\nServer:\n", response)
    back_to_menu()


def create_coop():
    keypair = Keypair.random()

    print("🤝 Cooperative Vault generated successfully\n")

    print("Public: ", keypair.public_key)
    print("Secret: ", keypair.secret)

    url = "https://friendbot.stellar.org"
    response = requests.get(url, params={"addr": keypair.public_key})
    print("\nServer:\n", response)

    server = Server(horizon_url="https://horizon-testnet.stellar.org")
    root_keypair = Keypair.from_secret(keypair.secret)

    root_account = server.load_account(account_id=root_keypair.public_key)

    secondary_signer = Signer.ed25519_public_key(account_id=input("🔑 Add new signer's Public Key: ").upper(), weight=1
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
    back_to_menu()


def countdown(h, m, s):
    # Calculate the total number of seconds
    total_seconds = h * 3600 + m * 60 + s

    # While loop that checks if total_seconds reaches zero
    # If not zero, decrement total time by one second
    while total_seconds > 0:
        # Timer represents time left on countdown
        timer = datetime.timedelta(seconds=total_seconds)

        # Prints the time left on the timer
        print(timer, end="\r")

        # Delays the program one second
        time.sleep(1)

        # Reduces total time by one second
        total_seconds -= 1

    print("\n ✈️ Airdrop executed")


def payment():
    source_secret_key = "SBZPHIQI4GRLVLUAGEFW4U5RXDGSDG6HM4TN677GHTENCS6IQNSB33C2"
    source_keypair = Keypair.from_secret(source_secret_key)
    source_public_key = source_keypair.public_key

    receiver_public_key = input("Enter Public Key: ").upper()
    print(receiver_public_key)
    check_address = input("\nIs this correct? Y/N :").upper()
    if check_address == "Y":
        print("\nPublic Key entered successfully\n")
        h = input("Enter the time in hours: ")
        m = input("Enter the time in minutes: ")
        s = input("Enter the time in seconds: ")
        print("\nAirdrop scheduled successfully! ⏰")
        countdown(int(h), int(m), int(s))

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
    print("💸 Transaction Completed!")
    back_to_menu()


welcome()
