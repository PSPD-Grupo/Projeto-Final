from redaction.pseudonymize import pseudonymize

def test_mesmo_id_e_salt_gera_mesmo_hash():
    assert pseudonymize("P000001", "salt") == pseudonymize("P000001", "salt")


def test_ids_diferentes_geram_hashes_diferentes():
    assert pseudonymize("P000001", "salt") != pseudonymize("P000002", "salt")


def test_hash_tem_prefixo_padrao():
    assert pseudonymize("P000001", "salt").startswith("hash")