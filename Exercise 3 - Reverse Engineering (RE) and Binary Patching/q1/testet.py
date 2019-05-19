

def calcxor(s):
	sum = 47
	for x in s:
		sum = sum^ord(x)
	return sum

def main():
	s = "\"You're not a good artist, Adolf.\"\n"
	x = (calcxor(s))
	print (chr(len(s)))
	print (chr(x))
	return 1

if __name__ == "__main__":
	main() 