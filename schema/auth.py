from typing import Optional
from fastapi import Request


# class RegisterForm(BaseModel):
#     email: EmailStr
#     username: str = Field(..., min_length=4)
#     firstname: str
#     lastname: str
#     password: str = Field(..., min_length=6)
#     password2: str = Field(..., min_length=6)

#     @validator('password2')
#     def passwords_match(cls, password2, values, **kwargs):
#         if 'password' in values and password2 != values['password']:
#             raise ValueError('Passwords do not match')
#         return password2

class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")