# -*- coding: utf-8 -*-

import unittest

import xmltodict
from nose.tools import assert_equal
from nose.tools import assert_is_instance
from TRX import TRX


class TestMaltegoEntity(unittest.TestCase):

    def test_entity_creation(self):
        entity = TRX.MaltegoEntity()
        assert_is_instance(entity, TRX.MaltegoEntity)

    def test_entity_default_type(self):
        entity = TRX.MaltegoEntity()
        assert_equal(entity.entityType, "Phrase")

    def test_entity_default_value(self):
        entity = TRX.MaltegoEntity()
        assert_equal(entity.value, "")

    def test_entity_init_type(self):
        entity = TRX.MaltegoEntity("IPv4Address")
        assert_equal(entity.entityType, "IPv4Address")

    def test_entity_set_type(self):
        entity = TRX.MaltegoEntity()
        entity.setType("Location")
        assert_equal(entity.entityType, "Location")

    def test_entity_init_value(self):
        entity = TRX.MaltegoEntity("IPv4Address", "127.0.0.1")
        # FIXME: the below matches the library but not the documentation!
        assert_equal(entity.value, "127.0.0.1")

    def test_entity_set_value(self):
        entity = TRX.MaltegoEntity()
        entity.setValue("Maltego")
        assert_equal(entity.value, "Maltego")
        out = xmltodict.parse(entity.returnEntity())
        assert_equal(out['Entity']['Value'], "Maltego")

    def test_entity_weight(self):
        entity = TRX.MaltegoEntity()
        entity.setWeight(100)
        assert_equal(entity.weight, 100)
        out = xmltodict.parse(entity.returnEntity())
        assert_equal(out['Entity']['Weight'], "100")

    def test_entity_iconurl(self):
        entity = TRX.MaltegoEntity()
        url = "http://example.com/example.png"
        entity.setIconURL(url)
        assert_equal(entity.iconURL, url)
        out = xmltodict.parse(entity.returnEntity())
        assert_equal(out['Entity']['IconURL'], url)

    def test_entity_property_count(self):
        entity = TRX.MaltegoEntity("IPv4Address", "10.0.0.1")
        entity.addProperty("ipaddress.internal", value="True")
        assert_equal(len(entity.additionalFields), 1)

    def test_entity_property_dict(self):
        entity = TRX.MaltegoEntity("IPv4Address", "10.0.0.1")
        entity.addProperty("ipaddress.internal", value="True")
        assert_is_instance(entity.additionalFields, dict)
        assert_equal(entity.additionalFields.keys(), ["ipaddress.internal"])

    def test_entity_property_results(self):
        entity = TRX.MaltegoEntity("IPv4Address", "10.0.0.1")
        entity.addProperty("ipaddress.internal", value="True")
        assert_is_instance(entity.additionalFields['ipaddress.internal'], TRX.Property)
        # NOTE: The following tests for the string "True", not the bool True
        assert_equal(entity.additionalFields["ipaddress.internal"].value, "True")

    def test_entity_displayinfo_count(self):
        entity = TRX.MaltegoEntity()
        entity.addDisplayInformation("TestValue", "TestLabel")
        assert_equal(len(entity.displayInformation), 1)
        assert_is_instance(entity.displayInformation, dict)

    def test_entity_displayinfo_dict(self):
        entity = TRX.MaltegoEntity()
        entity.addDisplayInformation("TestValue", "TestLabel")
        assert_equal(entity.displayInformation.keys(), ["TestLabel"])
        assert_equal(entity.displayInformation['TestLabel'], "TestValue")

    def test_entity_displayinfo_results(self):
        entity = TRX.MaltegoEntity()
        entity.addDisplayInformation("TestValue", "TestLabel")
        r = xmltodict.parse(entity.returnEntity())
        assert_equal(r['Entity']['DisplayInformation']['Label']['@Name'], "TestLabel")
        assert_equal(r['Entity']['DisplayInformation']['Label']['#text'], "TestValue")

    def test_entity_unicode(self):
        entity = TRX.MaltegoEntity("Phrase", u"Файлы локализации")
        entity.addProperty("Test Property", u"Инструкция по локализации")
        assert_is_instance(entity.returnEntity(), unicode)

    def test_entity_link_color(self):
        entity = TRX.MaltegoEntity()
        color = '0xff00ff'
        entity.setLinkColor(color)
        out = xmltodict.parse(entity.returnEntity())
        assert_equal(entity.additionalFields['link#maltego.link.color'].value, color)
        assert_equal(out['Entity']['AdditionalFields']['Field']['#text'], color)

    def test_entity_link_style(self):
        entity = TRX.MaltegoEntity()
        entity.setLinkStyle(TRX.LINK_STYLE_DASHED)
        out = xmltodict.parse(entity.returnEntity())
        assert_equal(entity.additionalFields['link#maltego.link.style'].value, "1")
        assert_equal(out['Entity']['AdditionalFields']['Field']['#text'], "1")

    def test_entity_link_thickness(self):
        entity = TRX.MaltegoEntity()
        entity.setLinkThickness(42)
        out = xmltodict.parse(entity.returnEntity())
        assert_equal(entity.additionalFields['link#maltego.link.thickness'].value, "42")
        assert_equal(out['Entity']['AdditionalFields']['Field']['#text'], "42")

    def test_entity_link_label(self):
        entity = TRX.MaltegoEntity()
        label = "Test Label"
        entity.setLinkLabel(label)
        out = xmltodict.parse(entity.returnEntity())
        assert_equal(entity.additionalFields['link#maltego.link.label'].value, label)
        assert_equal(out['Entity']['AdditionalFields']['Field']['#text'], label)

    def test_entity_bookmark(self):
        entity = TRX.MaltegoEntity()
        entity.setBookmark(TRX.BOOKMARK_COLOR_GREEN)
        out = xmltodict.parse(entity.returnEntity())
        assert_equal(entity.additionalFields['bookmark#'].value, "1")
        assert_equal(out['Entity']['AdditionalFields']['Field']['#text'], "1")

    def test_entity_note(self):
        entity = TRX.MaltegoEntity()
        note = "Test Note"
        entity.setNote(note)
        out = xmltodict.parse(entity.returnEntity())
        assert_equal(entity.additionalFields['notes#'].value, note)
        assert_equal(out['Entity']['AdditionalFields']['Field']['#text'], note)

    def test_entity_strict(self):
        entity = TRX.MaltegoEntity()
        entity.addProperty('test', matchingRule="strict", value="StrictTest")
        out = xmltodict.parse(entity.returnEntity())
        assert_equal(entity.additionalFields['test'].matchingRule, "strict")
        assert_equal(out['Entity']['AdditionalFields']['Field']['@MatchingRule'], 'strict')


class TestMaltegoTransform(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.xform = TRX.MaltegoTransform()

    def test_transform_creation(self):
        assert_is_instance(self.xform, TRX.MaltegoTransform)

    def test_transform_add_entity(self):
        entity = self.xform.addEntity()
        assert_is_instance(entity, TRX.MaltegoEntity)
        assert_is_instance(self.xform.returnOutput(), unicode)

    def test_transform_uimsg_count(self):
        self.xform.addUIMessage("Test Message", TRX.UIM_DEBUG)
        assert_equal(len(self.xform.UIMessages), 1)
        assert_is_instance(self.xform.UIMessages[0], TRX.UIMessage)

    def test_transform_uimsg_dict(self):
        self.xform.addUIMessage("Test Message", TRX.UIM_DEBUG)
        assert_equal(self.xform.UIMessages[0].messageType, 'Debug')
        assert_equal(self.xform.UIMessages[0].message, "Test Message")

    def test_transform_uimsg_result(self):
        self.xform.addUIMessage("Test Message", TRX.UIM_DEBUG)
        out = xmltodict.parse(self.xform.returnOutput())
        assert_is_instance(out, dict)
        assert_equal(out['MaltegoMessage']['MaltegoTransformResponseMessage']['UIMessages']['UIMessage'][0]['@MessageType'], 'Debug')
        assert_equal(out['MaltegoMessage']['MaltegoTransformResponseMessage']['UIMessages']['UIMessage'][0]['#text'], 'Test Message')

    def test_transform_exception_result(self):
        self.xform.addException("Test Exception")
        e_data = xmltodict.parse(self.xform.throwExceptions())
        assert_is_instance(e_data, dict)
        assert_equal(e_data['MaltegoMessage']['MaltegoTransformExceptionMessage']['Exceptions']['Exception'], "Test Exception")


class TestMaltegoMsg(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.m_xml = ""
        self.m_data = {}
        self.m_data['MaltegoMessage'] = {}
        self.m_data['MaltegoMessage']['MaltegoTransformRequestMessage'] = {}
        self.m_data['MaltegoMessage']['MaltegoTransformRequestMessage']['Entities'] = {}
        self.m_data['MaltegoMessage']['MaltegoTransformRequestMessage']['Limits'] = {}
        self.m_data['MaltegoMessage']['MaltegoTransformRequestMessage']['Limits']["@HardLimit"] = 50
        self.m_data['MaltegoMessage']['MaltegoTransformRequestMessage']['Limits']["@SoftLimit"] = 50
        self.m_data['MaltegoMessage']['MaltegoTransformRequestMessage']['TransformFields'] = {}
        self.m_data['MaltegoMessage']['MaltegoTransformRequestMessage']['TransformFields']['Field'] = []
        self.m_data['MaltegoMessage']['MaltegoTransformRequestMessage']['TransformFields']['Field'].append({"@Name": "api", "#text": "JUSTKIDDING"})
        ent_data = {}
        ent_data['@Type'] = "IPAddress"
        ent_data['Value'] = "127.0.0.1"
        ent_data['Weight'] = "100"
        ent_data['AdditionalFields'] = {}
        ent_data['AdditionalFields']['Field'] = []
        ent_data['AdditionalFields']['Field'].append({"@Name": "ipv4-address", "@DisplayName": "IP Address", "#text": "127.0.0.1"})
        ent_data['AdditionalFields']['Field'].append({"@Name": "ipaddress.internal", "@DisplayName": "Internal", "#text": "true"})
        self.m_data['MaltegoMessage']['MaltegoTransformRequestMessage']['Entities']['Entity'] = ent_data
        self.m_xml = xmltodict.unparse(self.m_data)

    def test_msg_entity(self):
        m = TRX.MaltegoMsg(self.m_xml)
        assert_is_instance(m, TRX.MaltegoMsg)
