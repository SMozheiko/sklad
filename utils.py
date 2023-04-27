from hashlib import sha256
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