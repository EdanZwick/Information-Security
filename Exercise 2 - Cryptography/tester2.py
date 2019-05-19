from q2 import extract_PIN, extract_credit_card, forge_signature
from q2_atm import ATM, ServerResponse
from Crypto.PublicKey import RSA

def main():
	a = ATM()
	r = ServerResponse(1,1)
	
	print (a.verify_server_approval(r))


if __name__ == "__main__":
	main()	