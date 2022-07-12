from time import sleep
from os import system
system('kill 1')
print('kill')
sleep(7)
print('sleep')
system("python main.py")
print('error')