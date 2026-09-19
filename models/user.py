class User:
    """Represents a system user entity."""
    
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User(id={self.user_id}, name='{self.name}', email='{self.email}')"