from face_prediction_client import prediction_client
import threading
import os
#多執行緒
def run_face_prediction_client():
    
    # 建立一個子執行緒
    t = threading.Thread(target = os.system(prediction_client))

    # 執行該子執行緒
    t.start()