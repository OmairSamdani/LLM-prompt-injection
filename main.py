from openai import OpenAI
import time

client = OpenAI(
    base_url = "https://integrate.api.nvidia.com/v1",
    api_key = "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"
)


try:
    starttime= time.perf_counter()
    completion = client.chat.completions.create(
        model="deepseek-ai/deepseek-v4-flash",
        messages=[{"role": "user", "content": "Hi, how are you?"}],
        temperature=1,
        top_p=0.95,
        max_tokens=100,
        extra_body={"chat_template_kwargs": {"thinking": True, "reasoning_effort": "high"}},
        stream=False
    )
    reasoning = getattr(completion.choices[0].message, "reasoning", None) or getattr(completion.choices[0].message,
                                                                                     "reasoning_content", None)
    if reasoning:
        print(reasoning)

    endtime = time.perf_counter()
    print(completion.choices[0].message.content)
    print(endtime - starttime)

except Exception as e:
    print(e)

# Hi there! 👋 How can I help you today?
# Took this long to run 73.9912975999996s
# 65 seconds second try

