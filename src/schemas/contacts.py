from datetime import date
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber


class UAPhone(PhoneNumber):
    default_region_code = 'UA'
    supported_regions = ['UA']
    phone_format = 'NATIONAL'

class ContactModel(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=100)
    phone_number: UAPhone
    birthday: date
    additional_info: str | None = Field(default=None, max_length=200)

    model_config = ConfigDict(str_strip_whitespace=True)

class ContactUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=50)
    last_name: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=100)
    phone_number: UAPhone | None = None
    birthday: date | None = None
    additional_info: str | None = Field(default=None, max_length=200)

    model_config = ConfigDict(str_strip_whitespace=True)

class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str  
    birthday: date
    additional_info: str | None = None

    model_config = ConfigDict(from_attributes=True)