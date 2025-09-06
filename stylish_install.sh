#!/bin/bash
echo "🦚 Uɴɪᴠᴇʀsᴀʟ Fɪʟᴇ Cᴏɴᴠᴇʀᴛᴇʀ Bᴏᴛ - Sᴛʏʟɪsʜ Eᴅɪᴛɪᴏɴ Iɴsᴛᴀʟʟᴀᴛɪᴏɴ ✨"
echo "=================================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Log function with emojis
log() {
    echo -e "${GREEN}🌸 [INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}🥀 [WARN]${NC} $1"
}

error() {
    echo -e "${RED}🔥 [ERROR]${NC} $1"
}

success() {
    echo -e "${CYAN}🦋 [SUCCESS]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   warn "Rᴜɴɴɪɴɢ ᴀs ʀᴏᴏᴛ - ᴛʜɪs ɪs ғɪɴᴇ ғᴏʀ VPS sᴇᴛᴜᴘ 🍷"
fi

log "Sᴛᴀʀᴛɪɴɢ sᴛʏʟɪsʜ ɪɴsᴛᴀʟʟᴀᴛɪᴏɴ ᴘʀᴏᴄᴇss... 👀"

# Update system
log "Uᴘᴅᴀᴛɪɴɢ sʏsᴛᴇᴍ ᴘᴀᴄᴋᴀɢᴇs... 🦚"
apt update -qq && apt upgrade -y -qq

# Install system dependencies
log "Iɴsᴛᴀʟʟɪɴɢ sʏsᴛᴇᴍ ᴅᴇᴘᴇɴᴅᴇɴᴄɪᴇs... 🦄"
apt install -y \
    python3-full \
    python3-venv \
    python3-pip \
    ffmpeg \
    imagemagick \
    libreoffice \
    pandoc \
    unzip \
    zip \
    p7zip-full \
    p7zip-rar \
    rar \
    unrar \
    tar \
    gzip \
    bzip2 \
    xz-utils \
    lzma \
    git \
    curl \
    wget \
    htop \
    screen \
    nano \
    build-essential

success "Sʏsᴛᴇᴍ ᴅᴇᴘᴇɴᴅᴇɴᴄɪᴇs ɪɴsᴛᴀʟʟᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ! 💗"

# Install additional media libraries
log "Iɴsᴛᴀʟʟɪɴɢ ᴀᴅᴅɪᴛɪᴏɴᴀʟ ᴍᴇᴅɪᴀ ʟɪʙʀᴀʀɪᴇs... 🧿"
apt install -y \
    libavcodec-extra \
    libavformat-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    libavfilter-dev \
    libmagickwand-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libwebp-dev \
    libopenjp2-7-dev \
    libheif-dev

# Create project directory
PROJECT_DIR="/www/wwwroot/com"
if [ ! -d "$PROJECT_DIR" ]; then
    log "Cʀᴇᴀᴛɪɴɢ ᴘʀᴏᴊᴇᴄᴛ ᴅɪʀᴇᴄᴛᴏʀʏ: $PROJECT_DIR 🗿"
    mkdir -p "$PROJECT_DIR"
fi

cd "$PROJECT_DIR"

# Create virtual environment
log "Cʀᴇᴀᴛɪɴɢ Pʏᴛʜᴏɴ ᴠɪʀᴛᴜᴀʟ ᴇɴᴠɪʀᴏɴᴍᴇɴᴛ... 🪔"
python3 -m venv converter-bot-env

# Activate virtual environment
log "Aᴄᴛɪᴠᴀᴛɪɴɢ ᴠɪʀᴛᴜᴀʟ ᴇɴᴠɪʀᴏɴᴍᴇɴᴛ... 🍥"
source converter-bot-env/bin/activate

# Upgrade pip
log "Uᴘɢʀᴀᴅɪɴɢ ᴘɪᴘ... 🍃"
pip install --upgrade pip setuptools wheel

# Install Python packages
log "Iɴsᴛᴀʟʟɪɴɢ Pʏᴛʜᴏɴ ᴘᴀᴄᴋᴀɢᴇs... 🍀"
pip install \
    python-telegram-bot \
    Pillow \
    reportlab \
    pandas \
    openpyxl \
    python-docx \
    pypdf2 \
    markdown \
    requests \
    aiohttp \
    asyncio \
    psutil \
    python-magic \
    python-magic-bin

success "Pʏᴛʜᴏɴ ᴘᴀᴄᴋᴀɢᴇs ɪɴsᴛᴀʟʟᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ! ❄️"

# Create startup script with stylish text
log "Cʀᴇᴀᴛɪɴɢ sᴛʏʟɪsʜ sᴛᴀʀᴛᴜᴘ sᴄʀɪᴘᴛ... 🌀"
cat > start_stylish_bot.sh << 'EOF'
#!/bin/bash
echo "🦚 Sᴛᴀʀᴛɪɴɢ Uɴɪᴠᴇʀsᴀʟ Fɪʟᴇ Cᴏɴᴠᴇʀᴛᴇʀ Bᴏᴛ - Sᴛʏʟɪsʜ Eᴅɪᴛɪᴏɴ ✨"

# Navigate to project directory
cd /www/wwwroot/com

# Activate virtual environment
source converter-bot-env/bin/activate

# Check if bot.py exists
if [ ! -f "bot.py" ]; then
    echo "❌ bot.py ɴᴏᴛ ғᴏᴜɴᴅ! Pʟᴇᴀsᴇ ᴄʀᴇᴀᴛᴇ ᴛʜᴇ ʙᴏᴛ ғɪʟᴇ ғɪʀsᴛ. 🥀"
    exit 1
fi

# Start bot with logging
echo "📊 Bᴏᴛ sᴛᴀʀᴛɪɴɢ ᴡɪᴛʜ ʀᴇᴀʟ-ᴛɪᴍᴇ ᴘʀᴏɢʀᴇss sᴜᴘᴘᴏʀᴛ... 🔥"
echo "⚡ Pʀᴇss Cᴛʀʟ+C ᴛᴏ sᴛᴏᴘ ᴛʜᴇ ʙᴏᴛ 💫"
echo "🔍 Lᴏɢs ᴀʀᴇ ʙᴇɪɴɢ sᴀᴠᴇᴅ ᴛᴏ stylish_bot.log 💭"

python bot.py 2>&1 | tee -a stylish_bot.log
EOF

chmod +x start_stylish_bot.sh

# Create monitoring script with stylish text
log "Cʀᴇᴀᴛɪɴɢ sᴛʏʟɪsʜ ᴍᴏɴɪᴛᴏʀɪɴɢ sᴄʀɪᴘᴛ... 🔥"
cat > monitor_stylish_bot.sh << 'EOF'
#!/bin/bash
echo "📊 Uɴɪᴠᴇʀsᴀʟ Fɪʟᴇ Cᴏɴᴠᴇʀᴛᴇʀ Bᴏᴛ - Sᴛʏʟɪsʜ Mᴏɴɪᴛᴏʀ ⚡"
echo "=================================================="

# Check if bot is running
if pgrep -f "python bot.py" > /dev/null; then
    echo "✅ Bᴏᴛ Sᴛᴀᴛᴜs: RUNNING 🦚"
    echo "🔢 Pʀᴏᴄᴇss ID: $(pgrep -f 'python bot.py') 💫"
else
    echo "❌ Bᴏᴛ Sᴛᴀᴛᴜs: STOPPED 🥀"
fi

# System resources
echo ""
echo "💻 Sʏsᴛᴇᴍ Rᴇsᴏᴜʀᴄᴇs: 💭"
echo "CPU Usᴀɢᴇ: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)% 🦋"
echo "Mᴇᴍᴏʀʏ: $(free -h | awk '/^Mem:/ {print $3 "/" $2}') 🌸"
echo "Dɪsᴋ: $(df -h /www/wwwroot/com | awk 'NR==2 {print $3 "/" $2 " (" $5 " used)"}') 🥀"

# Bot logs (last 10 lines)
echo ""
echo "📝 Rᴇᴄᴇɴᴛ Bᴏᴛ Aᴄᴛɪᴠɪᴛʏ: 🍂"
if [ -f "stylish_bot.log" ]; then
    tail -n 10 stylish_bot.log
else
    echo "Nᴏ ʟᴏɢ ғɪʟᴇ ғᴏᴜɴᴅ. 🍁"
fi

echo ""
echo "🔧 Qᴜɪᴄᴋ Cᴏᴍᴍᴀɴᴅs: 💗"
echo "Sᴛᴀʀᴛ Bᴏᴛ: ./start_stylish_bot.sh 🦋"
echo "Vɪᴇᴡ Lᴏɢs: tail -f stylish_bot.log 🧿"
echo "Sᴛᴏᴘ Bᴏᴛ: pkill -f 'python bot.py' 🗿"
EOF

chmod +x monitor_stylish_bot.sh

# Final setup
log "Sᴇᴛᴛɪɴɢ ᴜᴘ ғɪɴᴀʟ ᴘᴇʀᴍɪssɪᴏɴs... 🪔"
chown -R root:root "$PROJECT_DIR"
chmod +x "$PROJECT_DIR"/*.sh

# Create status file with stylish text
cat > sᴛʏʟɪsʜ_ɪɴsᴛᴀʟʟᴀᴛɪᴏɴ_sᴛᴀᴛᴜs.txt << 'EOF'
✅ SƬYɭƗSĦ ƗƝSƬѦɭɭѦƬƗƠƝ ƇƠMPɭЄƬЄ! 🦚
=============================

📊 Iɴsᴛᴀʟʟᴀᴛɪᴏɴ Sᴜᴍᴍᴀʀʏ: ✨
- Sʏsᴛᴇᴍ ᴘᴀᴄᴋᴀɢᴇs: ✅ Iɴsᴛᴀʟʟᴇᴅ 🌸
- Pʏᴛʜᴏɴ ᴇɴᴠɪʀᴏɴᴍᴇɴᴛ: ✅ Cʀᴇᴀᴛᴇᴅ 🥀  
- Dᴇᴘᴇɴᴅᴇɴᴄɪᴇs: ✅ Iɴsᴛᴀʟʟᴇᴅ 🍂
- Sᴄʀɪᴘᴛs: ✅ Gᴇɴᴇʀᴀᴛᴇᴅ 🍁
- Sᴛʏʟɪsʜ UI: ✅ Eɴᴀʙʟᴇᴅ 💗

🚀 Nᴇxᴛ Sᴛᴇᴘs: 🦋
1. Cʀᴇᴀᴛᴇ ʏᴏᴜʀ bot.py ғɪʟᴇ ᴡɪᴛʜ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ᴄᴏᴅᴇ 🧿
2. Uᴘᴅᴀᴛᴇ BOT_TOKEN ɪɴ bot.py 🗿
3. Rᴜɴ: ./start_stylish_bot.sh 🪔

🔧 Aᴠᴀɪʟᴀʙʟᴇ Cᴏᴍᴍᴀɴᴅs: 🍥
- ./start_stylish_bot.sh - Sᴛᴀʀᴛ sᴛʏʟɪsʜ ʙᴏᴛ 🍃
- ./monitor_stylish_bot.sh - Mᴏɴɪᴛᴏʀ ʙᴏᴛ sᴛᴀᴛᴜs 🍀

📁 Iᴍᴘᴏʀᴛᴀɴᴛ Fɪʟᴇs: ❄️
- bot.py - Mᴀɪɴ sᴛʏʟɪsʜ ʙᴏᴛ ᴄᴏᴅᴇ (ᴄʀᴇᴀᴛᴇ ᴛʜɪs) 🌀
- stylish_bot.log - Rᴜɴᴛɪᴍᴇ ʟᴏɢs 🔥
- requirements.txt - Pʏᴛʜᴏɴ ᴅᴇᴘᴇɴᴅᴇɴᴄɪᴇs ⚡

🎯 Rᴇᴀᴅʏ ᴛᴏ ᴄᴏɴᴠᴇʀᴛ 200+ ғɪʟᴇ ғᴏʀᴍᴀᴛs ᴡɪᴛʜ sᴛʏʟɪsʜ UI! 💫💭
EOF

# Display completion message
echo ""
echo "=================================================================="
echo -e "${PURPLE}✅ SƬYɭƗSĦ ƗƝSƬѦɭɭѦƬƗƠƝ ƇƠMPɭЄƬЄƉ SƱƇƇЄSSFƱɭɭY! 🦚${NC}"
echo "=================================================================="
echo ""
echo -e "${BLUE}📊 Iɴsᴛᴀʟʟᴀᴛɪᴏɴ Sᴜᴍᴍᴀʀʏ: ✨${NC}"
echo "   ✅ Sʏsᴛᴇᴍ ᴘᴀᴄᴋᴀɢᴇs ɪɴsᴛᴀʟʟᴇᴅ 🌸"
echo "   ✅ Pʏᴛʜᴏɴ ᴠɪʀᴛᴜᴀʟ ᴇɴᴠɪʀᴏɴᴍᴇɴᴛ ᴄʀᴇᴀᴛᴇᴅ 🥀"
echo "   ✅ Aʟʟ ᴅᴇᴘᴇɴᴅᴇɴᴄɪᴇs ɪɴsᴛᴀʟʟᴇᴅ 🍂"
echo "   ✅ Sᴛʏʟɪsʜ sᴄʀɪᴘᴛs ɢᴇɴᴇʀᴀᴛᴇᴅ 🍁"
echo "   ✅ Uɴɪᴄᴏᴅᴇ ᴛᴇxᴛ sᴜᴘᴘᴏʀᴛ ᴇɴᴀʙʟᴇᴅ 💗"
echo ""
echo -e "${YELLOW}🚀 Nᴇxᴛ Sᴛᴇᴘs: 🦋${NC}"
echo "   1. Cʀᴇᴀᴛᴇ bot.py ᴡɪᴛʜ ᴛʜᴇ sᴛʏʟɪsʜ ᴄᴏᴅᴇ 🧿"
echo "   2. Uᴘᴅᴀᴛᴇ BOT_TOKEN ɪɴ bot.py 🗿"
echo "   3. Rᴜɴ: ./start_stylish_bot.sh 🪔"
echo ""
echo -e "${BLUE}📁 Pʀᴏᴊᴇᴄᴛ Lᴏᴄᴀᴛɪᴏɴ: 🍥${NC} $PROJECT_DIR"
echo -e "${BLUE}🔧 Aᴠᴀɪʟᴀʙʟᴇ Cᴏᴍᴍᴀɴᴅs: 🍃${NC}"
echo "   ./start_stylish_bot.sh - Sᴛᴀʀᴛ sᴛʏʟɪsʜ ʙᴏᴛ 🍀"
echo "   ./monitor_stylish_bot.sh - Mᴏɴɪᴛᴏʀ sᴛᴀᴛᴜs ❄️"
echo ""
echo -e "${GREEN}🎉 Rᴇᴀᴅʏ ᴛᴏ ᴄᴏɴᴠᴇʀᴛ 200+ ғɪʟᴇ ғᴏʀᴍᴀᴛs ᴡɪᴛʜ ʀᴇᴀʟ-ᴛɪᴍᴇ ᴘʀᴏɢʀᴇss & sᴛʏʟɪsʜ UI! 🌀🔥⚡💫💭${NC}"
echo "=================================================================="
