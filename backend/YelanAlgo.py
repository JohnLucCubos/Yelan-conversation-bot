from flask import Flask, request
import flask
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/respond', methods=["GET", "POST"])
def users():
    print("users endpoint reached...")
    if request.method == "GET":
        with open("YelanResponses.json", "r") as f:
            data = json.load(f)
            data.append({
                "Yelan": "Greetings",
                "Traveler": ["Hi", "Hello", "Greetings"]
            })
            return flask.jsonify(data)
    
    if request.method == "POST":
        received_data = request.get_json()
        print(f"received data: {received_data}")
        message = received_data['data']
        return_data = {
            "status": "success"
            ,"message": f"received: {message}"
            ,"response": "Yelan: hi"
        }
        return flask.Response(response=json.dumps(return_data), status=201)

def main():
    app.run("localhost", 6969)  

if __name__ == "__main__":
    main()