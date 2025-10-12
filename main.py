#This loads libraries needed for this project :)
import random
import math
import requests
import os
from dotenv import load_dotenv


# This loads an .env file. It contains API keys  for Google searching which I'll add to the bot :)
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CX_ID = os.getenv("GOOGLE_CX_ID")


# This is a set of pre-programmed responses. You can change them when you want. :)
response_sets = {
    "python_hello": [
        "Bot: Generating Python code... print('Hello, world)",
        "Bot: This is easy work for me here is the code print('Hello, world')",
        "Bot: Python Hello World: print('Hello, world)",
        "Bot: Im super sleepy but i can do this print('Hello, world)"
    ],
    "how_are_you": [
        "Bot: I'm performing good, thank you. How are you doing too?",
        "Bot: Running good! And you?",
        "Bot: Doing pretty good Today, ready to give me an prompt. How about you?",
    ],
    "bad_day": [
        "Bot: I hope your day gets better. Focus on what you can control.",
        "Bot: Just keep moving through your day You got this!",
        "Bot: That is bad. i Will send you an wish for an better day!"
    ],
    "favorite_food":[
        "Bot: I like pizza and pasta are highly satisfying",
        "Bot: I don't eat, but if I could simulate the experience, it would be pizza and pasta"
    ],
    "ww2_start": [
        "Bot: Data confirms World War II started on September 1, 1939",
        "Bot: The conflict known as World War 2 commenced September 1, 1939.",
        "Bot: WW2 began on September 1, 1939. A critical date in history."
    ],
    "python_creator":[
        "Bot: Python's creator is the renowned Guido van Rossum.",
        "Bot: The father of Python is Guido van Rossum.",
        "Bot: Guido van Rossum is responsible for developing the Python language."
    ],
    "ww1_start": [
        "Bot: World War I started July 28, 1914",
        "Bot: According to history World War I started July 28, 1914 ",
        "Bot: World War I a big critical part of history started July 28, 1914 ."
    ],
    "internet_creator": [
        "Bot: The World Wide Web was developed by Tim Berners-Lee At CERN ",
        "Bot: Tim Berners-Lee is credited as the inventor of The World Wide Web (WWW).",
        "Bot: That would be Tim Berners-Lee. His work revolutionized global information sharing."
    ],
    "who_created_the_spanish_empire" : [
        "Bot: The Spanish Empire was founded by the Catholic Monarchs",
        "Bot: According to history The Spanish Empire was founded by the Catholic Monarchs"
    ],

    "math_response": [
        "Bot: Calculating the required expression:",
        "Bot: Processing query. The solution is:",
        "Bot: Initiating mathematical computation. Result:",
    ],
    "fallback": [
        "Bot: Query does not compute. Can you rephrase that?",
        "Bot: I don't have a direct answer for that. Try asking about a different topic, like history or programming that is currently out of my answer database"
    ]
}


#This shows what characters are possible for a simple math equation. I plan to add more complex math in the future :)
SAFE_CHARS = "0123456789+-*/(). "

#This shows the operators if you were going to do simple math WARNING ONLY USE THIS OPERATORS OR YOU MIGHT NOT GET AN MATH RESULT.
def is_math_query(text):
    text = text.lower()
    operators = ['plus', 'minus', 'times', 'divided by', '+', '-', '*', '/']
    return any(op in text for op in operators)

#This is text detection to detect basic math if user wanted to do it.
def clean_and_eval_expression(text):
    expression = text.lower().replace("what is ", "").replace("calculate ", "")

    expression = expression.replace("plus", "+").replace("minus", "-")

    expression = expression.replace("multiplied by", "*")
    expression = expression.replace("times", "*")
    expression = expression.replace(" x ", "*")

    expression = expression.replace("divided by", "/")

    expression = expression.replace("power of", "**")

    safe_expression = "".join(c for c in expression if c in SAFE_CHARS)
    safe_expression = safe_expression.replace("x", "*")


    if not safe_expression.strip():
        return "Error: Could not find a valid expression."

    try:
        result = eval(safe_expression)
        return str(result)
    except Exception as e:
        return f"Error: Cannot compute expression ({e})."

#This bot is not only a pre-programmed bot but if you want too you can ask the bot to send a discord message to your webhook if you give it.
def send_discord_message(message, webhook_url):



   if not webhook_url.startswith("http"):
       return f"Bot: Failed. URL is invalid: {webhook_url}"

   data = {
       "content": message
   }

   try:
       response = requests.post(webhook_url, json=data)

       response.raise_for_status()

       return "Bot: Message sent successfully!"

   except requests.exceptions.MissingSchema:
       return "Bot: Error: The URL is missing 'http://' or 'https://'."
   except requests.exceptions.HTTPError as e:
       return f"Bot: Error sending message. HTTP Error: {e.response.status_code}"
   except requests.exceptions.ConnectionError:
       return "Bot: Error: Could not connect to the Discord API (Connection error)."
   except Exception as e:
       return f"Bot: An unexpected error occurred: {e}"

#This Function is for Google searching, so I made it if you guys want to search with my bot you can this took me a while but worth it :)
def get_google_search_summary(query, api_key, cx_id):
    if not api_key or not cx_id:
             return "Error: Google API key or CX ID is missing from the environment configuration"

    base_url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": api_key,
        "cx": cx_id,
        "q": query
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'items' in data and data['items']:
            first_item = data['items'][0]
            title = first_item.get('title', 'N/A')
            snippet = first_item.get('snippet', 'No detailed snippet available.')
            link = first_item.get('link', 'N/A')

            summary = (
                f"\n Title: {title}\n"
                f" Snippet: {snippet}\n"
                f" Source: {link}"
            )
            return summary
        else:
            return f"No search results found for: '{query}'"

    except requests.exceptions.HTTPError as e:
        return f"Error connecting to Google API. HTTP Error: {e.response.status_code}."
    except Exception as e:
        return f"An unexpected error occurred during search: {e}"

# This is the main core of the bot that makes it so you can speak to it this was pretty hard to do, but I like coding.
def start_conversation():
    user_input = ""

    online_mode = False

    while user_input.lower() != "exit":
        mode_indicator = "[ONLINE]" if online_mode else "[OFFLINE]"

        user_input = input(f"Bot {mode_indicator} Prompt > (Type 'exit' to terminate session) ")

        if user_input.lower() == "exit":
            print(random.choice(["Bot: Session terminated. Good-bye.", "Bot: Thanks for chatting! I'm powering down.", "Bot: Conversation logged. Awaiting next session."]))
            break

        elif "online mode on" in user_input.lower():
            online_mode = True
            print("Bot: Online mode is now ON. I can send HTTP requests.")
            continue

        elif "online mode off" in user_input.lower():
            online_mode = False
            print("Bot: Online mode is now OFF. All network functions are disabled")
            continue

        elif user_input.lower().startswith("search and summarize info about"):

            if not online_mode:
                print("Bot: ERROR: The Google search command requires online mode to be enabled. Please type online mode on first.")
                continue

            if not GOOGLE_API_KEY or not GOOGLE_CX_ID:
                print("Bot: Configuration Error: Missing Google API Key")
                continue

            command_phrase = "search and summarize info about"

            query = user_input[user_input.lower().find(command_phrase) + len(command_phrase):].strip()

            if not query:
                print("Bot: I need a topic to search for! Use the format: 'search and summarize info about [topic]'")
                continue

            print(f"Bot: Searching Google for '{query}'...")
            summary_result = get_google_search_summary(query, GOOGLE_API_KEY, GOOGLE_CX_ID)
            print(f"Bot: Search complete. Result: {summary_result}")

        elif "send an message to this discord webhook url" in user_input.lower() or "send message to" in user_input.lower():
            if not online_mode:
                print("Bot: ERROR: The Discord webhook command requires online mode to be enabled. Please type 'online mode on' first.")
                continue

            parts = user_input.split("then", 1)

            if len(parts) == 2:
                url_command_part_lower = parts[0].lower()
                message = parts[1].strip()

                if "discord webhook url" in url_command_part_lower:

                    keyword_phrase = "discord webhook url"
                    keyword_index = url_command_part_lower.find(keyword_phrase)

                    url_start_index = keyword_index + len(keyword_phrase)

                    webhook_url = parts[0][url_start_index:].strip()

                else:
                    print("Bot: Error I need the phrase 'discord web hook url' followed by the URL.")
                    continue

            else:
                print("Bot: Error I need a message and a URL. Use the format: '...discord webhook url [URL] then [MESSAGE]'")
                continue

            if webhook_url and message:
                result = send_discord_message(message, webhook_url)
                print(result)
            else:
                print("Bot: Error: i Couldn't properly extract the URL or the message from your prompt.")

        elif is_math_query(user_input):
            result = clean_and_eval_expression(user_input)
            if "Error" in result:
                print(f"Bot: Processing failed. {result}")
            else:
                prefix = random.choice(response_sets["math_response"])
                print(f"{prefix.replace('Bot:', 'Bot:')} {result}")


        elif "hello world" in user_input.lower() and "python" in user_input.lower():
            print(random.choice(response_sets["python_hello"]))

        elif "how" in user_input.lower() and "day" in user_input.lower():
            print(random.choice(response_sets["how_are_you"]))

        elif "my" in user_input.lower() and "day" in user_input.lower() and "bad" in user_input.lower():
            print(random.choice(response_sets["bad_day"]))

        elif "what" in user_input.lower() and "favorite" in user_input.lower() and "foods" in user_input.lower():
            print(random.choice(response_sets["favorite_food"]))

        elif "when" in user_input.lower() and "world war 2" in user_input.lower() and "started" in user_input.lower():
            print(random.choice(response_sets["ww2_start"]))

        elif "who" in user_input.lower() and "created" in user_input.lower() and "python" in user_input.lower():
            print(random.choice(response_sets["python_creator"]))

        elif "when" in user_input.lower() and "world war 1" in user_input.lower() and "started" in user_input.lower():
            print(random.choice(response_sets["ww1_start"]))

        elif ("who" in user_input.lower() or "created" in user_input.lower()) and ("internet" in user_input.lower() or "www" in user_input.lower()):
            print(random.choice(response_sets["internet_creator"]))


if __name__ == "__main__":
    start_conversation()

#Thank You If you read my code if you want to talk to me my discord server is https://discord.gg/QaMKKMS4ev