//import liraries
import React, {useState, useEffect} from 'react';
import {View, Text, StyleSheet, SafeAreaView} from 'react-native';
import {Onboard} from './src/screens/Onboard';
import {NavigationContainer} from '@react-navigation/native';
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import {Home} from './src/screens/Home';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {Chatbot} from './src/screens/Chatbot';
import {VoiceConversation} from './src/screens/VoiceConversation';
import { Audio } from './src/screens/Audio';
import VideoTest from './src/screens/VideoTest';

const Stack = createNativeStackNavigator();

// create a component
const App = () => {
  const [onBoardState, setonBoardState] = useState();

  useEffect(() => {
    retrieveData();
  });

  //Onboarding check
  const retrieveData = async () => {
    try {
      const value = await AsyncStorage.getItem('hasOnboarded');
      // We have data!!
      setonBoardState(value);
    } catch (error) {
      // Error retrieving data
    }
  };

  return (
    <NavigationContainer>
      <Stack.Navigator>
      {/* <Stack.Screen
          name="Video"
          component={VideoTest}
          options={{title: 'Video'}}
        /> */}
        <Stack.Screen
          name="Home"
          component={Home}
          options={{title: 'Welcome'}}
        />
        <Stack.Screen
          name="Chatbot"
          component={Chatbot}
          options={{headerShown: false}}
        />
        <Stack.Screen
          name="VoiceConversation"
          component={VoiceConversation}
          options={{headerShown: false}}
        />
        <Stack.Screen
          name="Audio"
          component={Audio}
          options={{title: 'Audio'}}
        />
        <Stack.Screen
          name="Onboard"
          component={Onboard}
          initialParams
          options={{headerShown: false}}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

// define your styles
const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#2c3e50',
  },
});

//make this component available to the app
export default App;
