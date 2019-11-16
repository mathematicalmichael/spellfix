import make_names as mkn
import pytest
from faker import Factory
faker = Factory.create()

def test_delete_char():
    with pytest.raises(TypeError):
        mkn.delete_char(1)
    for _ in range(100):
        name = faker.company()
        target_len = len(name) - 1
        assert len(mkn.delete_char(name)) == target_len

