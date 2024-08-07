from typing import Annotated
from fastapi import Depends
from sqlalchemy import select

from src.library import schemas
from src.library.models import (
    BookModel,
    BooksAuthorsModel,
    BooksTagsModel,
    VolumeModel,
    ChapterModel,
    TagModel, 
    AuthorModel 
)
from src.database import async_session_dependency

######### Books CRUD #########

async def get_books(
    session: async_session_dependency
):
    stmt = select(BookModel) #.limit( )
    result = await session.execute(stmt)
    books = result.scalars().all()
            
    return books


async def get_book_by_name(
    book_name: str,
    session: async_session_dependency
):
    stmt = select(BookModel).where(BookModel.book_name == book_name)
    result = await session.execute(stmt)
    book = result.scalars().first()
    
    return book


async def get_book_author_by_name(
    book_name: str,
    session: async_session_dependency
):
    stmt = (
        select(AuthorModel)
        .join(BooksAuthorsModel)
        .join(BookModel)
        .where(BookModel.book_name == book_name))
    result = await session.execute(stmt)
    author = result.scalars().first()
    
    return author


async def get_book_chapter(
    book_name: str, 
    volume_number: int, 
    chapter_number: int, 
    session: async_session_dependency
) -> str:
    query = (
    select(ChapterModel.chapter_content)
    .join(VolumeModel, VolumeModel.volume_id == ChapterModel.volume_id)
    .join(BookModel, BookModel.book_id == VolumeModel.book_id)
    .filter(ChapterModel.chapter_number == chapter_number)
    .filter(VolumeModel.volume_number == volume_number)
    .filter(BookModel.book_name == book_name)
    )
    
    result = await session.execute(query)
    chapter_content = result.scalars().first()
    
    return chapter_content

######### Tags CRUD #########

async def get_tags(
    session: async_session_dependency
):
    stmt = select(TagModel)
    result = await session.execute(stmt)
    tags = result.scalars().all()
    return tags


######### Authors CRUD #########

async def get_authors(
    session: async_session_dependency
):
    stmt = select(AuthorModel)
    result = await session.execute(stmt)
    authors = result.scalars().all()
    
    return authors


async def get_books_by_author(
    author_name: str,
    session: async_session_dependency
):
    stmt = (
        select(BookModel)
        .join(BooksAuthorsModel)
        .join(AuthorModel)
        .where(AuthorModel.author_name == author_name))
    result = await session.execute(stmt)
    books = result.scalars().all()
    
    return books


