from bitcoinutils.setup import setup
from bitcoinutils.proxy import NodeProxy
from bitcoinutils.utils import to_satoshis
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, Sequence
from bitcoinutils.keys import P2pkhAddress, PrivateKey, PublicKey, Address, P2shAddress
from bitcoinutils.script import Script
from bitcoinutils.constants import SIGHASH_ALL, SIGHASH_NONE, SIGHASH_SINGLE, SIGHASH_ANYONECANPAY

def main():

    setup('testnet')
    print("\nWellcome! \n\nThis script spends all the found from a 2 of 3 P2SH MULTISIG testnet address using two PrivateKeys and one PublicKey.\nNote: For the execution of some commands, we are using Bitcoin node, make sure that you have configure your rpc user and password correctly in the script code before its execution.")

    #Before starting, you have to configured the proxy rpc user and the password, those values are in your bitcoin.config file of your node installation.
    print("\nBefore starting, it is necessary to configure the node proxy")
    admin = input("\nPlease, introduce your rpc user: ")
    adminkey = input("\nPlease, introduce your rpc user password: ")
    proxy = NodeProxy(admin, adminkey).get_proxy()
    print("\nNow we are ready to start!")

    #Private Keys necessary to sign the transaction
    #--------------------------------------------------------------------
    # We ask for a PrivateKey and we save the input from the terminal in the variable input1
    input1 = input("\nPlease introduce the first testnet PrivateKey for the MULTISIG signing:   ")
    # We convert the variable input1 (string) to a PrivateKey object, and we get the PublicKey and Address from the Private Key.
    privKey1 = PrivateKey(input1)
    pubKey1 = privKey1.get_public_key().to_hex()
    address1 = privKey1.get_public_key().get_address()
    #--------------------------------------------------------------------
    # We check using "validateaddress" node's command with proxy the validity of the introduced Private Key.

    # Next, we called the proxy, with the command "validateaddress" and the address1 variable in a string format.
    add_valid = proxy.validateaddress(address1.to_string())

    # In case the PrivateKey introduced is not valid, so the output from the previous call is False,
    # we use a while loop to ask again for a valid address until that requirement is fulfilled

    while add_valid["isvalid"] == False:
        print("\nThe PrivateKey introduced was not valid, please introduce a valid PrivateKey")
        input1 = input("Please introduce the first testnet PrivateKey for the MULTISIG:   ")
        privKey1 = PrivateKey(input1)
        pubKey1 = privKey1.get_public_key().to_hex()
        address1 = privKey1.get_public_key().get_address()
        add_valid1 = proxy.validateaddress(address1.to_string())
    print("\nValid testnet Private Key introduced", "First Address used to create the MULTISIG: ", address1.to_string())
    #--------------------------------------------------------------------
    # We ask for a PrivateKey and we save the input from the terminal in the variable input2
    input2 = input("\nPlease introduce the second testnet PrivateKey for the MULTISIG signing:   ")
    # We convert the variable input2 (string) to a PrivateKey object, and we get the PublicKey and Address from the Private Key. 
    privKey2 = PrivateKey(input2)
    pubKey2 = privKey2.get_public_key().to_hex()
    address2 = privKey2.get_public_key().get_address()
    #--------------------------------------------------------------------
    # We check using "validateaddress" node's command with proxy the validity of the introduced Private Key.

    # Next, we called the proxy, with the command "validateaddress" and the address2 variable in a string format.
    add_valid = proxy.validateaddress(address2.to_string())

    # In case the PrivateKey introduced is not valid, so the output from the previous call is False,
    # we use a while loop to ask again for a valid address until that requirement is fulfilled

    while (add_valid["isvalid"] == False) or (address2 == address1):
        print("\nThe PrivateKey introduced was not valid, please introduce a valid PrivateKey")
        input2 = input("Please introduce the second testnet PrivateKey for the MULTISIG:   ")
        privKey2 = PrivateKey(input2)
        pubKey2 = privKey2.get_public_key().to_hex()
        address2 = privKey2.get_public_key().get_address()
        add_valid2 = proxy.validateaddress(address2.to_string())
    print("\nValid testnet Private Key introduced", "Second Address used to create the MULTISIG: ", address2.to_string())
    #----------------------------------------------------------------------
    #We ask for the third Public Key that setup the P2SH address.
    input3 = input("\nPlease introduce the testnet PublicKey for the MULTISIG:   ")
    pubKey3 = PublicKey(input3)
    address3 = pubKey3.get_address()
    add_valid3 = proxy.validateaddress(address3.to_string())
    while (add_valid["isvalid"]== False) or (address3 == address2) or (address3 == address1):
        print("\nThe PublicKey introduced was not valid or was the same as the first or second public key introduced, please introduce a valid PublicKey")
        input3 = input("Please introduce the third testnet PublicKey for the MULTISIG:   ")
        pubKey3 = PublicKey(input3)
        address3 = pubKey3.getaddress()
        add_valid3 = proxy.validateaddress(address3.to_string())
    print("\nValid testnet Public Key introduced", "Third Address used to create the MULTISIG: ", address3.to_string())
    
    
    #We ask for the P2SH address created with the previous script
    print("Thank you for introducing the two privateKeys and one PublicKey.")
    input_p2sh = input("\nPlease introduce the P2SH address where you wish to spend all the funds inside and that it is unlocked with the private and public Keys provided.")
    #Now we check the UTXOs from the P2SH address with the node command scantxoutset
    #---------------------------------------------------------------------------------
    input_p2sh = input("Please introduce the P2SH address: ")
    utxo_info = proxy.scantxoutset('start', [{"desc":"addr("+input_p2sh+")"}])
    #From the previous command, we get a dictionary, we are interested in the variable "unspents"
    unspents_list = utxo_info["unspents"]
    #Since could be several unspent lists, we process the information and extract only the values we are interested in. Those are the txid of each UTXO, it's vout, and we also calculate the total amount from all the UTXOs
    amounts_array = []
    txin = []
    for x in unspents_list:
        #In the loop, when we are looking to extract the UTXOs, we already built a txin array, that includes all the transaction inputs. We save the variables as a TXInput object. 
        txin.append(TxInput(x["txid"], x["vout"]))
        amounts_array.append(x["amount"])
        amount_sum = 0
        #We sum all the UTXOs amounts
        for x in amounts_array:
            amount_sum += x
        print(amount_sum)

    #send/spend to a chosen address, needs to be an input
    input_addr = input("Please introduce a valid P2PKH address where the founds from the P2SH address have to be send: ")
    to_addr = P2pkhAddress(input_addr)
    #We create the transaction output, since we have not calculated the transaction fee yet, we introduce the whole amount of the UTXOs to be sent.
    txout = TxOutput(to_satoshis(amount_sum), to_addr.to_script_pub_key())


    #create the transaction from inputs/outputs. The variable txin, is already an array, so no need to put it in [], and include the list of TxInput(txid, vout).
    tx = Transaction(txin, [txout])

    #create the redeem script. Needs to be the same redeem script that was used to create the P2SH address. 
    redeem_script = Script(['OP_2', pubKey1, pubKey2, pubKey3.to_hex(),'OP_3','OP_CHECKMULTISIG'])

    #Now, we need to sign with both private keys, and all the UTXOs that we want to spend (all of them). To do it, we use a counter, that changes the txid that we are signing, until all are signed. 
    counter = 0
    for x in txin:
        #We sign with the two private keys every UTXO 
        sig1 = privKey1.sign_input(tx, counter, redeem_script)
        sig2 = privKey2.sign_input(tx, counter, redeem_script)
        txin[counter].script_sig = Script(['OP_0', sig1, sig2, redeem_script.to_hex()])
        counter += 1
        
    #set the scriptSig, it is the first rawSigned transaction
    signed_tx = tx.serialize()

    #Calculating the transaction fee, we use the node command estimatesmartfee, that returns the bitcoin/kB fee expected in the "feerate" variable 
    smartfee = proxy.estimatesmartfee(6)
    ratefee = smartfee["feerate"]
    #We use the node command decoderawtransaction to get the size of the signed raw transaction, which depends on its inputs and outputs. We get the size of the transaction in B. 
    decode_transaction = proxy.decoderawtransaction(signed_tx)
    transaction_size = decode_transaction["size"]
    #To get the fee value for our transaction, we multiply the fee rate (bitcoins/kB) x Transaction size (B) and divided it between 1000 (1kB/1000B) to get the fee value in bitcoins.
    fairfee = ratefee*transaction_size/1000
    #Finally we rest the fee to the UTXOs amount.
    max_amount_minus_fee = amount_sum - fairfee
    #To build the output, we use the UTXOs amount minus the fee, and we convert it to satoshis with to_satoshis(), also include the address provided where to send the funds. 
    txout = TxOutput(to_satoshis(max_amount_minus_fee), to_addr.to_script_pub_key())
    #create the transaction from inputs/outputs again since we have changed the txout.
    tx = Transaction(txin, [txout])
    #We print the raw unsigned transaction. 
    print("\n RawTxId: ", tx.serialize())

    #We repeat the signing process with the new tx. 
    counter = 0
    for x in txin:
        sig1 = privKey1.sign_input(tx, counter, redeem_script)
        sig2 = privKey2.sign_input(tx, counter, redeem_script)
        txin[counter].script_sig = Script(['OP_0', sig1, sig2, redeem_script.to_hex()])
        counter += 1
    
    signed_tx = tx.serialize()

    #print raw signed transaction ready to be broadcasted
    print("\nRaw signed transaction:\n" + signed_tx)
    print("\nTxId: ", tx.get_txid())

    #We verify with the node command testmempoolaccept if the transaction is valid. 
    mempool = proxy.testmempoolaccept([signed_tx])
    mempool0 = mempool[0]
    #If it is valid, broadcast the transaction.
    if mempool0["allowed"] == True:
        send_transaction = proxy.sendrawtransaction(signed_tx)

if __name__ == "__main__":
    main()
