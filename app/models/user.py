from app.models.base_model import BaseModel

class User(BaseModel):
	def __init__(self, first_name, last_name, email, is_admin=False):
		super().__init__()
		self.first_name = first_name[:50]
		self.last_name = last_name[:50]
		self.email = email
		self.is_admin = is_admin