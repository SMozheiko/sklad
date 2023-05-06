import random
from hashlib import sha256
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
import os.path

from jinja2 import FileSystemLoader, Environment

from settings import settings


def render(template_path: str, template_name: str, context: dict) -> str:
    loader = FileSystemLoader(os.path.join(settings.base_templates_path, template_path))
    environment = Environment(loader=loader)
    template = loader.load(environment, template_name)
    return template.render(context)


def get_hashed_password(password: str) -> str:
    salt = sha256(password.encode()).hexdigest() + password
    return sha256(salt.encode()).hexdigest()


def get_code():
    numbers = list(range(10))
    code = ''
    for i in range(4):
        code += str(random.choice(numbers))
    return code


def send_code(code: str, address: str) -> bool:
    message = 'Код подтверждения сброса пароля: {}'.format(code)
    try:
        send_email(address, message)
    except Exception as e:
        print(str(e))
        return False
    return True


def send_password(password: str, address: str):
    message = 'Добро пожаловать в команду! Твой пароль: {}'.format(password)
    send_email(address, message)


def send_email(address: str, msg: str):
    mail_from = settings.notifY_email
    mail_to = address
    message = "------START------\nFrom: {}\nTo: {}\n\n{}\n------END------".format(mail_from, mail_to, msg)
    print(message)


def generate_password():
    password = ''
    while len(password) < 10:
        password += random.choice(ascii_uppercase + ascii_lowercase + digits + punctuation)
    return password
