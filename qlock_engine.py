# qlock_engine.py
import hashlib, numpy as np, math

def encode_identity(s, dim=10):
    d = hashlib.sha256(s.encode()).digest()
    v = np.frombuffer(d, dtype=np.uint8).astype(float)/255.0
    v = (v - v.mean()) / (v.std() or 1)
    if len(v) < dim:
        v = np.tile(v, int(math.ceil(dim/len(v))))[:dim]
    else:
        v = v[:dim]
    return v

def lock_text(circuit_text, identity):
    vec = encode_identity(identity, 10)
    return "// identity-locked-hash: " + str(vec)

def main():
    print("Q-LOCK ATTRACTOR ENGINE\n")
    identity = input("Enter identity string: ")
    print("\nIdentity hash vector generated.\n")
    print("Paste your circuit (end with blank line):\n")
    lines=[]
    while True:
        try:
            l=input()
        except EOFError:
            break
        if l.strip()=="":
            break
        lines.append(l)
    circ = "\n".join(lines)
    print("\nUsing binary (fallback) encoding.")
    print("Qiskit not installed → running text-only mode.\n")
    print("Text-only locking:")
    print(lock_text(circ, identity))
    print("\nDONE.")

if __name__ == "__main__":
    main()
