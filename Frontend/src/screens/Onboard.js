import React from 'react';
import { Image, View, StyleSheet, TouchableOpacity, Text, Button } from 'react-native';
import Onboarding from 'react-native-onboarding-swiper';
import { useNavigation } from '@react-navigation/core';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { COLOR } from '../themes';


const Square = ({ isLight, selected }) => {
  let backgroundColor;
  let width;
  if (isLight) {
    backgroundColor = selected ? COLOR.primary : 'rgba(0, 0, 0, 0.3)';
    width = selected ? 40 : 8
  } else {
    backgroundColor = selected ? COLOR.primary : 'rgba(255, 255, 255, 0.5)';
  }
  return (
    <View
      style={{
        width,
        height: 8,
        marginHorizontal:1,
        borderRadius:8,
        backgroundColor,
      }}
    />
  );
};

const Done = ({ isLight, ...props }) => {
    const navigation = useNavigation();
  return (  <TouchableOpacity {...props} onPress={async ()=>{
  // await AsyncStorage.setItem('hasOnboarded',true
  // );
  navigation.navigate('Home')
       }
    }>
    <View style={{
        backgroundColor: COLOR.primary,
        alignItems: 'center', 
        justifyContent: 'center',
        paddingVertical:"3%",
        paddingHorizontal:"10%",
        marginRight:15,
        borderRadius: 20
      }}
    >
      <Text style={{ color: COLOR.white,fontSize:16 }}>Get Start</Text>
    </View>
  </TouchableOpacity>
);
    }
const Skip = ({ ...props}) =>{
    const navigation = useNavigation();
  return(
  <TouchableOpacity {...props} onPress={async ()=>{
    await AsyncStorage.setItem('hasOnboarded', JSON.stringify({
    hasOnboarded:true
  }));
  navigation.navigate('Home')
  }}>
  <View style={{
      backgroundColor: COLOR.white,
      alignItems: 'center', 
      justifyContent: 'center',
      paddingVertical:"3%",
      paddingHorizontal:"10%",
      marginLeft:15,
      borderRadius: 20
    }}
  >
    <Text style={{ color: COLOR.primary,fontSize:16, fontWeight:"bold"}}>Skip</Text>
  </View>
</TouchableOpacity>
)};


const Next = ({ isLight, ...props }) => (
    <TouchableOpacity {...props}>
  <View style={{
      backgroundColor: COLOR.primary,
      alignItems: 'center', 
      justifyContent: 'center',
      paddingVertical:"3%",
      paddingHorizontal:"10%",
      marginRight:15,
      borderRadius: 20
    }}
  >
    <Text style={{ color: COLOR.white,fontSize:16 }}>Next</Text>
  </View>
</TouchableOpacity>
  );

export const Onboard = () => (
  <Onboarding
    DotComponent={Square}
    NextButtonComponent={Next}
    SkipButtonComponent={Skip}
    DoneButtonComponent={Done}
    bottomBarColor={COLOR.white}
    subTitleStyles={{fontSize:14,marginTop:-60,paddingHorizontal:10}}
    titleStyles={{fontWeight:"bold", fontSize:24, marginTop:-120}} // set default color for the title
    pages={[
      {
        backgroundColor: COLOR.backgroundOnBoard,
        image: <Image style={styles.image} source={require('../assets/images/onboard1.jpg')} />,
        title: "Buy & Selling",
        subtitle: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.',

      },
      {
        backgroundColor: COLOR.backgroundOnBoard,
        image: <Image style={styles.image} source={require('../assets/images/onboard2.jpg')} />,
        title: 'From Anywhere ',
        subtitle: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
      },
      {
        backgroundColor: COLOR.backgroundOnBoard,
        image: <Image style={[styles.image]} source={require('../assets/images/onboard3.jpg')} />,
        title: 'Real State',
        subtitle: "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
      },
    ]}
  />
);

const styles = StyleSheet.create({
    image:{
        width:"100%",
        height:"75%",
        margin:0
    },
    button:{
        backgroundColor:COLOR.white,
    }
})