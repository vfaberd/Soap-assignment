from xml.etree import ElementTree as ET


class Juggler():
    def __init__(self, xml_contents, request_headers=None):
        self.xml_root = ET.fromstring(xml_contents)

    def extract_data(self, elements, tag, namespace=''):
        data = []
        for element in elements:
            found = element.find(namespace+tag)
            data.append(found.text)
        return data


class AgregatorJuggler(Juggler):
    def __init__(self, xml_contents, request_headers=None):
        super().__init__(xml_contents, request_headers)
        self.namespaces = {
            'soap12': 'http://www.w3.org/2003/05/soap-envelope',
            'a': 'urn:Agregator'
        }

        self.user_request_logs = self.xml_root.findall(
            './soap12:Body'
            '/a:ListOfUserRequestResponse/a:ListOfUserRequestResult/a:UserRequestLog',
            self.namespaces
        )

        ET.register_namespace(
            '', 'urn:Agregator')
        ET.register_namespace(
            'xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        ET.register_namespace(
            'xsd', 'http://www.w3.org/2001/XMLSchema')
        ET.register_namespace(
            'soap12', 'http://www.w3.org/2003/05/soap-envelope')

        print(ET.tostring(self.xml_root, encoding="unicode"))

    def gather_user_requests(self, user_id,
                             namespace='{urn:Agregator}'):
        '''
        1. Accept a list of requests (<UserRequestLog>) and user_id
        2. Iterate through each log entry in that list
            and find requests belonging to the specific user (via user_id)
        3. Iterate through these requests and extract the actual data.
        '''
        trimmed = []

        for log in self.user_request_logs:
            for e in log:
                if e.tag == namespace+'userId' and e.text == user_id:
                    trimmed.append(log)
        request_list = super().extract_data(trimmed, 'userRequest', namespace=namespace)
        return request_list

    def gather_all_requests(self, namespace='{urn:Agregator}'):
        '''
        Extract all data inside <userRequest> and return it
        '''
        all_requests = super().extract_data(self.user_request_logs,
                                            'userRequest', namespace=namespace)
        return all_requests

    def build_request(self, request_template, begin, end):
        template_root = ET.fromstring(request_template)
        element = template_root.find(
            './soap12:Body'
            '/a:ListOfUserRequest',
            self.namespaces,
        )
        element[0].text = begin  # <begin> tag
        element[1].text = end  # <end> tag
        print(element[0].text, element[1].text)
        built = ET.tostring(template_root, encoding="unicode")
        return built
