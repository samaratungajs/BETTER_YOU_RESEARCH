//import liraries
import { useNavigation } from '@react-navigation/core';
import React, { Component, useEffect, useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image,
    Alert,
    ScrollView,
    FlatList,} from 'react-native';


// create a component
export const Home = () => {
    const [data, setData] = useState([]);

    const navigation = useNavigation();

    useEffect(() => {
    setData( [
        {id:1, title: "Chatbot",  color:"#00BFFF", members:8,  image:"https://img.icons8.com/external-prettycons-flat-prettycons/200/null/external-conversation-multimedia-prettycons-flat-prettycons.png", name:"Chatbot"},
        {id:1, title: "Record Audio",     color:"#87CEEB", members:6,  image:"https://img.icons8.com/bubbles/200/null/voice-memos.png", name:"Audio" },
        {id:2, title: "Conversation",     color:"#4682B4", members:12, image:"https://img.icons8.com/external-smashingstocks-flat-smashing-stocks/200/null/external-chatbot-tech-support-mentoring-and-training-smashingstocks-flat-smashing-stocks.png", name:'VoiceConversation'} ,
        {id:3, title: "Activities",   color:"#20B2AA", members:5,  image:"https://img.icons8.com/external-flaticons-flat-flat-icons/200/null/external-activities-vacation-planning-guys-trip-flaticons-flat-flat-icons.png"} ,
        // {id:4, title: "Friends",  color:"#FF69B4", members:6,  image:"https://img.icons8.com/color/70/000000/groups.png"} ,
        // {id:5, title: "School",   color:"#00BFFF", members:7,  image:"https://img.icons8.com/color/70/000000/classroom.png"} ,
        // {id:6, title: "Things",   color:"#00FFFF", members:8,  image:"https://img.icons8.com/dusk/70/000000/checklist.png"} ,
        // {id:8, title: "World",    color:"#20B2AA", members:23, image:"https://img.icons8.com/dusk/70/000000/globe-earth.png"} ,
        // {id:9, title: "Remember", color:"#191970", members:45, image:"https://img.icons8.com/color/70/000000/to-do.png"} ,
        // {id:9, title: "Game",     color:"#008080", members:13, image:"https://img.icons8.com/color/70/000000/basketball.png"} ,
      ])
    }, [])

    const clickEventListener=(item)=> {
        navigation.navigate(item.name);
      }

      
    return (
       
        // <View style={styles.container}>
        //     <Text style={{fontSize:20, fontFamily:FONT.Regular}}>Home</Text>
        //     <Button title="Chatbot" onPress={()=> navigation.navigate('Chatbot')}/>
        //     <Button title="Voice Conversation" onPress={()=> navigation.navigate('VoiceConversation')}/>
        //     <Button title="Audio" onPress={()=> navigation.navigate('Audio')}/>
        // </View>
        <View style={{flex:1}}>
        <Image style={styles.backgroundImg}
        source={require('../assets/images/onboard2.jpg')}/>
        <View style={styles.container}>
        <FlatList style={styles.list}
          contentContainerStyle={styles.listContainer}
          data={data}
          horizontal={false}
          numColumns={2}
          keyExtractor= {(item) => {
            return item.id;
          }}
          renderItem={({item}) => {
            return (
              <TouchableOpacity style={[styles.card, {backgroundColor:item.color}]} onPress={() => {clickEventListener(item)}}>
                <View style={styles.cardHeader}>
                  <Text style={styles.title}>{item.title}</Text>
                  <Image style={styles.icon} source={{uri:"https://img.icons8.com/ios/40/000000/settings.png"}}/>
                </View>
                <Image style={styles.cardImage} source={{uri:item.image}}/>
                <View style={styles.cardFooter}>
                  <Text style={styles.subTitle}>{item.members} members</Text>
                </View>
              </TouchableOpacity>
            )
          }}/>
      </View>
      </View>
    );
};

// define your styles
const styles = StyleSheet.create({
    container:{
      flex:0.,
    },
    backgroundImg:{
    flex: 1,
    width: null,
    height: null,
    resizeMode: 'cover'
    },
    list: {
      //paddingHorizontal: 5,
      backgroundColor:"#E6E6E6",
    },
    listContainer:{
      alignItems:'center'
    },
    /******** card **************/
    card:{
      marginHorizontal:2,
      marginVertical:2,
      flexBasis: '48%',
    },
    cardHeader: {
      paddingVertical: 17,
      paddingHorizontal: 16,
      borderTopLeftRadius: 1,
      borderTopRightRadius: 1,
      flexDirection: 'row',
      alignItems:"center", 
      justifyContent:"center"
    },
    cardContent: {
      paddingVertical: 12.5,
      paddingHorizontal: 16,
    },
    cardFooter:{
      flexDirection: 'row',
      justifyContent: 'space-between',
      paddingTop: 12.5,
      paddingBottom: 25,
      paddingHorizontal: 16,
      borderBottomLeftRadius: 1,
      borderBottomRightRadius: 1,
    },
    cardImage:{
      height: 70,
      width: 70,
      alignSelf:'center'
    },
    title:{
      fontSize:16,
      flex:1,
      color:"#FFFFFF",
      fontWeight:'bold'
    },
    subTitle:{
      fontSize:12,
      flex:1,
      color:"#FFFFFF",
    },
    icon:{
      height: 20,
      width: 20, 
    }
  });    
