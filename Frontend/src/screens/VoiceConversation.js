import React, {useEffect, useState} from 'react';
import {
  View,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Text,
  ToastAndroid,
  ImageBackground,
  Button,
} from 'react-native';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import {COLOR, FONT} from '../themes';
import Voice from '@react-native-community/voice';
import {sendToRasa} from '../api/';
import {IMAGE} from '../assets/images/chatbotImage';
import Tts from 'react-native-tts';
import Lottie from 'lottie-react-native';
import {LogBox} from 'react-native';
import { friendSuggest, predict } from '../api';
import AsyncStorage from '@react-native-async-storage/async-storage';


export function VoiceConversation() {
  LogBox.ignoreLogs(['new NativeEventEmitter']); // Ignore log notification by message
  LogBox.ignoreAllLogs(); //Ignore all log notifications
  Tts.setDefaultRate(0.4);

  const [pitch, setPitch] = useState('');
  const [error, setError] = useState('');
  const [end, setEnd] = useState(true);
  const [started, setStarted] = useState(false);
  const [reply, setReply] = useState('');
  const [request, setRequest] = useState("")
  const [results, setResults] = useState([]);
  const [partialResults, setPartialResults] = useState([]);

  const BOT_USER = {
    _id: 2,
    name: 'FAQ Bot',
    avatar: IMAGE.chatbot,
  };
  const USER = {
    _id: 1,
    name: 'USER',
  };

  const onSpeechStart = e => {
    setStarted(true);
  };
  const onSpeechEnd = () => {
    setStarted(false);
    setEnd(true);
    setStarted(false);
  };
  const onSpeechError = e => {
    setError(JSON.stringify(e.error));
  };
  const onSpeechResults = async e => {
    console.log(e.value[0]);
    setResults(e.value[0]);
    setRequest(prev=> prev + e.value[0]);
    getReply(e.value[0]);
  };
  const onSpeechPartialResults = e => {
    setPartialResults(e.value);
  };
  const onSpeechVolumeChanged = e => {
    setPitch(e.value);
  };

  useEffect(() => {
    Voice.onSpeechStart = onSpeechStart;
    Voice.onSpeechEnd = onSpeechEnd;
    Voice.onSpeechError = onSpeechError;
    Voice.onSpeechResults = onSpeechResults;
    Voice.onSpeechPartialResults = onSpeechPartialResults;
    Voice.onSpeechVolumeChanged = onSpeechVolumeChanged;
  }, []);

  const getReply = async text => {
    console.log('hit');
    try {
      const res = await sendToRasa({message: text, sender: USER._id});
      console.log(res)
      if(res.data.length>0){
        setReply(res.data[0].text);    
      Tts.getInitStatus().then(() => {
        Tts.speak(res.data[0].text, {
          androidParams: {
            KEY_PARAM_PAN: -1,
            KEY_PARAM_VOLUME: 0.5,
            KEY_PARAM_STREAM: 'STREAM_MUSIC',
          },
        });
      });
    }else{
      Tts.getInitStatus().then(() => {
        Tts.speak("Cannot understand you", {
          androidParams: {
            KEY_PARAM_PAN: -1,
            KEY_PARAM_VOLUME: 0.5,
            KEY_PARAM_STREAM: 'STREAM_MUSIC',
          },
        });
      });
    }
      Tts.addEventListener('tts-finish', (event) => startSpeechRecognizing());
    } catch (err) {
      ToastAndroid.show(err, ToastAndroid.LONG);
    }
  };
  const startSpeechRecognizing = async () => {
    setPitch('');
    setError('');
    setReply('')
    setStarted(true);
    // setReply('');
    setResults([]);
    setPartialResults([]);
    setEnd(false);
    try {
      await Voice.start('en-US');
    } catch (e) {
      console.error(e);
    }
  };
  const stopSpeechRecognizing = async () => {
    try {
      
      await Voice.stop();
      stops();
      setStarted(false);
      setResults([]);
      setPartialResults([]);
      setReply("")
    } catch (e) {
      console.error(e);
    }
  };

  
  //send for prediction
  const getPreditction = async ()=>{
    const prediction = await predict({"start": true, "text":request, "end":false});
    AsyncStorage.setItem('textPredict',JSON.stringify(prediction.data));
    await review()
  }

  const sortEmotions = (d) => {
      const emoList = {
        "happy":d.happy,
        "sad":d.sad,
        "angry": d.angry,
        "fearful":d.fearful,
        "calm": d.calm
      }
    return Object.values(emoList);
  }

  const review = async () => {
    
    let audioResult = await AsyncStorage.getItem('textPredict');  
    let aResult = JSON.parse(audioResult); 
 
    let textResult = await AsyncStorage.getItem('audioPredict');  
    let tResult = JSON.parse(textResult);

    const aArray = sortEmotions(aResult);
    const tArray = sortEmotions(tResult);

    console.log(aArray, tArray)
    // Happy", "Sad", "Angry", "Calm", "Fearful",
    console.log(aResult, tResult);
    const bd = {
      "model_1": aArray,
      "model_2": [0.088, 0.432, 0.345, 0.934, 0.777],
      "model_3": tArray,
      "weight": [72.73, 82.28, 92.68]
      }
    const res = await friendSuggest(bd)
    console.log(res.data);
  }
  
  return (
    <View style={styles.container}>
    <ImageBackground style={styles.image} 
      resizeMode='cover' 
      source={require('../assets/images/voice_background.jpg')}
      imageStyle={{opacity:0.25}}
      >
      <View style={styles.hBox1}>
      <Text style={{textAlign:'center',fontFamily:FONT.SemiBold,color:COLOR.greyFont, fontSize:30,padding:5,borderRadius:50}}>Start the Conversation</Text>
      </View>
      <View style={styles.hBox2}>
        {/* {partialResults.map((result, index) => {
          return (
            <Text key={`partial-result-${index}`} style={styles.message}>
              {results}
            </Text>
          );
        })} */}
        <Text style={[styles.message, {color: COLOR.primary, padding:5, backgroundColor:'white', borderRadius:50}]}>{reply}</Text>
      </View>
      <View style={styles.hBox3}>
      <Text style={styles.message}>{results}</Text>
        <TouchableOpacity onPress={startSpeechRecognizing}>
          <View style={{position: 'relative', alignItems:'center', paddingBottom:10}}>
          
            {started ? (
              <Lottie
                style={styles.checkAnimation}
                source={require('../assets/lottie/mic_animation.json')}
                autoPlay
                resizeMode="cover"
                loop={true}
                speed={1}
              />
            ) : (
              <View style={{borderRadius:140, width:'100%', backgroundColor: COLOR.primary}}>
              <MaterialCommunityIcons
                name="microphone"
                color={COLOR.white}
                size={90}
              />
              </View>
                
            )}
          </View>
        </TouchableOpacity>
      </View>
      <View style={{flexDirection:'row', justifyContent:'space-between'}}>
      <TouchableOpacity onPress={()=> stopSpeechRecognizing()}>
          <MaterialCommunityIcons
                name="stop-circle"
                color='red'
                size={55}
              /> 
              </TouchableOpacity>
        <TouchableOpacity onPress={()=>getPreditction()}>
        <MaterialCommunityIcons
                name="arrow-right-bold-circle"
                color='green'
                size={55}
              /> 
        </TouchableOpacity>

      </View>
      </ImageBackground>
    </View>
  );
}







const styles = StyleSheet.create({
  checkAnimation: {
    width: '95%',
    height: '95%',
    marginLeft: 7,
    marginTop: 10,
  },
  container: {
    flex: 1,
    backgroundColor:'white',
    flexDirection: 'column',
  },
  hBox1: {
    flex: 2,
    alignItems:'center',
    // backgroundColor: 'red',
  },
  hBox2: {
    flex: 3,
    // backgroundColor: 'darkorange',
    justifyContent: 'center',
    alignItems: 'center',
    flexDirection: 'column',
  },
  hBox3: {
    flex: 2,
    // backgroundColor: 'green',
    justifyContent: 'center',
    alignItems: 'center',
  },
  message: {
    fontFamily: FONT.SemiBold,
    fontSize: 30,
    color: 'black',
  },
  image:{
    flex:1,
    justifyContent:'center',
    padding: 20,
  },
  button: {
    flex:1,
    width: 80,
    height: 20,
    borderRadius:"50%"
  }
});
