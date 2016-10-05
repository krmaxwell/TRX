from xml.dom import minidom

BOOKMARK_COLOR_NONE = "-1"
BOOKMARK_COLOR_BLUE = "0"
BOOKMARK_COLOR_GREEN = "1"
BOOKMARK_COLOR_YELLOW = "2"
BOOKMARK_COLOR_ORANGE = "3"
BOOKMARK_COLOR_RED = "4"

LINK_STYLE_NORMAL = "0"
LINK_STYLE_DASHED = "1"
LINK_STYLE_DOTTED = "2"
LINK_STYLE_DASHDOT = "3"

UIM_FATAL = 'FatalError'
UIM_PARTIAL = 'PartialError'
UIM_INFORM = 'Inform'
UIM_DEBUG = 'Debug'


class MaltegoEntity(object):

    def __init__(self, eT=None, v=None):
        """Create a Maltego entity of type eT and value v."""
        if (eT is not None):
            self.entityType = eT
        else:
            self.entityType = "Phrase"

        if (v is not None):
            self.value = v
        else:
            self.value = ""
        self.additionalFields = {}
        self.weight = 100
        self.displayInformation = []
        self.iconURL = ""

    def setType(self, eT=None):
        """Sets the type of the entity to eT.

        See list of Entity definitions in TRX documentation for possible values.
        """
        if (eT is not None):
            self.entityType = eT

    def setValue(self, eV=None):
        """Sets the value of Maltego entity to eV."""
        if (eV is not None):
            self.value = eV

    def setWeight(self, w=None):
        """Sets weight of Maltego entity to w."""
        if (w is not None):
            self.weight = w

    def addDisplayInformation(self, di=None, dl='Info'):
        """Adds display information to entity.

        This field is rendered as HTML within Maltego. See pages 29 & 50 in
        TRX documentation.
        """
        if (di is not None):
            self.displayInformation.append([dl, di])

    def addProperty(self, fieldName=None, displayName=None, matchingRule=False, value=None):
        """Add a property to the entity.

        Each property has a name, value and a display name. The display name is
        how it will be represented within Maltego. The matching rule determines
        how entities will be matched and could be 'strict' (default) or 'loose'.
        See pages 30 & 50 in TRX documentation.
        """
        self.additionalFields[fieldName] = {}
        self.additionalFields[fieldName]['displayName'] = displayName
        self.additionalFields[fieldName]['matchingRule'] = matchingRule
        self.additionalFields[fieldName]['value'] = value

    def setIconURL(self, iU=None):
        """Define a URL pointing to a PNG or JPG for the icon.

        Maltego will size to fit but lots of large files will drain
        resources.
        """
        if (iU is not None):
            self.iconURL = iU

    def setLinkColor(self, color):
        """Sets the color of the link to the node. Colors are in hex, for example '0xff00ff'."""
        self.addProperty('link#maltego.link.color', 'LinkColor', '', color)

    def setLinkStyle(self, style):
        """Set the style of a link to an entity using LINK_STYLE_* constants."""
        self.addProperty('link#maltego.link.style', 'LinkStyle', '', style)

    def setLinkThickness(self, thick):
        """Set the thickiness of a link to an entity in pixels."""
        self.addProperty('link#maltego.link.thickness', 'Thickness', '', str(thick))

    def setLinkLabel(self, label):
        """Sets the label of the link to the node."""
        self.addProperty('link#maltego.link.label', 'Label', '', label)

    def setBookmark(self, bookmark):
        """Sets the bookmark color of the node.

        Keep in mind that these are chosen from a set number of colors. Use the
        BOOKMARK_COLOR_* constants.
        """
        self.addProperty('bookmark#', 'Bookmark', '', bookmark)

    def setNote(self, note):
        """Creates an annotation to the node.

        If a subsequent transform sets an annotation on the node it will be
        appended to the note.
        """
        self.addProperty('notes#', 'Notes', '', note)

    def returnEntity(self):
        """Generate XML snippet for returning to Maltego."""
        r = ''
        r += "<Entity Type=\"" + str(self.entityType) + "\">"
        r += "<Value>" + unicode(self.value) + "</Value>"
        r += "<Weight>" + str(self.weight) + "</Weight>"
        if (len(self.displayInformation) > 0):
            r += "<DisplayInformation>"
            for i in range(len(self.displayInformation)):
                r += '<Label Name=\"' + self.displayInformation[i][0] + '\" Type=\"text/html\"><![CDATA[' + str(self.displayInformation[i][1]) + ']]></Label>'
            r += '</DisplayInformation>'
        if (len(self.additionalFields) > 0):
            r += "<AdditionalFields>"
            for field in self.additionalFields:
                if (str(field['matchingRule']) != "strict"):
                    r += "<Field Name=\"" + str(field) + "\" DisplayName=\"" + str(field['displayName']) + "\">" + str(field['value']) + "</Field>"
                else:
                    r += "<Field MatchingRule=\"strict\" Name=\"" + str(field) + "\" DisplayName=\"" + str(field['displayName']) + "\">" + str(field['value']) + "</Field>"
            r += "</AdditionalFields>"
        if (len(self.iconURL) > 0):
            r += "<IconURL>" + self.iconURL + "</IconURL>"
        r += "</Entity>"
        return r


class MaltegoTransform(object):
    """This is used to construct the reply to the TDS.

    All values are strings.
    """

    def __init__(self):
        """Create Maltego transform to hold entities, exceptions, and messages.

        See page 49 in TRX documentation.
        """
        self.entities = []
        self.exceptions = []
        self.UIMessages = []

    def addEntity(self, enType=None, enValue=None):
        """Adds an entity to the return vessel with type 'enType' and
        value 'enValue'.
        """
        me = MaltegoEntity(enType, enValue)
        self.entities.append(me)
        return me

    def addUIMessage(self, message, messageType=UIM_INFORM):
        """Shows a message 'msg' in the Maltego GUI.

        Use UIM_* constants.
        """
        self.UIMessages.append([messageType, message])

    def addException(self, exceptionString):
        """Throws a transform exception."""
        self.exceptions.append(exceptionString)

    def throwExceptions(self):
        """Returns the XML of the exception(s)."""
        r = ''
        r += "<MaltegoMessage>"
        r += "<MaltegoTransformExceptionMessage>"
        r += "<Exceptions>"

        for i in range(len(self.exceptions)):
            r += "<Exception>" + self.exceptions[i] + "</Exception>"
        r += "</Exceptions>"
        r += "</MaltegoTransformExceptionMessage>"
        r += "</MaltegoMessage>"
        return r

    def returnOutput(self):
        """Returns the XML of the vessel."""
        r = ''
        r += "<MaltegoMessage>"
        r += "<MaltegoTransformResponseMessage>"

        r += "<Entities>"
        for i in range(len(self.entities)):
            r += self.entities[i].returnEntity()
        r += "</Entities>"

        r += "<UIMessages>"
        for i in range(len(self.UIMessages)):
            r += "<UIMessage MessageType=\"" + \
                self.UIMessages[i][0] + "\">" + self.UIMessages[i][1] + "</UIMessage>"
        r += "</UIMessages>"

        r += "</MaltegoTransformResponseMessage>"
        r += "</MaltegoMessage>"
        return r


class MaltegoMsg:
    """This reads the Maltego request and is passed along to each transform.


    See page 49 in TRX documentation.
    """

    def __init__(self, MaltegoXML=""):
        """Parse XML received from Maltego."""

        xmldoc = minidom.parseString(MaltegoXML)

        # read the easy stuff like value, limits etc
        self.Value = self.i_getNodeValue(xmldoc, "Value")
        self.Weight = self.i_getNodeValue(xmldoc, "Weight")
        self.Slider = int(
            self.i_getNodeAttributeValue(xmldoc, "Limits", "SoftLimit"))
        self.Type = self.i_getNodeAttributeValue(xmldoc, "Entity", "Type")

        # read additional fields
        Properties = {}
        AFNodes = xmldoc.getElementsByTagName("AdditionalFields")[0]
        Settings = AFNodes.getElementsByTagName("Field")
        for node in Settings:
            AFName = node.attributes["Name"].value
            AFValue = self.i_getText(node.childNodes)
            Properties[AFName] = AFValue

        # parse transform settings
        TransformSettings = {}
        TSNodes = xmldoc.getElementsByTagName("TransformFields")[0]
        Settings = TSNodes.getElementsByTagName("Field")
        for node in Settings:
            TSName = node.attributes["Name"].value
            TSValue = self.i_getText(node.childNodes)
            TransformSettings[TSName] = TSValue

        # load back into object
        self.Properties = Properties
        self.TransformSettings = TransformSettings

    def i_getText(self, nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)

    def i_getNodeValue(self, node, Tag):
        return self.i_getText(node.getElementsByTagName(Tag)[0].childNodes)

    def i_getNodeAttributeValue(self, node, Tag, Attribute):
        return node.getElementsByTagName(Tag)[0].attributes[Attribute].value

    def getProperty(self, skey):
        """Returns the value of the key, or None if not defined."""
        if skey in self.Properties:
            return self.Properties[skey]
        else:
            return None

    def getTransformSetting(self, skey):
        if skey in self.TransformSettings:
            return self.TransformSettings[skey]
        else:
            return None
