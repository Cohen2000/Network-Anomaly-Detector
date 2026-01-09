import psutil
import time
import pandas as pd
from pynput import mouse, keyboard
from datetime import datetime
import os

# Settings
INTERVAL = 1.0 
DATA_DIR = "data"

# Global to track user activity
last_activity = time.time()

def update_activity(*args):
    global last_activity
    last_activity = time.time()

# Listeners for mouse and keyboard events
m_listener = mouse.Listener(on_move=update_activity, on_click=update_activity, on_scroll=update_activity)
k_listener = keyboard.Listener(on_press=update_activity)
m_listener.start()
k_listener.start()

def get_sys_metrics():
    # Get network counters and filter for established TCP connections
    net = psutil.net_io_counters()
    conns = psutil.net_connections(kind='tcp')
    est_conns = len([c for c in conns if c.status == 'ESTABLISHED'])
    return net.bytes_sent, net.bytes_recv, est_conns

def start_monitoring(name, label, duration_min):
    data = []
    print(f"--- Monitoring Scenario: {name} ---")
    
    # Baseline for rate calculation
    old_s, old_r, _ = get_sys_metrics()
    old_t = time.perf_counter()

    try:
        ticks = int((duration_min * 60) / INTERVAL)
        for i in range(ticks):
            time.sleep(INTERVAL)
            
            # Snapshots
            curr_s, curr_r, tcp_count = get_sys_metrics()
            curr_t = time.perf_counter()
            
            # Calculations
            dt = curr_t - old_t
            idle = round(time.time() - last_activity, 2)
            up_speed = round(((curr_s - old_s) / 1024) / dt, 2)
            down_speed = round(((curr_r - old_r) / 1024) / dt, 2)
            
            data.append({
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "sent_kb_s": up_speed,
                "recv_kb_s": down_speed,
                "tcp_established": tcp_count,
                "idle_sec": idle,
                "label": label
            })
            
            # Update baseline
            old_s, old_r, old_t = curr_s, curr_r, curr_t
            
            if (i + 1) % 20 == 0:
                print(f"Logged {i + 1} seconds...")

    except KeyboardInterrupt:
        print("\nStopping...")

    # Export to CSV
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    df = pd.DataFrame(data)
    file_path = os.path.join(DATA_DIR, f"{name}.csv")
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

if __name__ == "__main__":
    name = input("Scenario Name: ").strip()
    label = int(input("Label (0=Normal, 1=Anomaly): "))
    duration = float(input("Duration (minutes): "))
    start_monitoring(name, label, duration)