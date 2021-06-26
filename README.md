# copyasffuf
Hello Amazing People, <br>
copyasffuf is a simple python script that takes a raw HTTP request as input and convert it into a working ffuf command.<br>
Wonder why would you need this, read along!

![copyasffuf-help](https://user-images.githubusercontent.com/54149916/123513208-d3df6b00-d659-11eb-9c82-ab956b2226fa.JPG)


## Usage
wget the python script to your computer and execute:
[link to raw file!](https://raw.githubusercontent.com/w33knd/copyasffuf/main/copyasffuf.py)
```bash
wget https://raw.githubusercontent.com/w33knd/copyasffuf/main/copyasffuf.py
```
Make it executable:
```bash
chmod +x copyasffuf.py
```
and then, Execute!!
```bash
./copyasffuf.py -f <request file> -m ffuf
or
python3 copyasffuf.py -f <request file>
```
![copyasffuf](https://user-images.githubusercontent.com/54149916/123513585-fb373780-d65b-11eb-90f6-de3a528b617b.JPG)

Works on POST request too!!

![copyasffuf2](https://user-images.githubusercontent.com/54149916/123513586-fd999180-d65b-11eb-910d-20faeadf2400.JPG)


## Need
When testing an aggresively firewalled api or target, we need to fuzz multiple times, and creating a vanilla ffuf payload won't get you anywhere because you will just keep adding headers and won't find out why firewall is blocking your request. <br>
Solution: Capture a working HTTP request, be it GET, POST or PUT, run this python script and you will have, a working ffuf payload.
You just need to switch wordlist path and FUZZ keyword and you are good to go.

If you find a bug, headover to issues section and fill the form..

Thank you.
