from app import app


@app.route('/')
@app.route('/index')
def index():
    return "HCA App Landing Page"
