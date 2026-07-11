import os
from dataclasses import dataclass

@dataclass
class Settings:
        grpc_port: int = int(os.getenv("GRPC_PORT", "50053"))
        metrics_port: int = int(os.getenv("METRICS_PORT", "9103"))
        jwt_secret: str = os.getenv("JWT_SECRET", "")
        pseudonymize_salt: str = os.getenv("PSEUDONYMIZE_SALT", "")

        def __post_init__(self):
            if not self.jwt_secret:
                raise ValueError("JWT_SECRET não configurado")
            if not self.pseudonymize_salt:
                raise ValueError("PSEUDONYMIZE_SALT não configurado")