from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain.agents import create_openai_tools_agent, AgentExecutor
from api_tools import get_weather, get_crypto_price
import os
from db_utils import init_db, save_message, load_last_messages 


init_db()


class SimpleAgentWithDB:

    def __init__(self, model_name: str = "llama-3.1-8b-instant", temperature: float = 0.7):
        self.llm = ChatGroq(
            model=model_name,
            temperature=temperature,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

        self.tools = [get_weather, get_crypto_price]

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant that can answer questions and use tools when needed.

You have access to the following tools:
- get_weather: Use this when the user asks about weather conditions in a specific city
- get_crypto_price: Use this when the user asks about cryptocurrency prices

For simple questions that don't require tools, answer directly without using any tools.

When the user asks about weather or cryptocurrency prices, you MUST use the appropriate tool.
"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        self.agent = create_openai_tools_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )

        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )

    def query(self, user_query: str, conversation_id: str, N: int = 10) -> str:
        """
        Save the user query, load last N messages, invoke agent, then save assistant response.
        """

        save_message(conversation_id, "user", user_query)


        chat_history = load_last_messages(conversation_id, N)

        try:
            result = self.agent_executor.invoke({
                "input": user_query,
                "chat_history": chat_history
            })
            response = result.get("output", "Sorry, I couldn't process your query.")

            save_message(conversation_id, "assistant", response)
            return response

        except Exception as e:
            return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("GROQ_API_KEY missing in .env!")
        exit(1)

    agent = SimpleAgentWithDB()
    conversation_id = "user123" 
    N = 10  
    print("Chat with the agent! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Ending chat.")
            break

        response = agent.query(user_input, conversation_id, N=N)
        print(f"Assistant: {response}\n")
