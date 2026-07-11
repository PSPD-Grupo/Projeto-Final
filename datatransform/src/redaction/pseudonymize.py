import hashlib

def pseudonymize(patient_id: str, salt: str) -> str:
    digest = hashlib.sha256(f"{salt}{patient_id}".encode()).hexdigest()[:8]
    return f"hash{digest}"