import numpy as np

def compute_satiety(frequency=1.0, duration=5.0, steps=10, start_tight=0.1, dip_pos=0.77, end_safe=True):
    """
    Simplified satiety: balanced path with start compression, mid dip, end balance.
    """
    t = np.linspace(0, duration, steps)
    path = np.sin(2 * np.pi * frequency * t)

    # Start tight (compress first 10%)
    early = int(steps * 0.1)
    path[:early] *= (1 + start_tight)

    # Dip at ~77%
    dip_idx = int(steps * dip_pos)
    if dip_idx < steps:
        path[dip_idx] -= 0.3

    # Keep balanced range
    path = np.clip(path, -1.5, 1.5)

    # Safe end
    if end_safe:
        path[-1] = 0.0

    return list(zip(t, path))

# Run simple test
satiety = compute_satiety(frequency=0.5, duration=4.0, steps=8, start_tight=0.2, dip_pos=0.77, end_safe=True)
print("Satiety path:")
for time, val in satiety:
    print(".2f")
