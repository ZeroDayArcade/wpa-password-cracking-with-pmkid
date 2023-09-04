# WPA/WPA2 Password Cracking in Python - PMKID
A WPA/WPA2 PSK password cracking script for a known PMKID. 

For capturing a PMKID from an access point, see the other repo: <a href="https://github.com/ZeroDayArcade/capture-pmkid-wpa-wifi-hacking">Capturing a PMKID from WPA/WPA2 Access Points with a Python Script</a>

This script can crack WiFi passwords for WPA and WPA2 networks when supplied with: 
1. PMKID
2. SSID
3. MAC address of the Access Point (AP)
4. MAC address of the Client

along with a passwords list.

A sample list of the top 100 passwords is included for testing. In a real world scenario, you'd typically use a much larger list. This script is for demonstration purposes and built for comprehension over speed. It is meant to help those looking to build their own cracking tools get started with a bare-bones example.

***Reminder:** Only ever hack a network you own and have legal permission to hack. Any hacking skills/knowledge gained from this repository should only be used in the context of security research, penetration testing, password recovery, and education.* 

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

You can obtain a PMKID from an AP with <a href="https://github.com/ZeroDayArcade/capture-pmkid-wpa-wifi-hacking">this short script</a> and a WiFi adapter. You can also obtain a PMKID with <a href="https://github.com/ZerBea/hcxdumptool">hcxdumptool</a> or the <a href="https://github.com/risinek/esp32-wifi-penetration-tool">ESP32 Wi-Fi Penetration Tool</a>.

This script (`crack_pmkid.py`) does the password cracking that comes after the PMKID has been obtained from the Access Point.

To generate a potential matching PMKID with a test password from the passwords list, the following steps are taken:
1. A PMK (Pairwise Master Key) is computed using a cryptographic function called PBKDF2 with the test password and SSID as inputs
2. A PMKID is then computed with a function called HMAC-SHA1-128 using the computed PMK, the string "PMK Name", the Access Point MAC address, and the Client MAC address as inputs.

In order to crack a password, `crack_pmkid.py` simply loops through a list of likely passwords and does the above 2 steps with each test password until a matching PMKID is found. It is essentially a less sophisticated, CPU-based way of doing something similar to what hashcat does with a dictionary attack in hash mode 22000 with a known PMKID.

Personally, I like to have short and simple code examples to build off of, or to port to other languages. All of the code uses only standard python libraries. There's only about ~50 total lines of python and without print statements and spaces it's closer to about ~25.

## Options

You can feed in PMKID, SSID, AP MAC, Client MAC and a custom passwords list when you run the script, or you can leave the parameters blank to run the script with a test PMKID taken from hashcat's example hashes (see 22000): [Hashcat Example Hashes](https://hashcat.net/wiki/doku.php?id=example_hashes#example_hashes). 

To use the default test parameters, simply run:
```
python3 crack_pmkid.py
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
python3 crack_pmkid.py <PMKID> "<SSID>" <MAC_AP> <MAC_CLIENT> <PASSWORD_LIST_SRC>
```

**Note:**
- You can omit the `<PASSWORD_LIST_SRC>` to use the sample `passlist.txt` file. 

- Quotes are usually not necessary except for terms with spaces in them or in some cases for terms that use characters other than letters and numbers (like `*`). A PMKID of `"4d4fe7aac3a2cecab195321ceb99a7d0"` or `4d4fe7aac3a2cecab195321ceb99a7d0` are treated the same. This usually only ever matters for the SSID, and potentially the passlist file name. When in doubt use quotes, or to be extra safe triple quotes can be used.

- MAC address octets can be seperated by `:`, `-`, or can omit seperators all together. Capitilization also doesn't matter for MAC addresses: `fc:69:0c:15:82:64`, `fc-69-0c-15-82-64`, `fc690c158264`, and `FC:69:0C:15:82:64` are all equivalent.

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
python3 crack_pmkid.py
```
Run the script with explicit params:
```
python3 crack_pmkid.py 4d4fe7aac3a2cecab195321ceb99a7d0 "hashcat-essid" fc:69:0c:15:82:64 f4:74:7f:87:f9:f4 passlist.txt
```

## Using hashcat hc22000 examples with this script
Hashcat now uses hash mode 22000 which has 2 types of hash lines: one type starts with `WPA*01`, and the other starts with `WPA*02`. See their <a href="https://hashcat.net/wiki/doku.php?id=cracking_wpawpa2">guide on hash mode 22000</a> for more detail. 

Specifically, the `WPA*01` lines contain the same information that our `crack_pmkid.py` script needs to crack passwords based on PMKID. They are of the form:

```
WPA*01*PMKID*MAC_AP*MAC_CLIENT*ESSID***MESSAGEPAIR
```
<br/>  

That means you can test hashcat `WPA*01` examples with `crack_pmkid.py`.

Here are a couple `WPA*01` hash line examples from the hashcat forums (<a href="https://hashcat.net/forum/thread-10548.html">Source 1</a>, <a href="https://hashcat.net/forum/thread-10414.html"> Source 2</a>):
1. `WPA*01*ca5396d611cf330aebefd48ebbfb0e63*020000000001*020000000020*61703031`
   
2. `WPA*01*5ce7ebe97a1bbfeb2822ae627b726d5b*27462da350ac*accd10fb464e*686173686361742d6573736964`

Let's use #1 as an example:
- The PMKID is `ca5396d611cf330aebefd48ebbfb0e63`
- The SSID (ESSID) in hex values is `61703031` which if you convert to ascii is `ap01` (<a href="https://www.rapidtables.com/convert/number/hex-to-ascii.html">hex to ascii converter</a>)
- The MAC_AP is `020000000001`
- The MAC_CLIENT is `020000000020`

To use this in our `crack_pmkid.py` script we can run:
```
python3 crack_pmkid.py ca5396d611cf330aebefd48ebbfb0e63 "ap01" 020000000001 020000000020
```
Similarly for #2 you could run:
```
python3 crack_pmkid.py 5ce7ebe97a1bbfeb2822ae627b726d5b "hashcat-essid" 27462da350ac accd10fb464e
```
Our sample password list is enough to successfully crack both of these examples. And of course you can always supply your own list. 
<br/>  
<br/>  


## Acknowledgements
`passlist.txt` is a sample list taken from the top 100 most common passwords put together by Daniel Miessler. I've added "hashcat!" to the list for the example hash. See the original list here:
https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-100.txt

<br/>

# More ZDA Code and Resources:
**Learn Reverse Engineering, Assembly, Code Injection and More:**  
🎓  <a href="https://zerodayarcade.com/tutorials">zerodayarcade.com/tutorials</a> 

**More WiFi Hacking with Simple Python Scripts:**  
<a href="https://github.com/ZeroDayArcade/capture-pmkid-wpa-wifi-hacking">Capturing PMKID from WiFi Networks</a>  
<a href="https://github.com/ZeroDayArcade/capture-handshake-wpa-wifi-hacking">Capturing 4-Way Handshake from WPA/WPA2 Networks</a>  
<a href="https://github.com/ZeroDayArcade/cracking-wpa-with-handshake">Cracking WPA/WPA2 Passwords with 4-Way Handshake</a>

# Find Hacking Bounties in Gaming:
🎮  <a href="https://zerodayarcade.com/bounties">zerodayarcade.com/bounties</a>
