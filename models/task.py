class Task:
    def __init__(self,  id: int, title:str, description: str, user_id: str, status: str):
        self.id = id
        self.title = title
        self.description = description
        self.user_id = user_id
        self.status = status
        