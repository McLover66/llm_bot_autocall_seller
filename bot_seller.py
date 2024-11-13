import os
import pandas as pd
import json
import openai
import streamlit as st
from bot_utils import Session, MessageHandler, InvStrategy, get_info
from gpt_service import GptClient
from dotenv import load_dotenv
from prompt_creator import SYSTEM_PROMPT, EXTRAC_FEATURES, IPD, DIALOGUE_PROMPT, ALL_PARAMS_COLLEXTED

load_dotenv()
openai_api_key = os.getenv("API_KEY")
# WELCOME MESSAGE
st.markdown("<h1 style='text-align: center;'>AI investment advisor</h1>", unsafe_allow_html=True)

if "strategy" not in st.session_state:
    st.session_state.strategy = InvStrategy()
# Пример использования объектов
message = MessageHandler()
session = Session()
client = GptClient(openai_api_key)
strategy = st.session_state.strategy 

if st.session_state.dialogue_stage == "start":
    #displays strategy table on left side, contain all parametrs for current strategy
    message.display_chat_history()

    user_message = st.chat_input("write here")
    if user_message:
        # FIRST PART
        if not st.session_state.selecting_parameters_starting:
            history = message.get_history()
            last_n_in_history = message.get_last_n_history(2)
            response = message.generate_response_message(user_message=user_message, gpt_client=client, prompt=SYSTEM_PROMPT.format(chat_history=history))
            indicator = message.generate_response_message(user_message=user_message, gpt_client=client, prompt=IPD.format(last_n = last_n_in_history))

            if indicator == "selecting_parameters_starting":
                st.session_state.selecting_parameters_starting = True 
            else:
                message.add_and_print("user", user_message)
                message.add_and_print("assistant", response)
        
        # SECOND PART
        if st.session_state.selecting_parameters_starting:
            if not strategy.is_all_not_none():
                message.add_and_print("user", user_message)
                curr_params = message.generate_response_message(user_message=user_message, 
                                                                gpt_client=client, 
                                                                prompt=EXTRAC_FEATURES)

                #update strategy with income parametrs
                strategy.update_by_json(json.loads(curr_params))
                
                #left side information
                strategy.strategy_table() 
                get_info()  

                # ask question if not everythong params are collected yet
                unknown_params = strategy.get_none()
                last_n_in_history = message.get_last_n_history(3)
                if not strategy.is_all_not_none():
                    response = message.generate_response_message(user_message=user_message, 
                                                                gpt_client=client, 
                                                                prompt=DIALOGUE_PROMPT.format(unknown_params=unknown_params, last_n = last_n_in_history))
                    message.add_and_print("assistant", response)                

                elif strategy.is_all_not_none():
                    all_params = strategy.get_all_pairs()
                    responcse = message.generate_response_message(user_message="", 
                                                                gpt_client=client,
                                                                prompt=ALL_PARAMS_COLLEXTED.format(params = all_params))
                    message.add_and_print("assistant", responcse)
                    session.make_cart_buttoms()




                

                
            
 