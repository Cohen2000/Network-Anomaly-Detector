import psutil
import time
import joblib
import numpy as np
from datetime import datetime
from pynput import mouse, keyboard

# Load model
model = joblib.load("models/model_rf.joblib")

# Idle tracking
last_activity = time.time()

def update_activity(*args):
    global last_activity
    last_activity = time.time()

m_listener = mouse.Listener(on_move=update_activity, on_click=update_activity)
k_listener = keyboard.Listener(on_press=update_activity)
m_listener.start()
k_listener.start()

def get_metrics():
    net = psutil.net_io_counters()
    conns = psutil.net_connections(kind='tcp')
    tcp_est = len([c for c in conns if c.status == 'ESTABLISHED'])
    return net.bytes_sent, net.bytes_recv, tcp_est

print("="*60)
print("ANOMALY DETECTOR - Press Ctrl+C to stop")
print("="*60)

old_sent, old_recv, _ = get_metrics()
old_time = time.perf_counter()

try:
    while True:
        time.sleep(1)
        
        curr_sent, curr_recv, tcp_est = get_metrics()
        curr_time = time.perf_counter()
        dt = curr_time - old_time
        
        sent_kb_s = (curr_sent - old_sent) / 1024 / dt
        recv_kb_s = (curr_recv - old_recv) / 1024 / dt
        idle_sec = round(time.time() - last_activity, 2)
        
        X = np.array([[sent_kb_s, recv_kb_s, idle_sec]])
        pred = model.predict(X)[0]
        proba = model.predict_proba(X)[0]
        label = ">>> ANOMALY <<<" if pred == 1 else "Normal"
        
        print(f"  Confidence: normal={proba[0]:.1%}, anomaly={proba[1]:.1%}")
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] sent={sent_kb_s:>7.1f} | recv={recv_kb_s:>7.1f} | tcp={tcp_est:>2} | idle={idle_sec:>6.1f} | {label}")
        
        old_sent, old_recv, old_time = curr_sent, curr_recv, curr_time

except KeyboardInterrupt:
    print("\nStopped.")