from ultralytics import YOLO
import streamlit as st
import cv2
from PIL import Image
import tempfile
import torch
import functools
import os

@functools.lru_cache(None)
def _patch_torch_load():
    orig = torch.load
    def _load(*args, **kwargs):
        if kwargs.get("weights_only") is None:
            kwargs["weights_only"] = False
        return orig(*args, **kwargs)
    torch.load = _load

_patch_torch_load()

@st.cache_resource
def load_model(model_path):
    try:
        model = YOLO(model_path)
        return model
    except Exception as ex:
        st.error(f"模型加载失败: {ex}")
        return None

def _display_detected_frames(conf, model, st_frame, image):
    image = cv2.resize(image, (720, int(720 * (9 / 16))))
    res = model.predict(image, conf=conf, classes=[0, 2, 5])
    plotted_img = image.copy()

    hat_count = no_hat_count = 0
    for r in res:
        for box in r.boxes:
            b = box.xyxy[0].cpu().numpy()
            cls = int(box.cls[0].item())
            cf = float(box.conf[0].item())
            if cls == 0:
                color, label = (0, 255, 0), f"有安全帽 {cf:.2f}"
                hat_count += 1
            elif cls == 2:
                color, label = (0, 0, 255), f"无安全帽 {cf:.2f}"
                no_hat_count += 1
            elif cls == 5:
                color, label = (255, 0, 0), f"人 {cf:.2f}"
            else:
                continue
            cv2.rectangle(plotted_img, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), color, 2)
            cv2.putText(plotted_img, label, (int(b[0]), int(b[1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    st_frame.image(plotted_img, channels="BGR")

    total = hat_count + no_hat_count
    if no_hat_count > 0:
        alert_html = f"""
        <div style='font-size:32px;color:red;font-weight:bold;background:#ffebee;padding:15px;border-radius:5px;margin:20px 0;'>
            ⚠️ 安全警报：发现 {no_hat_count} 人未佩戴安全帽！
        </div>"""
    else:
        alert_html = """
        <div style='font-size:32px;color:green;font-weight:bold;background:#e8f5e9;padding:15px;border-radius:5px;margin:20px 0;'>
            ✓ 安全状态：所有人均佩戴安全帽
        </div>"""

    st.markdown(alert_html, unsafe_allow_html=True)
    result_html = f"""
    <div><span style='font-size:35px;font-weight:bold;'>{hat_count}</span> 人佩戴安全帽</div>
    <div><span style='font-size:35px;font-weight:bold;color:red;'>{no_hat_count}</span> 人未佩戴安全帽</div>
    """
    st.markdown(result_html, unsafe_allow_html=True)

def infer_uploaded_image(conf, model):
    source_img = st.sidebar.file_uploader("选择一张图片...", type=("jpg", "jpeg", "png", "bmp", "webp"))
    col1, col2 = st.columns(2)
    if source_img:
        uploaded_image = Image.open(source_img)
        with col1:
            st.image(source_img, caption="已上传图片")

        if st.button("执行检测"):
            with st.spinner("正在运行..."):
                res = model.predict(uploaded_image, conf=conf, classes=[0, 2, 5])
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                hat_count = sum(1 for b in boxes if int(b.cls[0].item()) == 0)
                no_hat_count = sum(1 for b in boxes if int(b.cls[0].item()) == 2)

                with col2:
                    st.image(res_plotted)
                    total = hat_count + no_hat_count
                    result_html = f"""
                    <div style='font-size:40px;text-align:center;margin-top:15px;'>
                        共检测到 <span style='color:blue;'>{total}</span> 人
                    </div>
                    <div><span style='font-size:35px;font-weight:bold;'>{hat_count}</span> 人佩戴安全帽</div>
                    <div><span style='font-size:35px;font-weight:bold;color:red;'>{no_hat_count}</span> 人未佩戴安全帽</div>
                    """
                    st.markdown(result_html, unsafe_allow_html=True)

                with col1:
                    if no_hat_count > 0:
                        alert_html = f"""
                        <div style='font-size:28px;color:red;font-weight:bold;background:#ffebee;padding:15px;border-radius:5px;margin:20px 0;text-align:center;'>
                            ⚠️ 安全警报：发现 {no_hat_count} 人未佩戴安全帽！
                        </div>"""
                    else:
                        alert_html = """
                        <div style='font-size:28px;color:green;font-weight:bold;background:#e8f5e9;padding:15px;border-radius:5px;margin:20px 0;text-align:center;'>
                            ✓ 安全状态：所有人均佩戴安全帽
                        </div>"""
                    st.markdown(alert_html, unsafe_allow_html=True)

    return None, None

def infer_uploaded_video(conf, model):
    source_video = st.sidebar.file_uploader("选择一个视频...")
    if source_video:
        st.video(source_video)
        if st.button("执行检测"):
            with st.spinner("正在运行..."):
                try:
                    tfile = tempfile.NamedTemporaryFile(delete=False)
                    tfile.write(source_video.read())
                    tfile.close()
                    vid_cap = cv2.VideoCapture(tfile.name)
                    st_frame = st.empty()
                    while vid_cap.isOpened():
                        success, image = vid_cap.read()
                        if success:
                            _display_detected_frames(conf, model, st_frame, image)
                        else:
                            break
                    vid_cap.release()
                    os.unlink(tfile.name)
                except Exception as e:
                    st.error(f"视频加载错误: {e}")

def infer_uploaded_webcam(conf, model):
    try:
        flag = st.button("停止运行")
        vid_cap = cv2.VideoCapture(0)
        st_frame = st.empty()
        while not flag:
            success, image = vid_cap.read()
            if success:
                _display_detected_frames(conf, model, st_frame, image)
            else:
                break
        vid_cap.release()
    except Exception as e:
        st.error(f"摄像头访问错误: {e}")