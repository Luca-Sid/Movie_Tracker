from flask import Flask, jsonify
from recommendations import recommend

app = Flask(__name__)

@app.route('/recommendation/<user_id>')
def recommendation(user_id):
    return jsonify(recommend(user_id))

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=5001
    )