import socket
import sys
s = socket.socket()
port = int(sys.argv[1])
s.connect(('127.0.0.1', port))
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
while True:
	print('\n1. Fetch News')
	print('\n2. Exit')
	ans = int(input('\nEnter ur choice :'))
	if ans == 1:
		s.send('Need News!!!'.encode())
		#print(s.recv(1024).decode('ascii'))
		print(s.recv(102400).decode().translate(non_bmp_map))
	elif ans == 2:
		break
	else:
		print('\n Enter a 1 (or) 2 only!!!')
s.close()
