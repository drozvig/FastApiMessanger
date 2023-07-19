import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from views import router as views_router
from database import init_database

def bind_events(app: FastAPI) -> None:
    @app.on_event("startup")
    async def set_engine():
        init_database()

    @app.on_event("shutdown")
    async def close_engine():
        pass

def get_app() -> FastAPI:
    app = FastAPI(
        title="PIT",
        description="Some text",
        docs_url="/docs",
        openapi_url="/api/test"
    )
    bind_events(app)
    app.include_router(views_router, prefix="")
    # app.add_middleware(CORSMiddleware,
    #                    allow_origins=["*"],
    #                    allow_credentials=True,
    #                    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    #                    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
    #                                   "Access-Control-Allow-Origin",
    #                                   "Authorization" , "X-PID-Token", "fastapiusersauth"], )

    return app


app = get_app()
if __name__ == '__main__':
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8080,
        #workers=3,
        #reload=True
    )
