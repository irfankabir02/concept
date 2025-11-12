import numpy as np

def compute_trajectory(frequency=1.0, duration=5.0, steps=10, tightness_start=0.1, notch_position=0.77, safe_balancer=True):
    """
    Compute a trajectory with controlled tightness, balance, and a notch.
    """
    times = np.linspace(0, duration, steps)
    
    # Base sine wave
    values = np.sin(2 * np.pi * frequency * times)
    
    # Add tightness around entrance (first 10%)
    start_idx = int(steps * 0.1)
    tightness_factor = 1 + tightness_start * np.exp(-times[:start_idx] / 0.5)
    values[:start_idx] *= tightness_factor
    
    # Add slight notch at ~77% position
    notch_idx = int(steps * notch_position)
    if notch_idx < steps:
        notch_depth = 0.3  # Manageable dip
        values[notch_idx] -= notch_depth
    
    # Ensure balance and space for pace adjustment
    values = np.clip(values, -1.5, 1.5)  # Keep manageable range
    
    # 100% safe balancer at final point
    if safe_balancer:
        values[-1] = 0.0  # Perfect balance at end
    
    return list(zip(times, values))

# Execute with adjusted parameters
trajectory = compute_trajectory(
    frequency=0.5, 
    duration=4.0, 
    steps=20,  # More steps for detail
    tightness_start=0.2,  # Slight tightness
    notch_position=0.77,  # 77% position
    safe_balancer=True
)
print("Trajectory sample:")
for t, v in trajectory:
    print(".2f")
