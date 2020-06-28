# Ball-Free-Fall 自由落體實驗  #coding=utf-8   # 配合 IoTtalk -- by tsaiwn@cs.nctu.edu.tw
# 物理參數區  
# 實驗一修改處：以下兩行
height = 20.0     # 初始高度(m)
restitution = 0.9 # 恢復係數

# 模擬實驗參數區
freq = 1000        # 更新頻率(Hz)
dt = 1.0 / freq   # 更新間隔(second)
isr = True  # is_running 偷懶用 isr

# 讓它有聲音, 這次 gj (Good Job) 沒用到
preloadAudio('Startup.wav')
preloadAudio('chord.wav')
preloadAudio('gj.wav')

# 與流程控制有關參數
# 實驗三修改處：改變重力
g = 5.0          # 定義初始重力加速度

# 初始化場景
def scene_init():
    #initial scene 
    global scene, ball, floor, height, label_info
    scene = display(width=800, height=700, center = vector(0, height/2, 0), \
        background=vector(0.5, 0.5, 0))
    floor = box(length=30, height=0.01, width=10, texture=textures.wood )
    ball = sphere(
        pos = vec(0, height, 0), 
        radius = 0.5, 
        color = color.green,
        velocity = vector(0,0,0),
        visible = True
    )
    label_info = label( pos=vec(10,20,0), text='', color = color.yellow)
    myname = label( pos=vec(-10,23,0), text='我是 007008 張大千', \
        color = vector(0,1,51/255), height=28)
    scene.caption = "這是 Version 0.88" # 畫面下方, 方便知道是否抓到新的 .py 檔案 :-)
                
# 當 Radius 旋鈕收到新值時   # 用 Ball-throw1 的 Speed     
def Speed(data):  #Radius(data):
    global ball, isr   # 別忘了 isr 也要 global
    if data != None:
        ball.radius = data[0]
        isr = True # 讓它動
    if ball.radius == 0:  # 秘技 :-)
        ball.velocity.y = 0;
        ball.radius = 5
        ball.pos.y = 33
        isr = False

# 這是原先 自由落體實驗(Ball-Free-Fall) 沒有的 function; # 用 Ball-throw1 的 Height 
def Height(data):
    global ball, isr  # 別忘了 isr 也要 global
    if data != None:
        ball.pos.y = data[0]
        #isr=True   # 先註解掉, 就是改變高度時, 不干涉是否有在動

# 當 Gravity 旋鈕收到新值時  # 用 Ball-throw1 的 Angle 
def Angle(data):  # def Gravity(data):
    global g, isr  # 別忘了 isr 也要 global
    if data != None:
        g = data[0]
        isr=True

# 每秒鐘更新顯示數據  # 改每秒更新 10次 
def update_info():
    global label_info
    label_info.text='gravity重力: {:.2f}\nradius: {:.2f}\nspeed: {:.2f}\nheight: {:.2f}'.\
        format(g,ball.radius,abs(ball.velocity.y),ball.pos.y)
    rate(10, update_info)

# 設定
def setup():
    scene_init()
    profile = {
        'dm_name' : 'Ball-throw1', # 'Ball-Free-Fall',
        'odf_list' :  [Angle, Speed, Height], #[Gravity,Radius],
    }
    dai(profile)
    update_info()
    playAudio('Startup.wav') 

setup()

#scene.autoscale = False   # 看要不要讓場景遠近 AutoScale; 預設是 True
while True:
    # 在每秒重畫 freq 次
    rate(freq)
    if not isr:
        continue  # 回到 while True; 注意 continue 就是繼續下一回合 
    # 計算下一個時間點的資料並將改變畫出
    # 球的位置變化量是 速度 乘上 時間
    ball.pos = ball.pos + ball.velocity * dt
    # 判斷球的新位置是否高於地面
    if ball.pos.y > ball.radius:
        # 如是，依重力加速度修改速度
        ball.velocity.y = ball.velocity.y -g*dt
    else:
        # 如否，依恢復係數計算出反彈後速度，並設定球的位置在地面上
        ball.velocity.y = -ball.velocity.y * restitution
        ball.pos.y = ball.radius
        if abs(ball.velocity.y) < 0.088:  # 速度太小就歸 0 
            ball.velocity.y = 0
            isr = False
        if ball.velocity.y > 0.1:  # 這時播放撞擊聲 
            playAudio('chord.wav')
### End of the Program 自由落體實驗
