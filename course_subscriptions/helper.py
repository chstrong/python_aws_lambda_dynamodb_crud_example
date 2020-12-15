import json

class Helper:

    # Check if value is a string
    def __is_string(self, value):
        if(isinstance(value, str)):
            return True
        else:
            return False

    # Check if value is greater than char count
    def __has_char_count(self, value, num=0):
        if len(value) >= num:
            return True
        else:
            return False

    def validate_pk(self,pk):
        if not pk.startswith("U"):
            return False
        return True

    def validate_sk(self,sk):
        if not sk.startswith("C"):
            return False
        return True

    # Check if the payload fields are valid
    def validate_payload(self, json_map):
        keys = json_map.keys()
        payload_valid = True

        # Check if required keys are in json_map
        keys_required = {'PK', 'SK', 'Name', 'Description', 'Author'}
        for key in keys_required:
            if key not in keys:
                payload_valid = False

        # Do validations
        payload_valid = self.__is_string(json_map['PK'])
        payload_valid = self.__has_char_count(json_map['PK'], 1)
        payload_valid = self.__is_string(json_map['SK'])
        payload_valid = self.__has_char_count(json_map['PK'], 1)
        payload_valid = self.__is_string(json_map['Name'])
        payload_valid = self.__is_string(json_map['Description'])
        payload_valid = self.__is_string(json_map['Author'])

        # Check if all the values are strings
        return payload_valid                            

    # Returns a JSON error with statusCode 403 and a custom message
    def json_error(self, message):
        return {
            "statusCode": 403,
            "body": json.dumps({"message": message})
        }

    # Returns a JSON success message with a custom body
    def json_success(self, json_map):
        return {
            "statusCode": 200,
            "body": json_map
        }

    # Converts the html body string into a python dict construct
    def body_to_json(self, body):
        return json.loads(str(body), encoding='utf-8')