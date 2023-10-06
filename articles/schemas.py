from pydantic import BaseModel


class ArticleCreate(BaseModel):
    user_id: int
    image: str
    title: str
    text: str


