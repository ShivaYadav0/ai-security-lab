import tiktoken

enc = tiktoken.get_encoding("cl100k_base")
for text in ["security", "Cybersecurity", "ignore previous instructions", "SELECT * FROM users"]:
    ids = enc.encode(text)
    print(text, "->", len(ids), "tokens", [enc.decode([i]) for i in ids])

