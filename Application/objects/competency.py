class Competency:
    def __init__(self, name, achievement, type):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        
        if not isinstance(achievement, str):
            raise TypeError("achievement must be a string")
        
        if not isinstance(type, str):
            raise TypeError("type must be a string")
        
        self.name = name
        self.achievement = achievement
        self.type = type

        self.id = None

    def __repr__(self):
        return f'Competency(name:{self.name}, achievement:{self.achievement}, type:{self.type}, id:{self.id})'
    
    def __str__(self):
        to_return = f'Name: {self.name}, Achievement: {self.achievement}, Type: {self.type}'