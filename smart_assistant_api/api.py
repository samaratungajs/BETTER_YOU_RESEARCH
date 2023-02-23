from bson import ObjectId
from flask import Flask, request, url_for, redirect, render_template
from flask_cors import CORS
import json
from pymongo import MongoClient
from pandas._libs.lib import infer_dtype

import EmotionEnv
import pandas as pd

CLUSTER = MongoClient("mongodb+srv://RP_MA:lDlStI5Nan7gDUdx@cluster0.ikjpi.mongodb.net/?retryWrites=true&w=majority")
DB = CLUSTER["counseling_chatbot"]
env = EmotionEnv.EmotionEnv()
env.observation_space.sample()
state = env.reset()
done = False
score = 0
emotion = ''

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET', 'POST'])
def welcome():
    return_str = '{ "status" : "app works" }'
    return json.loads(return_str)


@app.route('/friend_suggestion', methods=['GET', 'POST'])
def friend_suggestion():
    COLLECTION = DB["users"]

    data = request.json
    model_output = []
    model_weights = []
    for i in data['model_1']:
        model_output.append(i)
    for i in data['model_2']:
        model_output.append(i)
    for i in data['model_3']:
        model_output.append(i)

    for i in data['weight']:
        model_weights.append(i)
        model_weights.append(i)
        model_weights.append(i)
        model_weights.append(i)
        model_weights.append(i)

    print(infer_dtype(model_weights))
    print(model_weights)

    global score, emotion

    df = pd.DataFrame(
        {
            "Score": model_output,
            "Weight": model_weights,
            "Model": ["A", "A", "A", "A", "A", "B", "B", "B", "B", "B", "C", "C", "C", "C", "C"],
            "Emotion": ["Happy", "Sad", "Angry", "Calm", "Fearful", "Happy", "Sad", "Angry", "Calm", "Fearful", "Happy",
                        "Sad", "Angry", "Calm", "Fearful"],
        }
    )
    df

    def grouped_weighted_avg(values, weights, by):
        return (values * weights).groupby(by).sum() / weights.groupby(by).sum()

    result = grouped_weighted_avg(df["Score"], df["Weight"], df["Emotion"])
    out = result.to_numpy()
    print(out)
    result_index = out.argmax()
    print(result_index)
    if result_index == 0:
        emotion = str("Angry")
        print(emotion)
    elif result_index == 1:
        emotion = str("Calm")
        print(emotion)
    elif result_index == 2:
        emotion = str("Fearful")
        print(emotion)
    elif result_index == 3:
        emotion = str("Happy")
        print(emotion)
    elif result_index == 4:
        emotion = str("Sad")
        print(emotion)
    else:
        emotion = str("love")
        print(emotion)

    action = env.action_space.sample()
    n_state, reward, done, info = env.step(action)
    score += int(result_index)


    user = COLLECTION.find_one({"_id": ObjectId("63708f92554a0cc61e80f3b1")})
    key_list = []
    for i in user['friendList']:
        key_list.append(i['username']);

    print(key_list)
    friend_name = key_list[action];

    return_str = '{ "suggested_friend_id" : ' + str(action) + ',' + '"emotion" : ' + '"' + str(
        emotion) + '"' + ',' + '"username" : ' + '"' + str(friend_name) + '"' + '} '

    print(return_str)

    return json.loads(return_str)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5500, debug=True)
