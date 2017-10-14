# If user needs to be paid, find private key of admin in state.
# Go to bitcoin, make transaction between the addresses. 
# Push to blockchain
# chain and state to be sent as parameters

import User
import hashlib, json, sys

def createGenesisBlock(state):
	genesisBlockTxns = [state]
	genesisBlockContents = {u'blockNumber':0, u'parentHash':None, u'txns':genesisBlockTxns}
	genesisHash = hashMe(genesisBlockContents)
	genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)
	chain.append(genesisBlockStr)
	return state

def addAdminUser(admin, state):
	updateState({hashMe(admin), 1000}, state)
	return state

def addUser(user, state):
	updateState({hashMe(user), 0}, state)
	return state

# admin pays UserObj the amt
def adminPayment(UserObj, amt, count, AdminObj, state):
	makeBlock({hashMe(UserObj): amt, hashMe(AdminObj): -amt})
	updateState({hashMe(UserObj): amt, hashMe(AdminObj): -amt}, state)
	return state

def hashMe(UserObj):
	if type(msg)!=str:
		msg = json.dumps(msg, sort_keys=True)
	
	return unicode(hashlib.sha256(msg).hexdigest(),'utf-8')

def makeBlock(transaction):
	# attributes are blocknumber, parenthash, transaction-list
	contents = json.loads(chain[-1])['contents']
	blockContents = {u'blockNumber':contents['blockNumber'], u'parentHash':contents['hash'], u'txns':[transaction]}
	blockHash = hashMe(blockContents)
	blockStr = json.dumps(genesisBlock, sort_keys=True)
	chain.append(blockStr)

def isValidTransaction(txn, state):
	if sum(txn.values()) is not 0:
		return False
	for key in txn.keys():
		if key in state.keys():
			acctBalance = state[key]
		else:
			acctBalance = 0
		if (acctBalance + txn[key]) < 0:
			return False
	return True

def checkBlockHash(block):
	expectedHash = hashMe( block['contents'] )
    if block['hash']!=expectedHash:
        raise Exception('Hash does not match contents of block %s'%
                        block['contents']['blockNumber'])
    return
def updateState(txn, state):
	state = state.copy()
	for key in txn:
		if key in state.keys():
			state[key]+=txn[key]
		else:
			state[key] = txn[key]
	return state

def checkBlockValidity(block, parent, state):
	parentNumber = parent['contents']['blockNumber']
    parentHash   = parent['hash']
    blockNumber  = block['contents']['blockNumber']
    for txn in block['contents']['txns']:
        if isValidTxn(txn,state):
            state = updateState(txn,state)
        else:
            raise Exception('Invalid transaction in block %s: %s'%(blockNumber,txn))
    checkBlockHash(block)
    if blockNumber!=(parentNumber+1):
        raise Exception('Hash does not match contents of block %s'%blockNumber)

    if block['contents']['parentHash'] != parentHash:
        raise Exception('Parent hash not accurate at block %s'%blockNumber)
    
    return state

def checkChain():
    if type(chain)==str:
        try:
            chain = json.loads(chain)
            assert(type(chain)==list)
        except:
            return False
    elif type(chain)!=list:
        return False
    
    state = {}

    for txn in chain[0]['contents']['txns']:
        state = updateState(txn,state)
    checkBlockHash(chain[0])
    parent = chain[0]
    for block in chain[1:]:
        state = checkBlockValidity(block,parent,state)
        parent = block
        
    return state
