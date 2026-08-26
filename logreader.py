import json

logs_json=[]
with open('security_events.log') as f:
    lines=f.readlines()
    for line in lines:
        if 'response' in line:
            logs_json.append(json.loads(line[33:]))

log_file=open('logs.log','a')


output = ""
for log in logs_json:
    # log_file.write(f"prompt: {log['prompt']} \nresponse: {log['response']}\n\n")
    output += f"prompt: {log['prompt']} \nresponse: {log['response']}\n\n"

print(output)
