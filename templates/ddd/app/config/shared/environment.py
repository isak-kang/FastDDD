from enum import Enum


class Environment(str, Enum):
    LOCAL = "local"
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"

    @property
    def is_development(self) -> bool:
        return self in {Environment.LOCAL, Environment.DEV}

    @property
    def is_production(self) -> bool:
        return self in {Environment.STAGING, Environment.PROD}
