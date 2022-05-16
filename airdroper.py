import fontstyle
import json
import requests
import time
import datetime
from stellar_sdk import *

# Define Stellar environment variables
master_public_key = "GDBBYISVGXL4CWVBRNSBIHDC6RCQ37NWUVFWI4F7M5LBW2QSB4JYWGYH"
master_secret_key = "SCQ6IX7GEKRIAU46PWRP3WZGFJG346XW7GG5JOAP4XYKPLA4KPIIOYWH"

test_public_key = "GBXROJ22FE2NGS7DMG76RMVMY2B5HRYTONO3RH4C55NMPOEB3F5L45DX"

source_secret_key = master_secret_key
source_keypair = Keypair.from_secret(source_secret_key)
source_public_key = source_keypair.public_key

receiver_public_key = test_public_key

server = Server(horizon_url="https://horizon-testnet.stellar.org")

source_account = server.load_account(source_public_key)

base_fee = 100


# Defines welcome text and initializes main menu
def welcome():
    welcome_text = fontstyle.apply("Welcome to Tellus' Airdrop v.0.2\n", 'BOLD/purple/CYAN_BG')
    print(welcome_text)
    run_quiz(questions)

# Airdrop function
def airdrop():
    airdrop_key = input("Enter Public Key: ").upper()
    print(airdrop_key)
    check_address = input("\nIs this correct? Y/N :").upper()
    if check_address == "Y":
        print("\nPublic Key entered successfully\n")

        # Inputs for hours, minutes, seconds on timer
        h = input("Enter the time in hours: ")
        m = input("Enter the time in minutes: ")
        s = input("Enter the time in seconds: ")
        print("\nAirdrop scheduled successfully!")
        countdown(int(h), int(m), int(s))

    elif check_address:
        airdrop()


# Create class that acts as a countdown
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

    print("\nBzzzt! Airdrop Executed")
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


# Generate Random Keypair and fund account in testnet
def create_account():
    keypair = Keypair.random()

    print("Keypair generated successfully\n")
    print("Public: ", keypair.public_key)
    print("Secret: ", keypair.secret)

    url = "https://friendbot.stellar.org"
    response = requests.get(url, params={"addr": keypair.public_key})
    print("\nServer:\n", response)


# Main menu Class
class MenuQuestion:
    def __init__(self, prompt):
        self.prompt = prompt


question_prompts = [
    "Main Menu:\n(A) Create new account\n(B) Create new vault\n(C) Schedule Airdrop\n",
]
questions = [
    MenuQuestion(question_prompts[0]),
]



# Main menu function
def run_quiz(questions):
    for question in questions:
        answer = input(question.prompt).upper()
        if answer == "A":
            return create_account()
        if answer == "B":
            print("b selected")
        if answer == "C":
            airdrop()
    back_to_menu = input("\nGo back to Main Menu? Y/N\n").upper()
    if back_to_menu == "Y":
        run_quiz(questions)
    elif back_to_menu:
        pass


welcome()
