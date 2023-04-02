from decouple import config
import openai
import datetime

# # Set up OpenAI API key
# openai.api_key = config('OPENAI_API_KEY')
#
# response = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Who won the world series in 2020?"}
#     ]
# )
#
# r = response.choices[0]['message']['content'].strip()
# # https://platform.openai.com/docs/guides/chat/introduction
#
# print(r)

WHITELISTED_USERS = list(int(user_id) for user_id in config('WHITELISTED_USERS', default='', cast=str).split(','))
print(WHITELISTED_USERS)

print(datetime.datetime.utcnow().isoformat())
