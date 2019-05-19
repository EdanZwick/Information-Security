from q1 import RepeatedKeyCipher
from q1 import BreakerAssistant


def main():

	ci = RepeatedKeyCipher([98,78,34,99,11,23,4,250,1,17,89,32,124,1,126,98,45,12,18,76,11,20,43,126,167,187,21])
	tmp = ci.encrypt(" hello is bla bla it me you'r looking for? can you look out the door and see z If a sequence contains an expression list, it is evaluated first. It has the ability to iterate over the items of any sequence, such as a list or a string. Then, the first item in the sequence is assigned to the iterating variable iterating_var. Next, the statements block is executed. Each item in the list is assigned to iterating_var, and the statement(s) block is executed until the entire sequence is exhausted.")
	print tmp
	
	b = BreakerAssistant()
	tmp = b.smarter_break(tmp, 27)
	print tmp
	return
	




if __name__ == "__main__":
	main()