# Python One-Way Communication
One-way communication using PyAudio and RTP

## Description
One-way communication using PyAudio, a python library that provides code to record and playback audio, and Real-time Transport Protocol.

## How-To
In order to run this program, you will need to have installed PyAudio onto your computer.
```bash
pip install pyaudio
```
Once installed, you have two ways you can go about testing/running these programs...

### Loopback/One device
With your device's loopback, you can act as both the sender and the receiver. Open two command prompts and head to where you downloaded the folder.
```bash
cd /Downloads/python-one-way-communication
```
On one cmd prompt, run the Receiver.py program with your loopback IP address and your choice of port number, eg.) 9999
```bash
python Receiver.py 127.0.0.1 9999
```
On the other, run the Sender.py program with the same IP address and port number
```bash
python Sender.py 127.0.0.1 9999
```
Use Ctrl-C on Receiver.py, then Sender.py, in order to stop both programs.

### Two devices on the same network
This approach is somewhat similar to using a Loopback. Open one command prompt on both devices and head to where you downloaded the folder.
```bash
cd /Downloads/python-one-way-communication
```
On one cmd prompt, run the Receiver.py program with the IP address of the Receiver and your choice of port number, eg.) 9999
```bash
python Receiver.py 192.168.1.50 9999
```
On the other, run the Sender.py program with the same IP address and port number
```bash
python Sender.py 192.168.1.50 9999
```
Use Ctrl-C on Receiver.py, then Sender.py, in order to stop both programs.

## Note
### Tested on:
- Windows 10/11 machine
### Dependencies
- Python3
- Pip
- PyAudio
