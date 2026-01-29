import firebase_admin
from firebase_admin import credentials, db
import requests
import time
import os

# Firebase Connection Logic
def connect_firebase():
    if not firebase_admin._apps:
        # File path check
        if os.path.exists("serviceAccountKey.json"):
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://movie-1e6fc-default-rtdb.firebaseio.com'
            })
            return True
        else:
            print("Error: serviceAccountKey.json not found!")
            return False

def run_ziddi_engine():
    if not connect_firebase(): return
    
    tasks_ref = db.reference('tasks')
    tasks = tasks_ref.get()

    if not tasks:
        print("No tasks in queue.")
        return

    for tid, tdata in tasks.items():
        if tdata.get('status') == 'Waiting for Engine...':
            t_type = tdata.get('type')
            url = tdata.get('post_url')
            
            # Update status on Website
            tasks_ref.child(tid).update({'status': '⚡ Processing Order...'})
            print(f"Working on {t_type} for: {url}")

            # --- Yahan API Connection Hoga ---
            # Abhi hum testing ke liye success bhej rahe hain
            time.sleep(10) 
            
            tasks_ref.child(tid).update({'status': 'completed'})
            print(f"Task {tid} Done!")

if __name__ == "__main__":
    run_ziddi_engine()
