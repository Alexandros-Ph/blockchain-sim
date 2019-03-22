import settings as st
import wallet
import blockchain as bch
import Crypto
from Crypto.PublicKey import RSA


if (st.my_id==0):
    wallets = []
    rsa_key = RSA.generate(1024)
    privkey = rsa_key.exportKey('PEM').decode()
    pubkey = rsa_key.publickey().exportKey('PEM').decode()
    w = wallet.Wallet(privkey, pubkey, [])
    wallets.append(w)
    start_chain = bch.Blockchain.genesis_chain(wallets)
    print(f"Your balance is {wallets[0].utxos[0]['amount']} coins")
else:
    rsa_key = RSA.generate(1024)
    privkey = rsa_key.exportKey('PEM').decode()
    pubkey = rsa_key.publickey().exportKey('PEM').decode()
    my_w = wallet.Wallet(privkey, pubkey, [st.my_id])    # pass id into utxos list, so that bootsrap node knows who you are
    print (send(my_w, "wallet/get", ips[0]))
