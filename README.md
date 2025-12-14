
<div align="center">

# SafetyHelmet - Smart Construction Site Detection System

**智慧工地检测系统**

基于 YOLOv8 的工地安全帽检测系统，采用 Streamlit 构建用户友好的交互界面。

</div>

## Introduction
SafetyHelmet is an intelligent construction site safety detection system based on [YOLOv8](https://github.com/ultralytics/ultralytics) object detection framework and [Streamlit](https://github.com/streamlit/streamlit) web interface. The system can detect in real-time whether construction site personnel are wearing safety helmets, improving construction site safety management efficiency.

## 简介
SafetyHelmet 是一个智能工地安全检测系统，基于 [YOLOv8](https://github.com/ultralytics/ultralytics) 目标检测框架，使用 [Streamlit](https://github.com/streamlit/streamlit) 构建交互式 Web 界面。系统能够实时检测工地人员是否佩戴安全帽，提高工地安全管理效率。

## Features / 功能特性
- 🎯 Safety Helmet Detection / 安全帽检测：Real-time detection of whether personnel are wearing safety helmets / 实时检测人员是否佩戴安全帽
- 📊 Multiple Input Methods / 多种输入方式：Support for images, videos, and real-time webcam detection / 支持图像、视频、摄像头实时检测
- 🚀 Efficient Inference / 高效推理：Based on YOLOv8 lightweight model with fast inference speed / 基于 YOLOv8 轻量级模型，推理速度快
- 💻 User-Friendly Interface / 友好界面：Intuitive web interface based on Streamlit / 基于 Streamlit 的直观 Web 界面
- ⚠️ Safety Alerts / 安全警报：Real-time alerts when unsafe helmet wearing is detected / 检测到未佩戴安全帽时实时警报

## Detection Results / 检测效果
- With Safety Helmet / 有安全帽：Green bounding box / 绿色框标注
- Without Safety Helmet / 无安全帽：Red bounding box with safety alert / 红色框标注，触发安全警报
- Personnel Statistics / 人员统计：Real-time display of detected personnel count and helmet wearing status / 实时显示检测到的人员数量和安全帽佩戴情况


## 环境要求
- Python 3.8+
- CUDA 11.0+ (可选，用于 GPU 加速)
- 4GB+ 内存

## 安装步骤

### 1. 创建虚拟环境
```bash
conda create -n safety-helmet python=3.9 -y
conda activate safety-helmet
```

### 2. 克隆项目
```bash
git clone <repository-url>
cd <project-directory>
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 模型文件
项目已包含以下模型文件：
- `weights/detection/yolov8n.pt` - YOLOv8 baseline 模型
- `weights/detection/SafetyHelmetWearing.pt` - 安全帽检测专用模型

## 使用方法

### 方式一：直接运行（已弃用）
```bash
python app.py
```

### 方式二：使用启动脚本
```bash
python start_services.py
```

### 方式三：Streamlit 命令（不建议）
```bash
streamlit run app.py
```

启动后，系统会自动打开浏览器访问 `http://localhost:8501`

## 功能说明

### 图像检测
1. 在侧边栏选择"图像"作为输入源
2. 上传图片文件
3. 点击"执行检测"按钮
4. 查看检测结果和安全警报

### 视频检测
1. 在侧边栏选择"视频"作为输入源
2. 上传视频文件
3. 点击"执行检测"按钮
4. 实时显示检测结果

### 摄像头实时检测（未测试）
1. 在侧边栏选择"摄像头"作为输入源
2. 点击"停止运行"按钮开始检测
3. 实时显示摄像头画面和检测结果

## Project Structure / 项目结构
```
.
├── app.py                          # Main application / 主应用程序
├── config.py                       # Configuration file / 配置文件
├── utils.py                        # Utility functions / 工具函数
├── start_services.py               # Startup script / 启动脚本
├── requirements.txt                # Dependencies / 依赖列表
├── weights/
│   └── detection/
│       ├── yolov8n.pt             # YOLOv8 nano model / YOLOv8 nano 模型
│       └── SafetyHelmetWearing.pt # Safety helmet detection model / 安全帽检测模型
└── README.md                       # This file / 本文件
```

## Configuration / 配置说明
In `config.py` you can configure:
- Model paths / 模型路径
- Detection classes / 检测类别
- Input source types / 输入源类型

在 `config.py` 中可以配置：
- 模型路径
- 检测类别
- 输入源类型

## FAQ / 常见问题

### Q: How to use GPU acceleration? / 如何使用 GPU 加速？
A: Make sure CUDA and cuDNN are installed. PyTorch will automatically detect and use GPU. / 确保已安装 CUDA 和 cuDNN，PyTorch 会自动检测并使用 GPU。

### Q: Detection results are not ideal? / 检测效果不理想？
A: Try adjusting the confidence parameter in the sidebar, or use a larger model (e.g., yolov8s). / 可以尝试调整侧边栏的置信度参数，或使用更大的模型（如 yolov8s）。

### Q: How to use custom models? / 如何自定义模型？
A: Place trained models in the `weights/detection/` directory and add them to the model list in `config.py`. / 将训练好的模型放在 `weights/detection/` 目录下，并在 `config.py` 中添加模型列表。

## License / 许可证
MIT License

## Contributing / 贡献
Welcome to submit Issues and Pull Requests! / 欢迎提交 Issue 和 Pull Request！

## Changelog / 更新日志

### v1.0.0 (2025-12-14)
- ✅ Complete basic detection functionality / 完成基础检测功能
- ✅ Support for image, video, and webcam input / 支持图像、视频、摄像头输入
- ✅ Real-time safety alerts / 实时安全警报
- ✅ Dynamic GPU information display / 动态显示 GPU 信息
- ✅ Bilingual documentation (English/Chinese) / 双语文档（英文/中文）

## Contact / 联系方式
If you have any questions or suggestions, please submit an Issue or Pull Request. / 如有问题或建议，欢迎提交 Issue 或 Pull Request。
