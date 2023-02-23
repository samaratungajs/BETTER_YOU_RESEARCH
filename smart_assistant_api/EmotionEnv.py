from bson import ObjectId
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import random
from pymongo import MongoClient
from bson.json_util import dumps, loads
CLUSTER = MongoClient("mongodb+srv://RP_MA:lDlStI5Nan7gDUdx@cluster0.ikjpi.mongodb.net/?retryWrites=true&w=majority")
DB = CLUSTER["counseling_chatbot"]

class EmotionEnv(Env):
    def __init__(self):
        COLLECTION = DB["users"]
        user = COLLECTION.find_one({"_id": ObjectId("63708f92554a0cc61e80f3b1")})
        friend_list = []
        for i in user['friendList']:
            friend_list.append(i)
        print(friend_list)
        list_len = len(friend_list)
        # Actions we can take, down, stay, up
        self.action_space = Discrete(list_len)
        # Friends array
        self.observation_space = Box(low=np.array([0]), high=np.array([list_len]))
        # self.observation_space = Box(0, 2, [11, 12, 59, 56])

        # Set start emotion
        self.state = 3 + random.randint(-3, 3)
        # Set emotion length
        self.emotion_length = 60

    def step(self, action):
        # should take actions by human
        # print('This is suggested friend id', action)
        # self.state += int(input("Enter your emotional level : "))

        self.state = action

        # Reduce emotion length by 1 second
        self.emotion_length -= 1

        reward = 0

        # Calculate reward
        if self.state == 0:
            reward = 3
        elif self.state == 1:
            reward = -1
        elif self.state == 2:
            reward = -3
        elif self.state == 3:
            reward = 2
        elif self.state == 4:
            reward = -2
        # elif self.state == 5:
        #     reward = 4

        # Check if emotion is done
        if self.emotion_length <= 0:
            done = True
        else:
            done = False

        # self.state += random.randint(-1,1)
        # Set placeholder for info
        info = {}

        # Return step information
        return self.state, reward, done, info

    def render(self):
        # Implement viz
        pass

    def reset(self):
        # Reset emotion state
        self.state = 38 + random.randint(-3, 3)
        # Reset emotion time
        self.shower_length = 60
        return self.state
