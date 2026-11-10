import sys
from rag_lib import get_collection, embed, build_prompt

question = sys.argv[1]
col = get_collection()
res = col.query(query_embeddings=embed([question]), n_results=2)
chunks = res["documents"][0]

print("Retrieved chunks:")
for c in chunks:
    print(" *", c)
print("\n--- Prompt that would be sent to the model ---")
print(build_prompt(question, chunks))
