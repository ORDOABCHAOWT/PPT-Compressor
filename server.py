#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPT Compressor Web Server
macOS Sequoia Style - 增强版 Flask 服务器，支持自动打开浏览器
"""

from flask import Flask, render_template, request, send_file, jsonify, Response
import os
import sys
import webbrowser
import threading
import time
import uuid
from werkzeug.utils import secure_filename
from ppt_compressor_v3 import ModernPPTCompressor
import shutil
from pathlib import Path
import queue

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['COMPRESSED_FOLDER'] = 'compressed'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB limit

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['COMPRESSED_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)

# 进度跟踪
progress_queues = {}

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress_file():
    """启动压缩任务并返回任务ID"""
    if 'file' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400

    if file and (file.filename.endswith('.ppt') or file.filename.endswith('.pptx')):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        preset = request.form.get('preset', 'balanced')

        # 生成任务ID
        task_id = str(uuid.uuid4())
        progress_queues[task_id] = queue.Queue()

        # 在后台线程中执行压缩
        thread = threading.Thread(
            target=compress_worker,
            args=(task_id, upload_path, filename, preset)
        )
        thread.daemon = True
        thread.start()

        return jsonify({
            'success': True,
            'task_id': task_id
        })

    return jsonify({'error': '不支持的文件格式'}), 400

def compress_worker(task_id, upload_path, filename, preset):
    """后台压缩任务"""
    try:
        progress_queue = progress_queues[task_id]

        # 发送初始化消息
        progress_queue.put({'status': 'progress', 'percent': 0, 'message': '开始压缩...'})

        # 初始化压缩器
        compressor = ModernPPTCompressor(preset=preset)

        # 定义输出路径
        output_filename = f"compressed_{filename}"
        output_path = os.path.join(app.config['COMPRESSED_FOLDER'], output_filename)

        # 定义进度回调函数
        def progress_callback(percent, message):
            progress_queue.put({'status': 'progress', 'percent': percent, 'message': message})

        # 压缩（传入进度回调）
        compressor.compress_ppt(upload_path, output_path, progress_callback=progress_callback)

        # 获取统计信息
        original_size = os.path.getsize(upload_path)
        compressed_size = os.path.getsize(output_path)
        reduction = original_size - compressed_size
        percent = (reduction / original_size) * 100

        # 发送完成消息
        progress_queue.put({
            'status': 'completed',
            'percent': 100,
            'filename': output_filename,
            'original_size': compressor.format_size(original_size),
            'compressed_size': compressor.format_size(compressed_size),
            'reduction': f"{percent:.1f}%",
            'download_url': f"/download/{output_filename}"
        })

    except Exception as e:
        print(f"压缩错误: {str(e)}")
        progress_queue.put({
            'status': 'error',
            'message': f'压缩失败: {str(e)}'
        })
    finally:
        # 清理上传文件
        if os.path.exists(upload_path):
            try:
                os.remove(upload_path)
            except:
                pass

@app.route('/progress/<task_id>')
def progress(task_id):
    """SSE 进度流"""
    def generate():
        if task_id not in progress_queues:
            yield f"data: {jsonify({'status': 'error', 'message': '任务不存在'}).get_data(as_text=True)}\n\n"
            return

        progress_queue = progress_queues[task_id]

        while True:
            try:
                # 等待新的进度更新
                data = progress_queue.get(timeout=30)

                import json
                yield f"data: {json.dumps(data)}\n\n"

                # 如果任务完成或出错，停止流
                if data.get('status') in ['completed', 'error']:
                    # 清理队列
                    del progress_queues[task_id]
                    break

            except queue.Empty:
                # 超时，发送心跳
                yield f"data: {json.dumps({'status': 'heartbeat'})}\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route('/download/<filename>')
def download_file(filename):
    """下载文件接口"""
    filepath = os.path.join(app.config['COMPRESSED_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': '文件不存在'}), 404

def cleanup_old_files():
    """清理旧文件（1小时前的）"""
    now = time.time()
    for folder in [app.config['UPLOAD_FOLDER'], app.config['COMPRESSED_FOLDER']]:
        if not os.path.exists(folder):
            continue
        for f in os.listdir(folder):
            f_path = os.path.join(folder, f)
            try:
                if os.stat(f_path).st_mtime < now - 3600:
                    os.remove(f_path)
            except:
                pass

def open_browser(port=5001):
    """等待服务器启动后自动打开浏览器"""
    time.sleep(1.5)  # 等待服务器启动
    url = f"http://127.0.0.1:{port}"
    print(f"\n🌐 正在打开浏览器: {url}")
    print(f"💡 如果浏览器没有自动打开，请手动访问: {url}\n")
    webbrowser.open(url)

def main():
    """主函数"""
    port = 5001

    # 启动时清理临时文件
    print("\n🧹 清理临时文件...")
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        shutil.rmtree(app.config['UPLOAD_FOLDER'])
    if os.path.exists(app.config['COMPRESSED_FOLDER']):
        shutil.rmtree(app.config['COMPRESSED_FOLDER'])

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['COMPRESSED_FOLDER'], exist_ok=True)

    print("\n" + "="*60)
    print("   🎨 PPT Compressor - macOS Sequoia Style")
    print("="*60)
    print(f"\n✅ 服务器启动中...")
    print(f"📡 地址: http://127.0.0.1:{port}")
    print(f"🚀 浏览器将自动打开\n")
    print("💡 提示:")
    print("   - 按 Ctrl+C 停止服务器")
    print("   - 服务器运行时请保持此窗口打开")
    print("="*60 + "\n")

    # 在新线程中打开浏览器
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()

    # 启动 Flask 服务器
    try:
        app.run(host='127.0.0.1', port=port, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止\n")
        sys.exit(0)

if __name__ == '__main__':
    main()
