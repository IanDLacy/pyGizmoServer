from pyGizmoServer.query_handler import merge
import pytest


class TestQueryHandler:
    @pytest.fixture
    def merge_result(self):
        self.og_dict = {
            "key": {
                "list": [
                    {"key": None},
                    {"key": False},
                    {"key": True},
                    {"key": 0},
                    {"key": 1},
                    {"key": {}},
                    {"key": [None, False, True, 0, 1, {"key": "val"}]},
                    {"key": [None, False, True, 0, 1, {"key": "val"}]},
                    {},
                ]
            }
        }
        self.newvals = {
            "key": {
                "list": [
                    {"key": False},
                    {"key": None},
                    {"key": False},
                    {"key": "string"},
                    {},
                    False,
                    {"key": [1, 2, 3, 4, 5, {"key": "newval"}]},
                    {},
                    False,
                ]
            }
        }
        return merge(self.og_dict, self.newvals)

    def test_merge_result_0(self, merge_result):
        t = merge_result["key"]["list"][0]["key"]
        assert t is not None and not t

    def test_merge_result_1(self, merge_result):
        t = merge_result["key"]["list"][1]["key"]
        assert t is None

    def test_merge_result_2(self, merge_result):
        t = merge_result["key"]["list"][2]["key"]
        assert t is not None and not t

    def test_merge_result_3(self, merge_result):
        t = merge_result["key"]["list"][3]["key"]
        assert t == "string"

    def test_merge_result_4(self, merge_result):
        t = merge_result["key"]["list"][4]["key"]
        assert t == 1

    def test_merge_result_5(self, merge_result):
        t = merge_result["key"]["list"][5]
        assert t is not None and not t

    def test_merge_result_6(self, merge_result):
        t = merge_result["key"]["list"][6]["key"]
        assert t == [1, 2, 3, 4, 5, {"key": "newval"}]

    def test_merge_result_7(self, merge_result):
        t = merge_result["key"]["list"][7]["key"]
        assert t == [None, False, True, 0, 1, {"key": "val"}]

    def test_merge_result_8(self, merge_result):
        t = merge_result["key"]["list"][8]
        assert t is not None and not t
