import settings as st
import wallet
import blockchain as bch
import Crypto
from Crypto.PublicKey import RSA

wall_list=[]

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
    my_w = wallet.Wallet(privkey, pubkey, [])    # pass id into utxos list, so that bootsrap node knows who you are
    temp_dict = vars(my_w)
    temp_dict['node_id'] = st.my_id
    print (st.send(temp_dict, "wallet/get", st.ips[0]))
    
