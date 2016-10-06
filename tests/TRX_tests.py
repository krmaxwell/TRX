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
    assert isinstance(entity.additionalFields, dict)
    assert entity.additionalFields.keys() == ["ipaddress.internal"]
    assert isinstance(entity.additionalFields['ipaddress.internal'], TRX.Property)
    assert entity.additionalFields["ipaddress.internal"].value == "True"
    assert isinstance(entity.returnEntity(), str)


def test_entity_displayinfo():
    entity = TRX.MaltegoEntity()
    entity.addDisplayInformation("TestValue", "TestLabel")
    assert len(entity.displayInformation) == 1
    assert isinstance(entity.displayInformation, dict)
    assert entity.displayInformation.keys() == ["TestLabel"]
    assert entity.displayInformation['TestLabel'] == "TestValue"


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


def test_transform_add_ui_msg():
    xform = TRX.MaltegoTransform()
    xform.addUIMessage("Test Message", TRX.UIM_DEBUG)
    assert len(xform.UIMessages) == 1
    assert isinstance(xform.UIMessages[0], TRX.UIMessage)
    assert xform.UIMessages[0].messageType == TRX.UIM_DEBUG
    assert xform.UIMessages[0].message == "Test Message"


def test_transform_throw_exception():
    xform = TRX.MaltegoTransform()
    xform.addException("Test Exception")
    e = xform.throwExceptions()
    assert isinstance(e, str)
    test_e = "<MaltegoMessage><MaltegoTransformExceptionMessage><Exceptions><Exception>Test Exception</Exception></Exceptions></MaltegoTransformExceptionMessage></MaltegoMessage>"
    # TODO: better to do this with XPath or something
    print e
    assert e == test_e
