import os
import zipfile
import shutil
import urllib.request

FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
FFMPEG_ZIP = "ffmpeg.zip"
EXTRACT_DIR = "ffmpeg_temp"

def download_ffmpeg():
    if os.path.exists("ffmpeg.exe") and os.path.exists("ffprobe.exe"):
        print("✅ FFmpeg is already installed!")
        return

    print(f"⬇️ Downloading FFmpeg from {FFMPEG_URL}...")
    try:
        urllib.request.urlretrieve(FFMPEG_URL, FFMPEG_ZIP)
        print("📦 Extracting...")
        
        with zipfile.ZipFile(FFMPEG_ZIP, 'r') as zip_ref:
            zip_ref.extractall(EXTRACT_DIR)
            
        # Find the bin directory
        for root, dirs, files in os.walk(EXTRACT_DIR):
            if "bin" in dirs:
                bin_dir = os.path.join(root, "bin")
                shutil.move(os.path.join(bin_dir, "ffmpeg.exe"), "ffmpeg.exe")
                shutil.move(os.path.join(bin_dir, "ffprobe.exe"), "ffprobe.exe")
                break
        
        print("🧹 Cleaning up...")
        os.remove(FFMPEG_ZIP)
        shutil.rmtree(EXTRACT_DIR)
        
        print("🎉 Success! FFmpeg installed in project root.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    download_ffmpeg()
