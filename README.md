# 🌟 Universal Downloader

Universal Downloader is a **batch downloading tool** primarily for **Pinterest** but also supports **YouTube downloads** via [`yt-dlp`](https://github.com/yt-dlp/yt-dlp). It provides a **web-based interface** for easy management of downloads and utilizes [`GalleryDL`](https://github.com/mikf/gallery-dl) for batch image downloads.

---

## 🎯 Features
✅ **Download** images and videos from Pinterest in bulk.  
✅ **Download** YouTube videos using [`yt-dlp`](https://github.com/yt-dlp/yt-dlp).  
✅ **Web-based UI** for user-friendly downloads.  
✅ Supports **additional options** for customization.  
✅ **File explorer** for managing downloaded content.  
✅ **Dockerized** for easy deployment.  

---

## 🚀 Installation
### 🛠 Prerequisites
- 🐳 [Docker](https://docs.docker.com/get-docker/)

### 📌 Steps
1. Clone this repository:
   ```sh
   git clone https://github.com/DeadLaurin/universal-downloader.git
   cd universal-downloader
   ```
2. Build and start the container:
   ```sh
   docker build -t universal-downloader .
   docker run -d -p 5000:5000 -v /path/to/your/downloads:/app/downloads --name universal-downloader
   ```
3. Open your browser and visit:
   ```sh
   http://localhost:5000
   ```

---

## 🎮 Usage
1. **Enter** the URL of a Pinterest board, search, pin or YouTube video.
2. **(Optional)** Add options like `--range 1-10` for Pinterest or `-f best` for YouTube.
3. Click **▶ Start Download** to begin.
4. **Monitor** the status and manage files in the **📂 Downloaded Files** section.
5. Use **⏹ Stop Download** to cancel an active download.
6. Use **🗑 Clear Directory** to remove all downloaded files.

---

## 🛠 API Endpoints
📌 `POST /download` – Download from **Pinterest** using [`GalleryDL`](https://github.com/mikf/gallery-dl).  
📌 `POST /download-video` – Download from **YouTube** using [`yt-dlp`](https://github.com/yt-dlp/yt-dlp).  
📌 `POST /stop` – Stop an active download.  
📌 `GET /list-files` – List downloaded files.  
📌 `GET /download-file/<filepath>` – Download a specific file.  
📌 `GET /download-folder/<folderpath>` – Download a folder as a ZIP.  
📌 `POST /clear-directory` – Clear all downloads.  

---

## 🤝 Contributing
🎉 Contributions are **welcome**! Feel free to **submit pull requests** or report issues.  

---

## 📜 License
This project is **licensed under the MIT License**. 📝

