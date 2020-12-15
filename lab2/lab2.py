#
# Вторая лабораторная по защите информации. Шифровальная машина Энигма
#

from random import shuffle, randint        

class File():

    def __init__(self, fname):
        self.__name = fname
    
    def write(self, text):
        handle = open(self.__name, "w")
        handle.write(text)
        handle.close()

    def read(self):
        handle = open(self.__name, "r")
        data = handle.read()
        handle.close()
        return data

    def write_as_byte(self, text):
        handle = open(self.__name, "wb")
        handle.write(text)
        handle.close()

    def read_as_byte(self):
        handle = open(self.__name, "rb")
        data = handle.read()
        handle.close()
        return data


class Rotor():

    def __init__(self, rotor_name, state_file_name=None):
        self.__rotor_name = rotor_name
        self.__state_file_name = state_file_name

        if self.__state_file_name:
            self.load_state()
        else:
            self.__numbers = [i for i in range(256)]
            shuffle(self.__numbers)
            self.__rotation_flag = randint(0, 255)
            self.__position = 0
            self.__reverse__numbers = self.__swap_index_and_value(self.__numbers)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, pos):
        pos %= 256
        self.__position = pos

    @property
    def straight__numbers(self):
        return self.__numbers

    @property
    def rotation_flag(self):
        return self.__rotation_flag

    @property
    def reverse__numbers(self):
        return self.__reverse__numbers

    def __swap_index_and_value(self, lst):
        swap_list = [0 for i in range(len(lst))]
        counter = 0
        for i in lst:
            swap_list[i] = counter
            counter += 1
        return swap_list

    def get_pair_straight(self, num):
        if 0 <= num <= 255: 
            return self.__numbers[num]
        else:
            raise Exception('Num must be between 0 and 255')

    def get_pair_reverse(self, num):
        if 0 <= num <= 255:
            return self.__reverse__numbers[num]
        else:
            raise Exception('Num must be between 0 and 255')

    def save_state(self):
        file_handler = File(self.__rotor_name + ' rotor state')
        numbers_state = ' '.join(str(num) for num in self.__numbers)
        reverse__numbers_state = ' '.join(
            str(num) for num in self.__reverse__numbers
            )
        rotation_flag = str(self.__rotation_flag)
        position = str(self.__position)
        
        file_handler.write(
            numbers_state + '\n' +
            reverse__numbers_state + '\n' +
            rotation_flag + '\n' +
            position + '\n'
            )

    def load_state(self):
        file_handler = File(self.__state_file_name)
        text = file_handler.read()
        states_list = text.split('\n')
        self.__numbers = [int(num) for num in states_list[0].split()]
        self.__reverse__numbers = [int(num) for num in states_list[1].split()]
        self.__rotation_flag = int(states_list[2])
        self.__position = int(states_list[3])
        

class Reflector():
    
    def __init__(self, state_file_name=None):
        self.__state_file_name = state_file_name

        if self.__state_file_name:
            self.load_state()
        else:
            self.__numbers = [i for i in range(256)]
            shuffle(self.__numbers)
            self.__numbers = self.create_reflector_numbers(self.__numbers)

    def create_reflector_numbers(self, random_nums):
        res = [-1 for i in range(len(random_nums))]

        i = 0
        while random_nums:
            random_num = random_nums[0]
            while res[i] != -1:
                i += 1
            res[i] = random_num
            res[random_num] = i
            if i in random_nums:
                random_nums.remove(i)
            if random_num in random_nums:
                random_nums.remove(random_num)
            i += 1
        return res

    def save_state(self):
        file_handler = File('reflector state')
        numbers_state = ' '.join(str(num) for num in self.__numbers)
        file_handler.write(numbers_state)

    def load_state(self):
        file_handler = File(self.__state_file_name)
        numbers_state_str = file_handler.read()
        numbers_state_list = numbers_state_str.split()
        numbers_state = [int(num) for num in numbers_state_list]
        self.__numbers = numbers_state

    def get_pair(self, num):
        if 0 <= num <= 255: 
            return self.__numbers[num]
        else:
            raise Exception('Num must be between 0 and 255')


class Enigma():

    def __init__(self, rotors, reflector):
        self.__rotors = rotors
        self.__reflector = reflector

    def setup_rotors(self, pos1, pos2, pos3):
        positions = [pos1, pos2, pos3]
        for i in range(3):
            if 0 <= positions[i] <= 255:
                self._rotors[i].position = positions[i]
            else:
                raise Exception('The rotor position must be between 0 and 255')
    
    def encrypt(self, plainbytes):
        ciphertext_list = []
        for byte in plainbytes:
            # со входа на 1-й ротор
            self.__rotors[0].position += 1
            cipherbyte = byte + self.__rotors[0].position
            cipherbyte %= 256
            cipherbyte = self.__rotors[0].get_pair_straight(cipherbyte)
            
            # с 1-го роторна на 2-й ротор
            if self.__rotors[0].position == self.__rotors[0].rotation_flag:
                self.__rotors[1].position += 1
            cipherbyte += (self.__rotors[1].position - self.__rotors[0].position) % 256
            cipherbyte %= 256
            cipherbyte = self.__rotors[1].get_pair_straight(cipherbyte)

            # со 2-го ротора на 3-й ротор
            if self.__rotors[1].position == self.__rotors[1].rotation_flag:
                self.__rotors[2].position += 1
            cipherbyte += (self.__rotors[2].position - self.__rotors[1].position) % 256
            cipherbyte %= 256
            cipherbyte = self.__rotors[2].get_pair_straight(cipherbyte)

            # с 3-го ротора на рефлектор
            cipherbyte = (cipherbyte - self.__rotors[2].position) % 256
            cipherbyte = self.__reflector.get_pair(cipherbyte)
            
            # обратный ход
            
            # с рефлектора на 3-й ротор
            cipherbyte += self.__rotors[2].position
            cipherbyte %= 256
            cipherbyte = self.__rotors[2].get_pair_reverse(cipherbyte)

            # с 3-го ротора на 2-й ротор
            cipherbyte -= (self.__rotors[2].position - self.__rotors[1].position) % 256
            cipherbyte %= 256
            cipherbyte = self.__rotors[1].get_pair_reverse(cipherbyte)

            # со 2-го ротора на 1-й ротор
            cipherbyte -= (self.__rotors[1].position - self.__rotors[0].position) % 256
            cipherbyte %= 256
            cipherbyte = self.__rotors[0].get_pair_reverse(cipherbyte)

            # с 1-го ротора на выход
            cipherbyte -= self.__rotors[0].position
            cipherbyte %= 256

            ciphertext_list.append(cipherbyte)
            
        ciphertext = bytes(ciphertext_list)
        return ciphertext
            
      
def encrypt_file(filename):
    reflector = Reflector()
    reflector.save_state()
    rotors = []
    for i in range(3):
       rotors.append(Rotor(str(i)))
       rotors[i].save_state()

    #rotors[0].position = rotors[0].rotation_flag - 1
    #rotors[0].save_state()

    enigma = Enigma(rotors, reflector)

    file_handler = File(filename)
    data = file_handler.read_as_byte()

    new_file_handler = File('encrypted_data')
    encrypted_data = enigma.encrypt(data)
    new_file_handler.write_as_byte(encrypted_data)

def decrypt_file(output_name='decrypted_data'):
    reflector = Reflector(state_file_name='reflector state')
    rotors = [
        Rotor('0', state_file_name='0 rotor state'),
        Rotor('1', state_file_name='1 rotor state'),
        Rotor('2', state_file_name='2 rotor state')
        ]
    enigma = Enigma(rotors, reflector)

    file_handler = File('encrypted_data')
    data = file_handler.read_as_byte()

    new_file_handler = File(output_name)
    decrypted_data = enigma.encrypt(data)
    new_file_handler.write_as_byte(decrypted_data)
    
if __name__ == '__main__':
    encrypt_file('plaindata.zip')
    decrypt_file('decrypted_data.zip')
    
