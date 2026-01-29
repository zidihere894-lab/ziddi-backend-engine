import firebase_admin
from firebase_admin import credentials, db
import json
import os
import time

def init_firebase():
    if not firebase_admin._apps:
        # GitHub Secret se key uthana
        key_data = os.environ.get('FIREBASE_KEY')
        if not key_data:
            print("❌ Error: FIREBASE_KEY Secret nahi mila!")
            return False
        
        try:
            # Secret ko JSON mein convert karna
            cred_dict = json.loads(key_data)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://movie-1e6fc-default-rtdb.firebaseio.com'
            })
            return True
        except Exception as e:
            print(f"❌ Firebase Init Error: {e}")
            return False

def run_ziddi_engine():
    if not init_firebase(): return
    
    ref = db.reference('tasks')
    tasks = ref.get()

    if not tasks:
        print("📭 Queue khali hai.")
        return

    for tid, tdata in tasks.items():
        # Check if task is new and waiting
        if tdata.get('status') == 'Waiting for Engine...':
            t_type = tdata.get('type')
            print(f"⚙️ Processing {t_type} Task: {tid}")
            
            # Website par status update karna
            ref.child(tid).update({'status': f'⚡ Sending {t_type}...'})
            
            # --- Actual Processing Start ---
            # Yahan hum simulate kar rahe hain
            time.sleep(10) 
            # --- Actual Processing End ---
            
            # Task complete status bhejna
            ref.child(tid).update({'status': 'completed'})
            print(f"✅ Task {tid} Successfully Done!")

if __name__ == "__main__":
    run_ziddi_engine()
