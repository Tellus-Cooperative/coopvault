import fontstyle
import json
import requests
import time
import datetime
from stellar_sdk import *

# Imports setup file with account information
import setup


def welcome():

    welcome_text = fontstyle.apply("Welcome to Tellus' Airdrop v.0.3.1\n", 'BOLD/purple/CYAN_BG')
    print(welcome_text)
    main_menu()


def main_menu():
    print("Main Menu\n (A) Schedule Airdrop\n (B) Create test account\n (C) Create test Cooperative Vault\n (D) New Cooperative Asset")
    answer = input().upper()
    if answer == "A":
        payment()
    if answer == "B":
        create_account()
    if answer == "C":
        create_coop()
    if answer == "D":
        coop_asset()
    else:
        main_menu()


def back_to_menu():
    answer = input("\nGo back to Main Menu? Y/N\n").upper()
    if answer == "Y":
        welcome()
    else:
        quit()


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

def coop_asset():
    server = Server(horizon_url="https://horizon-testnet.stellar.org")

    # Keys for accounts to issue and receive the new asset
    issuing_keypair = Keypair.from_secret(
        "SBZW7VWGVK5DJGKL42IHN6YLOEM6WYHC3YM3FLRIIJO7YFX6UVDRLLS2"
    )
    issuing_public = issuing_keypair.public_key

    distributor_keypair = Keypair.from_secret(
        "SAMISJ7KMPDI62U2L4NXPAAWKF6AOJIOZ7BDE5WEQUVPLQOCFRBQJWZA"
    )
    distributor_public = distributor_keypair.public_key

    # Transactions require a valid sequence number that is specific to this account.
    # We can fetch the current sequence number for the source account from Horizon.
    distributor_account = server.load_account(distributor_public)

    # Create an object to represent the new asset
    coop_asset = Asset("COOPXTEST2", issuing_public)

    # First, the receiving account must trust the asset
    trust_transaction = (
        TransactionBuilder(
            source_account=distributor_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
            .append_change_trust_op(asset=coop_asset)
            .set_timeout(30)
            .build()
    )

    trust_transaction.sign(distributor_keypair)
    resp = server.submit_transaction(trust_transaction)
    print(f"Change Trust Op Resp:\n{resp}")
    print("-" * 32)

    issuing_account = server.load_account(issuing_public)
    # Second, the issuing account actually sends a payment using the asset.
    # We recommend that you use the distribution account to distribute assets and
    # add more security measures to the issue account. Other acceptances should also
    # add a trust line to accept assets like the distribution account.
    payment_transaction = (
        TransactionBuilder(
            source_account=issuing_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
            .append_payment_op(destination=distributor_public, amount="420", asset=coop_asset)
            .set_timeout(30)
            .build()
    )
    payment_transaction.sign(issuing_keypair)
    resp = server.submit_transaction(payment_transaction)
    print(f"Payment Op Resp:\n{resp}")
    back_to_menu()


welcome()
