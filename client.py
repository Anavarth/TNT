import socket
import sys
s = socket.socket()
port = int(sys.argv[1])
s.connect(('127.0.0.1', port))
while True:
	print('\n1. Fetch News')
	print('\n2. Exit')
	ans = int(input('\nEnter ur choice :'))
	if ans == 1:
		s.send('Need News!!!'.encode())
		print(s.recv(1024).decode('ascii'))
		file = open("News.txt","r")
		for lines in file:
			print(lines)
		file.close()
	elif ans == 2:
		break
	else:
		print('\n Enter a 1 (or) 2 only!!!')
s.close()