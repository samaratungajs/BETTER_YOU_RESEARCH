import axios from 'axios';
import React, { useCallback, useEffect, useState } from 'react'
import { Text, View } from 'react-native'
import { Bubble, GiftedChat, Send } from 'react-native-gifted-chat';
import { getChats, sendToRasa } from '../api';
import { ChatHeader } from '../components/chatbot/ChatHeader'
import uuid from 'react-native-uuid';
import {IMAGE} from '../assets/images/chatbotImage'
import { COLOR, FONT } from '../themes';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons'
import { unixConvertion } from '../assets/utils/UnixConverter';

export const Chatbot = () => {
  const [messages, setMessages] = useState([]);

  const BOT_USER = {
    _id: 2,
    name: 'FAQ Bot',
    avatar: IMAGE.chatbot
  };
  const USER = {
    _id:1,
    name: 'USER',
  };

  const BOT_MSG = [{
    _id: uuid.v4(),
    text: `Hi! I am the FAQ bot 🤖 from TEST.\n\nHow may I help you with today?`,
    createdAt: new Date(),
    user: BOT_USER
  }]

  useEffect(() => {
    getChatForUser();
  }, [])

const getChatForUser=async() => {
    try{
      const res = await getChats(USER._id)
      const filter1 = res.data[0].events

      //Filter the User and Bot messaages
      const chats = filter1.filter((n)=>{
        return (n.event == "user" || n.event=="bot") && n
      }) 
      console.log(chats)
      let conv = [];
      chats.map((c)=>{
        if(c.event=="bot"){
          const chat = {
           ...c,
           _id:uuid.v4(),
           createdAt:new Date(unixConvertion(c.timestamp)),
           user: BOT_USER
           }
           conv.push(chat)
        }
        else{
          const chat = {
            ...c,
            _id:uuid.v4(),
            createdAt:new Date(unixConvertion(c.timestamp)),
            user:USER
          }
          conv.push(chat)
        }
      }
      )
      console.log(conv)
      setMessages(conv.concat(BOT_MSG));
    }
    catch(err){
      console.log(err)
    }
  }


  const onSend = useCallback(async(msg = []) => {
    console.log(msg[0].text);
    setMessages(previousMessages => (GiftedChat.append(previousMessages, msg)));
    try{
      const req = {message:msg[0].text, sender: USER._id}
      const res = await sendToRasa(req);
      console.log(res);
      
      let reply = [];
      res.data.map((d)=>{
        console.log(d.text);
         const rp = {
          _id:uuid.v4(),
          text: d.text,
          createdAt: new Date(),
          user: BOT_USER
          }
          reply.push(rp)
      }
      )
      setMessages(prev=> prev.concat(reply));
    }
    catch(err){
      console.log(err)
    }
  }, [])


  //Customize bubbles
  const renderBubble = (props)=>{
    return(
    <Bubble
      {...props}
      wrapperStyle={{
        right:{
          backgroundColor: COLOR.primary
        },
        left:{
          backgroundColor: COLOR.white
        }
      }}
      textStyle={{
        right:{
          fontFamily:FONT.Regular,
          color:COLOR.white,
          fontSize:14,
        },
        left:{
          fontFamily:FONT.Regular,
          fontSize:14,
          color:COLOR.greyFont
        }
      }}
    />
    )
  }


  //Change the send button
  const renderSend = (props) => {
    return(
      <Send {...props}>
        <View>
          <MaterialCommunityIcons name='send-circle' size={42} style={{marginBottom:5, marginRight:5}} color={COLOR.primary}/>
        </View>
      </Send>
    )

  }

  return (
    <View style={{flex:1}}>
    <ChatHeader/>
    <GiftedChat
      messages={messages.reverse()}
      onSend={msg => onSend(msg)}
      user={USER}
      alwaysShowSend={true}
      renderAvatarOnTop={true}
      renderBubble={renderBubble}
      renderSend={renderSend}
      scrollToBottom
    />
    </View>
  )
}
