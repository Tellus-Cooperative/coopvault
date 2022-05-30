from stellar_sdk.asset import Asset
from stellar_sdk.keypair import Keypair
from stellar_sdk.network import Network
from stellar_sdk.server import Server
from stellar_sdk.transaction_builder import TransactionBuilder

server = Server(horizon_url="https://horizon-testnet.stellar.org")

issuing_keypair = Keypair.from_secret(
    "SBZW7VWGVK5DJGKL42IHN6YLOEM6WYHC3YM3FLRIIJO7YFX6UVDRLLS2"
)
issuing_public = issuing_keypair.public_key

distributor_keypair = Keypair.from_secret(
    "SAMISJ7KMPDI62U2L4NXPAAWKF6AOJIOZ7BDE5WEQUVPLQOCFRBQJWZA"
)
distributor_public = distributor_keypair.public_key

distributor_account = server.load_account(distributor_public)

coop_asset = Asset("COOPXTEST", issuing_public)

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