# Please install OpenAI SDK first: `pip3 install openai`

# from openai import OpenAI
#
# client = OpenAI(api_key="sk-", base_url="https://api.deepseek.com")
#
# from openai import OpenAI
# import json
# client = OpenAI(api_key="sk-", base_url="https://api.deepseek.com")
#
#
# json_file = "ireland_soil_ph_data.json"
# with open(json_file, "r") as f:
#     soil_data = json.load(f)
# # "latitude": 53.908625,
# # "longitude": -6.6364,
# #
# def get_soil_ph(latitude, longitude):
#     """从 JSON 文件查询 pH 值"""
#     for entry in soil_data:
#         if round(entry["latitude"], 3) == round(latitude, 3) and round(entry["longitude"], 3) == round(longitude, 3):
#             return entry["ph_h2o"]
#     return "Data not found"
# Properly structured message sequence
# messages = [
#     {"role": "system", "content": "You are a helpful assistant for dance choreography."},  #  System message
#     {"role": "user", "content": "Could you help me to do dance choreography: contemporary, emotional, Solo?"}  # First user message
# ]
#
# # Request to DeepSeek Reasoner
# response = client.chat.completions.create(
#     model="deepseek-reasoner",
#     messages=messages
# )
#
# # Print the assistant's response
# assistant_response = response.choices[0].message.content
# print(assistant_response)
#
# # Continue the conversation - Append the response and ask another question
# messages.append({"role": "assistant", "content": assistant_response})  # Append generated assistant response
# messages.append({"role": "user", "content": "Can you give me a choreography breakdown for the first 30 seconds?"})
#
# response = client.chat.completions.create(
#     model="deepseek-reasoner",
#     messages=messages
# )
#
# # Print the next response
# print(response.choices[0].message.content)
from openai import OpenAI
import json

# DeepSeek API
client = OpenAI(api_key="sk-58dd597725f34c5ba25a2c9f9f473be4", base_url="https://api.deepseek.com")

# read pH data
json_file = "ireland_soil_ph_data.json"
with open(json_file, "r") as f:
    soil_data = json.load(f)

# get ph function
def get_soil_ph(latitude, longitude):
    """JSON pH """
    for entry in soil_data:
        if round(entry["latitude"], 3) == round(latitude, 3) and round(entry["longitude"], 3) == round(longitude, 3):
            return entry["ph_h2o"]
    return "Data not found"

# Function Calling
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_soil_ph",
            "description": "Retrieve soil pH value based on given latitude and longitude",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number", "description": "Latitude coordinate"},
                    "longitude": {"type": "number", "description": "Longitude coordinate"}
                },
                "required": ["latitude", "longitude"]
            }
        }
    }
]

#
user_query = input("Please input your query: (example: What is the soil pH at latitude 53.908625 and longitude -6.6364?）\n")

#  DeepSeek  get_soil_ph
response = client.chat.completions.create(
    model="deepseek-coder",  # deepseek-reasoner  function calling
    messages=[{"role": "system", "content": "You are a soil expert. If the user asks for soil pH at a specific location, you MUST call the get_soil_ph function."},
              {"role": "user", "content": user_query}],
    tools=tools,
    tool_choice="auto"  # 让 DeepSeek 自动决定是否调用 `get_soil_ph()`
)

# DeepSeek
response_message = response.choices[0].message

# 🔹
if hasattr(response_message, "tool_calls") and response_message.tool_calls:
    for tool_call in response_message.tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)  #

        if function_name == "get_soil_ph":
            #
            latitude = arguments["latitude"]
            longitude = arguments["longitude"]

            #
            ph_value = get_soil_ph(latitude, longitude)
            print(f"The soil pH at latitude {latitude} and longitude {longitude} is {ph_value}")
            #
            analysis_messages = [
                {"role": "system", "content": "You are a soil health analysis assistant."},
                {"role": "user", "content": f"The soil pH at latitude {latitude} and longitude {longitude} is {ph_value}. Can you analyze what this means for agriculture?"}
            ]

            analysis_response = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=analysis_messages
            )

            print("soil pH analysis：")
            print(analysis_response.choices[0].message.content)
else:
    # DeepSeek answer directly
    print("DeepSeek answer directly：")
    print(response_message.content)  #

