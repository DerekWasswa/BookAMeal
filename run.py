from v1.api import create_app

app = create_app('development')

# Run the app :)
if __name__ == '__main__':
    app.run(debug=True)  