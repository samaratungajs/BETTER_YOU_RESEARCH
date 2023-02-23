from ast import Return
import json
from flask import Flask, jsonify, request
from sentiment_analysis import Sentiment
import operator
from pymongo import MongoClient
from bson.json_util import dumps, loads

CLUSTER = MongoClient("mongodb+srv://RP_MA:lDlStI5Nan7gDUdx@cluster0.ikjpi.mongodb.net/?retryWrites=true&w=majority")
DB = CLUSTER["counseling_chatbot"]

print('Loading Sentiment Analysis model')

sa = Sentiment()

app = Flask(__name__)

sentiment_dict = dict()

score_report = list()


@app.route('/test', methods=['POST'])
def index_test():

    global sentiment_dict
    global score_report
    overall_output=dict()

    js_text = request.get_json()

    #Initialize the dictionary
    if "start" in js_text:
        if js_text["start"]:
            sentiment_dict=dict()
            score_report=list() 
    else:
        return jsonify({"error":"You have to define the start in the payload"})
    
    pred=sa.get_sentiment_prediction(js_text['text'])

    # max_emotion = max(pred.items(), key=operator.itemgetter(1))[0]
    # max_value = max(pred.items(), key=operator.itemgetter(1))[1]
    # output={"text":js_text['text'], "matchedEmotion":max_emotion,"maximumValue":max_value, "emotionWithAverage":pred}
    # score_report.append(output)

    # if max_emotion in sentiment_dict:
    #     sentiment_dict[max_emotion]+=max_value
    # else:
    #     sentiment_dict[max_emotion]=max_value
    
    # sorted_values = {k:v for k,v in sorted(sentiment_dict.items(), key=lambda x: x[1], reverse=True)}
    # overall_output={"overalEmotion":list(sorted_values.keys())[0],"overalScore":list(sorted_values.values())[0], "otherScores":dict(zip(list(sorted_values.keys())[1:],list(sorted_values.values())[1:]))}

    # overal_output={"overall":overall_output, "individual": score_report}
    # overal_res=json.dumps(overal_output)

    overall_res = json.dumps(pred)
    ##clear the dictionary
    if "end" in js_text:
        if js_text["end"]:
             sentiment_dict=dict() 
             score_report=list()

    return overall_res


@app.route('/chats/<id>', methods=['GET'])
def index_chats(id):
    COLLECTION = DB["conversations"]
    chats = COLLECTION.find({"sender_id":str(id)})
    print(chats)
    list_chat = list(chats)
    json_data = dumps(list_chat, indent = 2)
    return json_data

app.run(debug=True, port=8000)