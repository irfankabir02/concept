# === Inference Engine Core Logic ===
# Mirrors the P2P combo pattern logic — detects meaningful input sequences (signals) and triggers actions.
# This keeps it simple and modular, suitable for integration with any codebase.

class InferenceEngine:
    def __init__(self):
        self.patterns = {}
        self.buffer = []
        self.max_buffer = 10

    def register_pattern(self, name, sequence, action):
        """Register a named pattern with a callable action."""
        self.patterns[name] = {"sequence": sequence, "action": action}

    def feed(self, signal):
        """Feed new signal (input, event, data point) into the buffer."""
        self.buffer.append(signal)
        if len(self.buffer) > self.max_buffer:
            self.buffer.pop(0)
        self._evaluate()

    def _evaluate(self):
        for name, p in self.patterns.items():
            seq = p["sequence"]
            if self.buffer[-len(seq):] == seq:
                p["action"](name, seq)

# === Example Usage ===
if __name__ == "__main__":
    def on_combo_detected(name, seq):
        print(f"Pattern detected: {name} -> {seq}")

    engine = InferenceEngine()
    engine.register_pattern("focus_combo", ["start", "breathe", "commit"], on_combo_detected)

    # Simulate inputs
    for s in ["idle", "start", "breathe", "commit"]:
        engine.feed(s)
