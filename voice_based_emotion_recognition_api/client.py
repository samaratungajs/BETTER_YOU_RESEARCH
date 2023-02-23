import requests

URL="http://127.0.0.1:5000/predict"
TEST_AUDIO_FILE_PATH="03-01-03-01-01-01-03.wav"


if __name__ == "__main__":

    audio_file=open(TEST_AUDIO_FILE_PATH,"rb")
    values={"file":(TEST_AUDIO_FILE_PATH,audio_file,)}
    response=requests.post(URL,files=values)
    data=response.json()

    print("hello")
    print("Predicted keyword is:"+ {data})

