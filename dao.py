import asyncio

from database import async_session_maker
from models import Recipe, User
from sqlalchemy import delete, insert, select, update


async def create_user(
        name: str,
        login: str,
        password: str,
        notes: str = '',
        is_conflict: bool = False,
):
    
    async with async_session_maker() as session:

        query = insert(User).values(
            name=name,
            login=login,
            password=password,
            notes=notes,
            is_conflict=is_conflict,
        ).returning(User.id, User.login, User.name)


        print(query)
        data = await session.execute(query)
        await session.commit()
        
        return tuple(data)[0]



async def fetch_users(skip: int = 0, limit: int = 10):
    
    async with async_session_maker() as session:
        query = select(User).offset(skip).limit(limit)
        result = await session.execute(query)

        return result.scalars().all()



async def get_user_by_id(user_id: int):

    async with async_session_maker() as session:
        query = select(User).filter_by(id=user_id)
        print(query)
        result = await session.execute(query)

        return result.scalar_one_or_none()



async def get_user_by_login(user_login: str):

    async with async_session_maker() as session:
        query = select(User).filter_by(login=user_login)
        result = await session.execute(query)
        return result.scalar_one_or_none()



async def update_user(user_id: int):

    async with async_session_maker() as session:
        query = update(User).where(User.id == user_id).values(name='Olik')
        print(query)

        await session.execute(query)
        await session.commit(query)



async def delete_user(user_id: int):
    
    async with async_session_maker() as session:
        query = delete(User).where(User.id == user_id)
        print(query)

        await session.execute(query)
        await session.commit(query)



#recipe
async def create_recipe(
        *,
        title: str,
        image: str,
        complexity: str,
        category: str,
        recipe: str,
):
    
    async with async_session_maker() as session:
        
        query = insert(Recipe).values(
            title=title,
            image=image,
            complexity=complexity,
            category=category,
            recipe=recipe,
        ).returning(Recipe.id, Recipe.image, Recipe.title)
        
        print(query)
        data = await session.execute(query)
        await session.commit()
        
        return tuple(data)[0]
    
    

async def fetch_recipes(skip: int = 0, limit: int = 10):
    
    async with async_session_maker() as session:
        query = select(Recipe).offset(skip).limit(limit)
        result = await session.execute(query)

        return result.scalars().all()
    
    
    
async def get_recipe_by_id(recipe_id: int):

    async with async_session_maker() as session:
        query = select(Recipe).filter_by(id=recipe_id)
        print(query)
        result = await session.execute(query)

        return result.scalar_one_or_none()
    
    
async def get_recipe_by_title(recipe_title: str):
    async with async_session_maker() as session:
        query = select(Recipe).filter_by(title=recipe_title)
        print(query)
        result = await session.execute(query)

        return result.scalar_one_or_none()