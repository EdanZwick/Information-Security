from q2_atm import ATM, ServerResponse


def extract_PIN(encrypted_PIN):
    """Extracts the original PIN string from an encrypted PIN."""
    # Return an integer.
    for i in range(0,10000): #i is all possible pin options (as it is four digits)
    	a = ATM()
    	x = a.encrypt_PIN(i)
    	if x == encrypted_PIN: 
    		return i #this pin yielded the exact pin as one we intercepted
    raise NotImplementedError()


def extract_credit_card(encrypted_credit_card):
    """Extracts a credit card number string from its ciphertext."""
    # Return an integer.
    return int(round(encrypted_credit_card ** (1./3))) 
    raise NotImplementedError()


def forge_signature():
    """Forge a server response that passes verification."""
    # Return a ServerResponse instance.
    return ServerResponse(1,1)
    raise NotImplementedError()
