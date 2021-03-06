import socket
import re
import matplotlib.pyplot as pl
from math import sin
import os
import threading
import webbrowser
try:
	import matplotlib.pyplot as pl
	PLOTTABLE = True
except ImportError:
	print "Cannot import matplotlib"
	PLOTTABLE = False

global toOpen
functions,howManyArgs={},{}
DIR = "CV"

def add(*args):
	try:
		return args[0]+args[1]
	except TypeError:
		print args[0],args[1],"BUONT TYPU"

def sub(*args):
	try:
		return args[0]-args[1]
	except TypeError:
		print args[0],args[1],"BUONT TYPU"

def mul(*args):
	try:
		return args[0]*args[1]
	except TypeError:
		print args[0],args[1],"BUONT TYPU"

def div(*args):
	try:
		return args[0]/args[1]
	except TypeError:
		print args[0],args[1],"BUONT TYPU"

def power(*args):
	try:
		return pow(args[0],args[1])
	except TypeError:
		print args[0],args[1],"BUONT TYPU"

functions["+"]=add
functions["-"]=sub
functions["*"]=mul
functions["/"]=div
functions["^"]=power
howManyArgs["+"]=2
howManyArgs["-"]=2
howManyArgs["*"]=2
howManyArgs["/"]=2
howManyArgs["^"]=2

def whatType(arg):
	try:
		x = 2.0  + arg
		return "numeric"
	except TypeError:
		try:
			if(arg=="x"): return "identifier"
			else: return None
		except TypeError:
			if(isList(arg)): return "list"
			else: return None

def assoc(i):
	left=["+","-","*","/"]
	if i in left: return True
	else: return False

def precedence(i,j):
	pre = {}
	pre["("]=-4
	pre["+"]=1
	pre["-"]=1
	pre["*"]=2
	pre["/"]=2
	pre["^"]=3
	pre[")"]=99
	if((pre[i]<=pre[j] and assoc(i)) or (pre[i]<pre[j] and assoc(i))): return True
	else: return False

def upgradedSplit(strin):
	ret = strin.split(" ")
	return ret

def shuntingYard(strin):
	operator = "(\+|-|\*|\/|(\^)|sin|cos|tan|tg|cotan|ctg|ln|exp)"
	numeric = "-?(\d+(\.\d*)?)"
	identifier = "(x)"
	left = "\("
	right = "\)"
	output = []
	stack = []
	tokens = upgradedSplit(strin)
	for token in tokens:
		x = re.match(numeric,token)
		if(x): 
			output.append(float(x.group(1)))
			continue
		x = re.match(identifier,token)		
		if(x): output.append(x.group(1))
		x = re.match(operator,token)
		if(x):
			op = x.group(1)
			while(len(stack)):
				temp = stack.pop()
				if(precedence(op,temp)):output.append(temp)
				else:
					stack.append(temp)				
					break
			stack.append(op)
		x = re.match(left,token)
		if(x): stack.append("(")
		x = re.match(right,token)
		if(x):
			while(len(stack)):
				temp = stack.pop()
				if(temp=="("):
					stack.append(temp)
					if(len(stack)):
						temp = stack.pop()
						if re.match(function,temp): output.append(temp)
					break
				else:
					output.append(temp)
	while(len(stack)):
		temp = stack.pop()
		if all((temp!="(",temp!=")")): output.append(temp)
		else: return False
	return output

def evaluate(strinput, val=0):
	operator = "(\+|-|\*|\/|(\^)|sin|cos|tan|tg|cotan|ctg|ln)"
	numeric = "-?(\d+(\.\d*)?)"
	identifier = "(x)"
	stack = []
	postfix = shuntingYard(strinput)
	for i in postfix:
		#print stack
		if whatType(i)=="numeric":stack.append(i)
		if whatType(i)=="identifier": stack.append(val)
		try:
			if re.match(operator,str(i)):
				args=[]
				for j in range(howManyArgs[i]):
					args = [stack.pop()] + args
				stack.append(functions[i](*args))
		except TypeError:
			print "KURWA BUONT TYPU"
	if(len(stack)>1):return None
	return stack[0]

def plotfun(asc,scale=10):
	x,y = [],[]
	for i in range(200):
		print i
		x.append((scale/100.0)*i-scale)
		y.append(evaluate(asc,(scale/100.0)*i-scale))
	print x,y
	pl.plot(x,y)
	pl.show()

def openWeb():
	webbrowser.open('http://localhost:1488')

def viewhome():
	ls = os.listdir("\\home")
	for i in ls:
		print ls
	return

def getMessage(toOpen):
	global DIR
	header = "HTTP/1.1\nContent-Type: text/html; charset=UTF-8\n\n"
	if(toOpen[:6] == "<html>"):
		return header + toOpen
	filename = DIR+os.sep+toOpen
	with open((filename),"r") as f:
		message = f.read()
	return header + message

def HTTPtostr(asc):
	asc = asc.replace("+"," ")
	while(re.search("%[0-9A-F]{2}",asc)):
		x = re.search("%([0-9A-F]{2})",asc).group(1)
		asc = asc.replace("%"+x,x.decode("hex"))
		print x, asc
	return asc

def addToNotepad(asc):
	x = re.search("name=([^&]*)&company=([^&]*)&smth=([^&]*)",asc)
	name = HTTPtostr(x.group(1))
	company = HTTPtostr(x.group(2))
	smth = HTTPtostr(x.group(3))
	with open("notes.dat","a") as f:
		f.write("Name: " + name + "\nCompany: " + company + "\nFew words: " + smth + "\n\n")

def extract(string):
	global toOpen
	try:
		mess = re.search("EXP=(.*)&PLOT=Plot.21",string)
		if mess:
			print HTTPtostr(mess.group(1))
			plotfun(HTTPtostr(mess.group(1)),10)
			return
	except:
		print "Nought"
		mess = ""
	try:
		mess = re.search("EXP=(.*)&CALC=Compute.21",string)
		if mess:
			toOpen = "<html><body><center>Wynik to: " + str(evaluate(HTTPtostr(mess.group(1)))) +  "</center></body></html>"
			return
	except:
		print "Nought"
		mess = ""
	try:
		mess = re.search("(name=[^&]*&company=[^&]*&smth=[^&]*)",string)
		if mess:
			addToNotepad(mess.group(1))
			return
	except TypeError:
		print "Nought"
		mess = ""

#MAIN HTML SERVER

PORT = 1488
BUFFERSIZE=1024
net = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
net.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
net.bind(('', PORT))
th = threading.Thread(target=openWeb)
th.run()
while(1):
	print "Port Estabilished"
	net.listen(2)
	(clientsocket, address) = net.accept()
	print "Socket Created"
	data = clientsocket.recv(BUFFERSIZE)
	print data
	try:
		toOpen = re.search("(GET|POST) .(.*\.(html|css|jpg))",data).group(2)
		print "FILE TO BE FOUND: " + toOpen
	except:
		print "Error Occured - no page found - returning HOME"
		toOpen = "index.html"
	extract(data)
	message = getMessage(toOpen)
	clientsocket.send(message)
	clientsocket.close()
	print "Page Sent"
net.shutdown(socket.SHUT_RDWR)
net.close(socket.SHUT_RDWR)
