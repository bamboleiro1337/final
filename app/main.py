import sentry_sdk
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.auth import router_auth
from app.sockets import router_websocket
from app.web_pages import router_web_pages

sentry_sdk.init(
    dsn="https://1a6b12e7dbf7418233793cb807de9e53@o4505229726318592.ingest.sentry.io/4505761003864065",
    traces_sample_rate=1.0,
)


app = FastAPI(
    title='First our app',
    description='asdfasdfasd',
    version='0.0.1',
    debug=True,
)

app.mount('/app/static', StaticFiles(directory='app/static'), name='static')


app.include_router(router_web_pages.router)
app.include_router(router_auth.router)
app.include_router(router_websocket.router)



@app.get('/')
@app.post('/')
async def main_page() -> dict:
    return {'greeting': 'HELLO'}



@app.get('/{username}')
@app.get('/{username}/{user_nick}')
async def user_page(user_name: str, user_nick: str = '', limit: int = 10, skip: int = 0) -> dict:
    
    data = [i for i in range(1000)][skip:][:limit]
    return {'user_name': user_name, 'user_nick': user_nick, 'data': data}



