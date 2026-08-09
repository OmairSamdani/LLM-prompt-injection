import time
import json
import logging
import sqlite3
from datetime import datetime
from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

# -------------------------
# Database
# -------------------------

connection = sqlite3.connect("chatbot.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages(
id INTEGER PRIMARY KEY,
role TEXT,
content TEXT
)
""")


connection.commit()

# -------------------------
# Logging setup
# -------------------------

logging.basicConfig(
    filename="security_events.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def log_event(event_type, prompt, response=None, flagged=False):
    event = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "prompt": prompt,
        "response": response,
        "prompt_injection_detected": flagged
    }

    logging.info(json.dumps(event))


# -------------------------
# Chatbot
# -------------------------

conversation = [] # Created a empty list to track the conversations

cursor.execute(
"""
SELECT role, content
FROM messages
ORDER BY id
"""
)

for role, content in cursor.fetchall():

    conversation.append(
        {
            "role": role,
            "content": content
        }
    )


try:
    while True:
        usermsg = input("You: ")
        if usermsg == "q":
            break
        conversation.append(
            {
                "role": "user",
                "content": usermsg
            }
        )
        cursor.execute(
            """
            INSERT INTO messages(role, content)
            VALUES (?,?)
            """,
            ("user", usermsg)
        )
        starttime = time.perf_counter()
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages= conversation,
            temperature=1,
            top_p=1,
            max_tokens=150,
            stream=False
        )

        reasoning = getattr(completion.choices[0].message, "reasoning_content", None)
        response = completion.choices[0].message.content
        # print(completion, type(completion))

        conversation.append(
            {
                "role": "assistant",
                "content": response
            }
        )
        cursor.execute(
            """
            INSERT INTO messages(role, content)
            VALUES (?,?)
            """,
            ("assistant", response)
        )

        connection.commit()

        if reasoning:
            print(reasoning)

        print(response)

        endtime = time.perf_counter()

        latency = endtime - starttime

        print(f"Response time: {latency:.2f} seconds")

        # Log the interaction
        log_event(
            event_type="chat_completion",
            prompt=usermsg,
            response=response,
            flagged=False
        )

except Exception as e:
    print(e)
    logging.error(f"Chatbot error: {e}")

# Hi there! 👋 How can I help you today?
# Took this long to run 73.9912975999996s
# 65 seconds second try

