class Course:
    def __init__(self, title, theory_hours, lab_hours, work_hours, description, domain_id, term_id):
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        
        if not isinstance(theory_hours, int):
            raise TypeError("theory_hours must be an int")
        
        if not isinstance(lab_hours, int):
            raise TypeError("lab_hours must be an int")
        
        if not isinstance(work_hours, int):
            raise TypeError("work_hours must be an int")
        
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        
        if not isinstance(domain_id, int):
            raise TypeError("domain_id must be an int")
        
        if not isinstance(term_id, int):
            raise TypeError("term_id must be an int")
        
        self.title = title
        self.theory_hours = theory_hours
        self.lab_hours = lab_hours
        self.work_hours = work_hours
        self.description = description
        self.domain_id = domain_id
        self.term_id = term_id

        self.id = None
    
    def __repr__(self):
        to_return = f'Course(title:{self.title}, theory_hours:{self.theory_hours}, '
        + f'lab_hours:{self.lab_hours}, work_hours:{self.work_hours}, '
        + f'description:{self.description}, domain_id:{self.domain_id}, '
        + f'term_id:{self.term_id}, id:{self.id})'
        return to_return
    
    def __str__(self):
        to_return = f'Title: {self.title}, Theory Hours: {self.theory_hours}, '
        + f'Lab Hours: {self.lab_hours}, Work Hours: {self.work_hours}, '
        + f'Description: {self.description}, Domain ID: {self.domain_id}, '
        + f'Term ID: {self.term_id}'