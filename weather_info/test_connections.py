from django.test import TestCase
from .apps import get_data_from_cwb

def test_get_data_from_cwb():
    result = get_data_from_cwb()
    assert result == True

