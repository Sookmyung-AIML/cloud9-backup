class User:
    def __init__(self, user_id):
        self.user_id = user_id.strip()
    
    def login(self):
        if self.user_id:
            return self.user_id
        else:
            return False