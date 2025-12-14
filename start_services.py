#!/usr/bin/env python3
import os
import sys
import subprocess
import signal

def signal_handler(signum, frame):
    print("\n🛑 接收到停止信号，正在关闭服务...")
    
    try:
        subprocess.run(["pkill", "-f", "streamlit"], check=False)
    except:
        pass
    
    print("✅ 服务已停止")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🚀 启动智慧工地检测系统...")
    print("=" * 50)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_script = os.path.join(script_dir, "app.py")
    
    if not os.path.exists(app_script):
        print(f"❌ 找不到主应用脚本: {app_script}")
        return 1
    
    try:
        print("🌐 启动Streamlit应用...")
        streamlit_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", app_script,
            "--browser.gatherUsageStats", "false"
        ])
        
        print("\n" + "=" * 50)
        print("🎉 系统启动成功！")
        print("📱 Streamlit界面: http://localhost:8501")
        print("=" * 50)
        print("\n按 Ctrl+C 停止服务")
        
        streamlit_process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 接收到中断信号...")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return 1
    finally:
        try:
            streamlit_process.terminate()
        except:
            pass
        
        subprocess.run(["pkill", "-f", "streamlit"], check=False)
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
