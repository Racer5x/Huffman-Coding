import sys
import ast
from tkinter import *

def break_code(send_code, table, child, parent):
	#now this functions decipher the code
	node = parent
	code = ""

	for c in send_code:
		if c == '0':
			node = child[node][0]
		else:
			node = child[node][1]

		if child[node][0] == -1:
			code += table[node]
			node = parent
		
	return code

with open(sys.argv[1]) as file:
	send_code = file.read()

with open(sys.argv[2]) as file:
	table = ast.literal_eval(file.read())

with open(sys.argv[3]) as file:
	child = ast.literal_eval(file.read())

with open(sys.argv[4]) as file:
	parent = int(file.read())

message = break_code(send_code, table, child, parent)

root = Tk()
root.title("break_code")
root.geometry("400x100")

Label(root, text=send_code).pack()
Label(root, text=message).pack()

Button(root, text="exit", command=root.destroy).pack()

mainloop()