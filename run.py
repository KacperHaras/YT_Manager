from app import create_app

app = create_app()

from app import routes

if __name__ == '__main__':
    app.run(debug=True)