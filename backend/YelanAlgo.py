from flask import Flask, request
import flask
from flask_cors import CORS
import json
import re
import random


# Responses
def unknown():
    response = [
        "could you repeat that?",
        "I can't undestand",
        "try again",
        "what does that mean?"
    ][random.randrange(4)]
    return response

#checks how monika should respond
def message_probability(user_message, recognized_words, single_response = False, required_words = []):
    message_certainty = 0
    has_required_words = True
    # counts how many words are present in each predefined message
    for word in user_message:
        if word in recognized_words:
            message_certainty += 1
    # calculates the percent of recognized words in a user message
    percentage = float(message_certainty) / float(len(recognized_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}
    def response(bot_response, list_of_words, single_response = False, required_words = []):
       nonlocal highest_prob_list
       highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)
    # Response list ======================================================
    response("Hi", ["hello", "hi", "sup", "hey", "heyo", "heya", "howdy"], single_response = True)
    response("I\'m doing fine, and you?", ["how", "are", "you", "doing"], required_words = ["how"])
    response("I\'m Yelan, a virtual assistant and a character from genshin impact", ["who", "are", "you"], required_words = ["who"])
    # finds the best response
    best_match = max(highest_prob_list, key=highest_prob_list.get)
    #print(highest_prob_list) # Displays the probability
    return unknown() if highest_prob_list[best_match] < 1 else best_match


#filters out the user input
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


# Main
app = Flask(__name__)
CORS(app)

# routes to connect
@app.route('/respond', methods=["GET", "POST"])
def users():
    print("users endpoint reached...")
    # retrieves user data
    if request.method == "GET":
        with open("YelanResponses.json", "r") as f:
            data = json.load(f)
            received_data = request.get_json()
            message = received_data['data']
            response_data = get_response(message)
            data.append({
                "Yelan": f"{response_data}",
                "Traveler": f"{message}"
            })
            return flask.jsonify(data)
    # returns a response
    if request.method == "POST":
        received_data = request.get_json()
        print(f"received data: {received_data}")
        message = received_data['data']
        response_data = get_response(message)
        #return_data = {
        #    "status": "success"
        #    ,"message": f"received: {message}"
        #    ,"response": f"Yelan: {response_data}"
        #}
        return_data = f"Yelan: {response_data}"
        return flask.Response(response=json.dumps(return_data), status=201)

def main():
    app.run("localhost", 6969)  

if __name__ == "__main__":
    main()