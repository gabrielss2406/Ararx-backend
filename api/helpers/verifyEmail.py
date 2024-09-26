from typing import Union

from pydantic import EmailStr, BaseModel, ValidationError


def is_email(text: Union[EmailStr, str]):
    class EmailModel(BaseModel):
        email: EmailStr

    try:
        EmailModel(email=text)
        return True
    except ValidationError:
        return False
