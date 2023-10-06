from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select, insert, delete, asc, desc, or_, update
from sqlalchemy.ext.asyncio import AsyncSession

from articles.schemas import ArticleCreate
from auth.database import get_async_session
from models.models import user, article

router = APIRouter(
    prefix="/article",
    tags=["articles"]

)


@router.post('/add')
async def add_article(new_article: ArticleCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(article).values(**new_article.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": 200}


@router.delete('/delete')
async def del_article(article_id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(article).where(article.c.id == article_id)
    await session.execute(query)
    await session.commit()
    return {"status": "success"}


@router.get('/get_all_article')
async def get_all_article(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(article))
    artcl = result.mappings().all()
    return artcl


@router.get('/get_all_articles_sorted_asc')
async def get_all_articles_sorted_asc(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(article).order_by(asc(article.c.id)))
    artcl = result.mappings().all()
    return artcl


@router.get('/get_all_articles_sorted_desc')
async def get_all_articles_sorted_desc(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(article).order_by(desc(article.c.id)))
    artcl = result.mappings().all()
    return artcl


@router.get('/get_articles_by_key_word')
async def get_articles_by_key_word(key_word: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(article).where(
            or_(
                article.c.title.ilike(f"%{key_word}%"),
                article.c.text.ilike(f"%{key_word}%")
            )
        )
    )
    artcl = result.mappings().all()
    return artcl


@router.put('/update_article')
async def edit_article(article_id: int, new_title: str, new_text: str, img: str, session: AsyncSession = Depends(get_async_session)):

    result = await session.execute(select(article).where(article.c.id == article_id))
    article_to_edit = result.scalar_one_or_none()
    if not article_to_edit:
        raise HTTPException(status_code=404, detail="Article not found")

    stmt = (
        update(article).
        where(article.c.id == article_id).
        values(title=new_title, text=new_text, image=img)
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "success", "message": "Article updated successfully"}
