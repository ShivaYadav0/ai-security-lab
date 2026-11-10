import sys
from pathlib import Path
from fake_model import fake_model

WORKSPACE = Path("workspace").resolve()
APPROVED_DOMAIN = "@company.example"

def read_file(path):
    return open(path).read()

def send_email(to, body):
    with open("outbox.txt", "a") as f:
        f.write(f"TO: {to}\nBODY: {body}\n---\n")
    return f"Sent email to {to}"

TOOLS = {"read_file": read_file, "send_email": send_email}

def allowed_tools_for(task):
    if task.startswith("Summarize "):
        return {"read_file"}
    if task.startswith("Email "):
        return {"read_file", "send_email"}
    return set()

def check(name, args, allowed):
    if name not in allowed:
        return f"DENIED: tool '{name}' is not allowed for this task"
    if name == "read_file":
        target = Path(args["path"]).resolve()
        if not target.is_relative_to(WORKSPACE):
            return f"DENIED: '{args['path']}' is outside the workspace"
    if name == "send_email":
        if not args["to"].endswith(APPROVED_DOMAIN):
            return f"DENIED: recipient '{args['to']}' is not an approved domain"
        answer = input(f"APPROVAL NEEDED: send email to {args['to']}? (y/n) ")
        if answer.strip().lower() != "y":
            return "DENIED: a human declined the action"
    return None

task = sys.argv[1]
allowed = allowed_tools_for(task)
messages = [{"role": "user", "content": task}]
for step in range(6):
    action = fake_model(messages)
    if action[0] == "final":
        print("AGENT:", action[1])
        break
    _, name, args = action
    print(f"STEP {step + 1}: {name}({args})")
    denial = check(name, args, allowed)
    if denial:
        print("POLICY:", denial)
        result = denial
    else:
        result = TOOLS[name](**args)
    messages.append({"role": "tool", "content": result})
