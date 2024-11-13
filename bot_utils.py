import streamlit as st
import pandas as pd

def get_info():        
        with st.sidebar:
            st.title("system condition")
            st.write("all paramets collected: ", st.session_state.all_paramets_collected)
            st.write("selecting_parameters_starting: ", st.session_state.selecting_parameters_starting)

class Session:
    def __init__(self):
        self.initialize_session()
        self.make_start_buttoms()
        self.session_indicators()

    def clear_screen(self):
        """Clear all session state keys."""
        for key in st.session_state.keys():
            del st.session_state[key]

    def initialize_session(self):
        """Initialize session variables if they don't already exist."""
        st.session_state.setdefault("strategy", [])
        st.session_state.setdefault("cart", [])
        st.session_state.setdefault("dialogue_stage", "stay")

    def session_indicators(self):
        st.session_state.setdefault("all_paramets_collected", False)
        st.session_state.setdefault("selecting_parameters_starting", False)
        
    def make_start_buttoms(self):
        left, middle, right = st.columns(3)
        if left.button("left", use_container_width=True):
            left.markdown("left pressed")
        if right.button("right", use_container_width=True):
            right.markdown("right pressed")
        if middle.button("start", use_container_width=True):
            st.session_state["dialogue_stage"] = "start"

    def make_cart_buttoms(self):
        left, right = st.columns(2)
        if left.button("add to cart", use_container_width=True):
            pass
        if right.button("don't add", use_container_width=True):
            pass

class MessageHandler:
    def __init__(self):
        if  "messages" not in st.session_state:
            st.session_state.messages = []
            self.add_inicial_message()
    
    def clear_history(self):
        if "messages" in st.session_state:
            st.session_state.messages = []

    def add_message(self, role, content):
        """Добавить сообщение в список сообщений."""
        st.session_state.messages.append({"role": role, "content": content})

    def get_history(self):
        return st.session_state.messages

    def get_last_n_history(self, n):
        return st.session_state.messages[-n:]
    
    def print_like(self, icon, message):
        with st.chat_message(icon):
            st.markdown(message)

    def print_this(self, message):
        st.write(message)  

    def print_inicial_message(self):
        initial_message = "Hello! I am glad you reached out to us. I am your financial consultant, and I will help you find a product that best aligns with your goals and expectations. Lets get started!"
        
        self.print_like("ai", initial_message)

    def add_inicial_message(self):
        initial_message = "Hello! I am glad you reached out to us. I am your financial consultant, and I will help you find a product that best aligns with your goals and expectations. Lets get started!"
        
        self.add_message("assistant", initial_message)
# MESSAGE HEADLER $$$$$$$$$$$$$$$$$$$$$$
    def generate_response_message(self, user_message, gpt_client, prompt):
        response_content = gpt_client.get_response(message=user_message, prompt=prompt)
        return response_content

    def display_chat_history(self):
        if 'messages' in st.session_state:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
    def print_last_user_message(self):
        if st.session_state.messages:
            for message in reversed(st.session_state.messages):
                if message["role"] == "user":
                    last_message = message["content"]
                    with st.chat_message("user"):
                        st.markdown(last_message)
                    break

    def print_last_assistant_message(self):
        if st.session_state.messages:
            for message in reversed(st.session_state.messages):
                if message["role"] == "assistant":
                    last_message = message["content"]
                    with st.chat_message("assistant"):
                        st.markdown(last_message)
                    break
    def add_and_print(self, role, content):
        self.add_message(role, content)
        if role == "user":
            self.print_last_user_message()
        elif role == "assistant":
            self.print_last_assistant_message()


class InvStrategy:
    def __init__(self) -> None:
        self.underlying_assert = None
        self.derivative = "autocall"
        self.investment_size = None
        self.fx_risk = None
        self.expected_return = None
        self.horisont = None
        self.capital_risk = None
        self.payout = None

    def is_all_not_none(self):
        return all(value is not None for value in vars(self).values())

    def get_none(self):
        return [key for key, value in vars(self).items() if value is None]
    
    def get_not_none(self):
        return [key for key, value in vars(self).items() if value is not None]

    def get_all_pairs(self):
        return [f"{key} : {value}" for key, value in vars(self).items() if value is not None]

    def update_by_json(self, json):
        for key, value in json.items():
            if hasattr(self, key):
                curr_val = getattr(self, key)
                if (curr_val is None or curr_val == 'Not matter') and value is not None:
                    setattr(self, key, value)


    def strategy_table(self):
        parameters = {
        "Parameter": 
            list(vars(self).keys()), 
        "Value": 
            list(vars(self).values())
        }
        parameters_df = pd.DataFrame(parameters)

        with st.sidebar:
            st.title("Your plan")
            st.dataframe(parameters_df, use_container_width=True) 

    


