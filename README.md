# Universal File Converter Telegram Bot 🦚✨

<div align="center">

![Bot Demo](https://via.placeholder.com/800x400/1a1a2e/16213e?text=Universal+File+Converter+Bot+🦚)

**The most comprehensive file converter bot on Telegram with stylish Unicode interface!**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg?style=for-the-badge&logo=telegram)](https://telegram.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/yourusername/universal-file-converter-bot?style=for-the-badge)](https://github.com/yourusername/universal-file-converter-bot)

</div>

## ✨ Features

- 🦋 **Real-time Progress Bars** with animated indicators  
- 🌸 **Stylish Unicode Interface** with beautiful text formatting  
- 🔥 **200+ File Format Conversions** supported  
- ⚡ **Smart Timeout Management** (60-300s based on file size)  
- 💗 **Multi-Engine Support** (FFmpeg, ImageMagick, LibreOffice, Pandoc)  
- 🧿 **Automatic Quality Optimization** for different file types  
- 🗿 **Error Recovery System** with multiple fallback methods  
- 🪔 **Production Ready** with comprehensive logging  

## 📂 Supported Formats

<div align="center">

| Category | Input Formats | Output Formats |
|----------|---------------|----------------|
| **🌸 Images** | JPG, PNG, GIF, BMP, TIFF, WEBP, HEIC, SVG, ICO | JPG, PNG, GIF, BMP, PDF, WEBP, ICO |
| **🦄 Videos** | MP4, AVI, MKV, MOV, WMV, FLV, WEBM, M4V | MP4, AVI, MKV, GIF, MP3 (audio) |
| **🍷 Audio** | MP3, WAV, FLAC, AAC, OGG, M4A, WMA, OPUS | MP3, WAV, FLAC, AAC, OGG, M4A |
| **🪔 Documents** | PDF, DOC, DOCX, TXT, RTF, ODT, HTML, MD | PDF, DOC, DOCX, TXT, RTF, HTML |
| **🧿 Spreadsheets** | XLSX, XLS, CSV, ODS, TSV | XLSX, XLS, CSV, ODS, PDF |
| **🗿 Presentations** | PPTX, PPT, ODP, PPS | PPTX, PPT, PDF, ODP |
| **🍥 Archives** | ZIP, RAR, 7Z, TAR, GZ, BZ2 | ZIP, 7Z, TAR, GZ |

</div>

## 🎮 Demo

<div align="center">

![Conversion Demo](https://via.placeholder.com/600x400/16213e/1a1a2e?text=Real-time+Progress+Demo+🦋)

*Real-time progress bars with stylish animations*

</div>

## 🚀 Quick Start

### Prerequisites

- Python 3.8+  
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))  
- System dependencies (FFmpeg, ImageMagick, etc.)  

### 1️⃣ Get Bot Token
1. Message [@BotFather](https://t.me/BotFather)  
2. Create new bot: `/newbot`  
3. Choose name and username  
4. Copy the bot token  

### 2️⃣ Clone Repository
```bash
git clone https://github.com/isyrae/Universal-File-Converter-Telegram-Bot.git
cd Universal-File-Converter-Telegram-Bot
```

### 3️⃣ Platform-Specific Setup
(See full setup guide in README – Linux, Windows, VPS, Docker)

---

## 🔧 Configuration

### Environment Variables
Create `.env` file:
```env
BOT_TOKEN=your_bot_token_here
MAX_FILE_SIZE=20971520 # 20MB in bytes
CONVERSION_TIMEOUT=300 # 5 minutes
LOG_LEVEL=INFO
```

### Custom Settings
Edit `bot.py`:
```python
BOT_TOKEN = "your_token_here"
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
DEFAULT_TIMEOUT = 120  # 2 minutes
TEMP_DIR = "/tmp/filebot"
```

---

## 📊 Usage Examples

**Images**  
`photo.jpg → photo.png`  
`image.heic → image.jpg`  
`multiple.png → combined.pdf`

**Videos**  
`movie.mp4 → movie.gif`  
`video.avi → audio.mp3`

**Documents**  
`document.pdf → document.docx`  
`text.txt → text.pdf`

---

## 🛠️ Development

```
universal-file-converter-bot/
├── bot.py
├── stylish_install.sh
├── start_stylish_bot.sh
├── monitor_stylish_bot.sh
├── requirements.txt
├── README.md
├── LICENSE
```

---

## 🔍 Monitoring

- **View Logs**: `tail -f stylish_bot.log`  
- **Check Status**: `./monitor_stylish_bot.sh`  

---

## 🆘 Troubleshooting

| Code | Description | Solution |
|------|-------------|----------|
| `CONV_ERR_001` | FFmpeg timeout | Reduce file size |
| `CONV_ERR_002` | Missing dependency | Install required tools |
| `CONV_ERR_003` | File format not supported | Check supported formats |
| `CONV_ERR_004` | Insufficient disk space | Free up space |

---

## 🔒 Security
- ✅ No permanent file storage  
- ✅ Auto-cleanup temp files  
- ✅ Input validation  
- ✅ Secure token handling  

---

## 📝 License
GPL 3.0 PUBLIC LICENSE - see the [LICENSE](LICENSE) file  

---

## 🙏 Acknowledgments
- [python-telegram-bot](https://python-telegram-bot.org/)  
- [FFmpeg](https://ffmpeg.org/)  
- [ImageMagick](https://imagemagick.org/)  
- [LibreOffice](https://libreoffice.org/)  
- [Pillow](https://pillow.readthedocs.io/)  

---

## 📞 Support
- 🐛 Bug Reports → [Issues](https://github.com/isyrae/Universal-File-Converter-Telegram-Bot/issues)  
- 💡 Feature Requests → [Discussions](https://github.com/isyrae/Universal-File-Converter-Telegram-Bot/discussions)  
- 💬 Telegram → [@intologs](https://t.me/intologs)  

---

<div align="center">

**Made with 💗 by [Rahul]**  

⭐ *Don’t forget to star the repo!* ⭐  

</div>
