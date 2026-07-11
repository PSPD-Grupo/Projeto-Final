import pytest
from auth.access_level import resolve_access_level, AccessLevel, NoAccessLevelError
from auth.jwt_decoder import TokenClaims


def claims(**kwargs):
    defaults = dict(full=False, partial=False, anonymized=False, aggregated=False, exp=0)
    defaults.update(kwargs)
    return TokenClaims(**defaults)


def test_full_tem_prioridade_maxima():
    assert resolve_access_level(claims(full=True, aggregated=True)) == AccessLevel.FULL


def test_aggregated_isolado():
    assert resolve_access_level(claims(aggregated=True)) == AccessLevel.AGGREGATED


def test_nenhuma_permissao_gera_erro():
    with pytest.raises(NoAccessLevelError):
        resolve_access_level(claims())