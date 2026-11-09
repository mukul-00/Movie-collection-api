from pydantic import BaseModel, Field, ConfigDict, field_validator

from typing import Literal

class MovieBase(BaseModel):
    title : str = Field(..., min_length=1, max_length=100)
    director: str
    genre: str
    rating: float = Field(ge=0, le=10)
    release_year: int = Field(ge=1888)

class MovieCreate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: int
    model_config = ConfigDict(from_attributes=True) # Dictionary → user["name"] , Object → user.name


class MovieUpdate(MovieBase):
    pass

class MovieListResponse(BaseModel):
    total: int
    page: int
    limit: int
    pages: int
    items: list[MovieResponse]




class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must not exceed 72 bytes when encoded as UTF-8")
        return value

class UserResponse(UserBase):
    id: int

class UserUpdate(UserBase):
    pass



class Token(BaseModel):
    access_token: str
    token_type: str


class UserRoleUpdate(BaseModel):
    role: Literal["user", "admin"]