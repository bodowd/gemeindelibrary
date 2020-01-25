from gemlibapp import create_app  # since this exists in __init__.py it can be found and imported

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
