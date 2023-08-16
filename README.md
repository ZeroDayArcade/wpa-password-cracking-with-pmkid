# wpa-psk-password-cracking-pmkid
A WPA/WPA2 PSK password cracking script for a known PMKID. 

The active files include the main script crack_password.py, a file containing a PBKDF2 function in pbkdf2.py that's called in the main script, and a sample passwords list in passlist.txt.

This script can crack WiFi passwords for WPA and WPA2 networks when supplied with:  
1. PMKID
2. SSID
3. MAC address of the Access Point (AP)
4. MAC address of the Client

For those unfamiliar:
- The SSID (specifically the ESSID) is the name of the WiFi network.
- The AP is typically the WiFi router for the network in question and the MAC address of the AP is available to WiFi devices in range of it.
- The Client is the network interface you are using to connect to WiFi: either an internal or external WiFi adapter on your computer or device. The MAC address for the Client is known by your computer/device. 

In other words, the SSID, AP MAC, and Client MAC are typically readily available to all WiFi devices in range, including a WiFi adapter that has been put into monitor mode.

The PMKID is derived by running those values + the WiFi password through a series of cryptographic hashing functions. The PMKID is part of an optional field that many modern WiFi routers add to the end of the first EAPOL frame that they send to a Client device when connecting. EAPOL stands for "Extensible Authentication Protocol over LAN". The optional field is known as a "Robust Security Network Information Element" (RSN IE) and includes the PMKID. 

By obtaining this frame and thus the PMKID, a hacker can take a list of potential passwords and run them through the same cryptographic hashing functions to obtain a unique PMKID for each potential password. If they find that one of the passwords on the list produces the same PMKID as the known PMKID obtained in the EAPOL frame, then they know that that is the true password of the WiFi network. Having cracked the password, they can now gain unauthorized access to the network.

To obtain a PMKID for a potential password the following steps are taken:
1. A PMK is computed using a cryptographic function called PBKDF2 and supplying it with the password and ssid (network name)
2. The PMKID is then computed with a function called HMAC-SHA1-128 and supplying it with the PMK, the string "PMK Name", and the MAC addresses of the AP and Client.

The most straightforward way to do this is to simply loop through a list of likely passwords and do the above 2 steps with each password until a matching PMKID is found. This is essentially what crack_password.py does. It is essentially a less sophisticated, single-threaded, CPU-based way of doing what hashcat does with mode 16800/22000 to crack WPA/WPA2 psk passwords when a PMKID is known.

Note that this is for demonstration purposes, and not a particularly effective way of cracking WiFi passwords since it is slow compared to more sophisticated methods. Also, the sample passlist is just 100 passwords. Most people use *much* bigger lists. Still, I'm hoping this can get you started building your own cracking tools from the ground up. It is one thing to install software and learn a few commands, but there is something to be said about having a short and understandable code example that you can build off of. All of the code, including the PDKDF2 imlementation I borrowed from Stefano Palazzo's code uses only standard python libraries. This means it should run on any python 3 installation. Other than comments/license info, there's only about 50 total lines of python between the two python files, and that's counting print statements, spaces, and formatting.

Also, and I hope this goes without saying, hacking a network you don't own or have permission to hack is very illegal. Don't do it. This is for educational purposes only and to advance your penetration testing skills and knowledge.

You can feed in PMKID, ESSID, MAC AP, and MAC Client when you run `crack_password()`, or leave the parameters blank to run the script with a test PMKID taken from hash-mode 22000 in hashcat's example hashes: [https://hashcat.net/wiki/doku.php?id=example_hashes#example_hashes](Hashcat Example Hashes). The example has:

PMKID:                     4d4fe7aac3a2cecab195321ceb99a7d0  
SSID:                      hashcat-essid  
AP MAC Address:            fc:69:0c:15:82:64  
Client MAC Address:        f4:74:7f:87:f9:f4  

The "unknown" password is "hashcat!". If you feed in values, make sure they are in the same format as they are written within the crack_password.py which look like:

```
pmkid="4d4fe7aac3a2cecab195321ceb99a7d0", 
essid=b"hashcat-essid", 
mac_ap=b"\xfc\x69\x0c\x15\x82\x64", 
mac_cl=b"\xf4\x74\x7f\x87\xf9\xf4", 
```

## To test that everything runs correctly:
Clone the project:
```
git clone https://github.com/ZeroDayArcade/wpa-psk-password-cracking-pmkid.git
```
cd into project directory:
```
cd wpa-psk-password-cracking-pmkid
```
Run python:
```
python
```
Import password cracking script:
```
>>> import crack_password as cp
```
Crack password with given PMKID, SSID, MAC AP, and MAC Client:
```
cp.crack_password()
```

## Acknowledgements
passlist.txt is a sample list taken from the top 100 most common passwords put together by Daniel Miessler. I've added "hashcat!" to the list for this example. See the original list here:
https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-100.txt

pbkdf2.py contains a PDKDF2 python implementation by Stefano Palazzo written using only standard libraries. I've stripped out comments and unneeded parts to keep it short, see the original on his github: https://github.com/sfstpala/python3-pbkdf2/blob/master/pbkdf2.py
