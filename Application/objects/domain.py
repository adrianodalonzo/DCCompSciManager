class Domain:
    def __init__(self, name, description):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        
        self.name = name
        self.description = description

        self.id = None
    
    def __repr__(self):
        return f'Domain(id:{self.id}, name:{self.name}, description:{self.description})'
    
    def __str__(self):
        return f'ID: {self.id}, Name: {self.name}, Description: {self.description}'