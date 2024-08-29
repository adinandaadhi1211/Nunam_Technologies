from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/overview', methods=['GET'])
def get_cell_summary():
    return render_template('overview.html')

@app.route('/cell/<int:cell_id>/data', methods=['GET'])
def get_cell_data(cell_id):
    return render_template('cell.html', cell_id=cell_id)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
