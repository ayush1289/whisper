from openai import OpenAI

class ChatAssistant:
    def __init__(self,api_key):
        self.client = OpenAI(api_key=api_key)
      
    def translate(self,text,target_language):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={ "type": "text" },
            messages=[
                {"role": "system", "content": f"You are a helpful assistant designed to translate the text given by user in {target_language}"},
                {"role": "user", "content": f"{text}"}
            ]   
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    api_key="your api key"
    openai = ChatAssistant(api_key=api_key)
    openai.translate("My name is ayush and I am from India. I want to learn about the culture of India. Can you help me with that?"," Korean")