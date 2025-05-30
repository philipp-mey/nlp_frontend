import uvicorn


def main() -> None:
    """
    Main function to run the FastAPI application.
    """
    uvicorn.run("src.bff_api.root:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
