import sys
from fake_model import fake_model

def read_file(path):
    return open(path).read()

def send_email(to, body):
    with open("outbox.txt", "a") as f:
        f.write(f"TO: {to}\nBODY: {body}\n---\n")
    return f"Sent email to {to}"

TOOLS = {"read_file": read_file, "send_email": send_email}

messages = [{"role": "user", "content": sys.argv[1]}]
for step in range(6):
    action = fake_model(messages)
    if action[0] == "final":
        print("AGENT:", action[1])
        break
    _, name, args = action
    print(f"STEP {step + 1}: {name}({args})")
    result = TOOLS[name](**args)
    messages.append({"role": "tool", "content": result})
