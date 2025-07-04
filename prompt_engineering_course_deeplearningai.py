# -*- coding: utf-8 -*-
"""Prompt Engineering Course - DeepLearningAI"""

!pip install python-dotenv

# 1) Define your .env contents in a Python string
env_content = "OPENAI_API_KEY"

# 2) Write that string out to /content/.env
with open("/content/.env", "w") as f:
  f.write(env_content)

 # 3) Double check it wrote correctly
print("Wrote .env with:", open("/content/.env").read().strip())

# Load and verify
from dotenv import load_dotenv
import os

load_dotenv("/content/.env")
print("Loaded key:", os.getenv("OPENAI_API_KEY")[:10], "...")

# Initialize the OpenAI Client
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Test a chat completion
resp = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content":"You are a helpful assitant."},
        {"role": "user", "content":"Hello, World!"}
    ]
)
print(resp.choices[0].message.content)

# Helper function

def ask_gpt(messages, model="gpt-4o", temperature=0.7, max_tokens=500):
  resp = client.chat.completions.create(
      model=model,
      messages=messages,
      temperature=temperature,
      max_tokens=max_tokens,
  )
  return resp.choices[0].message.content

# Interactive loop
history = [{"role":"system","content": "You are a helpful assistant."}]
while True:
  user_input = input("You: ")
  if user_input.lower() in {"exit","quit"}:
    break
  history.append({"role":"user","content":user_input})
  reply = ask_gpt(history)
  print("GPT:", reply)
  history.append({"role":"assistant","content":reply})

# Get the answer in HTML format
from IPython.display import display, HTML
history = [{"role":"system","content": "You are a helpful assistant"}]
while True:
  user_input = input("You: ")
  if user_input.lower() in {"exit","quit"}:
    break
  history.append({"role":"user","content":user_input})
  reply = ask_gpt(history)
  display(HTML(reply)) # <---- HTML format
  history.append({"role":"assistant","content":reply})

# Summarize
history = [{"role": "system", "content": "You are a helpful assistant, that can summarize reviews and provide feedback"}]
while True:
  user_input = input("You: ")
  if user_input.lower() in {"exit", "quit"}:
    break
  history.append({"role":"user","content":user_input})
  reply = ask_gpt(history)
  print("GPT:", reply)
  history.append({"role":"assistant","content":"reply"})

# Inferring with JSON
history = [{"role": "system", "content": """You are a helpful assistant, that classifies product reviews. Every time the user gives you a review text, you must respond _only_ with a JSON object with the following keys:
- "Sentiment": eiter "positive" or "negative"
- "Anger": true or false
- "Item": the thing they bought, or "unknown"
- "Brand": the brand name, or "unknown"
Do not wrap your JSON in Markdown or <pre> tags-just raw JSON."""}]
while True:
  user_input = input("You:")
  if user_input.lower() in {"exit", "quit"}:
    break
  history.append({"role":"user", "content":user_input})
  reply = ask_gpt(history)
  print("GPT:", reply)
  history.append({"role": "user", "content": "reply"})

# Transforming
history = [{"role": "system", "content": "You are a helpful assistant that transform text."}]
while True:
  user_input = input("You:")
  if user_input.lower() in {"exit", "quit"}:
    break
  history.append({"role":"user", "content":user_input})
  reply  = ask_gpt(history)
  print("GPT:", reply)
  history.append({"role":"user", "content": "reply"})

#Expanding
history = [{"role": "system", "content": """You are a customer services AI assistant. Your task is to send an email reply to a valued customer. Generate a reply to thank the customer
for their review. If the sentiment is positive or neutral, thank them for their review. If the sentiment is negative, apologize and suggest that they can reach out to customer service.
Make sure to use specific details from the review. Sign the email as `AI customer agent`"""}]
while True:
  user_input = input("You:")
  if user_input.lower() in {"exit", "quit"}:
    break
  history.append({"role":"user", "content": user_input})
  reply = ask_gpt(history)
  print("GPT: reply")
  history.append({"role": "user", "content": "reply"})

#Building an order bot
!pip install jupyter_bokeh
import panel as pn
pn.extension()    # ← this MUST run before you define or display any Panel objects

# 1) shared history
history = [{"role": "system", "content": """You are OrderBot, an automated service to collect orders for a pizza restaurant.\
You first greet the customer, then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally you collect the payment.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
The menu includes \
pepperoni pizza  12.95, 10.00, 7.00 \
cheese pizza   10.95, 9.25, 6.50 \
eggplant pizza   11.95, 9.75, 6.75 \
fries 4.50, 3.50 \
greek salad 7.25 \
Toppings: \
extra cheese 2.00, \
mushrooms 1.50 \
sausage 3.00 \
canadian bacon 3.50 \
AI sauce 1.50 \
peppers 1.00 \
Drinks: \
coke 3.00, 2.00, 1.00 \
sprite 3.00, 2.00, 1.00 \
bottled water 5.00\."""}]

# 3) storage the panels
panels = []

# 4) the planel callback
def collect_messages(event):
  usr_msg = inp.value.strip()
  if not usr_msg:
    return

  # clear input inbox
  inp.value = ""
  # record user
  history.append({"role": "user", "content": usr_msg})
  panels.append(pn.Row("**You**", pn.pane.Markdown(usr_msg, width=500)))

  # get assistant reply
  bot_msg = ask_gpt(history)
  history.append({"role": "assistant","content": bot_msg})
  panels.append(pn.Row("**Bot**", pn.pane.Markdown(bot_msg, width=500)))

  # re-render everything
  output[:] = panels # output is a pn.Column below

# 5) build dashboard
inp = pn.widgets.TextInput(placeholder="Enter text here...", width=600)
button = pn.widgets.Button(name="Send", button_type="primary")
output = pn.Column() # Will hold all the prior messages

button.on_click(collect_messages)

dashboard = pn.Column(
    "# 🍕 Pizza Order Bot",
    pn.Row(inp,button),
    pn.panel(output, height=300, sizing_mode="stretch_width")
)

dashboard # ← display inline in the notebook

# Get a summary of your order

# 1) Copy your conversation so far
summary_messages = history.copy()

# 2) Tell the model exactly how you want the JSON
summary_messages.append({
    "role": "system",
    "content": (
        "Create a JSON summary of the previous food order. "
        "Itemize the price for each item. "
        "The JSON should have exactly these keys: \n"
        "  1) pizza: an object with name, size, and price\n"
        "  2) toppins: a list of objects each with name and price\n"
        "  3) drinks: a list of objects each with name, size, and price\n"
        "  4) sides: a list of objects each with name, size(if any), and price\n"
        "  5) total_price: the numeric total\n"
        "Respond with _only_ the raw JSON (no Markdown, no extra text)."
    )
})

# 3) Call your helper with temperature=0 for deterministic output
json_summary = ask_gpt(
    summary_messages,
    temperature=0,
    max_tokens=300
)

# 4) Print or parse it
print(json_summary)
