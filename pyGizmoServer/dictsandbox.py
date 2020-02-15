og = {"key": {"list": [{"1": 1}, {"2": 2}, {"3": 3}]}}


def getptr(dict):
    ptr = dict["key"]["list"][0]
    return ptr


ptr = getptr(og)
ptr = "number"

print(og)
