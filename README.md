# wpa-password-cracking-with-pmkid
A WPA/WPA2 PSK password cracking script for a known PMKID. 

Active files include the main script `crack_password.py`, another python file called `pbkdf2.py` containing a PBKDF2 function used in the main script, and a sample passwords list in `passlist.txt`.

This script can crack WiFi passwords for WPA and WPA2 networks when supplied with: 
1. PMKID
2. SSID
3. MAC address of the Access Point (AP)
4. MAC address of the Client

along with a passwords list.

A sample list of the top 100 passwords is included for testing. In a real world scenario, you'd typically use a much larger list. This script is for demonstration purposes and built for comprehension over speed. It is meant to help those looking to build their own cracking tools get started with a bare-bones example.

Also, and I hope this goes without saying, only ever hack a network you own and have legal permission to hack. This is for educational purposes only and to help you advance your penetration testing skills and knowledge. 

## Background Information on the exploit
What the terms above mean in simple language:
- The SSID (specifically the ESSID) is the name of the WiFi network.
- The Access Point (AP) is typically the WiFi router for the network in question. The MAC address of the AP is available to WiFi devices in range of it.
- The Client is the network interface you are using to connect to WiFi: either an internal or external WiFi adapter on your computer or device. The MAC address for the Client is known by your computer/device. 

In other words, the SSID, AP MAC, and Client MAC are typically readily available to all WiFi devices in range. The PMKID is an optional value that can be sent from the Access point to the client, and is derived by running the above values + the WiFi password through a series of cryptographic hashing functions.

Many modern WiFi routers append an optional field to the end of the first EAPOL frame that they send to a Client device when associating. The optional field is known as a "Robust Security Network Information Element" (RSN IE) and includes the PMKID.

By obtaining this frame and thus the PMKID, a hacker can take a list of potential passwords and run them through the same cryptographic hashing functions the AP uses to generate the PMKID with the true password. If the hacker finds that the output of these functions for one of their test passwords produces the same value as the known PMKID obtained in the EAPOL frame, then they know that their test password is the true password of the WiFi network. Having cracked the password, they can now gain unauthorized access to the network. 

Note that this process happens offline. Once the PMKID is obtained, the hacker can make as many attempts as they want to find the password without having to interact with the Access Point.

This exploit was originally found in 2018 by atom and the hashcat team. See the thread on the hashcat forums: <a href="https://hashcat.net/forum/thread-7717.html">Thread</a>

## How the script works

This script (`crack_password.py`) does the password cracking that comes after the PMKID has been obtained from the Access Point.

To generate a potential matching PMKID from a test password on the passwords list, the following steps are taken:
1. A PMK (Pairwise Master Key) is computed using a cryptographic function called PBKDF2 with the test password and SSID as inputs
2. A PMKID is then computed with a function called HMAC-SHA1-128 using the computed PMK, the string "PMK Name", the Access Point MAC address, and the Client MAC address as inputs.

In order to crack a password, crack_password.py simply loops through a list of likely passwords and does the above 2 steps with each test password until a matching PMKID is found. It is essentially a less sophisticated, single-threaded, CPU-based way of doing what hashcat does with mode 16800/22000 to crack WPA/WPA2 PSK passwords when a PMKID is known.

Note that this is for demonstration purposes, and not a particularly effective way of cracking WiFi passwords given it's slow speed. Most of the time you'd want to use *much* bigger lists, a faster language and more sophisticated parallel processing techniques. Still, I'm hoping this can get you started building your own cracking tools from the ground up. Personally, I like to have short and simple code examples to build off of, or to port to other languages. All of the code, including the PDKDF2 implementation that I grabbed from Stefano Palazzo's <a href="https://github.com/sfstpala/python3-pbkdf2/blob/master/pbkdf2.py">example</a> uses only standard python libraries. Other than comments/license info, there's only ~65 total lines of python over both .py files, and without print statements, spaces, and formatting it's closer to ~35.

## Options

You can feed in PMKID, ESSID, AP MAC, Client MAC and a custom passwords list when you run the script, or you can leave the parameters blank to run the script with a test PMKID taken from hashcat's example hashes (see 22000): [Hashcat Example Hashes](https://hashcat.net/wiki/doku.php?id=example_hashes#example_hashes). 

To use the default test parameters, simply run:
```
python crack_password.py
```
The default parameters are:
<br/>  
**PMKID:**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4d4fe7aac3a2cecab195321ceb99a7d0  
**SSID:**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hashcat-essid  
**AP MAC Address:**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;fc:69:0c:15:82:64  
**Client MAC Address:**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;f4:74:7f:87:f9:f4  
<br/>
The password for the default parameters is "hashcat!". 

<br/>  
You can feed in your own values like so:
<br/>  
<br/>  


```
crack_password.py <PMKID> <ESSID> <MAC_AP> <MAC_CLIENT> <PASSWORD_LIST_SRC>
```

**Note:**
- You can omit the `<PASSWORD_LIST_SRC>` to use the sample `passlist.txt` file. 

- Quotes are not necessary but can be used i.e. a PMKID of `"4d4fe7aac3a2cecab195321ceb99a7d0"` or `4d4fe7aac3a2cecab195321ceb99a7d0` are treated the same.

- MAC address octets can be seperated by `:`, `-`, or can omit seperators all together. Capitilization also doesn't matter: `fc:69:0c:15:82:64`, `fc-69-0c-15-82-64`, `fc690c158264`, `FC:69:0C:15:82:64` are all equivalent.

## Getting and Running the Script:
Clone the project:
```
git clone https://github.com/ZeroDayArcade/wpa-password-cracking-with-pmkid.git
```
cd into project directory:
```
cd wpa-password-cracking-with-pmkid
```
Test the script with default params:
```
python crack_password.py
```
Run the script with explicit params:
```
python crack_password.py 4d4fe7aac3a2cecab195321ceb99a7d0 hashcat-essid fc:69:0c:15:82:64 f4:74:7f:87:f9:f4 passlist.txt
```


## Acknowledgements
`passlist.txt` is a sample list taken from the top 100 most common passwords put together by Daniel Miessler. I've added "hashcat!" to the list for the example hash. See the original list here:
https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-100.txt

`pbkdf2.py` contains a PDKDF2 python implementation by Stefano Palazzo written using only standard libraries. I've stripped out comments (other than the license info) and unneeded parts to keep it short, see the original on his github: https://github.com/sfstpala/python3-pbkdf2/blob/master/pbkdf2.py
