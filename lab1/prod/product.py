import wmi

ALPHA = 'abcdefghijklmnopqrstuvwxyz'.upper()

filename = 'key'
step = 2

def get_disk_serial():
    c = wmi.WMI()
    for item in c.Win32_DiskDrive():
        serial = item.SerialNumber

    serial = serial.replace('-', '')
    serial = serial.replace(' ', '')
    return serial

def read_from_file(filename):
    try:
        key_file = open(filename, "r")
    except FileNotFoundError:
        #todo тут типа лог
        return
        
    text = key_file.read()
    key_file.close()
    return text

def decode(text, step):
    decoded = text.translate(str.maketrans(ALPHA[step:] + ALPHA[:step], ALPHA))
    
    return decoded

def func():
    print('Hello world!!!')

serial = get_disk_serial()
encoded_key = read_from_file(filename)
if encoded_key:
    decoded_key = decode(encoded_key, step)

    if serial == decoded_key[10:24]:
        print('Я узнаю этот компьютер!')
        func()
    else:
        print('Ключ не опознан!')
else:
    print('File key not found!')

wait = input()
