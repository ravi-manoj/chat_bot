class Query:
    def __init__(self, name,query, phone, count=0, res=""):
        self.name = name
        self.query = query
        self.phone = phone
        self.count = count
        self.res = res

    def __repr__(self):
        return f"{self.conv_id} - {self.query}"
