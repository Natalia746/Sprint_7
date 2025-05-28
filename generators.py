
import random
import string
import time



def generate_random_string(length):
    """Генерация случайной строки из букв нижнего регистра"""
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generate_unique_login ():
    unique_login = f"user_{int(time.time() * 1000)}_{generate_random_string(4)}"
    return unique_login

