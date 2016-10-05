from TRX import TRX


def setup():
    print "SETUP!"


def teardown():
    print "TEAR DOWN!"


def test_entity_creation():
    entity = TRX.MaltegoEntity()
    assert isinstance(entity, TRX.MaltegoEntity)
