#Метод str.translate() возвращает копию строки, в которой каждый
#символ был сопоставлен и преобразован согласно карте перевода символов table.

#Windows Management Instrumentation — технология, которая позволяет управлять компонентами и параметрами Windows.
#Дает возможность изменять различные параметры операционной системы, управлять общими ресурсами, запрашивать
#информацию об установленных устройствах, запущенных процессах и т.д.

import wmi
import random
import string

ALPHA = 'abcdefghijklmnopqrstuvwxyz'.upper()

filename = 'key'
step = 2

def random_str(size):
    symb_list = []
    for i in range(size):
        symb = random.choice(string.ascii_letters + string.digits)
        symb_list += [symb.upper()]
    return ''.join(symb_list)
 
def encode(text, step):
    text = text.replace('-', '')
    text = text.replace(' ', '')
    
    encoded = text.translate(str.maketrans(ALPHA, ALPHA[step:] + ALPHA[:step]))
    encoded = random_str(10) + encoded + random_str(10)
    
    return encoded

def get_disk_serial():
    c = wmi.WMI()
    for item in c.Win32_DiskDrive():
        return(item.SerialNumber)

def write_to_file(filename, text):
    key_file = open(filename, 'w')
    key_file.write(text)
    key_file.close()

serial = get_disk_serial()
encoded_serial = encode(serial, step)
write_to_file(filename, encoded_serial)
print('Key was successfully created')

wait = input()
