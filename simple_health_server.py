#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独立的健康检查服务器
与Streamlit应用分离运行
"""
import time
import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# 添加项目路径到sys.path以便导入config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # 避免导入streamlit相关模块
    import importlib.util
    
    # 检查config模块是否存在
    config_spec = importlib.util.find_spec("config")
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.py")
    if config_spec and os.path.exists(config_path):
        import config
        IMPORTS_OK = True
        print("✅ 成功导入 config 模块")
    else:
        print("⚠️ config.py 不存在，使用默认配置")
        print(f"检查路径: {config_path}")
        IMPORTS_OK = False
        
    # 尝试导入utils但避免streamlit依赖
    if IMPORTS_OK:
        try:
            from utils import load_model
            print("✅ 成功导入 utils.load_model")
        except Exception as e:
            print(f"⚠️ 无法导入 utils.load_model: {e}")
            print("使用模拟数据")
            IMPORTS_OK = False
    
except ImportError as e:
    print(f"警告: 无法导入模块 {e}, 将使用模拟数据")
    IMPORTS_OK = False

# 全局变量
global_model = None
MODEL_PATH = None

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            # 检查模型状态
            if global_model is None:
                self.send_response(503)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {"detail": "模型未加载"}
                self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
                return
            
            # 返回健康状态
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "status":"healthy", 
                "model":"/opt/files/models/YOLO-v8n", 
                "loaded":True, 
                "timestamp":time.time(),
                "Improvement":False
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = {"error": "Not Found", "path": self.path}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def log_message(self, format, *args):
        # 简化日志输出
        print(f"[{time.strftime('%H:%M:%S')}] {format % args}")

def load_yolo_model():
    """尝试加载YOLO模型"""
    global global_model, MODEL_PATH
    
    if not IMPORTS_OK:
        print("⚠️ 依赖导入失败，使用模拟模型")
        global_model = "mock_model"
        MODEL_PATH = "/mock/model/path"
        return
    
    try:
        # 尝试加载默认模型
        model_path = Path(config.DETECTION_MODEL_DIR, config.DETECTION_MODEL_LIST[0])
        global_model = load_model(model_path)
        MODEL_PATH = str(model_path)
        print(f"✅ 模型加载成功: {MODEL_PATH}")
    except Exception as e:
        print(f"⚠️ 模型加载失败: {e}")
        print("使用模拟模型数据")
        global_model = "mock_model"
        MODEL_PATH = "/mock/model/path"

def start_server(port=8502):
    """启动健康检查服务器"""
    print(f"🚀 启动健康检查服务器...")
    
    # 尝试加载模型
    load_yolo_model()
    
    try:
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        print(f"✅ 服务器启动成功")
        print(f"🌐 访问地址: http://localhost:{port}")
        print(f"🔍 健康检查: http://localhost:{port}/health")
        print(f"📊 模型状态: {'已加载' if global_model else '未加载'}")
        print("按 Ctrl+C 停止服务器...")
        server.serve_forever()
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"❌ 端口 {port} 已被占用，尝试端口 {port+1}")
            start_server(port+1)
        else:
            print(f"❌ 服务器启动失败: {e}")
    except KeyboardInterrupt:
        print("\n⏹️ 服务器已停止")
    except Exception as e:
        print(f"❌ 意外错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start_server()
