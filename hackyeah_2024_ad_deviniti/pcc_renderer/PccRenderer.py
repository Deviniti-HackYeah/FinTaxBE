import lxml.etree as ET

class FileResolver(ET.Resolver):
    def resolve(self, url, pubid, context):
        return self.resolve_filename(url, context)
    



class PccRenderer:

    xslt_doc = None

    def __init__(self ):
        x = 2
        parser = ET.XMLParser()
        parser.resolvers.add(FileResolver())

        # Parse the XSLT content
        self.xslt_doc = ET.parse('styl.xsl', parser)

        
    def render(self, data: str, kod_urzedu: str, pesel : str) -> str:

        xml_string = self.xml(data, kod_urzedu, pesel)

        # Parse the XML content
        xml_doc = ET.XML(bytes(xml_string, encoding='utf-8'))

        # Create an XSLT transform object
        transform = ET.XSLT(self.xslt_doc)

        # Apply the transformation
        newdom = transform(xml_doc)

        # Print the transformed XML
        html = ET.tostring(newdom, pretty_print=True).decode('utf-8')

        return html
                

    def xml(self, data: str, kod_urzedu: str, pesel : str) -> str:
        with open('data.xml', 'r', encoding="utf-8") as xml_file:
            xml_string = xml_file.read()
            xml_string = xml_string.replace("%%DATA", data)
            xml_string = xml_string.replace("%%KOD_URZEDU", kod_urzedu)
            xml_string = xml_string.replace("%%PESEL", pesel)
        return xml_string