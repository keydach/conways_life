from fastapi import FastAPI
from routers import router

app = FastAPI(
    title="Conways Life",
    version="0.1.0"
)
app.include_router(router)


def main():
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=16000)


if __name__ == '__main__':
    main()
