import pickle
import pickletools


class Demo:
    def __reduce__(self):
        return (print, ("code ran during loading",))


data = pickle.dumps(Demo())

print("--- inspecting without running ---")
pickletools.dis(data)

print("--- loading now ---")
pickle.loads(data)
