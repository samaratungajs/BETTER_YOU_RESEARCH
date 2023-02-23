pip install -r requirements.txt





#add new intents
    data -> nlu.yml, domain.yml

#add new responses
    data -> response.yml

#connect intents and responses
    data -> rules.yml
    

cd Rasa_chatbbot
rasa_env --> rasa train




#run the rasa chatbot
cd Rasa_chatbbot
rasa run --enable-api --cors "*" --port 5005





#API end-points
    1) http://localhost:5005/webhooks/rest/webhook   type=POST
        -body -->json -> {message:"text",
                    send_id:"1"}

    2) http://localhost:5005/model/parse   type=POST
            -body -->json -> {text:"text"}



