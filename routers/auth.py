from datetime import timedelta
from fastapi import APIRouter, Form, Request, Response, Depends, status, HTTPException
from pydantic import ValidationError
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from services.auth import authenticate_user, create_access_token, get_password_hash
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from schema.auth import LoginForm
import models
from logger import logger

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={401: {'user': 'Not authorized'}}
)


templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()




@router.post('/token')
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token_expires = timedelta(minutes=60)
    token = create_access_token(user.username,
                                user.id,
                                expires_delta=token_expires)
    response.set_cookie(key='access_token', value=token, httponly=True)
    # return {"access_token": token, "token_type": "bearer"}
    return True




@router.get("/", response_class=HTMLResponse)
async def authentication_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url="/todo", status_code=status.HTTP_302_FOUND)

        validate_user_cookie = await login_for_access_token(response=response, form_data=form, db=db)

        if not validate_user_cookie:
            msg = "Incorrect Username or Password"
            return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
        return response
    except HTTPException:
        msg = "Incorrect Username or Password"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})



@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})




@router.post("/register", response_class=HTMLResponse)
async def register_user(request: Request, email: str = Form(...), username: str = Form(...),
                        firstname: str = Form(...), lastname: str = Form(...),
                        password: str = Form(...), password2: str = Form(...),
                        db: Session = Depends(get_db)):

    # validation1 = db.query(models.Users).filter(models.Users.username == username).first()

    # validation2 = db.query(models.Users).filter(models.Users.email == email).first()

    # if password != password2 or validation1 is not None or validation2 is not None:
    #     msg = "Invalid registration request"
    #     return templates.TemplateResponse("register.html", {"request": request, "msg": msg})

    # Check if the username already exists
    username_exists = db.query(models.Users).filter(models.Users.username == username).first()

    # Check if the email already exists
    email_exists = db.query(models.Users).filter(models.Users.email == email).first()

    # Check if passwords match
    passwords_match = password == password2

    # Determine the appropriate error message
    if not passwords_match:
        msg = "Passwords do not match."
    elif username_exists:
        msg = "Username already exists. Please choose a different one."
    elif email_exists:
        msg = "Email already exists. Please use a different email."
    else:
        msg = None  # No errors

    # Return the error message if there is one
    if msg:
        return templates.TemplateResponse("register.html", {"request": request, "msg": msg})

    user_model = models.Users()
    user_model.username = username
    user_model.email = email
    user_model.first_name = firstname
    user_model.last_name = lastname

    hash_password = get_password_hash(password)
    user_model.hashed_password = hash_password
    user_model.is_active = True

    db.add(user_model)
    db.commit()

    msg = "User successfully created"
    return templates.TemplateResponse("login.html", {"request": request, "msg": msg})

