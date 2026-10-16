import parser as pars
import pytest as pt
import json as js

def test_is_anomaly():
    assert pars.is_anomaly({"alerts": True}) == True
    assert pars.is_anomaly({}) == False

@pt.fixture
def test_info_fixture():
    data = js.dumps({"alerts": True, "id": "test_id"}, )
    yield js.loads(data)

def test_pars_json_from_decoded_payload(test_info_fixture):
    assert pars.pars_json_from_decoded_payload("")['rc'] == -1
    assert pars.pars_json_from_decoded_payload(test_info_fixture)['rc'] == -1

def test_data_generator():
    assert pars.data_generator("")


