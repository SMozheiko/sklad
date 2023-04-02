import os.path

from jinja2 import FileSystemLoader, Environment

from settings import settings


def render(template_path: str, template_name: str, context: dict) -> str:
    loader = FileSystemLoader(os.path.join(settings.base_templates_path, template_path))
    environment = Environment(loader=loader)
    template = loader.load(environment, template_name)
    return template.render(context)
