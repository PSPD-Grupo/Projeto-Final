import os


class Settings:
    servidor_auth_host: str
    servidor_b_host: str
    servidor_datatransform_host: str

    def __init__(self) -> None:
        self.servidor_auth_host = os.getenv("SERVIDOR_AUTH_HOST", "localhost:50054")
        self.servidor_b_host = os.getenv("SERVIDOR_B_HOST", "localhost:50052")
        self.servidor_datatransform_host = os.getenv("SERVIDOR_DATATRANSFORM_HOST", "localhost:50053")
        print("AUTH:", self.servidor_auth_host)
        print("DATA:", self.servidor_b_host)
        print("TRANSFORM:", self.servidor_datatransform_host)

settings = Settings()