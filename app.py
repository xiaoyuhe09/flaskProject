from flask import Flask, request, render_template

# 实例化flask对象
app = Flask(__name__)


# 其它模块使用app数据，完成http访问
def get_app():
    return app

# @app.route('/index')
# def index():
#     return render_template("index.html")

@app.route('/subpage')
def subpage():
    return render_template("subpage.html")




# 测试get请求
@app.route('/getTest')
def get_test():
    # 获取get请求参数
    data = request.args.get('name')
    print(data)
    return "get request"


# 测试post请求
@app.route('/postTest', methods=['POST'])
def post_test():
    # 获取post请求参数-json格式
    data = request.get_json()
    print(data)
    return "post request"


# 启动服务
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)