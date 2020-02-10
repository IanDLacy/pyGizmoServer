import json

class CanDatabaseMessage:
    def __init__(self):
        pass

    def setCanDatabase(self, db):
        print(json.dumps(db,indent=2))