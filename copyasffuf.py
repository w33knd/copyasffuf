#!/usr/bin/python3

import os
import sys
import argparse
import subprocess

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"


def check_if_http(file_content):
    allowed_methods=["GET","POST","PUT"]
    temp_file_content=file_content
    for i in range(len(temp_file_content)):
        temp_file_content[i]=' '.join(temp_file_content[i].split())
    temp_file_content=list(filter(None,file_content))
    request_type=""
    for x in allowed_methods:
        if x in temp_file_content[0]:
            request_type=x
    if request_type=="":
        sys.stdout.write(BOLD+RED)
        print("[-] Request does not seem to be HTTP or Supported request type (Get, Post, Put)")
        exit()
    else:
        return request_type

def parse_request(file_content,request_type):
    sys.stdout.write(BOLD+CYAN)
    print("[+] Parsing request...")
    req=dict()
    req["request_type"]=request_type
    if request_type=="GET":
        #remove all blank lines and tabs
        for i in range(len(file_content)):
            file_content[i]=' '.join(file_content[i].split())
        file_content=list(filter(None,file_content))
        #headers parsing
        req["headers"]=file_content[1:]
        for header in req["headers"]:
            key,value = header.split(':',1)#split each line by http field name and value
            if(key=="Host"):
                req["host"]=value.strip()
        #get request query
        req["query"]=file_content[0].split(" ")[1].strip()
        return(req)
    else:
        #parsing post request
        while 1:
            if file_content[0]=="":
                del file_content[0]
            elif file_content[len(file_content)-1]=="":
                del file_content[len(file_content)-1]
            else:
                break
        req["request_type"]=request_type
        #post request query
        req["query"]=file_content[0].split(" ")[1].strip()
        #headers and body parsing
        for i in range(len(file_content)):
            if file_content[i]=="":
                lastheaderat=i
                break
        req["headers"]=file_content[1:lastheaderat]
        req["body"]=file_content[lastheaderat:]
        #host parsing
        for header in req["headers"]:
            key,value = header.split(':')#split each line by http field name and value
            if(key=="Host"):
                req["host"]=value.strip()
                break
        return req
        
def make_ffuf_command(req):
    sys.stdout.write(BOLD+CYAN)
    print("[+] Generating ffuf command")
    #ffuf -u http://target.com/FUZZ -w wordlist.txt
    str=""
    for header in req['headers']:
        str+=f' -H \'{header}\''
    url=f'https://{req["host"]}{req["query"]}'
    if url[len(url)-1]=="/":
        url=url[:-1]
    if "body" in req :
        body=f" -d \'{' '.join(req['body']).strip()}\'"
    else:
        body=""
    cmd=f"ffuf -X {req['request_type']}{body} {str} -u {url}/FUZZ -w "
    process = subprocess.Popen('printf "hello\nDhello2\nhello3" |'+cmd+'- > /dev/null 2>&1 ', shell=True, stdout=subprocess.PIPE)
    process.wait()
    cmd+="wordlist"
    if process.returncode==0 :
        sys.stdout.write(BOLD+CYAN)
        print("[+] ffuf command created successfully")
        process = subprocess.Popen('echo -n "'+cmd+'" | xclip -selection clipboard', shell=True, stdout=subprocess.PIPE)
        process.wait()
        if process.returncode==0:
            sys.stdout.write(BOLD+CYAN)
            print("[+] Command copied to clipboard")
        sys.stdout.write(BOLD+BLUE)
        print("[+] Don't forget to change wordlist and FUZZ")

    else:
        process = subprocess.Popen('echo -n "'+cmd+'" | xclip -selection clipboard', shell=True, stdout=subprocess.PIPE)
        process.wait()
        if process.returncode==0:
            sys.stdout.write(BOLD+CYAN)
            print("[+] Command copied to clipboard")
        sys.stdout.write(BOLD+RED)
        print("[-] errr... code bugged out, this is what i come up with")
    sys.stdout.write(BOLD+RESET)    
    print(cmd)
    exit()


def make_curl_command(req):
    sys.stdout.write(BOLD+RED)
    print("[+] To be added soon")
    exit()

if __name__ == "__main__":
    # Parse command line
    parser = argparse.ArgumentParser(description="Automatically output ffuf and curl commands that works bypassing firewall for an input request file!! ＼(*￢*)／")
    parser.add_argument("-f","--file",help="Input a captured request file from burp", 
                        required="True",action="store")
    parser.add_argument("-m","--mode",help="Output command type (ffuf,kr,curl)",
                        default="ffuf", action="store")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        sys.stdout.write(BOLD+RED)
        parser.error("[-] The file %s does not exist!" % args.file)
        exit
    else:
        f=open(args.file, 'r')
        file_content=f.read().split('\n')
        if len(file_content)==1 and file_content[0]=="":
            sys.stdout.write(BOLD+RED)
            print("[-] File is empty. Please check")
            exit()

        request_type=check_if_http(file_content)

        req=parse_request(file_content,request_type)

        if args.mode=="ffuf":
            make_ffuf_command(req)
        elif args.mode=="curl":
            make_curl_command(req)
        else:
            print("[-] Nothing matches %s" % args.mode)