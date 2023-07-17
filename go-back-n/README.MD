The code for Part B Go Back N is present in this folder.
To run follow :
1. Open VM's terminal in this folder 

2. On terminal type :
```
sudo mn
```

3. You are now on the mininet prompt.Run below commands to open the Host terminals:
```
xterm h1
xterm h2
```
4. Commands to run on h2’s terminal to run receiver 
```
make receiver 
python3 CS20BTECH11006_receiverGBN.py
```
5. Command to run on  h1’s terminal to run sender 
```
make sender
python3 CS20BTECH11006_senderGBN.py
```
