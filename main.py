import firebase_admin
from firebase_admin import credentials, db
import json
import os
import time

def init_firebase():
    if not firebase_admin._apps:
        # GitHub Secret se data uthana
        key_data = os.environ.get('FIREBASE_KEY')
        
        if key_data:
            print("✅ Firebase Key found in Secrets!")
            cred_dict = json.loads(key_data)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://movie-1e6fc-default-rtdb.firebaseio.com'
            })
            return True
        else:
            print("❌ Error: FIREBASE_KEY Secret nahi mila!")
            return False

def run_engine():
    if not init_firebase(): return
    
    ref = db.reference('tasks')
    tasks = ref.get()

    if not tasks:
        print("Queue khali hai.")
        return

    for tid, tdata in tasks.items():
        if tdata.get('status') == 'Waiting for Engine...':
            print(f"Task process ho raha hai: {tid}")
            ref.child(tid).update({'status': '⚡ Engine Working...'})
            
            # Simulation (10 second ka gap)
            time.sleep(10)
            
            ref.child(tid).update({'status': 'completed'})
            print(f"Task {tid} khatam!")

if __name__ == "__main__":
    run_engine()
