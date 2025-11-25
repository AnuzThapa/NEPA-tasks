*Groq Chat Agent with Persistent Conversation

This project implements a Groq-powered conversational agent that can answer general questions and use external tools for weather and cryptocurrency price queries. All conversation history is stored in a SQLite database, allowing follow-up questions to work across restarts.

Features

1.General question answering via Groq LLM.
2.Weather queries using OpenWeatherMap API.
3.Cryptocurrency price queries using CoinMarketCap API key.
4.Persistent conversation history in SQLite.
5.Supports multiple conversations using conversation_id.


*Below are the Prerequisites

Python 3.10+

pip install -r requirements.txt

Example requirements.txt:
python-dotenv
requests
langchain-groq
sqlite3

2. Configure External APIs

Create a .env file in the root directory with your API keys:

# Groq API key
GROQ_API_KEY="your_groq_api_key_here"

# OpenWeatherMap API key
OPENWEATHER_API_KEY="your_openweathermap_api_key_here"

# CoinMarketCap API Key
CMC_API_KEY="your_cmc_api_key_here"


Install python-dotenv (already in requirements) so keys are automatically loaded.

3. Initialize the SQLite Database

The project uses a database to store conversation history.

The database is automatically created by running below line of code:

from db_utils import init_db
init_db()

This will create chat_history.db with a table messages containing:
id (primary key)
conversation_id
role (user/assistant)
content
timestamp

4. Run a Sample Chat Session

You can interact with the agent using a Python loop:

from agent_with_db import SimpleAgentWithDB

agent = SimpleAgentWithDB()
conversation_id = "user123"  # Can be a user ID or session ID

print("Start chatting with the agent (type 'exit' to quit)...")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    response = agent.query(user_input, conversation_id)
    print(f"Assistant: {response}\n")


Features of this chat session:
1.Conversation is persistent across restarts.
2.Last N messages are loaded automatically to provide context.
3.Weather and crypto queries will call the respective APIs.

Below is the architecture on how the system actually works.

ARCHITECTURE.md (Optional)
Groq Chat Agent - Architecture
       +-----------------+
       |  User Input     |
       +--------+--------+
                |
                v
       +--------+--------+
       |  Save message   |
       |  (SQLite DB)    |
       +--------+--------+
                |
                v
       +--------+--------+
       | Load last N msgs|
       | from DB          |
       +--------+--------+
                |
                v
       +--------+--------+
       |  Groq Agent     |
       |  + Tools        |
       +--------+--------+
        |             |
        v             v
   get_weather()    get_crypto_price()
        |             |
        v             v
   Weather API      CoinGecko API
   (OpenWeather)    
        \             /
         \           /
          \         /
           +-------+
           | Response
           | (Assistant)
           +-------+
                |
                v
       +--------+--------+
       | Save response    |
       | to DB            |
       +-----------------+


Flow Summary:

1.User sends a query.
2.Query is saved to SQLite DB.
3.Last N messages for the conversation are loaded.
4.Agent decides whether to answer directly or use tools.
5.Tools call external APIs as needed.
6.Agent response is saved to database.
7.Agent response returned to the user.
8.In successive query,the previous conversation gets persisted in db.
