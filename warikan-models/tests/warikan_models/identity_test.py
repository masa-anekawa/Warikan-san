import pytest
import copy

from src.warikan_models.identity import Identity

def test_identity_is_value_object(identity_1):
    copied_identity = copy.deepcopy(identity_1)
    assert copied_identity == identity_1


def test_identity_hash_ignores_hashed_password(identity_1):
    updated_identity = Identity(email=identity_1.email, hashed_password='new_hashed_password')
    assert hash(identity_1) == hash(updated_identity)
