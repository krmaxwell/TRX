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


def test_entity_init_type():
    entity = TRX.MaltegoEntity("IPv4Address")
    assert entity.entityType == "IPv4Address"


def test_entity_set_type():
    entity = TRX.MaltegoEntity()
    entity.setType("Location")
    assert entity.entityType == "Location"


def test_entity_init_value():
    entity = TRX.MaltegoEntity("IPv4Address", "127.0.0.1")
    # FIXME: the below matches the library but not the documentation!
    assert entity.value == "127.0.0.1"


def test_entity_set_value():
    entity = TRX.MaltegoEntity()
    entity.setValue("Maltego")
    assert entity.value == "Maltego"


def test_entity_add_property():
    entity = TRX.MaltegoEntity("IPv4Address", "10.0.0.1")
    entity.addProperty("ipaddress.internal", value="True")
    assert len(entity.additionalFields) == 1
    assert entity.additionalFields.keys() == ["ipaddress.internal"]
    assert entity.additionalFields["ipaddress.internal"]["value"] == "True"


def test_transform_creation():
    xform = TRX.MaltegoTransform()
    assert isinstance(xform, TRX.MaltegoTransform)


def test_transform_add_entity():
    xform = TRX.MaltegoTransform()
    entity = xform.addEntity()
    assert isinstance(entity, TRX.MaltegoEntity)


def test_transform_add_exception():
    xform = TRX.MaltegoTransform()
    xform.addException("Test Exception")
    assert len(xform.exceptions) == 1
    assert xform.exceptions[0] == "Test Exception"
