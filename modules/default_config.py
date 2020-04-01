from dataclasses import dataclass
from typing import Optional


@dataclass
class UserConfig:
    email: str
    """
    Email used for Roman account.
    """

    password: str
    """
    Password to Roman account.
    """

    service_name: Optional[str]
    """
    Name of the service in the Roman.
    """

    bot_summary: Optional[str]
    """
    Summary displayed in the Wire UI. 
    """

    env: Optional[str]
    """
    Defines which environment configuration should be used. If no is selected, LocalConfig is used.
    """

    roman_url: Optional[str]
    """
    Overwrites used environment.
    """

    charon_url: Optional[str]
    """
    Overwrites used environment.
    """


@dataclass
class Config:
    service_name: str = 'Webhook Bot'
    bot_summary: str = 'Webhooks sent to the conversations.'


@dataclass
class LocalConfig(Config):
    roman_url: str = 'http://proxy.services.zinfra.io'
    charon_url: str = 'http://localhost:8080'


@dataclass
class StagingConfig(Config):
    roman_url: str = 'http://proxy.services.zinfra.io'
    charon_url: str = 'http://charon.services.zinfra.io'


@dataclass
class ProdConfig(Config):
    roman_url: str = 'http://proxy.services.wire.com'
    charon_url: str = 'http://charon.services.wire.com'
