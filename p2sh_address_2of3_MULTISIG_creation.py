#MIT License

#Copyright (c) 2018-2020 The python-bitcoin-utils developers
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

from bitcoinutils.setup import setup
from bitcoinutils.proxy import NodeProxy
from bitcoinutils.setup import setup
from bitcoinutils.utils import to_satoshis
from bitcoinutils.transactions import Transaction, TxInput, TxOutput
from bitcoinutils.keys import PublicKey, Address, P2pkhAddress,P2shAddress, PrivateKey
from bitcoinutils.script import Script
from bitcoinutils.constants import SIGHASH_ALL, SIGHASH_NONE, SIGHASH_SINGLE, SIGHASH_ANYONECANPAY

# This script creates a P2SH Bitcoin address that implements MULTISIG scheme,
# where 2 out of 3 potential sigs are need to unlock the founds.

# Fot the implemention it is used the python-bitcoin-utils library.
# python-bitcoin-utils has a MIT License.

def main():

    # Network setup in testnet
    setup('testnet')

    #--------------------------------------------------------------------
    print("\nWellcome! \n\nThis script creates a 2 of 3 P2SH MULTISIG testnet address with three P2PKH testnet public keys.\nTo start, please introduce three valid testnet PublicKeys.\nNote: For the execution of some commands, we are using Bitcoin node, make sure that you have configure your rpc user and password correctly in the script code before its execution.")
    
    #-------------------------------------------------
    #Before starting, you have to configure the proxy rpc user and the password, that values are in your .config file of your node instalation. 
    print("\nBefore starting, it is necessary to configure the node proxy")
    admin = input("\nPlease, introduce yout rpc user: ")
    adminkey = input("\nPlease, introduce your rpc user password: ")
    # Get a node proxy, need to replace "admin" for your rpc user and "adminkey" for your password
    proxy = NodeProxy(admin, adminkey).get_proxy()
    print("\nNow we are ready to start!")
    #--------------------------------------------------------------------
    # We ask for a PublicKey and we safe the input from the terminal in the variable input1
    input1 = input("\nPlease introduce the first testnet PublicKey for the MULTISIG:   ")

    # We convert the variable input1 (string) to a PublicKey object
    pubKey1 = PublicKey(input1)

    #--------------------------------------------------------------------
    # We check using "validateaddress" node's command with proxy the validity of introduced Public Key.
    # First we get the address from the public key object pubKey1.
    address1 = pubKey1.get_address()

    # Next, we called the proxy, with the command "validateaddress" and the address1 variable in an string format.
    add_valid = proxy.validateaddress(address1.to_string())

    # In case the PublicKey introduced is not valid, so the output from the previous call is False,
    # we use a while loop to ask again for a valid address until that requeriment it is fulfilet

    while add_valid["isvalid"] == False:
        print("\nThe PublicKey introduced was not valid, please introduce a valid PublicKey")
        input1 = input("Please introduce the first testnet PublicKey for the MULTISIG:   ")
        pubKey1 = PublicKey(input1)
        address1 = pubKey1.getaddress()
        add_valid1 = proxy.validateaddress(address1.to_string())
    print("\nValid testnet Public Key introduced", "First Address used to create the MULTISIG: ", address1.to_string())

    #---------------------------------------------------------------------
    #We repeat the same process for the second PublicKey.
    input2 = input("\nPlease introduce the second testnet PublicKey for the MULTISIG:   ")
    pubKey2 = PublicKey(input2)
    address2 = pubKey2.get_address()
    add_valid = proxy.validateaddress(address2.to_string())
    #In second while loop to check if the second public key is valid, it is also check if the pecond public key is different than the first public key.
    while (add_valid["isvalid"]== False) or (address2 == address1):
        print("\nThe PublicKey introduced was not valid or was the same as the first public key introduced, please introduce a valid PublicKey")
        input2 = input("Please introduce the second testnet PublicKey for the MULTISIG:   ")
        pubKey2 = PublicKey(input2)
        address2 = pubKey2.getaddress()
        add_valid2 = proxy.validateaddress(address2.to_string())
    print("\nValid testnet Public Key introduced", "Second Address used to create the MULTISIG: ", address2.to_string())

    #----------------------------------------------------------------------
    #We repeat the same process for the third PublicKey.
    input3 = input("\nPlease introduce the third testnet PublicKey for the MULTISIG:   ")
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

    #-------------------------------------------------------------------------
    #Now with the three addresses from the three public keys introduced, it is created the redeem script that locks the address's funds. 
    redeem_script = Script(['OP_2', address1.to_hash160(), address2.to_hash160(), address3.to_hash160(),'OP_3','OP_CHECKMULTISIG'])
    #With the redeem script, it is created the P2SH address with the P2shAddress class. 
    addr_sh = P2shAddress.from_script(redeem_script)
    print("\n\nYour Multisig testnet address has been created with success!\nThe P2SH address is: ",addr_sh.to_string(),"\n")

if __name__ == "__main__":
    main()
