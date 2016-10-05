from TRX import TRX


def setup():
    print "SETUP!"


def teardown():
    print "TEAR DOWN!"


def test_entity_creation():
    entity = TRX.MaltegoEntity()
    assert isinstance(entity, TRX.MaltegoEntity)


def test_entity_default_type():
    entity = TRX.MaltegoEntity()
    assert entity.entityType == "Phrase"


def test_entity_default_value():
    entity = TRX.MaltegoEntity()
    assert entity.value == ""


def test_entity_set_type():
    entity = TRX.MaltegoEntity("IPv4Address")
    assert entity.entityType == "IPv4Address"


def test_entity_set_value():
    entity = TRX.MaltegoEntity("IPv4Address", "127.0.0.1")
    # FIXME: the below matches the library but not the documentation!
    assert entity.value == "127.0.0.1"
