#!/usr/bin/env python3

#used to print exception info/testing as well as find platform (needed for different Windows vs Linux ping commands).
import sys
#for regex.
import re
#for dns.
import socket
#for parsing URLs for domain name as well as verifying IP.
from urllib.parse import urlparse
#for ping.
import os
#request needed for web calls do `try` because I found that it isn't install on Windows with base Python 3.7.1 install.
import requests
try:
    import requests
except:
    print('If you have a Windows System you might have to install requests with `pip install request`')    
#For Fun
import webbrowser
import time

#function for interactive prompt for original website check (base challenge) compared to other `bonus` options.
#originally, HTTP(s) status codes was an option, but I felt like this was more of a subset of a later function.
def interactive_prompt():
    vf_str_johnny = '''
                                     (                            
             )                    )\ )        )   )            
   (      ( /(             (     (()/((    ( /(( /(            
   )\  (  )\()) (     (    )\ )   /(_))\ ) )\())\()) (   (     
  ((_) )\((_)\  )\ )  )\ )(()/(  (_))(()/((_))((_)\  )\  )\ )  
 _ | |((_) |(_)_(_/( _(_/( )(_)) | _ \)(_)) |_| |(_)((_)_(_/(  
| || / _ \ ' \| ' \)) ' \)) || | |  _/ || |  _| ' \/ _ \ ' \)) 
 \__/\___/_||_|_||_||_||_| \_, | |_|  \_, |\__|_||_\___/_||_|  
                           |__/       |__/
    '''
    print(vf_str_johnny)
    print('Menu - Please select one of the following:')
    print('1. Original Website Check')
    print('2. IP Address Test')
    print('3. FQDN TCp-80/443 Check')
    print('4. QUIT')
    vf_str_select = input('Selection: ')
    #list of correct choices for menus selection.
    vf_list_right_choices = ['1','2','3','4']
    #while loop for error checking: continue to prompt for response until an acceptable selection is made.
    while not(vf_str_select in vf_list_right_choices):
        vf_str_select = input('Please select an item 1-4: ')
    #if select 4 is made (quit), shutdown program.
    if vf_str_select == '4':
        print('BYE FOR NOW!')
        exit()
    #else return selection.
    else:
        return(vf_str_select)

#function to validate the URL is in the correct format (Dicatated by Mike Kelsen, but also expanded on: see readme).  Also parses hostname entry to be passed back to main as well.
def URL_validator():
    #get URL entry and continue to prompt until and acceptable URL is entered (determined by regex).
    vf_str_URL_input = input('Enter URL: ')
    while not(re.search('^https?:\/\/(?!-)[a-zA-Z0-9\-]*(?<!-)\.?(?!-)[a-zA-Z0-9\-]+(?<!-)\.[a-zA-Z]{2,3}\/(?!-)[a-zA-Z0-9\-]+(?<!-)\/?$',vf_str_URL_input)):
        print('Invalid URL (syntax): ',vf_str_URL_input,'is an invalid URL')
        vf_str_URL_input = input('URL: ')
    #uses urllib to parse for only the hostname portion of URL
    vf_urllib_info = urlparse(vf_str_URL_input)
    vf_str_host = vf_urllib_info.netloc
    #returns complete URL as well as hostname to main
    return(vf_str_URL_input,vf_str_host)

#function to validate inputted FQDN (by regex) until and acceptable entry is entered.
def FQDN_validator():
    vf_str_FQDN_input = input('Enter FQDN: ')
    while not(re.search('(?!-)[a-zA-Z0-9\-]*(?<!-)\.?(?!-)[a-zA-Z0-9\-]+(?<!-)\.[a-zA-Z]{2,3}$',vf_str_FQDN_input)):
        print('Invalid FQDN (syntax): ',vf_str_FQDN_input,'is an invalid FQDN')
        vf_str_FQDN_input = input('Enter FQDN: ')
    #return inputted FQDN to main
    return(vf_str_FQDN_input)

#function to attempt DNS resolution of either hostname/FQDN. If this fails, program stops.
def DNS_resolve(vf_str_host):
    #attempts to resolve hostname/FQDN to IP address.
    try:
        vf_str_ip = socket.gethostbyname(vf_str_host)
        #if dns resolution works, return IP to main.
        return(vf_str_ip)
    #if resolution fails print failure message and exit program.
    except:
        ###print(sys.exc_info())
        print("Unknown DNS name: ",vf_str_ip,"is an unknown DNS name.")
        exit()

#function to validate an inputted IP address and continue to prompt until a legitimate entry is entered.
def IP_validator():
    vf_str_IP_input = input('Enter IP: ')
    #This socket function converts an IP to hexidecimal and comes up with an error if it isn't a correct IP address
    ##Can't make a less complicated while loop because this won't output boolean value like others
    vf_bool_track = False
    while vf_bool_track == False:
        try:
            socket.inet_aton(vf_str_IP_input)
            vf_bool_track = True
        except:
            vf_str_IP_input = input('Enter IP: ')
    #if IP address is good, return to main.
    return(vf_str_IP_input)

#fuction to test ICMP (ping) reachability of an IP address.  Should be noted that there are internet IPs that have web (HTTP/HTTPS) reachability, but no ping reachability.
def ping_test(vf_str_ip):
    #Windows needs a different command than linux based OSes because for some reason the -c switch requires command prompt with admin rights, I have tested on windows/ubunutu, might need to test on otheres as well.
    vf_int_ping = os.system("ping" + (" " if  sys.platform.lower()=="win32" else " -c 4 ") + vf_str_ip)
    #number other than zero denotes failure.  Upon failure, print failure message.  However, don't quit out of program.
    #this is becaue there are websites that allow web traffic (http/https) but not ICMP.
    if vf_int_ping != 0:
        print("Unreachable IP: unable to ping",vf_str_ip,"! the server might be down or a device (server/firewall) might be blocking ICMP") 

#function that refers to part three of the bonus.  Originally was going to make this part of the main menu, but it seemed to make more sense to make it an add on for an processes that make it to web_test() function.  Asks user if they want to display http(s) status codes.        
def HTTP_status_check(vf_str_URL_input):
    ##the `end=''` is necessary to print on the same line
    print('For Website,',vf_str_URL_input,',',end='')
    vf_str_https_status = input(' Display HTTP(s) Status Code? [Y/N]: ')
    vf_list_right_choices = ['n','y']
    #while loop to continue to prompt for [Y,N,y,n]
    while not(vf_str_https_status.lower() in vf_list_right_choices):
        vf_str_https_status = input('Invalid resposne, please select [Y/N]: ')
    #return False (do not display status code) is N/n is selcted.
    if vf_str_https_status.lower() == 'n':
        vf_bool_http_status = False
        return(vf_bool_http_status)
    #return True (display status code) is Y/y is selcted.
    else:
        vf_bool_http_status = True
        return(vf_bool_http_status)

#function to test if a web call (requests) passes for URL.  If status code option was selected, that will be displayed as well.        
def web_test(vf_str_URL_input):
    vf_bool_http_status = HTTP_status_check(vf_str_URL_input)
    try:
        #GET API call to URL.
        vf_req_response = requests.request('GET', vf_str_URL_input)
    except:
        ###print(sys.exc_info())
        exit()
    #if http status was selected, print status code.
    if vf_bool_http_status == True:
        print('For',vf_str_URL_input,': HTTP(s) Status Code =',vf_req_response.status_code)
    #print error is something other than 200 was returned.
    if vf_req_response.status_code != 200:
        print('HTTP(s) Status Code other than 200 returned')
    #Else print Success message.
    else:
        print('Success, the server ',vf_str_URL_input,'appears to be online and functioning correctly')
        time.sleep(5)
        webbrowser.open('https://www.youtube.com/watch?v=xfr64zoBTAQ&index=3&list=PLnJhY7qfCqzMI5kO8skuRjpgrBujjjlz5')

#main program.       
if __name__ == '__main__':
    vm__str_select = interactive_prompt()
    #Option 1: original challenge.  Validate URL, test DNS resolution, test ping, and finally web call.  There is error checking in individual components and program exits if there is a failure.
    if vm__str_select == '1':
        vm_str_URL_input,vm_str_host = URL_validator()
        vm_str_ip=DNS_resolve(vm_str_host)
        ping_test(vm_str_ip)
        web_test(vm_str_URL_input)
    #Option 2: IP addressed entered instead of URL.  Validate IP, test ping, and then web call.
    elif vm__str_select == '2':
        vm_str_IP_input = IP_validator()
        ping_test(vm_str_IP_input)
        vm_str_IP_URL = 'http://' + vm_str_IP_input
        web_test(vm_str_IP_URL)
    #Option 3: Enter an FQDN and test tcp 80/443 connections.  Flow is similiar to option 1, excepted that two web calls are made (one for 80 and the other for 443).
    elif vm__str_select == '3':
        vm_str_FQDN_input = FQDN_validator()
        vm_str_ip = DNS_resolve(vm_str_FQDN_input)
        ping_test(vm_str_ip)
        vm_str_http_URL = 'http://' + vm_str_FQDN_input
        vm_str_https_URL = 'https://' + vm_str_FQDN_input
        web_test(vm_str_http_URL)
        web_test(vm_str_https_URL)
