import settings
import wallet
import blockchain as bch
import Crypto
from Crypto.PublicKey import RSA


if (settings.my_id==0):
    wallets = []
    rsa_key = RSA.generate(1024)
    privkey = rsa_key.exportKey('PEM').decode()
    pubkey = rsa_key.publickey().exportKey('PEM').decode()
    w = wallet.Wallet(privkey, pubkey, [])
    wallets.append(w)
    start_chain = bch.Blockchain.genesis_chain(wallets)
    print(wallets[0].utxos['amount'])
# else:
    # w = Wallet()
