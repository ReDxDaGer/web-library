from flask import Flask , render_template , request
import json
import os
app = Flask(__name__)


def load_data(category):
    data_folder = 'data'
    filename = os.path.join(data_folder, f'{category}.json')
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

@app.route("/")
def index():
    category = request.args.get('category', 'all')
    if category == 'all':
        data = load_data('tech') + load_data('romance') + load_data('horror') + load_data('psychology')
    elif category in ['tech', 'romance', 'horror', 'psychology']:
        data = load_data(category)
    else:
        data = []
    return render_template('index.html', data=data, category=category)

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query')
    if query:
        with open('data.json') as f:
            data = json.load(f)
        search_results = [item for item in data if query.lower() in item['name'].lower()]
        return render_template('search.html', query=query, results=search_results)
    else:
        return render_template('search.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_code=404, error_message="Page Not Found"), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error_code=500, error_message="Internal Server Error"), 500


if __name__ == "__main__":
    app.run(debug=True)
