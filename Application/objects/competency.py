class Competency:
    def __init__(self, id, name, achievement, type):
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        
        if not isinstance(achievement, str):
            raise TypeError("achievement must be a string")
        
        if not isinstance(type, str):
            raise TypeError("type must be a string")
        
        self.id = id
        self.name = name
        self.achievement = achievement
        self.type = type
        
    def __repr__(self):
        return f'Competency(id:{self.id}, name:{self.name}, achievement:{self.achievement}, type:{self.type}, id:{self.id})'
    
    def __str__(self):
        return f'Id:{self.id}, Name: {self.name}, Achievement: {self.achievement}, Type: {self.type}'