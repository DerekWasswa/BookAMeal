from v1.api import create_app
from v1.api import db

app = create_app('production')
with app.app_context():
    db.create_all()

# Run the app :)
if __name__ == '__main__':
    app.run(debug=True)
