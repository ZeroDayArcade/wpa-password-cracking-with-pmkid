# wpa-password-cracking-with-pmkid
A WPA/WPA2 PSK password cracking script for a known PMKID. 

Active files include the main script crack_password.py, another python file called pbkdf2.py containing a PBKDF2 function used in the main script, and a sample passwords list in passlist.txt.

This script can crack WiFi passwords for WPA and WPA2 networks when supplied with:  
1. PMKID
2. SSID
3. MAC address of the Access Point (AP)
4. MAC address of the Client

## Background Information on the exploit
What these terms mean:
- The SSID (specifically the ESSID) is the name of the WiFi network.
- The AP is typically the WiFi router for the network in question. The MAC address of the AP is available to WiFi devices in range of it.
- The Client is the network interface you are using to connect to WiFi: either an internal or external WiFi adapter on your computer or device. The MAC address for the Client is known by your computer/device. 

In other words, the SSID, AP MAC, and Client MAC are typically readily available to all WiFi devices in range. The PMKID is an optional value that can be sent from the Access point to the client, and is derived by running the above values + the WiFi password through a series of cryptographic hashing functions.

Many modern WiFi routers append an optional field to the end of the first EAPOL frame that they send to a Client device when associating. The optional field is known as a "Robust Security Network Information Element" (RSN IE) and includes the PMKID.

By obtaining this frame and thus the PMKID, a hacker can take a list of potential passwords and run them through the same cryptographic hashing functions the AP used to generate the PMKID with the real password. If the hacker finds that the output of these functions for one of the passwords produces the same value as the known PMKID obtained in the EAPOL frame, then they know that that is the true password of the WiFi network. Having cracked the password, they can now gain unauthorized access to the network. 

Note that this process happens offline. Once the PMKID is obtained, the hacker can make as many attempts as they want to find the password without having to interact with the Access Point.

This exploit was originally found in 2018. See the thread on the Hashcat forums: <a href="https://hashcat.net/forum/thread-7717.html">Thread</a>

## How the script works

This script (crack_password.py) does the password cracking that comes after the PMKID has been obtained from the Access Point.

To generate a potential matching PMKID from a password on the passwords list, the following steps are taken:
1. A PMK is computed using a cryptographic function called PBKDF2 with the WiFi password and SSID as inputs
2. A PMKID is then computed with a function called HMAC-SHA1-128 using the PMK, the string "PMK Name", the AP MAC address and the Client MAC address as inputs.

In order to crack a password, crack_password.py simply loops through a list of likely passwords and does the above 2 steps with each password until a matching PMKID is found. It is essentially a less sophisticated, single-threaded, CPU-based way of doing what hashcat does with mode 16800/22000 to crack WPA/WPA2 psk passwords when a PMKID is known.

Note that this is for demonstration purposes, and not a particularly effective way of cracking WiFi passwords given it's slow speed and the fact that the passlist only has 100 passwords for this simple example. Most of the time you'd want to use *much* bigger lists, a faster language and more sophisticated parallel processing techniques. Still, I'm hoping this can get you started building your own cracking tools from the ground up. It is one thing to install software and learn a few commands, but there is something to be said about having a short and understandable code example that you can build off of. All of the code, including the PDKDF2 implementation that I borrowed from Stefano Palazzo's code uses only standard python libraries. This means it should run on any python 3 installation. Other than comments/license info, there's only about 50 total lines of python between the two .py files, and that's counting print statements, spaces, and formatting.

Also, and I hope this goes without saying, hacking a network you don't own or have permission to hack is very illegal. Don't do it. This is for educational purposes only and to advance your penetration testing skills and knowledge.

## Options

You can feed in PMKID, ESSID, MAC AP, and MAC Client when you run `crack_password()`, or leave the parameters blank to run the script with a test PMKID taken from hashcat's example hashes (see 22000): [Hashcat Example Hashes](https://hashcat.net/wiki/doku.php?id=example_hashes#example_hashes). The example has:
<br/>
<br/>  
**PMKID:**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4d4fe7aac3a2cecab195321ceb99a7d0  
**SSID:**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hashcat-essid  
**AP MAC Address:**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;fc:69:0c:15:82:64  
**Client MAC Address:**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;f4:74:7f:87:f9:f4  
<br/>
<br/>
The "unknown" password is "hashcat!". If you feed in your own values, make sure they are in the same format as they are written within crack_password.py which look like:

```
pmkid="4d4fe7aac3a2cecab195321ceb99a7d0", 
essid=b"hashcat-essid", 
mac_ap=b"\xfc\x69\x0c\x15\x82\x64", 
mac_cl=b"\xf4\x74\x7f\x87\xf9\xf4", 
```

## Getting and Running the Script:
Clone the project:
```
git clone https://github.com/ZeroDayArcade/wpa-password-cracking-with-pmkid.git
```
cd into project directory:
```
cd wpa-password-cracking-with-pmkid
```
Run python:
```
python
```
Import password cracking script:
```
>>> import crack_password as cp
```
Crack password with given PMKID, SSID, MAC AP, and MAC Client (leave empty to use default values):
```
>>> cp.crack_password()
```
<br/>  

And you shoud see:  
<br/>  

<img width="559" alt="Screen Shot 2023-08-16 at 3 40 57 AM" src="https://github.com/ZeroDayArcade/wpa-password-cracking-with-pmkid/assets/141867962/5a220bef-cb2b-498d-a90a-2c0637c64cff">
<br/>  
<br/>  

Enter "y" to continue:  
<br/>  

<img width="686" alt="Screen Shot 2023-08-16 at 3 42 46 AM" src="https://github.com/ZeroDayArcade/wpa-password-cracking-with-pmkid/assets/141867962/552c6ce0-8cab-46a1-8417-59b0b8e6f8f9">
<br/>  
<br/>  

And when it finds a match you'll see:  
<br/>  

<img width="678" alt="Screen Shot 2023-08-16 at 3 43 33 AM" src="https://github.com/ZeroDayArcade/wpa-password-cracking-with-pmkid/assets/141867962/2928cd3b-052a-4060-9503-26368ded6ad1">



## Acknowledgements
passlist.txt is a sample list taken from the top 100 most common passwords put together by Daniel Miessler. I've added "hashcat!" to the list for this example. See the original list here:
https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-100.txt

pbkdf2.py contains a PDKDF2 python implementation by Stefano Palazzo written using only standard libraries. I've stripped out comments and unneeded parts to keep it short, see the original on his github: https://github.com/sfstpala/python3-pbkdf2/blob/master/pbkdf2.py
