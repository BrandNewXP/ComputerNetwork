import socket
import random
import datetime

IRCSocket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
IRCServer = '127.0.0.1'
IRCPort = 6667
UserName = 'b05902004'
NickName = 'bot_b05902004'
Channel = '#CN_DEMO'
Intro = ' : Hi! I am bot_b0902004!'
ZSign = ['​Capricorn' , 'Aquarius' , 'Pisces' , 'Aries' , 'Taurus' , 'Gemini' , 'Cancer' , 'Leo' , 'Virgo' , 'Libra' , 'Scorpio' , 'Sagittarius']
ZOutcome = ['Today is your lucky day!' ,
			'Be careful, cause you\'re going to have a bad day.' ,
			'Don\'t be afraid to take that big step.' ,
			'You\'ve just wasted 3 seconds reading this message.' ,
			'If you spell stressed backwards, you get desserts.' ,
			'Wait, I\'m searching for some fortune messages on Google.'] #Total : 6
Bufsize = 4096

def IRCFormat(msg) :
	return (msg + '\r\n').encode()

def sendmsg(msg):
	if msg is None:
		return
		
	if isinstance(msg , list) :
		for _ in msg :
			IRCSocket.send(IRCFormat(_))
	else :
		IRCSocket.send(IRCFormat(msg))

def IRCRobot():
	#Connect to server
	print(IRCServer , IRCPort)
	IRCSocket.connect((IRCServer, IRCPort))
	
	#Login
	sendmsg('NICK {}'.format(NickName))
	sendmsg('USER {}'.format(UserName))

	#Join channel
	sendmsg('JOIN {}'.format(Channel))
	
	#Auto introduction
	sendmsg('PRIVMSG {} {}'.format(Channel , Intro))

	while True:
		IRCMsg = IRCSocket.recv(Bufsize).decode().strip('\r\n')
		if not IRCMsg :
			continue
		msg = IRCMsg.split()
		# PING PONG
		if msg[0] == 'PING':
			sendmsg('PONG ' + msg[1])
			print('PINGed.')
			continue

		ClientName , IRCCommand = msg[0].split('!', 1)[0][1:], msg[1]
		action = None

		if IRCCommand == 'PRIVMSG':
			action = msg[3][1:]
			text = msg[4:]
			if action in ZSign :
				TodayDate = datetime.datetime.now()
				Outcome = ZOutcome[(ZSign.index(action) * TodayDate.day) % 6]
				sendmsg(Outcome)
			elif action == '!guess' :
				print('G')
			elif action == '!song':
				print('S')
			else :
				sendmsg('I don\'t understand. You must have misspelled something.')
			

if __name__ == '__main__':
	IRCRobot()
