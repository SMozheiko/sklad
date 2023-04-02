from pathlib import Path


class DBSettings:
    driver: str = ''
    dialect: str = 'sqlite'
    user: str = ''
    password: str = ''
    host: str = ''
    port: str = ''
    name: str = 'db.sqlite3'

    def get_src(self) -> str:
        return '{}{}://{}{}{}{}/{}'.format(
           self.dialect,
           f'+{self.driver}' if self.driver else self.driver,
           self.user or self.user,
           f':{self.password}' if self.password else self.password,
           f'@{self.host}' if self.host else self.host,
           f':{self.port}' if self.port else self.port,
           self.name
        )


class Settings:

    debug: bool = True
    base_templates_path: str = f'{Path(__file__).resolve().parent}/frontend/templates'


settings = Settings()
db_settings = DBSettings()
