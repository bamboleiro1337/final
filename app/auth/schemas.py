from pydantic import BaseModel, EmailStr, Field

import settings


class AuthDetails(BaseModel):
    name: str = Field(min_length=settings.Settings.MIN_PASSWORD_LENGTH, max_length=50, examples=['Barak Obama'])
    login: EmailStr = Field(examples=['login@ukr.net'])
    password: str = Field(min_length=3, max_length=50, examples=['dfhaskdf&^R&^*B^w98723'])
    notes: str = Field(default='', max_length=settings.Settings.MAX_NOTES_LEN)



class AuthRegistered(BaseModel):
    success: bool = Field(examples=[True])
    id: int = Field(examples=[656])
    login: EmailStr = Field(examples=['login@ukr.net'])



class AuthLogin(BaseModel):
    login: EmailStr = Field(examples=['login@ukr.net'])
    password: str = Field(min_length=settings.Settings.MIN_PASSWORD_LENGTH, max_length=50, examples=['dfhaskdf&^R&^*B^w98723'])
   
