import settings as st
import wallet
import blockchain as bch
import transaction as trans
import Crypto
from Crypto.PublicKey import RSA

wall_list=[]


if (st.my_id==0):
    for i in range (st.n):
        rsa_key = RSA.generate(1024)
        privkey = rsa_key.exportKey('PEM').decode()
        pubkey = rsa_key.publickey().exportKey('PEM').decode()
        if (i == 0):
            w = wallet.Wallet(privkey, pubkey, [{'id': 0,
                'to_who': pubkey,
                'amount': 100*st.n
                }])
        else:
            w = wallet.Wallet(privkey, pubkey, [])
        st.wallets.append(w)
    #start_chain = bch.Blockchain.genesis_chain(wallets)
    print(f"Your balance is {st.wallets[0].utxos[0]['amount']} coins")
    for wall in st.wallets:
        wall_list.append(vars(wall))
    for k in range (1, st.n):
        st.send(wall_list, 'wallet/all', st.ips[k])

    temp_t = trans.create_transaction(st.wallets[0], st.wallets[1].public_key, 50)
    for i in range (1, st.n):
        print(st.send(vars(temp_t), 'transaction/get', st.ips[i]))
'''
else:
    rsa_key = RSA.generate(1024)
    privkey = rsa_key.exportKey('PEM').decode()
    pubkey = rsa_key.publickey().exportKey('PEM').decode()
    my_w = wallet.Wallet(privkey, pubkey, [])    # pass id into utxos list, so that bootsrap node knows who you are
    temp_dict = vars(my_w)
    temp_dict['node_id'] = st.my_id
    print (st.send(temp_dict, "wallet/get", st.ips[0]))
'''
