from xml.etree import ElementTree as ET


class Soap_Juggler():

    @staticmethod
    def parse_soap_response(xml_root, x_path, namespaces):
        parsed = xml_root.findall(
            x_path,
            namespaces
        )
        return parsed

    @staticmethod
    def extract_data(elements, tag, namespace=''):
        data = []
        for element in elements:
            print('hey it is me', element)
            found = element.find(namespace+tag)
            data.append(found.text.rstrip())
        return data


class AgregatorJuggler(Soap_Juggler):
    def __init__(self):
        self.namespaces = {
            'soap12': 'http://www.w3.org/2003/05/soap-envelope',
            'a': 'urn:Agregator'
        }

    def reg_ns(self):
        ET.register_namespace(
            'a', 'urn:Agregator')
        ET.register_namespace(
            'xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        ET.register_namespace(
            'xsd', 'http://www.w3.org/2001/XMLSchema')
        ET.register_namespace(
            'soap12', 'http://www.w3.org/2003/05/soap-envelope')

    def get_request_builder(self, request_template):
        self.rq = self.AgregatorRequest(
            request_template, self.namespaces, lambda: self.reg_ns())
        return self.rq

    def get_response_parser(self, response):
        self.rp = self.AgregatorResponse(
            response, self.namespaces, lambda: self.reg_ns())
        return self.rp

    class AgregatorRequest:
        def __init__(self, request_template, namespaces, reg_ns):
            self.xml_header = '<?xml version="1.0" encoding="utf-8"?>\n'
            self.template_root = ET.fromstring(request_template)
            self.namespaces = namespaces
            reg_ns()

        def build_soap_request(self, begin, end):
            element = self.template_root.find(
                './soap12:Body'
                '/a:GetListOfUsersReq',
                self.namespaces,
            )
            element[0].text = begin  # <startDate> tag
            element[1].text = end  # <endDate> tag
            print(element[0].text, element[1].text)
            built = self.xml_header
            built += ET.tostring(self.template_root, encoding="unicode")
            return built

    class AgregatorResponse:
        def __init__(self, response, namespaces, reg_ns):
            self.x_path = './soap12:Body/a:GetListOfUsersReqResponse/a:GetListOfUsersReqResult/'
            self.xml_root = ET.fromstring(response)
            self.user_request_logs = Soap_Juggler.parse_soap_response(
                self.xml_root, self.x_path, namespaces)
            reg_ns()

        def gather_user_requests(self, user_id,
                                 namespace='{urn:Agregator}'):
            '''
            1. Accept a list of requests (<UserRequest>) and user_id
            2. Iterate through each log entry in that list
                and find requests belonging to the specific user (via user_id)
            3. Iterate through these requests and extract the actual data.
            '''
            trimmed = []
            for log in self.user_request_logs:
                for e in log:
                    if e.tag == namespace+'UserId' and e.text == user_id:
                        trimmed.append(log)
            request_list = Soap_Juggler.extract_data(
                trimmed, 'DishName', namespace=namespace)
            return request_list

        def gather_all_requests(self, namespace='{urn:Agregator}'):
            '''
            Extract all dishes inside <UserRequest> and return it
            '''
            all_requests = Soap_Juggler.extract_data(
                self.user_request_logs,
                'DishName',
                namespace=namespace
            )
            return all_requests
