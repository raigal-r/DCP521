#Instructions to run the scripts. 

#First of all, to execute the scripts, is necessary to have installed in your machine the Bitcoin node and be capable to run the node, and executing bitcoin-cli commands. 
#Also, if the bitcoin node has been installed manually, you will have to create a bitcoin.conf document in the root of .bitcoin, since in the current actualization it is not created automatically. 

#The bitcoin.conf document looks like this: 

	testnet=1
	blocksonly=1
	rpcport=5000
	server=1
	listen=0
	prune=1000 # this has no effect during syncing
	dbcache=16000 # will take too much memory
	rpcallowip=0.0.0.0/0
	rpcuser=admin #You will use the rpcuser later, the value should be modified for a username of your choice
	rpcpassword=adminkey #You will use the rpcpassword later, the value should be modified for your password
	
#If the prerequisites are fulfilled, it is possible to proceed to execute both scripts. 

#First of all would be necessary to include the scripts in your Python environment. And run them from there, or know the path to the scripts. 

#To enter the environment: 
source session3_env/bin/activate
(session3_env) raquel@raquel-GS65-Stealth-8SE:~$ source session3_env/bin/activate


#Once in the python session, we can execute the first script: carrasco_raquel_script.py
#That script will ask for three Public Keys. That would be needed to be included through the terminal. 

#The Addresses used for the creation, and test of that exercises are the following, but notice that you can use any compressed PublicKeys (knowing the PrivateKeys for the following script and being capable to unlock the P2SH address after) that you desire. 

#Addresses used: 

#Private key WIF: cT4LJaQaH8UC2qzTiysdMJp3ChjPZiJu5C79TDq1Q4hJ67RgPtut
#Public key: 0221b5c682c4585b74b8539e61044ab0f56dba42dc97ca9d8960ba085e34273b05
#Address: n28Etyq8nL1RY1TZbAhtQaGNFhNMiUg4ra


#Private key WIF: cRA7mS1tX54ehuu3tPCm7tm5pEvAvd1wm2v7VTYKYhFn9MbhmAiT
#Public key: 034d8ec98f5852b982131b017f6fda636e9b9de201465685e5d2b9fe137fd48a56
#Address: mi1QwpijVWpuQYe4GJ5wcsRKAsSfEz9Byc


#Private key WIF: cNj3sb9wJf1ZJPjiyHrA5QCjPjDzSDHwNgLUkn7qZYA3fHiToc42
#Public key: 03bf0998251451dcc744c22817b6c0be1046e903b3e0df4ab0beea704feb55de2c
#Address: mi5we5T1DEHQErvFf6gEWKjHKjDSvJ52gb

#---------------------------------------------------------
#Now execute the first script with the python command:

	(session3_env) ~$ python carrasco_raquel_script1.py

#It will ask first for your rpcuser: 
	Please, introduce your rpc user: "admin" #I introduced admin, since it is my rpcuser, but you have to introduce your rpcuser.
#And, you will also need to introduce your rpc password
	Please, introduce your rpc user password: "adminkey" #I introduced adminkey, since it is my password, but you have to introduce your rpcuser.

#Following will ask for three Public Keys, if any of the Public Keys introduced is not valid, or it is the same as one of the Keys already introduced, it will request to introduce a valid or different Public Key again. 
	Please introduce the first testnet PublicKey for the MULTISIG: "PubKey1"
	Please introduce the second testnet PublicKey for the MULTISIG: "PubKey2"
	Please introduce the third testnet PublicKey for the MULTISIG: "PubKey3"

#Once introduced the three Public Keys will return the P2SH address created. 
	The P2SH address is 2NCNaUnSZFKZdbPrzygR4TB8pcriNPdhw5p #That is the P2SH address used for testing the scripts, and the one that has been created with the PublicKeys and PrivatedKeys mentioned a few lines above. If other PubKeys are used, the value will be different. 

#-------------------------------------------------------------

#If the same address that is in this example is used, would be some UTXOs on the P2SH address, but it has been just created, would be necessary to send some bitcoins to the new P2SH address to have UTXOs to spend from.

#Now we can execute the second script with the python command:
  	(session3_env) ~$ python carrasco_raquel_script2.py	

#We will need to introduce again the rpcuser and the password. 
#After we will need to introduce the first two Private Keys and one PublicKey, which corresponds with the three PublicKeys used to create the P2SH address. It will check again if are valid, and none of them is repeated. 

	Please introduce the first testnet PrivateKey for the MULTISIG:   "PrivateKey1"
	Please introduce the second testnet PrivateKey for the MULTISIG:   "PrivateKey2"
	Please introduce the testnet PublicKey for the MULTISIG:  "PublicKey"

#Next will ask for the P2SH address from which we want to spend the funds, and that it is unlocked with the PivateKeys provided: 

	Please introduce the P2SH address that is unlocked with the private and public Keys provided: "P2SH address"
	
#Next, will ask for the P2PKH address where the funds are going to be sent. 

	Please introduce a valid P2PKH address where the funds from the P2SH address have to be sent: "P2PKH address"
	
#Finally the script will display the: 
	#Raw unsigned transaction, RawTxID
	#Raw signed transaction
	#Raw signed transaction id, TxId 
	
	RawTxId:  0200000003306e718ead0e2cf5d38e273f5ce0447e...#Quite long, it has been cut for the example. 
	
	Raw signed transaction: 0200000003306e718ead0e2cf5d38e273f5ce044 ... #Quite long, it has been cut for the example. 

	TxId:  864954ec432d6bd443cc47de1922b1b4a88651aedea03281a3e70dae8b503718

	
#And, if the transaction is valid, what will be checked, it will be broadcasted to the node to be sent. No further action will be required, and the transaction can be checked in a testnet block explorer with the raw signed transaction id. 
