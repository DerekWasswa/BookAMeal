''' Link to the API documentation '''
from flask import render_template
from .import doc

@doc.route('/', methods=['GET'])
def index():
    return render_template('index.html')
