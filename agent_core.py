# from google import genai
# from google.genai import types
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.agents import create_agent
# from langchain_community.utilities import SerpAPIWrapper
# from langchain_community.tools import Tool
# import os
# from secret_key import gemini_api_key, serpapi_key

# # Set API Keys
# os.environ["GOOGLE_API_KEY"] = gemini_api_key
# os.environ["SERPAPI_API_KEY"] = serpapi_key

# # Gemini LLM
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     temperature=0
# )

# # 🔍 SerpAPI Search Tool
# search = SerpAPIWrapper()

# serp_tool = Tool(
#     name="search",
#     description="Search Google for real-time information.",
#     func=search.run,
# )

# # 🧮 Calculator Tool
# def calculator(expression: str):
#     return str(eval(expression))

# math_tool = Tool(
#     name="calculator",
#     description="Useful for performing math calculations.",
#     func=calculator,
# )

# # 🤖 Create Agent
# # agent = create_agent(
# #     model=llm,
# #     tools=[serp_tool, math_tool],
# # )
# agent = create_agent(
#     model=llm,
#     tools=[serp_tool, math_tool],
#     system_prompt="""
# You are an intelligent assistant.
# For factual real-world information like birth dates, always use the google_search tool.
# For mathematical calculations, always use the calculator tool.
# Do not rely only on internal knowledge.
# """
# )

# # 🔥 Run Query
# response = agent.invoke(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "What is 12 × 7?"
#             }
#         ]
#     }
# )

# # Final Answer
# print(response["messages"][-1].content)

# # Show Full Agent Process
# for msg in response["messages"]:
#     print("\nROLE:", msg.type)

#     if hasattr(msg, "tool_calls") and msg.tool_calls:
#         print("TOOL CALLED:", msg.tool_calls)

#     if hasattr(msg, "content"):
        # print("CONTENT:", msg.content)


# SAME CODE FOR USING IT IN STREAMLIT APP
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.tools import Tool

import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

if GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

if SERPAPI_API_KEY:
    os.environ["SERPAPI_API_KEY"] = SERPAPI_API_KEY

# LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    # model="gemini-2.0-flash",
    temperature=0
)

# Search Tool
search = SerpAPIWrapper()

serp_tool = Tool(
    name="search",
    description="Search Google for real-time information.",
    func=search.run,
)

# Calculator Tool
def calculator(expression: str):
    return str(eval(expression))

math_tool = Tool(
    name="calculator",
    description="Useful for performing math calculations.",
    func=calculator,
)

# Create Agent
agent = create_agent(
    model=llm,
    tools=[serp_tool, math_tool],
    system_prompt="""
You are an intelligent conversational AI assistant.

You remember recent conversation history.

Rules:
- Use previous messages to understand pronouns like he, she, his, her, it.
- If the question is unclear, ask the user for clarification.
- Do not return empty answers.
- Use google_search tool for real-world facts.
- Use calculator tool for math.
- Be helpful and conversational.
"""
)

# Function to call agent
# def ask_agent(user_query):
#     response = agent.invoke(
#         {
#             "messages": [
#                 {"role": "user", "content": user_query}
#             ]
#         }
#     )
#     return response["messages"][-1].content

# for new memory
def ask_agent(user_query, chat_history):

    # Add user message
    chat_history.append({
        "role": "user",
        "content": user_query
    })

    # ✅ Keep only last 5 messages
    chat_history = chat_history[-5:]

    response = agent.invoke(
        {
            "messages": chat_history
        }
    )

    final_msg = response["messages"][-1].content

    if isinstance(final_msg, list):
        final_msg = final_msg[0]["text"]

    # Add AI response
    chat_history.append({
        "role": "assistant",
        "content": final_msg
    })

    # ✅ Again keep only last 5
    chat_history = chat_history[-5:]

    return final_msg, chat_history