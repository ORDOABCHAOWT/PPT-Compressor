// macOS Sequoia Style - PPT Compressor JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');
    const uploadContent = dropZone.querySelector('.upload-content');
    const compressBtn = document.getElementById('compressBtn');
    const resultOverlay = document.getElementById('resultOverlay');
    const removeFileBtn = document.getElementById('removeFile');
    const compressAnotherBtn = document.getElementById('compressAnother');

    let selectedFile = null;

    // Click to select file
    dropZone.addEventListener('click', () => {
        if (!selectedFile) {
            fileInput.click();
        }
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // Drag and drop events
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');

        if (e.dataTransfer.files.length > 0) {
            const file = e.dataTransfer.files[0];
            if (file.name.endsWith('.ppt') || file.name.endsWith('.pptx')) {
                handleFile(file);
            } else {
                showError('请选择 PPT 或 PPTX 文件');
            }
        }
    });

    // Handle file selection
    function handleFile(file) {
        selectedFile = file;

        // Update UI
        uploadContent.style.display = 'none';
        fileInfo.style.display = 'flex';

        document.getElementById('filename').textContent = file.name;
        document.getElementById('filesize').textContent = formatSize(file.size);

        compressBtn.disabled = false;

        // Add fade-in animation
        fileInfo.classList.add('fade-in');
    }

    // Remove file
    removeFileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetUpload();
    });

    // Reset upload
    function resetUpload() {
        selectedFile = null;
        fileInput.value = '';
        uploadContent.style.display = 'block';
        fileInfo.style.display = 'none';
        compressBtn.disabled = true;
    }

    // Compress button
    compressBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        const preset = document.querySelector('input[name="preset"]:checked').value;

        // Update button state
        compressBtn.disabled = true;
        const btnText = compressBtn.querySelector('.btn-text');
        const loader = compressBtn.querySelector('.loader');

        // 显示进度条
        showProgress();

        try {
            // Create form data
            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('preset', preset);

            // Send request to start compression
            const response = await fetch('/compress', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok && result.success && result.task_id) {
                // 连接到进度流
                connectToProgress(result.task_id);
            } else {
                hideProgress();
                showError(result.error || '压缩失败，请重试');
                compressBtn.disabled = false;
            }
        } catch (error) {
            console.error('Error:', error);
            hideProgress();
            showError('网络错误，请重试');
            compressBtn.disabled = false;
        }
    });

    // 连接到进度流
    function connectToProgress(taskId) {
        const eventSource = new EventSource(`/progress/${taskId}`);

        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);

            if (data.status === 'progress') {
                updateProgress(data.percent, data.message);
            } else if (data.status === 'completed') {
                eventSource.close();
                hideProgress();
                showResult({
                    originalSize: data.original_size,
                    compressedSize: data.compressed_size,
                    reduction: data.reduction,
                    downloadUrl: data.download_url
                });
            } else if (data.status === 'error') {
                eventSource.close();
                hideProgress();
                showError(data.message || '压缩失败');
                compressBtn.disabled = false;
            }
        };

        eventSource.onerror = (error) => {
            console.error('SSE Error:', error);
            eventSource.close();
            hideProgress();
            showError('连接中断，请重试');
            compressBtn.disabled = false;
        };
    }

    // Show result overlay
    function showResult(data) {
        document.getElementById('originalSize').textContent = data.originalSize;
        document.getElementById('compressedSize').textContent = data.compressedSize;
        document.getElementById('reductionSize').textContent = data.reduction;

        const downloadLink = document.getElementById('downloadLink');
        downloadLink.href = data.downloadUrl;

        resultOverlay.classList.add('show');
    }

    // Compress another file
    compressAnotherBtn.addEventListener('click', () => {
        resultOverlay.classList.remove('show');
        resetUpload();
    });

    // 进度条相关函数
    function showProgress() {
        // 创建进度条容器（如果不存在）
        let progressContainer = document.getElementById('progressContainer');
        if (!progressContainer) {
            progressContainer = document.createElement('div');
            progressContainer.id = 'progressContainer';
            progressContainer.className = 'progress-container';
            progressContainer.innerHTML = `
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <div class="progress-text" id="progressText">正在准备...</div>
            `;
            // 插入到上传区域之后，设置面板之前
            const uploadZone = document.getElementById('dropZone');
            const settingsPanel = document.querySelector('.settings-panel');
            uploadZone.parentNode.insertBefore(progressContainer, settingsPanel);
        }
        progressContainer.classList.add('show');
        updateProgress(0, '正在准备...');
    }

    function hideProgress() {
        const progressContainer = document.getElementById('progressContainer');
        if (progressContainer) {
            progressContainer.classList.remove('show');
        }
        compressBtn.disabled = false;
    }

    function updateProgress(percent, message) {
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');

        if (progressFill) {
            progressFill.style.width = percent + '%';
        }
        if (progressText) {
            progressText.textContent = message || `${percent}%`;
        }
    }

    // Show error message
    function showError(message) {
        alert(message);
    }

    // Format file size
    function formatSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // ESC to close result overlay
        if (e.key === 'Escape' && resultOverlay.classList.contains('show')) {
            resultOverlay.classList.remove('show');
            resetUpload();
        }

        // CMD/CTRL + O to open file
        if ((e.metaKey || e.ctrlKey) && e.key === 'o') {
            e.preventDefault();
            fileInput.click();
        }
    });

    // Close result overlay when clicking outside
    resultOverlay.addEventListener('click', (e) => {
        if (e.target === resultOverlay) {
            resultOverlay.classList.remove('show');
            resetUpload();
        }
    });
});
