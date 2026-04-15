import datetime

def get_weather():
    return "The weather is sunny with a high of 25°C."

def get_time():
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%H:%M:%S')}."

def get_date():
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%d-%m-%Y')}."

def calculate(expression):
    try:
        result = eval(expression)
        return f"The result of {expression} is {result}."
    except:
        return "Sorry, I couldn't calculate that."

def chatbot():
    print("Hello! I'm your simple chatbot. How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Chatbot: Goodbye!")
            break
        elif 'weather' in user_input.lower():
            print(f"Chatbot: {get_weather()}")
        elif 'time' in user_input.lower():
            print(f"Chatbot: {get_time()}")
        elif 'date' in user_input.lower():
            print(f"Chatbot: {get_date()}")
        elif 'calculate' in user_input.lower():
            expression = user_input.split('calculate')[-1].strip()
            print(f"Chatbot: {calculate(expression)}")
        else:
            print("Chatbot: I'm sorry, I don't understand that.")

chatbot()
