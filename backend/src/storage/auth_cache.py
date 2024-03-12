class AuthCache:
    def __init__(self):
        self.cache = {}

    def add(self, key, value):
        self.cache[key] = value
    
    def get(self, key):
        return self.cache.get(key, None)