# -*- coding: utf-8 -*-

from nose.tools import assert_equal, assert_is_instance
from TRX import TRX


def setup():
    print "SETUP!"


def teardown():
    print "TEAR DOWN!"


def test_entity_creation():
    entity = TRX.MaltegoEntity()
    assert_is_instance(entity, TRX.MaltegoEntity)


def test_entity_default_type():
    entity = TRX.MaltegoEntity()
    assert_equal(entity.entityType, "Phrase")


def test_entity_default_value():
    entity = TRX.MaltegoEntity()
    assert_equal(entity.value, "")


def test_entity_init_type():
    entity = TRX.MaltegoEntity("IPv4Address")
    assert_equal(entity.entityType, "IPv4Address")


def test_entity_set_type():
    entity = TRX.MaltegoEntity()
    entity.setType("Location")
    assert_equal(entity.entityType, "Location")


def test_entity_init_value():
    entity = TRX.MaltegoEntity("IPv4Address", "127.0.0.1")
    # FIXME: the below matches the library but not the documentation!
    assert_equal(entity.value, "127.0.0.1")


def test_entity_set_value():
    entity = TRX.MaltegoEntity()
    entity.setValue("Maltego")
    assert_equal(entity.value, "Maltego")


def test_entity_add_property():
    entity = TRX.MaltegoEntity("IPv4Address", "10.0.0.1")
    entity.addProperty("ipaddress.internal", value="True")
    assert_equal(len(entity.additionalFields), 1)
    assert_is_instance(entity.additionalFields, dict)
    assert_equal(entity.additionalFields.keys(), ["ipaddress.internal"])
    assert_is_instance(entity.additionalFields['ipaddress.internal'], TRX.Property)
    # NOTE: The following tests for the string "True", not the bool True
    assert_equal(entity.additionalFields["ipaddress.internal"].value, "True")
    assert_is_instance(entity.returnEntity(), unicode)


def test_entity_displayinfo():
    entity = TRX.MaltegoEntity()
    entity.addDisplayInformation("TestValue", "TestLabel")
    assert_equal(len(entity.displayInformation), 1)
    assert_is_instance(entity.displayInformation, dict)
    assert_equal(entity.displayInformation.keys(), ["TestLabel"])
    assert_equal(entity.displayInformation['TestLabel'], "TestValue")


def test_entity_unicode():
    entity = TRX.MaltegoEntity("Phrase", u"Файлы локализации")
    entity.addProperty("Test Property", u"Инструкция по локализации")
    assert_is_instance(entity.returnEntity(), unicode)


def test_transform_creation():
    xform = TRX.MaltegoTransform()
    assert_is_instance(xform, TRX.MaltegoTransform)


def test_transform_add_entity():
    xform = TRX.MaltegoTransform()
    entity = xform.addEntity()
    assert_is_instance(entity, TRX.MaltegoEntity)
    assert_is_instance(xform.returnOutput(), unicode)


def test_transform_add_exception():
    xform = TRX.MaltegoTransform()
    xform.addException("Test Exception")
    assert_equal(len(xform.exceptions), 1)
    assert_equal(xform.exceptions[0], "Test Exception")


def test_transform_add_ui_msg():
    xform = TRX.MaltegoTransform()
    xform.addUIMessage("Test Message", TRX.UIM_DEBUG)
    assert_equal(len(xform.UIMessages), 1)
    assert_is_instance(xform.UIMessages[0], TRX.UIMessage)
    assert_equal(xform.UIMessages[0].messageType, TRX.UIM_DEBUG)
    assert_equal(xform.UIMessages[0].message, "Test Message")


def test_transform_throw_exception():
    xform = TRX.MaltegoTransform()
    xform.addException("Test Exception")
    e = xform.throwExceptions()
    assert_is_instance(e, str)
    test_e = "<MaltegoMessage><MaltegoTransformExceptionMessage><Exceptions><Exception>Test Exception</Exception></Exceptions></MaltegoTransformExceptionMessage></MaltegoMessage>"
    # TODO: better to do this with XPath or something
    assert_equal(e, test_e)
