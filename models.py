import json

class Items:
    def __init__(self):
        try:
            with open("items.json", "r") as f:
                self.items = json.load(f)
        except FileNotFoundError:
            self.items = []

    def all(self):
        return self.items

    def get(self, id):
        return self.items[id]

    def create(self, data):
        self.items.append(data)
      
    def save_all(self):
        with open("items.json", "w") as f:
            json.dump(self.items, f)

    def update(self, id, data):
        data.pop('csrf_token')
        self.items[id] = data
        self.save_all()

    def delete(self, id):
        todo = self.get(id)
        if items:
            self.items.remove(todo)
            self.save_all()
            return True
        return False

items = Items()