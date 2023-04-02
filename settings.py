from pathlib import Path


class Settings:

    debug: bool = True
    base_templates_path: str = f'{Path(__file__).resolve().parent}/frontend/templates'


settings = Settings()

