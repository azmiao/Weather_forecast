from PyQt5 import QtCore,QtGui,QtWidgets
import sys
import qtawesome
import requests
import csv
import os

# 通用数据
key = '' # 聚合数据API的KEY
current_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)).replace('\code', ''), 'csv')

# 通用类
class universal_info():
    def __init__(self, headers, info, filename):
        self.headers = headers
        self.info = info
        self.filename = filename

# 界面类
class main_ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui() 

    def init_ui(self):
        # 创建网格布局的窗口
        self.setFixedSize(1280,720)
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        self.left_widget = QtWidgets.QWidget()
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()
        self.left_widget.setLayout(self.left_layout)
        self.right_widget = QtWidgets.QWidget()
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)
        # 左右布局
        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)
        self.setCentralWidget(self.main_widget)

        # 窗口优化
        self.setWindowOpacity(1)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.main_layout.setSpacing(0)
        self.main_widget.setStyleSheet('''
            QWidget#left_widget{
            background:gray;
            border-top:1px solid white;
            border-bottom:1px solid white;
            border-left:1px solid white;
            border-top-left-radius:10px;
            border-bottom-left-radius:10px;
            }
            ''')

        # 左边的效果
        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
            ''')

        # 右边的效果
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            ''')

        # 输入框
        self.search_icon = QtWidgets.QLabel('              ' + chr(0xf002))
        self.search_icon.setFont(qtawesome.font('fa', 16))
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("请输入您要查询的省份后再点左边按钮")
        self.right_layout.addWidget(self.search_icon, 0, 0, 1, 1)
        self.right_layout.addWidget(self.search_input, 0, 1, 1, 7)

        # 四个功能按钮
        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.tasks', color = 'white'), "城市列表")
        self.left_button_1.setObjectName('left_button')
        self.left_button_1.clicked.connect(pushButton_city)
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.sellsy', color = 'white'), "天气类型")
        self.left_button_2.setObjectName('left_button')
        self.left_button_2.clicked.connect(pushButton_wid)

        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.cloud', color = 'white'), "天气查询")
        self.left_button_3.setObjectName('left_button')
        self.left_button_3.clicked.connect(self.pushButton_weather)
        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.info', color = 'white'), "指数查询")
        self.left_button_4.setObjectName('left_button')
        self.left_button_4.clicked.connect(self.pushButton_index)
        self.left_layout.addWidget(self.left_button_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_2, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_3, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_4, 4, 0, 1, 3)

        # 控制按钮
        self.left_mini = QtWidgets.QPushButton("")
        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_mini.clicked.connect(self.showMinimized)
        self.left_visit = QtWidgets.QPushButton("")
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_visit.clicked.connect(self.max_or_recv)
        self.left_close = QtWidgets.QPushButton("")
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_close.clicked.connect(self.close)
        
        # 控制台
        self.right_console_label = QtWidgets.QLabel("详细控制台:")
        self.right_console_label.setObjectName('right_lable')
        self.right_layout.addWidget(self.right_console_label, 1, 0, 1, 2)
        self.textBrowser = QtWidgets.QTextBrowser()
        self.textBrowser.setObjectName("textBrowser")
        self.right_layout.addWidget(self.textBrowser, 2, 0, 1, 8)

        self.search_input.setStyleSheet(
            '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
            }''')

        # 按钮大小和颜色
        self.left_close.setFixedSize(20, 20)
        self.left_visit.setFixedSize(20, 20)
        self.left_mini.setFixedSize(20, 20)
        self.left_close.setStyleSheet('''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet('''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet('''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        # 重定向输出
        sys.stdout = signal(text = self.output)
        sys.stderr = signal(text = self.output)

    # 接收信号
    def output(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    # 窗口最大化和恢复
    def max_or_recv(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # 查询天气的点击事件
    def pushButton_weather(self):
        try:
            query_city = self.search_input.text()
            if query_city == '':
                print('\n省份为空！')
                return
            weather_info = get_weather(query_city)
            write_info(weather_info)
        except:
            print('出现异常！请尝试重启软件！\n可能的原因是：1.连接API失败\n2.今日接口使用次数已经达到上限\n')

    # 查询生活指数的点击事件
    def pushButton_index(self):
        try:
            query_city = self.search_input.text()
            if query_city == '':
                print('\n省份为空！')
                return
            life_info = get_life_index(query_city)
            write_info(life_info)
        except:
            print('出现异常！请尝试重启软件！\n可能的原因是：1.连接API失败\n2.今日接口使用次数已经达到上限\n')


# 发射信号类
class signal(QtCore.QObject):  
        text = QtCore.pyqtSignal(str)
        def write(self, text):
            self.text.emit(str(text))  

# 创建目录
def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path) 
        print('检测到目录不存在，现在创建目录：' + path +' 创建成功\n')
    else:
        print('检测到目录已存在，将不会创建目录\n')

# 通用函数：将信息写入CSV
def write_info(universal_info):
    file_dir = os.path.join(current_dir, universal_info.filename)
    with open(file_dir,'w')as f:
        f_csv = csv.writer(f)
        f_csv.writerow(universal_info.headers)
        f_csv.writerows(universal_info.info)
    f.close()
    print('\n文件' + str(universal_info.filename) + '的信息写入完毕\n')

# 获取城市列表的点击事件
def pushButton_city():
    try:
        universal_info = get_allcitys()
        write_info(universal_info)
    except:
        print('出现异常！请尝试重启软件！\n可能的原因是：1.连接API失败\n2.今日接口使用次数已经达到上限\n')

# 获取天气类型的点击事件
def pushButton_wid():
    try:
        wid_info = get_wid()
        write_info(wid_info)
    except:
        print('出现异常！请尝试重启软件！\n可能的原因是：1.连接API失败\n2.今日接口使用次数已经达到上限\n')

# 获取所有的城市列表
def get_allcitys():
    url = 'http://apis.juhe.cn/simpleWeather/cityList'
    params = {'key': key}
    data = requests.get(url, params).json()
    all_info = []
    # print(data)
    for row_info in data['result']:
        row = []
        row.append(row_info['id'])
        row.append(row_info['province'])
        row.append(row_info['city'])
        row.append(row_info['district'])
        all_info.append(row)

    print('\n所有的城市信息为：')
    print(all_info)
    universal_info.headers = ['ID', '省', '市', '区']
    universal_info.info = all_info
    universal_info.filename = 'citys.csv'
    return universal_info

# 查询天气种类
def get_wid():
    url = 'http://apis.juhe.cn/simpleWeather/wids'
    params = {'key': key}
    data = requests.get(url, params).json()
    wid_info = []
    # print(data)
    for row_info in data['result']:
        row = []
        row.append(row_info['wid'])
        row.append(row_info['weather'])
        wid_info.append(row)

    print('\n所有的天气种类为：')
    print(wid_info)
    universal_info.headers = ['类型ID', '天气种类']
    universal_info.info = wid_info
    universal_info.filename = 'wid.csv'
    return universal_info

# 获取某省前十个城市的天气
def get_weather(query_city):
    url = 'http://apis.juhe.cn/simpleWeather/cityList'
    params = {'key': key}
    resp = requests.get(url, params)
    data = resp.json()['result']
    city_list = []
    n = 0
    for city_tmp in data:
        if city_tmp['province'] == query_city:
            n = 1
            city_list.append(city_tmp['district'])

    if n == 0:
        print('该城市不存在！')
        sys.exit()

    # city实际上是district
    weather_info = []
    print('\n前十个城市天气信息为：')
    for city in city_list[0: 10]:
        url_w = 'http://apis.juhe.cn/simpleWeather/query'
        params_w = {'city': city, 'key': key}
        resp_w = requests.get(url_w, params_w)
        print(resp_w.json())
        print(' ')
        w_info = []
        w_info.append(city)
        w_info.append(resp_w.json()['result']['realtime']['temperature'])
        w_info.append(resp_w.json()['result']['realtime']['humidity'])
        w_info.append(resp_w.json()['result']['realtime']['info'])
        w_info.append(resp_w.json()['result']['realtime']['wid'])
        w_info.append(resp_w.json()['result']['realtime']['direct'])
        w_info.append(resp_w.json()['result']['realtime']['power'])
        w_info.append(resp_w.json()['result']['realtime']['aqi'])
        weather_info.append(w_info)
    
    universal_info.headers = ['城市', '温度', '湿度', '天气种类', '类型ID', '风向', '风力', '空气质量指数']
    universal_info.info = weather_info
    universal_info.filename = 'weather.csv'
    return universal_info

# 获取某省前十个城市的生活指数
def get_life_index(query_city):
    url = 'http://apis.juhe.cn/simpleWeather/cityList'
    params = {'key': key}
    resp = requests.get(url, params)
    data = resp.json()['result']
    city_list = []
    n = 0
    for city_tmp in data:
        if city_tmp['province'] == query_city:
            n = 1
            city_list.append(city_tmp['district'])

    if n == 0:
        print('该城市不存在！')
        sys.exit()

    # city实际上是district
    life_info = []
    print('\n前十个城市生活指数信息为：')
    for city in city_list[0: 10]:
        url_l = 'http://apis.juhe.cn/simpleWeather/life'
        params_l = {'city': city, 'key': key}
        resp_l = requests.get(url_l, params_l)
        print(resp_l.json())
        print(' ')
        w_info = []
        w_info.append(city)
        w_info.append(resp_l.json()['result']['life']['kongtiao']['v'])
        w_info.append(resp_l.json()['result']['life']['guomin']['v'])
        w_info.append(resp_l.json()['result']['life']['shushidu']['v'])
        w_info.append(resp_l.json()['result']['life']['ganmao']['v'])
        w_info.append(resp_l.json()['result']['life']['xiche']['v'])
        w_info.append(resp_l.json()['result']['life']['yundong']['v'])
        life_info.append(w_info)
    
    universal_info.headers = ['城市', '空调', '过敏', '舒适度', '感冒', '洗车', '运动']
    universal_info.info = life_info
    universal_info.filename = 'life_index.csv'
    return universal_info

# 主函数
def main():
    app = QtWidgets.QApplication(sys.argv)
    windows = main_ui()
    windows.show()
    mkdir(current_dir)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()