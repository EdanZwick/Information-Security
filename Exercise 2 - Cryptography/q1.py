import copy

class RepeatedKeyCipher(object):

    def __init__(self, key=[0, 0, 0, 0, 0]):
        """Initializes the object with a list of integers between 0 and 255."""
        assert all(0 <= k <= 255 and isinstance(k, (int, long)) for k in key)
        self.key = key

    def encrypt(self, plaintext):
        """Encrypts a given plaintext string and returns the ciphertext."""
        # Return a string, NOT an array of integers.
        n = len(self.key)
        i = 0
        ret = ""
        for x in plaintext:
        	ret += chr((ord(x)^self.key[i%n]))
        	i+=1
        return ret
        raise NotImplementedError()

    def decrypt(self, ciphertext):
        """Decrypts a given ciphertext string and returns the plaintext."""
        # Return a string, NOT an array of integers.
        return (self.encrypt(ciphertext)) #decrypt and encrypt are symmetrical, they both preform the same function
        raise NotImplementedError()


class BreakerAssistant(object):

    def plaintext_score(self, plaintext):
        """Scores a candidate plaintext string, higher means more likely."""
        # Return a number (int / long / float).
        # Please don't return complex numbers, that would be just annoying.
        n = len(plaintext)
        score = 0
        for x in plaintext:
        	if x==' ' or (x>='A' and x<='Z') or (x>='a' and x<='z'):
        		score +=1 #we expect the plaintext to contain english words
        	else:
        		score -=1 
        	if (ord(x)>128): #while the text might contain some punctuation, ascii signs above 128 are really un common
        		score -=5
        return score
        raise NotImplementedError()

    def brute_force(self, cipher_text, key_length):
        """Breaks a Repeated Key Cipher by brute-forcing all keys."""
        # Return a string.
        key = [0] * key_length #we will keep incrementing this key by 1 untill we went over all options for the key and examine which produced the highest scoring text 
        candidate = [0] * key_length
        finish = False
        max = -float('inf')
        while (finish == False):
			ci = RepeatedKeyCipher(key)
			val = self.plaintext_score(ci.decrypt(cipher_text))
			if (val>max): #this key produced a better solution than seen before
				max = val
				candidate = copy.deepcopy(key)
			i = 0
			key[0] += 1 #this line and while loop that follows is used to legaly increment key by 1 (without having any value out of legal range for key)
			while (key[i] == 256): #overflow occured in byte number i of the key. we deal with it by incrementing next byte by 1 and clearing current byte
				i+=1
				if (i == (key_length)): #we went over all keys (an overflow occured on the last byte)
					finish = True
					break
				key[i-1] = 0
				key[i] += 1
        ci = RepeatedKeyCipher(candidate)
        return (ci.decrypt(cipher_text)) #return the text that recieved the highest score
        raise NotImplementedError()

    def smarter_break(self, cipher_text, key_length):
    	"""Breaks a Repeated Key Cipher any way you like."""
    	# Return a string.
    	key = [0] * key_length #initialize an empty key
    	for i in range(0,key_length): #find key elements one by one
    		tmp = "" #tmp will hold a string of all chars encrypted with i's char of key
    		k = i
    		while k<len(cipher_text): #add all letters encrypted with key[i] to tmp
    			tmp += cipher_text[k]
    			k += key_length
    		max = -float('inf')
    		cand = 0
    		for j in xrange(0,256): #using previous ranking function, find most likely value for key[i]
    			ci = RepeatedKeyCipher([j])
    			val = self.plaintext_score(ci.decrypt(tmp))
    			if (val>max): #this key produced a better solution than seen before
    				max = val
    				cand = j
    		key[i] = cand #assign the most likely value to key[i]
    	ci = RepeatedKeyCipher(key) #return decrypted text
    	return ci.decrypt(cipher_text)

        raise NotImplementedError()
