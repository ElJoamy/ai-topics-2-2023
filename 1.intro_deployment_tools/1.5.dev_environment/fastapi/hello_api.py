from fastapi import FastAPI


app = FastAPI(title="Hello API")


@app.get("/")
def root():
    return {"message": "hello", "status": "OK"}


def main():
    """Main function"""
    import uvicorn

    uvicorn.run("hello_api:app", reload=True)


if __name__ == "__main__":
    # only run this if the file is executed as a script
    main()
