import heapq as pq
import os
from tkinter import *
from tkinter import scrolledtext

def make_code(para):
	heap = []

	#finding the initial frequency of the characters present
	freq = {}
	for c in para:
		if c in freq:
			freq[c] += 1
		else:
			freq[c] = 1

	#now, making the initial priority queue
	node = 1
	table = {}
	rev_table = {}

	for c in freq:
		pq.heappush(heap, (freq[c], node))
		table[c] = node
		rev_table[node] = c
		node += 1

	#main algo, taking two elements from pq, and then merging them into new id and then that id goes back to pq again
	par = {}
	child = {}

	#to stop when leaf node is reached
	for point in rev_table:
		child[point] = (-1, point)

	while len(heap) > 1:
		fst = pq.heappop(heap)
		snd = pq.heappop(heap)

		#parent and their children
		par[fst[1]] = -node
		par[snd[1]] = node

		child[node] = (fst[1], snd[1])

		pq.heappush(heap, (fst[0] + snd[0], node))
		node += 1


	# to stop the iteration when root/parent(not par) is reached
	par[node - 1] = node - 1
	parent = node - 1 #this is root
	codes = {}
	
	# Iterating over all the frequencies
	for c in freq:
		code = ""
		node = table[c]

		while abs(par[node]) != node:
			node = par[node]
			if node < 0:
				code += "0"
			else:
				code += "1"
			node = abs(node)

		code = code[::-1]
		codes[c] = code

	send_code = ""

	for c in para:
		send_code += codes[c]

	#this is the final code and the required tree that is to be sent
	return send_code, rev_table, child, parent



root = Tk()
root.title("Send Code!")
root.geometry("400x600")


text_box = scrolledtext.ScrolledText(root, wrap = WORD, width = 40, height = 10)
text_box.pack()
text_box.focus()


def clicked():
	para = text_box.get(1.0, END)

	send_code, table, child, parent = make_code(para)

	with open("Code.txt", "w") as file:
		file.write(send_code)

	with open("table.txt", "w") as file:
		file.write(str(table))

	with open("child.txt", "w") as file:
		file.write(str(child))

	with open("parent.txt", "w") as file:
		file.write(str(parent))

	Label(root, text=send_code).pack()

	expected_len = 8.0 * len(str(text_box.get(1.0, END)))
	new_len = len(send_code)

	eff = (new_len / expected_len) * 100

	st = "Efficiency = " + str(eff) + "%"
	Label(root, text=st).pack()

	def nxt_click():
		root.destroy()
		os.system("python break_code.py Code.txt table.txt child.txt parent.txt")

	Button(root, text="send_code", command=nxt_click).pack()


Button(root, text="process", command=clicked).pack()

Button(root, text="exit", command=root.destroy).pack()

mainloop()
