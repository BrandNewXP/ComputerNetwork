import socket
import random
import time
import datetime
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup


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
GuessList = ['1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '10']
Youtube = '{}: https://www.youtube.com{}'
YoutubePre = 'https://www.youtube.com/results?search_query={}'
YoutubeCls = 'yt-uix-tile-link'


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
	sendmsg('PRIVMSG {} :{}'.format(Channel , Intro))

	Guessing = False
	answer = None
	chances = None
	
	while True:
		IRCMsg = IRCSocket.recv(Bufsize).decode().strip('\r\n')
		if not IRCMsg :
			continue
		msg = IRCMsg.split()
		# PING PONG
		if msg[0] == 'PING':
			sendmsg('PONG ' + msg[1])
			print('PINGed at ' +  time.asctime(time.localtime(time.time())))
			continue

		ClientName , IRCCommand = msg[0].split('!', 1)[0][1:], msg[1]
		action = None

		if IRCCommand == 'PRIVMSG':
			action = msg[3][1:]
			text = msg[4:]
			if Guessing == True :
				if action in GuessList :
					num = int(action)
					if num == answer :
						sendmsg('PRIVMSG {} :{}'.format(ClientName , 'Grats! You got it!'))
						Guessing = False
					elif num > answer :
						sendmsg('PRIVMSG {} :{}'.format(ClientName , 'That\'s too big.'))
						chances = chances - 1
						sendmsg('PRIVMSG {} :{} {}'.format(ClientName , 'Chances left :' , chances))
					else :
						sendmsg('PRIVMSG {} :{}'.format(ClientName , 'Should be bigger.'))
						chances = chances - 1
						sendmsg('PRIVMSG {} :{} {}'.format(ClientName , 'Chances left :' , chances))
				else :
					sendmsg('PRIVMSG {} :{}'.format(ClientName , 'That\'s not valid before the holy guessing game ends!'))
				if chances < 1 :
					sendmsg('PRIVMSG {} :{}'.format(ClientName , 'Game over! Maybe next time.'))
					Guessing = False
			elif action in ZSign :
				TodayDate = datetime.datetime.now()
				Outcome = ZOutcome[(ZSign.index(action) * TodayDate.day) % 6]
				sendmsg('PRIVMSG {} :{}'.format(ClientName , Outcome))
			elif action == '!guess' :
				if Guessing == True :
					sendmsg('PRIVMSG {} :{}'.format(ClientName , 'Please finish previous game.'))
					continue
				sendmsg('PRIVMSG {} :{}'.format(ClientName , 'Game start! Guess a number between 1~10.'))
				answer = random.randint(1 , 10)
				print('Guessing game cheater :' , answer)
				chances = 3
				Guessing = True
			elif action == '!song':
				if not text :
					sendmsg('PRIVMSG {} :{}'.format(ClientName , 'I don\'t understand. You must have done something wrong.'))
				else :
					songname = '+'.join(text)
					url = YoutubePre.format(urllib.parse.quote(songname))
					with urllib.request.urlopen(url) as search :
						html = search.read()
						soup = BeautifulSoup(html , 'lxml')
						target = soup.find('a' , class_ = YoutubeCls)
						title = target['title']
						link =  target['href']
						sendmsg('PRIVMSG {} :{}'.format(ClientName , Youtube.format(title , link)))
			else :
				sendmsg('PRIVMSG {} :{}'.format(ClientName , 'I don\'t understand. You must have misspelled something.'))
			

if __name__ == '__main__':
	IRCRobot()
