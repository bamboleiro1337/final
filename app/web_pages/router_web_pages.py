from fastapi import (APIRouter, Depends, Form, HTTPException, Request,
                     Response, status)
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

import dao
import settings
from app.auth import dependencies
from app.auth.auth_lib import AuthHandler, AuthLibrary

router = APIRouter(
    prefix='/web',
    tags=['menu', 'landing'],
)

templates = Jinja2Templates(directory='app\\templates')



@router.get('/')
async def get_main_page(request: Request, user=Depends(dependencies.get_current_user_optional)):
    context = {
        'request': request,
        'user': user,
    }

    return templates.TemplateResponse(
        'base.html',
        context=context,
    )



@router.get('/home')
async def get_menu(request: Request, user=Depends(dependencies.get_current_user_optional)):
    context = {
        'request': request,
        'title': 'Головна',
        'user': user,
    }

    return templates.TemplateResponse(
        'home.html',
        context=context,
    )



@router.post('/menu')
@router.get('/menu')
async def get_menu(request: Request, dish_name: str = Form(None), user=Depends(dependencies.get_current_user_optional)):
    all_dishes = await dao.fetch_recipes()
    
    filtered_menu = []
    if dish_name:
        for dish in all_dishes:
            if dish_name.lower() in dish['title'].lower():
                filtered_menu.append(dish)

    context = {
        'request': request,
        'title': f'Результати пошуку за {dish_name}' if dish_name else 'Наше меню',
        'menu': filtered_menu if dish_name else all_dishes,
        'user': user,
        #'categories': menu_data.Categories

    }

    return templates.TemplateResponse(
        'menu.html',
        context=context,
    )



@router.get('/about')
async def get_menu(request: Request, user=Depends(dependencies.get_current_user_optional)):
    context = {
        'request': request,
        'title': 'Про автора',
        'user': user,
    }

    return templates.TemplateResponse(
        'about.html',
        context=context,
    )


@router.get('/contacts')
async def get_menu(request: Request, user=Depends(dependencies.get_current_user_optional)):
    context = {
        'request': request,
        'title': 'Наші контакти',
        'user': user,
    }

    return templates.TemplateResponse(
        'contacts.html',
        context=context,
    )


@router.get('/message')
async def message(request: Request, user=Depends(dependencies.get_current_user_optional)):
    context = {
        'request': request,
        'title': 'Написати всім повідомлення',
        'user': user,
    }

    return templates.TemplateResponse(
        'message_to_all.html',
        context=context,
    )



@router.get('/register')
@router.post('/register')
async def register(request: Request):
    context = {
        'request': request,
        'title': 'Реєстрація',
        'min_password_length': settings.Settings.MIN_PASSWORD_LENGTH,
    }

    return templates.TemplateResponse(
        'register.html',
        context=context,
    )


@router.post('/register-final')
async def register_final(request: Request,
                         name: str = Form(),
                         login: EmailStr = Form(),
                         notes: str = Form(default=''),
                         password: str = Form()):
    
    is_login_already_used = await dao.get_user_by_login(login)

    if is_login_already_used:
        context = {
            'request': request,
            'title': 'Помилка користувача',
            'content': f'Користувач {login} уже існує',
        }
        return templates.TemplateResponse(
            '400.html',
            context=context,
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    
    hashed_password = await AuthHandler.get_password_hash(password)

    user_data = await dao.create_user(
        name=name,
        login=login,
        password=hashed_password,
        notes=notes,
    )

    token = await AuthHandler.encode_token(user_data[0])

    menu = await dao.fetch_recipes()
    
    context = {
        'request': request,
        'title': 'Про нас',
        'menu': menu,
        'user': user_data,
    }

    template_response = templates.TemplateResponse(
        'menu.html',
        context=context,
    )


    template_response.set_cookie(key='token', value=token, httponly=True)
    return template_response



@router.get('/login')
async def login(request: Request):
    context = {
        'request': request,
        'title': 'Ввійти',
    }

    return templates.TemplateResponse(
        'login.html',
        context=context,
    )



@router.post('/login-final')
async def login(request: Request, login: EmailStr = Form(), password: str = Form()):
    user = await AuthLibrary.authenticate_user(login=login, password=password)
    token = await AuthHandler.encode_token(user.id)

    
    context = {
        'request': request,
        'title': 'Наше меню',
        'menu': await dao.fetch_recipes(),
        'user': user,
    }

    response =  templates.TemplateResponse(
        'menu.html',
        context=context,
    )
    
    response.set_cookie(key='token', value=token, httponly=True)
    return response




@router.post('/logout')
@router.get('/logout')
async def logout(request: Request, response: Response, user=Depends(dependencies.get_current_user_optional)):
    
    menu = await dao.fetch_recipes()
    
    context = {
        'request': request,
        'title': 'Наше меню',
        'menu': menu,
    }
    result = templates.TemplateResponse(
        'menu.html',
        context=context,
    )
    result.delete_cookie('token')
    return result



@router.get('/by_category/{category_name}')
async def by_category(category_name: str, request: Request, user=Depends(dependencies.get_current_user_optional)):
    
    menu = await dao.fetch_recipes()
    menu = [menu for menu in menu if category_name in menu['category']]

    context = {
        'request': request,
        'title': f'Наше меню - результати пошуку по категорії {category_name}',
        'menu': menu,
        'user': user,
        'categories': '',
    }
    return templates.TemplateResponse(
        'menu.html',
        context=context,
    )


# @router.get('/recipe/{dish_id}')
# async def recipe(request: Request, dish_id: int, user=Depends(dependencies.get_current_user_optional)):
#     required_dish = {}
    

#     for dish in await dao.get_recipe_by_title():
#         if dish['id'] == dish_id:
#             required_dish = dish
#             break
            
#     context = {
#         'request': request,
#         'title': f'Рецепт {dish_id}',
#         'user': user,
#         'recipe': required_dish,
#     }
    
#     return templates.TemplateResponse(
#         'recipe.html',
#         context=context,
#     )
    
################################################

@router.get('/create')
@router.post('/create')
async def create(request: Request, user=Depends(dependencies.get_current_user_optional)):

    context = {
        'request': request,
        'title': 'Створити рецепт',
        'user': user,
    }
    
    return templates.TemplateResponse(
        'create.html',
        context=context,
    )
    
    
    
@router.get('/create-final')
@router.post('/create-final')
async def create_final(request: Request,
                       title: str = Form(),
                       image: str = Form(),
                       complexity: str = Form(),
                       category: str = Form(),
                       recipe: str = Form(),
                       
                       user=Depends(dependencies.get_current_user_optional)
                       ):
    
    print(title, image, complexity, category, recipe, user)
    create_recipe = await dao.create_recipe(
        title=title,
        image=image,
        complexity=complexity,
        category=category,
        recipe=recipe,
    )
    
    recipes = await dao.fetch_recipes()
    
    context = {
        'request': request,
        'title': 'Створити рецепт',
        'menu': recipes,
        'user': user,
        'categories': '',
        
    }
    
    return templates.TemplateResponse(
        'menu.html',
        context=context,
    )
    
    
    
################
@router.get('/menu/{recipe_title}')
async def get_recipe_title(request: Request, recipe_title: str, user=Depends(dependencies.get_current_user_optional)):
    
    recipe_data = await dao.get_recipe_by_title(recipe_title=recipe_title)
    
    
    context = {
        'request': request,
        'title': f'{recipe_title}',
        'recipe': recipe_data,
        'user': user,
    }
    
    # print(context, 222222222222222222222222222222222222)
    return templates.TemplateResponse(
        'recipe.html',
        context=context,
    )
    