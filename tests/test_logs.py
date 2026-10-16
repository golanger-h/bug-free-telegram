import logs as log
import pytest as pt

@pt.fixture
def data():
    yield {"id": "awd"}

def test_generate_log(data):
    assert log.generate_log({})
    assert log.generate_log(data)

def test_alert_log(data):
    assert log.generate_alert({})
    assert log.generate_alert(data)