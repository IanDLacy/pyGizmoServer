from pyGizmoServer.query_handler import QueryHandler
from pyGizmoServer.utility import Utility
from tests.mock_variables import MockVars
import json


class TestUtility:
    def get_instance(self):
        self.mockvars = MockVars()
        with open("TestCubeUSB/schema.json") as f:
            self.schema = json.load(f)
        #self.schema = self.mockvars.mock_schema
        self.model = self.mockvars.mock_model

    def test_parse_path_against_schema_and_model_read_root_directory(self):
        self.get_instance()
        self.path = "/"
        result = Utility.parse_path_against_schema_and_model(
            self.model, self.schema, self.path, read_write="r"
        )
        assert result["path_up_to_array_index"] == "/"
        assert result["path_string"] == "/"
        assert result["model_data"] == self.model
        assert result["routine"] is None
        assert result["args"] == None
        assert result["error"] == None

    def test_parse_path_against_schema_and_model_read(self):
        self.get_instance()
        self.path = "/relayController/relays/2/enabled"
        result = Utility.parse_path_against_schema_and_model(
            self.model, self.schema, self.path, read_write="r"
        )
        assert result["path_up_to_array_index"] == "/relayController/relays"
        assert result["path_string"] == "/relayController/relays/2/enabled"
        assert result["model_data"] == False
        #assert result["routine"] == "getRelay"
        assert result["args"] == [2]
        assert result["error"] == None

    def test_parse_path_against_schema_and_model_indexed_read(self):
        self.get_instance()
        self.path = "/relayController.relays[2]/enabled"
        result = Utility.parse_path_against_schema_and_model(
            self.model, self.schema, self.path, read_write="r"
        )
        assert result["path_up_to_array_index"] == "/relayController/relays"
        assert result["path_string"] == "/relayController/relays/2/enabled"
        assert result["model_data"] == False
        #assert result["routine"] == "getRelay"
        assert result["args"] == [2]
        assert result["error"] == None

    def test_parse_path_against_schema_and_model_indexed_write(self):
        self.get_instance()
        self.path = ".relayController/relays[3]/enabled"
        result = Utility.parse_path_against_schema_and_model(
            self.model, self.schema, self.path, read_write="w"
        )
        assert result["path_up_to_array_index"] == "/relayController/relays"
        assert result["path_string"] == "/relayController/relays/3/enabled"
        assert result["model_data"] == False
        assert result["routine"] == "setRelay"
        assert result["args"] == [3]
        assert result["error"] == None

    def test_parse_path_against_schema_and_model_bad_path(self):
        self.get_instance()
        self.path = "///relayController....relays[10]/enabled"
        result = Utility.parse_path_against_schema_and_model(
            self.model, self.schema, self.path, read_write="w"
        )
        assert result["error"] == "PATH ERROR: /relayController/relays/10"
        assert result["path_up_to_array_index"] is None
        assert result["path_string"] is None
        assert result["model_data"] is None
        assert result["routine"] is None
        assert result["args"] is None

    def test_parse_path_against_schema_and_model_bad_path_2(self):
        self.get_instance()
        self.path = "./.relayController.misspelled[10]/enabled"
        result = Utility.parse_path_against_schema_and_model(
            self.model, self.schema, self.path, read_write="w"
        )
        assert result["error"] == "PATH ERROR: /relayController/misspelled"
        assert result["path_up_to_array_index"] is None
        assert result["path_string"] is None
        assert result["model_data"] is None
        assert result["routine"] is None
        assert result["args"] is None
