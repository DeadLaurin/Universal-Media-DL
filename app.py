from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import subprocess
import os
import threading
import zipfile
from io import BytesIO
import shutil

app = Flask(__name__)

# Define the download directory
DOWNLOAD_DIR = "/app/downloads"

# Ensure the download directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Global variables to track download status
download_process = None
is_downloading = False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    global download_process, is_downloading

    data = request.json
    url = data.get("url")
    options = data.get("options", "")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Reset status
    is_downloading = True

    try:
        # Build the gallery-dl command
        command = ["gallery-dl", "-o", f"base-directory={DOWNLOAD_DIR}"]
        if options:
            command.extend(options.split())
        command.append(url)

        # Run the command in a separate thread
        def run_download():
            global download_process, is_downloading
            download_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            download_process.wait()
            is_downloading = False

        threading.Thread(target=run_download).start()

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download-video", methods=["POST"])
def download_video():
    global download_process, is_downloading

    data = request.json
    url = data.get("url")
    options = data.get("options", "")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Reset status
    is_downloading = True

    try:
        # Build the yt-dlp command
        command = ["yt-dlp", "-o", f"{DOWNLOAD_DIR}/%(title)s.%(ext)s"]
        if options:
            command.extend(options.split())
        command.append(url)

        # Run the command in a separate thread
        def run_download():
            global download_process, is_downloading
            download_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            download_process.wait()
            is_downloading = False

        threading.Thread(target=run_download).start()

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/stop", methods=["POST"])
def stop():
    global download_process, is_downloading

    if download_process and download_process.poll() is None:
        download_process.terminate()
        is_downloading = False
        return jsonify({"success": True})
    else:
        return jsonify({"error": "No active download to stop"}), 400

@app.route("/list-files", methods=["GET"])
def list_files():
    try:
        def get_directory_structure(root_dir):
            structure = {}
            for item in os.listdir(root_dir):
                item_path = os.path.join(root_dir, item)
                if os.path.isdir(item_path):
                    structure[item] = get_directory_structure(item_path)
                else:
                    structure[item] = None
            return structure

        structure = get_directory_structure(DOWNLOAD_DIR)
        return jsonify(structure)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download-file/<path:filepath>", methods=["GET"])
def download_file(filepath):
    try:
        file_path = os.path.join(DOWNLOAD_DIR, filepath)
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"error": f"File not found: {file_path}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/preview-file/<path:filepath>", methods=["GET"])
def preview_file(filepath):
    try:
        file_path = os.path.join(DOWNLOAD_DIR, filepath)
        if os.path.isfile(file_path):
            return send_file(file_path)
        else:
            return jsonify({"error": f"File not found: {file_path}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download-folder/<path:folderpath>", methods=["GET"])
def download_folder(folderpath):
    try:
        folder_path = os.path.join(DOWNLOAD_DIR, folderpath)
        if not os.path.isdir(folder_path):
            return jsonify({"error": "Folder not found"}), 404

        # Create a ZIP file in memory
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, DOWNLOAD_DIR)
                    zf.write(file_path, arcname)
        memory_file.seek(0)

        # Send the ZIP file as a response
        return send_file(memory_file, download_name=f"{os.path.basename(folderpath)}.zip", as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/clear-directory", methods=["POST"])
def clear_directory():
    try:
        # Delete all files and folders in the download directory
        for item in os.listdir(DOWNLOAD_DIR):
            item_path = os.path.join(DOWNLOAD_DIR, item)
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)