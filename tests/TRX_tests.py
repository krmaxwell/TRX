# -*- coding: utf-8 -*-

import xmltodict
from nose.tools import assert_equal
from nose.tools import assert_is_instance
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
    out = xmltodict.parse(entity.returnEntity())
    assert_equal(out['Entity']['Value'], "Maltego")


def test_entity_weight():
    entity = TRX.MaltegoEntity()
    entity.setWeight(100)
    assert_equal(entity.weight, 100)
    out = xmltodict.parse(entity.returnEntity())
    assert_equal(out['Entity']['Weight'], "100")


def test_entity_iconurl():
    entity = TRX.MaltegoEntity()
    url = "http://cdn.slidesharecdn.com/profile-photo-VerisignInc-48x48.jpg"
    entity.setIconURL(url)
    assert_equal(entity.iconURL, url)
    out = xmltodict.parse(entity.returnEntity())
    assert_equal(out['Entity']['IconURL'], url)


def test_entity_property_count():
    entity = TRX.MaltegoEntity("IPv4Address", "10.0.0.1")
    entity.addProperty("ipaddress.internal", value="True")
    assert_equal(len(entity.additionalFields), 1)


def test_entity_property_dict():
    entity = TRX.MaltegoEntity("IPv4Address", "10.0.0.1")
    entity.addProperty("ipaddress.internal", value="True")
    assert_is_instance(entity.additionalFields, dict)
    assert_equal(entity.additionalFields.keys(), ["ipaddress.internal"])


def test_entity_property_results():
    entity = TRX.MaltegoEntity("IPv4Address", "10.0.0.1")
    entity.addProperty("ipaddress.internal", value="True")
    assert_is_instance(entity.additionalFields['ipaddress.internal'], TRX.Property)
    # NOTE: The following tests for the string "True", not the bool True
    assert_equal(entity.additionalFields["ipaddress.internal"].value, "True")


def test_entity_displayinfo_count():
    entity = TRX.MaltegoEntity()
    entity.addDisplayInformation("TestValue", "TestLabel")
    assert_equal(len(entity.displayInformation), 1)
    assert_is_instance(entity.displayInformation, dict)


def test_entity_displayinfo_dict():
    entity = TRX.MaltegoEntity()
    entity.addDisplayInformation("TestValue", "TestLabel")
    assert_equal(entity.displayInformation.keys(), ["TestLabel"])
    assert_equal(entity.displayInformation['TestLabel'], "TestValue")


def test_entity_displayinfo_results():
    entity = TRX.MaltegoEntity()
    entity.addDisplayInformation("TestValue", "TestLabel")
    r = xmltodict.parse(entity.returnEntity())
    assert_equal(r['Entity']['DisplayInformation']['Label']['@Name'], "TestLabel")
    assert_equal(r['Entity']['DisplayInformation']['Label']['#text'], "TestValue")


def test_entity_unicode():
    entity = TRX.MaltegoEntity("Phrase", u"Файлы локализации")
    entity.addProperty("Test Property", u"Инструкция по локализации")
    assert_is_instance(entity.returnEntity(), unicode)


def test_entity_link_color():
    entity = TRX.MaltegoEntity()
    color = '0xff00ff'
    entity.setLinkColor(color)
    out = xmltodict.parse(entity.returnEntity())
    assert_equal(entity.additionalFields['link#maltego.link.color'].value, color)
    assert_equal(out['Entity']['AdditionalFields']['Field']['#text'], color)


def test_entity_link_style():
    entity = TRX.MaltegoEntity()
    entity.setLinkStyle(TRX.LINK_STYLE_DASHED)
    out = xmltodict.parse(entity.returnEntity())
    assert_equal(entity.additionalFields['link#maltego.link.style'].value, "1")
    assert_equal(out['Entity']['AdditionalFields']['Field']['#text'], "1")


def test_entity_link_thickness():
    entity = TRX.MaltegoEntity()
    entity.setLinkThickness(42)
    out = xmltodict.parse(entity.returnEntity())
    assert_equal(entity.additionalFields['link#maltego.link.thickness'].value, "42")
    assert_equal(out['Entity']['AdditionalFields']['Field']['#text'], "42")


def test_entity_link_label():
    entity = TRX.MaltegoEntity()
    label = "Test Label"
    entity.setLinkLabel(label)
    out = xmltodict.parse(entity.returnEntity())
    assert_equal(entity.additionalFields['link#maltego.link.label'].value, label)
    assert_equal(out['Entity']['AdditionalFields']['Field']['#text'], label)


def test_entity_bookmark():
    entity = TRX.MaltegoEntity()
    entity.setBookmark(TRX.BOOKMARK_COLOR_GREEN)
    out = xmltodict.parse(entity.returnEntity())
    assert_equal(entity.additionalFields['bookmark#'].value, "1")
    assert_equal(out['Entity']['AdditionalFields']['Field']['#text'], "1")


def test_entity_note():
    entity = TRX.MaltegoEntity()
    note = "Test Note"
    entity.setNote(note)
    out = xmltodict.parse(entity.returnEntity())
    assert_equal(entity.additionalFields['notes#'].value, note)
    assert_equal(out['Entity']['AdditionalFields']['Field']['#text'], note)


def test_entity_strict():
    entity = TRX.MaltegoEntity()
    entity.addProperty('test', matchingRule="strict", value="StrictTest")
    out = xmltodict.parse(entity.returnEntity())
    assert_equal(entity.additionalFields['test'].matchingRule, "strict")
    assert_equal(out['Entity']['AdditionalFields']['Field']['@MatchingRule'], 'strict')


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


def test_transform_uimsg_count():
    xform = TRX.MaltegoTransform()
    xform.addUIMessage("Test Message", TRX.UIM_DEBUG)
    assert_equal(len(xform.UIMessages), 1)
    assert_is_instance(xform.UIMessages[0], TRX.UIMessage)


def test_transform_uimsg_dict():
    xform = TRX.MaltegoTransform()
    xform.addUIMessage("Test Message", TRX.UIM_DEBUG)
    assert_equal(xform.UIMessages[0].messageType, 'Debug')
    assert_equal(xform.UIMessages[0].message, "Test Message")


def test_transform_uimsg_result():
    xform = TRX.MaltegoTransform()
    xform.addUIMessage("Test Message", TRX.UIM_DEBUG)
    out = xmltodict.parse(xform.returnOutput())
    assert_is_instance(out, dict)
    assert_equal(out['MaltegoMessage']['MaltegoTransformResponseMessage']['UIMessages']['UIMessage']['@MessageType'], 'Debug')
    assert_equal(out['MaltegoMessage']['MaltegoTransformResponseMessage']['UIMessages']['UIMessage']['#text'], 'Test Message')


def test_transform_exception_str():
    xform = TRX.MaltegoTransform()
    xform.addException("Test Exception")
    e = xform.throwExceptions()
    assert_is_instance(e, str)


def test_transform_exception_result():
    xform = TRX.MaltegoTransform()
    xform.addException("Test Exception")
    e_data = xmltodict.parse(xform.throwExceptions())
    assert_is_instance(e_data, dict)
    assert_equal(e_data['MaltegoMessage']['MaltegoTransformExceptionMessage']['Exceptions']['Exception'], "Test Exception")


def test_msg_creation():
    m = TRX.MaltegoMsg()
    assert_is_instance(m, TRX.MaltegoMsg)
