from typing import Optional
from fastapi import Request
from pydantic import BaseModel, EmailStr, Field, validator


class LoginForm(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=6, description="User's password (at least 6 characters)")

    @classmethod
    async def create_from_form(cls, request: Request) -> 'LoginForm':
        form_data = await request.form()
        return cls(email=form_data.get("email"), password=form_data.get("password"))


class RegisterForm(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=4)
    firstname: str
    lastname: str
    password: str = Field(..., min_length=6)
    password2: str = Field(..., min_length=6)

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

# class LoginForm:
#     def __init__(self, request: Request):
#         self.request: Request = request
#         self.username: Optional[str] = None
#         self.password: Optional[str] = None

#     async def create_oauth_form(self):
#         form = await self.request.form()
#         self.username = form.get("email")
#         self.password = form.get("password")