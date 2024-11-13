import openai

class GptClient:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        openai.api_key = self.api_key

    def process_prompt(self, json_messages):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in json_messages
            ]
        )
        return response['choices'][0]['message']['content']

    def get_response(self, message, prompt = None):
        messages = []

        if prompt:
            messages.append({"role": "system", "content": prompt})
        messages.append({"role":"user", "content": message})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response['choices'][0]['message']['content']

        
    def check_for_trigger(self, message, trigger_intent):
        prompt = f"Does the following message indicate that the user is interested in '{trigger_intent}'? Answer with 'yes' or 'no'.\n\nMessage: {message}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip().lower() == "yes"  