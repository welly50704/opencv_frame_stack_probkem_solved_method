import cv2
import time
import threading


# 接收攝影機串流影像，用多線程的方式降低緩衝區堆疊圖幀的問題，以解決opencv卡礑的困。
# Using threading to sloved opencv(cv2)'s buffer size problem(frame lag),this can reduce the problem of frames stack.
class Cam_capture:
    def __init__(self, URL):
        self.Frame = []
        self.status = False
        self.isstop = False
		
	# Connecting the camera。
        self.capture = cv2.VideoCapture(URL)

    def start(self):
	# 把程式放進子執行緒，daemon=True 表示該執行緒會隨著主執行緒關閉而關閉。
        print('cam started!')
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()

    def stop(self):
	# 記得要設計停止無限迴圈的開關。
        self.isstop = True
        print('cam stopped!')
   
    def getframe(self):
	# 當有需要影像時，再回傳最新的影像。
        return self.Frame
        
    def queryframe(self):
        while (not self.isstop):
            self.status, self.Frame = self.capture.read()
        
        self.capture.release()



# 連接攝影機
cam = Cam_capture(0)
count = 0
# 啟動子執行緒
cam.start()


# 暫停1秒，確保影像已經填充
time.sleep(1)

# 使用無窮迴圈擷取影像，直到按下Esc鍵結束
while True:
    # 使用 getframe 取得最新的影像
    nowtime = str(round(time.time()))
    imgfilename = 'D:/cv2photo/' + nowtime + '.jpg'
    frame = cam.getframe()
    
    cv2.imshow('Image', frame)
    count += 1
    #0.1*25,也就是2.5秒拍一次
    if count == 25:
        cv2.imwrite(imgfilename, frame)
        count = 0
        print(nowtime)
    #1000 = 一秒一幀，我這設一秒10幀
    if cv2.waitKey(100) == 27:
        cv2.destroyAllWindows()
        ipcam.stop()
        break
