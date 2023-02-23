import pandas as pd
import text_hammer as th
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer,TFBertModel
import shutil
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.initializers import TruncatedNormal
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.metrics import CategoricalAccuracy
from tensorflow.keras.utils import to_categorical
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense

class Sentiment:
    def __init__(self) -> None:
        self.tokenizer=self.get_tokenizer()
        self.categories=self.get_categories()
        self.model=self.create_model(load_weights=True)

         
    def get_dataset(self):
        df_train = pd.read_csv('./datasets/train.txt', header=None, sep=';', names = ['Input','Sentiment'], encoding='utf-8')
        df_test = pd.read_csv('./datasets/test.txt', header=None, sep=';', names = ['Input','Sentiment'], encoding='utf-8')
        df_val = pd.read_csv('./datasets/val.txt', header=None, sep=';', names = ['Input','Sentiment'], encoding='utf-8')

        df_full = pd.concat([df_train,df_test,df_val], axis=0)
        return df_full



    def text_preprocessing(self,df,col_name):
        column = col_name
        df[column] = df[column].apply(lambda x:str(x).lower())
        df[column] = df[column].apply(lambda x: th.cont_exp(x))
        df[column] = df[column].apply(lambda x: th.remove_emails(x))
        df[column] = df[column].apply(lambda x: th.remove_special_chars(x))
        df[column] = df[column].apply(lambda x: th.remove_accented_chars(x))
        return df.copy()

    def inspect_dataset(self,df):
        print(df.head())

        if 'Sentiment' in df.columns:
            print(df.Sentiment.unique)



    def clean_dataset(self,df) -> pd.DataFrame:
        cdf=self.text_preprocessing(df, 'Input')
        cdf['num_words'] = cdf.Input.apply(lambda x: len(x.split()))
        cdf['Sentiment'] = cdf.Sentiment.astype('category')
        cdf['Sentiment'] = cdf.Sentiment.cat.codes
        cdf_copy=cdf.copy()
        return cdf_copy

    def get_categories(self):
        return {'angry':0, 'fearful':1, 'happy':2, 'calm':3, 'sad':4, 'surprise':5}


    def split_dataset(self,df):
        return train_test_split(df, test_size = 0.3, random_state = 42, stratify = df.Sentiment)

    def get_tokenizer(self):
        # tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')
        # tokenizer.save_pretrained('./bert_model/bert-tokenizer')
        tokenizer = AutoTokenizer.from_pretrained('./bert_model/bert-tokenizer')
        #shutil.make_archive('bert-tokenizer', 'zip', './bert_model/bert-tokenizer')
        return tokenizer

    def create_model(self,train_set=None, test_set=None, tokenizer=None, load_weights=False):
        # bert = TFBertModel.from_pretrained('bert-base-cased')
        bert = TFBertModel.from_pretrained('./bert_model/bert-model')
        # bert.save_pretrained('./bert_model/bert-model')

        # shutil.make_archive('bert-model','zip','./bert_model/bert-model')

        if train_set and test_set:
            x_train = tokenizer(
                text=train_set.Input.tolist(),
                add_special_tokens=True,
                max_length=70,
                truncation=True,
                padding=True, 
                return_tensors='tf',
                return_token_type_ids = False,
                return_attention_mask = True,
                verbose = True)

            x_test = tokenizer(
                text=test_set.Input.tolist(),
                add_special_tokens=True,
                max_length=70,
                truncation=True,
                padding=True, 
                return_tensors='tf',
                return_token_type_ids = False,
                return_attention_mask = True,
                verbose = True)



        max_len = 70

        input_ids = Input(shape=(max_len,), dtype=tf.int32, name="input_ids")
        input_mask = Input(shape=(max_len,), dtype=tf.int32, name="attention_mask")
        # embeddings = dbert_model(input_ids,attention_mask = input_mask)[0]


        embeddings = bert(input_ids,attention_mask = input_mask)[0] #(0 is the last hidden states,1 means pooler_output)
        out = tf.keras.layers.GlobalMaxPool1D()(embeddings)
        out = Dense(128, activation='relu')(out)
        out = tf.keras.layers.Dropout(0.1)(out)
        out = Dense(32,activation = 'relu')(out)

        y = Dense(6,activation = 'sigmoid')(out)
            
        model = tf.keras.Model(inputs=[input_ids, input_mask], outputs=y)
        model.layers[2].trainable = True
        # for training bert our lr must be so small

        optimizer = Adam(
        learning_rate=5e-05, # this learning rate is for bert model , taken from huggingface website 
        epsilon=1e-08,
        decay=0.01,
        clipnorm=1.0)

        loss =CategoricalCrossentropy(from_logits = True)
        metric = CategoricalAccuracy('balanced_accuracy'),

        model.compile(
        optimizer = optimizer,
        loss = loss, 
        metrics = metric)

        tf.config.experimental_run_functions_eagerly(True)
        tf.config.run_functions_eagerly(True)


        #Load weights
        if load_weights:
            model=self.load_model_weights(model)


        return model




    def load_model_weights(self,model):
        model.load_weights('./model_weights/sentiment_weights3.h5')
        return model


    def predict(self, model, text,encoded_dict,tokenizer):

        x_val = tokenizer(
            text=text,
            add_special_tokens=True,
            max_length=70,
            truncation=True,
            padding='max_length', 
            return_tensors='tf',
            return_token_type_ids = False,
            return_attention_mask = True,
            verbose = True) 
        validation = model.predict({'input_ids':x_val['input_ids'],'attention_mask':x_val['attention_mask']})
        
        predictions={}
        for key , value in zip(encoded_dict.keys(),validation[0]):
            st_value = str(value)
            predictions[key]=float(st_value)
        
        return predictions



    def get_sentiment_prediction(self, text):
        prediction= self.predict(self.model,text,self.categories, self.tokenizer)
        return prediction




if __name__=='__main__':
    # print('Loading dataset...')
    # df=get_dataset()
    # print('clean dataset...')
    # cdf=clean_dataset(df)
    # print('inspecting...')
    # inspect_dataset(cdf)
    # print('spliting...')
    # train_set, test_set=split_dataset(cdf) 
    sa = Sentiment()
    prediction= sa.get_sentiment_prediction("I am happy")
    print(prediction)


