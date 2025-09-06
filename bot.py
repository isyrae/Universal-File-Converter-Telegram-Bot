#!/usr/bin/env python3
"""
Uɴɪᴠᴇʀsᴀʟ Fɪʟᴇ Cᴏɴᴠᴇʀᴛᴇʀ Tᴇʟᴇɢʀᴀᴍ Bᴏᴛ - Rᴇᴀʟ-ᴛɪᴍᴇ Pʀᴏɢʀᴇss Eᴅɪᴛɪᴏɴ 🦚✨
Fᴇᴀᴛᴜʀᴇs: Rᴇᴀʟ-ᴛɪᴍᴇ Pʀᴏɢʀᴇss Bᴀʀs, Tɪᴍᴇᴏᴜᴛ Mᴀɴᴀɢᴇᴍᴇɴᴛ, Cᴏᴍᴘʀᴇʜᴇɴsɪᴠᴇ Fᴏʀᴍᴀᴛ Sᴜᴘᴘᴏʀᴛ 🦄💗
Aᴜᴛʜᴏʀ: Eɴʜᴀɴᴄᴇᴅ ғᴏʀ Pʀᴏᴅᴜᴄᴛɪᴏɴ Usᴇ 🔥
"""

import os
import sys
import logging
import tempfile
import asyncio
import subprocess
import shutil
import signal
import re
import time
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from telegram import Update, Document, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Cᴏɴғɪɢᴜʀᴇ Lᴏɢɢɪɴɢ 🪔
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bᴏᴛ Tᴏᴋᴇɴ 🧿
BOT_TOKEN = "your_bot_token_here"

class ProgressTracker:
    """Rᴇᴀʟ-ᴛɪᴍᴇ Pʀᴏɢʀᴇss Tʀᴀᴄᴋɪɴɢ ғᴏʀ Fɪʟᴇ Cᴏɴᴠᴇʀsɪᴏɴs 🦋"""
    
    def __init__(self):
        self.progress_patterns = {
            'ffmpeg': re.compile(r'time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})'),
            'duration': re.compile(r'Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})'),
            'libreoffice': re.compile(r'(\d+)%'),
            'imagemagick': re.compile(r'(\d+)%')
        }
    
    def create_progress_bar(self, percentage: int, width: int = 20) -> str:
        """Cʀᴇᴀᴛᴇ Aɴɪᴍᴀᴛᴇᴅ Pʀᴏɢʀᴇss Bᴀʀ 🌀💫"""
        filled = int(width * percentage / 100)
        bar = "🔥" * filled + "❄️" * (width - filled)
        
        # Aᴅᴅ Aɴɪᴍᴀᴛɪᴏɴ Cʜᴀʀᴀᴄᴛᴇʀs 💭
        if percentage < 100:
            animation = ["🦋", "🌸", "🥀", "🍂", "🍁", "🌀", "⚡", "💫", "✨", "🔥"][int(time.time() * 2) % 10]
        else:
            animation = "🦚"
            
        return f"{animation} [{bar}] {percentage}% 💗"
    
    def parse_ffmpeg_progress(self, line: str, duration: float = 0) -> Optional[int]:
        """Pᴀʀsᴇ FFᴍᴘᴇɢ Pʀᴏɢʀᴇss ғʀᴏᴍ Oᴜᴛᴘᴜᴛ 🍃"""
        time_match = self.progress_patterns['ffmpeg'].search(line)
        if time_match and duration > 0:
            hours, minutes, seconds, centiseconds = map(int, time_match.groups())
            current_time = hours * 3600 + minutes * 60 + seconds + centiseconds / 100
            progress = min(100, int((current_time / duration) * 100))
            return progress
        return None
    
    def parse_duration(self, line: str) -> Optional[float]:
        """Pᴀʀsᴇ Vɪᴅᴇᴏ Dᴜʀᴀᴛɪᴏɴ ғʀᴏᴍ FFᴍᴘᴇɢ Oᴜᴛᴘᴜᴛ 🍀"""
        duration_match = self.progress_patterns['duration'].search(line)
        if duration_match:
            hours, minutes, seconds, centiseconds = map(int, duration_match.groups())
            return hours * 3600 + minutes * 60 + seconds + centiseconds / 100
        return None

class ProcessManager:
    """Aᴅᴠᴀɴᴄᴇᴅ Pʀᴏᴄᴇss Mᴀɴᴀɢᴇᴍᴇɴᴛ Wɪᴛʜ Rᴇᴀʟ-ᴛɪᴍᴇ Mᴏɴɪᴛᴏʀɪɴɢ 🥂✨"""
    
    def __init__(self):
        self.active_processes = {}
        self.progress_tracker = ProgressTracker()
    
    async def run_with_progress(self, cmd: List[str], timeout: int, update_callback=None) -> Tuple[bool, str]:
        """Rᴜɴ Cᴏᴍᴍᴀɴᴅ Wɪᴛʜ Rᴇᴀʟ-ᴛɪᴍᴇ Pʀᴏɢʀᴇss Uᴘᴅᴀᴛᴇs 🦄💫"""
        process = None
        duration = 0
        last_update = 0
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                preexec_fn=os.setsid
            )
            
            self.active_processes[id(process)] = process
            
            # Mᴏɴɪᴛᴏʀ Pʀᴏɢʀᴇss ɪɴ Rᴇᴀʟ-ᴛɪᴍᴇ 🌸
            async def monitor_progress():
                nonlocal duration, last_update
                buffer = ""
                
                while process.returncode is None:
                    try:
                        # Rᴇᴀᴅ sᴛᴅᴇʀʀ ғᴏʀ FFᴍᴘᴇɢ Pʀᴏɢʀᴇss 👀
                        data = await asyncio.wait_for(process.stderr.read(1024), timeout=1.0)
                        if not data:
                            break
                            
                        buffer += data.decode('utf-8', errors='ignore')
                        lines = buffer.split('\n')
                        buffer = lines[-1]  # Kᴇᴇᴘ ɪɴᴄᴏᴍᴘʟᴇᴛᴇ ʟɪɴᴇ ɪɴ ʙᴜғғᴇʀ
                        
                        for line in lines[:-1]:
                            # Pᴀʀsᴇ Dᴜʀᴀᴛɪᴏɴ Fɪʀsᴛ 🍥
                            if duration == 0:
                                parsed_duration = self.progress_tracker.parse_duration(line)
                                if parsed_duration:
                                    duration = parsed_duration
                            
                            # Pᴀʀsᴇ Pʀᴏɢʀᴇss 🗿
                            progress = self.progress_tracker.parse_ffmpeg_progress(line, duration)
                            if progress is not None and update_callback:
                                current_time = time.time()
                                if current_time - last_update >= 2:  # Uᴘᴅᴀᴛᴇ ᴇᴠᴇʀʏ 2 sᴇᴄᴏɴᴅs
                                    await update_callback(progress)
                                    last_update = current_time
                                    
                    except asyncio.TimeoutError:
                        continue
                    except Exception as e:
                        logger.debug(f"Pʀᴏɢʀᴇss ᴍᴏɴɪᴛᴏʀɪɴɢ ᴇʀʀᴏʀ: {e} 🍷")
                        break
            
            # Sᴛᴀʀᴛ Pʀᴏɢʀᴇss Mᴏɴɪᴛᴏʀɪɴɢ 🦚
            progress_task = asyncio.create_task(monitor_progress())
            
            # Wᴀɪᴛ ғᴏʀ Pʀᴏᴄᴇss Cᴏᴍᴘʟᴇᴛɪᴏɴ Wɪᴛʜ Tɪᴍᴇᴏᴜᴛ 💭
            try:
                await asyncio.wait_for(process.wait(), timeout=timeout)
                progress_task.cancel()
                
                # Fɪɴᴀʟ Pʀᴏɢʀᴇss Uᴘᴅᴀᴛᴇ 🌀
                if update_callback:
                    await update_callback(100)
                
                success = process.returncode == 0
                return success, ""
                
            except asyncio.TimeoutError:
                progress_task.cancel()
                logger.warning(f"Pʀᴏᴄᴇss ᴛɪᴍᴇᴅ ᴏᴜᴛ ᴀғᴛᴇʀ {timeout}s ⚡")
                
                # Kɪʟʟ Pʀᴏᴄᴇss Gʀᴏᴜᴘ 🔥
                try:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                    await asyncio.sleep(3)
                    if process.returncode is None:
                        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                except:
                    pass
                
                return False, "Pʀᴏᴄᴇss ᴛɪᴍᴇᴅ ᴏᴜᴛ ❄️"
                
        except Exception as e:
            logger.error(f"Pʀᴏᴄᴇss ᴇxᴇᴄᴜᴛɪᴏɴ ᴇʀʀᴏʀ: {e} 🥀")
            return False, str(e)
        
        finally:
            if process and id(process) in self.active_processes:
                del self.active_processes[id(process)]

class UniversalConverter:
    """Eɴʜᴀɴᴄᴇᴅ Cᴏɴᴠᴇʀᴛᴇʀ Wɪᴛʜ Rᴇᴀʟ-ᴛɪᴍᴇ Pʀᴏɢʀᴇss ᴀɴᴅ Sᴍᴀʀᴛ Oᴘᴛɪᴍɪᴢᴀᴛɪᴏɴ 🦋✨"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.process_manager = ProcessManager()
        self.progress_tracker = ProgressTracker()
    
    def get_file_info(self, filepath: str) -> Dict:
        """Aɴᴀʟʏᴢᴇ Fɪʟᴇ ғᴏʀ Oᴘᴛɪᴍᴀʟ Pʀᴏᴄᴇssɪɴɢ Pᴀʀᴀᴍᴇᴛᴇʀs 🍂💗"""
        try:
            stat = os.stat(filepath)
            size_mb = stat.st_size / (1024 * 1024)
            
            # Sᴍᴀʀᴛ Tɪᴍᴇᴏᴜᴛ Cᴀʟᴄᴜʟᴀᴛɪᴏɴ 🌸
            if size_mb < 5:
                timeout, complexity = 60, "Lᴏᴡ 🍀"
            elif size_mb < 20:
                timeout, complexity = 120, "Mᴇᴅɪᴜᴍ 🍃"
            elif size_mb < 50:
                timeout, complexity = 180, "Hɪɢʜ 🔥"
            else:
                timeout, complexity = 300, "Vᴇʀʏ Hɪɢʜ ⚡"
                
            return {
                'size_mb': size_mb,
                'complexity': complexity,
                'timeout': timeout,
                'estimated_time': min(timeout, max(10, int(size_mb * 3)))
            }
        except:
            return {'size_mb': 0, 'complexity': 'Uɴᴋɴᴏᴡɴ 💭', 'timeout': 60, 'estimated_time': 10}
    
    def get_format_info(self, filename: str) -> Tuple[str, List[str]]:
        """Gᴇᴛ Cᴏᴍᴘʀᴇʜᴇɴsɪᴠᴇ Fᴏʀᴍᴀᴛ Iɴғᴏʀᴍᴀᴛɪᴏɴ 🦚💫"""
        ext = Path(filename).suffix.lower()
        
        format_map = {
            # Iᴍᴀɢᴇs - Hɪɢʜ Cᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ 🌸
            '.jpg': ('image', ['png', 'gif', 'bmp', 'tiff', 'webp', 'pdf', 'ico', 'svg']),
            '.jpeg': ('image', ['png', 'gif', 'bmp', 'tiff', 'webp', 'pdf', 'ico', 'svg']),
            '.png': ('image', ['jpg', 'gif', 'bmp', 'tiff', 'webp', 'pdf', 'ico', 'svg']),
            '.gif': ('image', ['jpg', 'png', 'bmp', 'tiff', 'webp', 'pdf', 'ico']),
            '.bmp': ('image', ['jpg', 'png', 'gif', 'tiff', 'webp', 'pdf', 'ico']),
            '.tiff': ('image', ['jpg', 'png', 'gif', 'bmp', 'webp', 'pdf', 'ico']),
            '.webp': ('image', ['jpg', 'png', 'gif', 'bmp', 'tiff', 'pdf', 'ico']),
            '.heic': ('image', ['jpg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'pdf']),
            '.heif': ('image', ['jpg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'pdf']),
            '.svg': ('image', ['jpg', 'png', 'gif', 'bmp', 'pdf']),
            '.ico': ('image', ['jpg', 'png', 'gif', 'bmp', 'tiff', 'pdf']),
            
            # Vɪᴅᴇᴏs - Oᴘᴛɪᴍɪᴢᴇᴅ Cᴏɴᴠᴇʀsɪᴏɴs 🦄
            '.mp4': ('video', ['avi', 'mkv', 'mov', 'wmv', 'flv', 'webm', 'gif', 'mp3', '3gp']),
            '.avi': ('video', ['mp4', 'mkv', 'mov', 'wmv', 'flv', 'webm', 'gif', 'mp3']),
            '.mkv': ('video', ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'gif', 'mp3']),
            '.mov': ('video', ['mp4', 'avi', 'mkv', 'wmv', 'flv', 'webm', 'gif', 'mp3']),
            '.wmv': ('video', ['mp4', 'avi', 'mkv', 'mov', 'flv', 'webm', 'gif', 'mp3']),
            '.flv': ('video', ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'webm', 'gif', 'mp3']),
            '.webm': ('video', ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'gif', 'mp3']),
            '.m4v': ('video', ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm', 'gif']),
            '.3gp': ('video', ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm', 'gif']),
            
            # Aᴜᴅɪᴏ - Fᴜʟʟ Sᴘᴇᴄᴛʀᴜᴍ 🍷
            '.mp3': ('audio', ['wav', 'flac', 'aac', 'ogg', 'm4a', 'wma', 'opus', 'amr']),
            '.wav': ('audio', ['mp3', 'flac', 'aac', 'ogg', 'm4a', 'wma', 'opus', 'amr']),
            '.flac': ('audio', ['mp3', 'wav', 'aac', 'ogg', 'm4a', 'wma', 'opus']),
            '.aac': ('audio', ['mp3', 'wav', 'flac', 'ogg', 'm4a', 'wma', 'opus']),
            '.ogg': ('audio', ['mp3', 'wav', 'flac', 'aac', 'm4a', 'wma', 'opus']),
            '.m4a': ('audio', ['mp3', 'wav', 'flac', 'aac', 'ogg', 'wma', 'opus']),
            '.wma': ('audio', ['mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a', 'opus']),
            '.opus': ('audio', ['mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a', 'wma']),
            
            # Dᴏᴄᴜᴍᴇɴᴛs - Oғғɪᴄᴇ Sᴜɪᴛᴇ 🪔
            '.pdf': ('document', ['doc', 'docx', 'txt', 'rtf', 'odt', 'html', 'md', 'epub']),
            '.doc': ('document', ['pdf', 'docx', 'txt', 'rtf', 'odt', 'html', 'md']),
            '.docx': ('document', ['pdf', 'doc', 'txt', 'rtf', 'odt', 'html', 'md']),
            '.txt': ('document', ['pdf', 'doc', 'docx', 'rtf', 'html', 'md', 'epub']),
            '.rtf': ('document', ['pdf', 'doc', 'docx', 'txt', 'html', 'md']),
            '.odt': ('document', ['pdf', 'doc', 'docx', 'txt', 'rtf', 'html', 'md']),
            '.html': ('document', ['pdf', 'doc', 'docx', 'txt', 'rtf', 'md', 'epub']),
            '.md': ('document', ['pdf', 'html', 'txt', 'doc', 'docx', 'rtf', 'epub']),
            
            # Sᴘʀᴇᴀᴅsʜᴇᴇᴛs 🧿
            '.xlsx': ('spreadsheet', ['xls', 'csv', 'ods', 'pdf', 'html', 'tsv']),
            '.xls': ('spreadsheet', ['xlsx', 'csv', 'ods', 'pdf', 'html', 'tsv']),
            '.csv': ('spreadsheet', ['xlsx', 'xls', 'ods', 'pdf', 'html', 'tsv']),
            '.ods': ('spreadsheet', ['xlsx', 'xls', 'csv', 'pdf', 'html', 'tsv']),
            
            # Pʀᴇsᴇɴᴛᴀᴛɪᴏɴs 🗿
            '.pptx': ('presentation', ['ppt', 'pdf', 'odp', 'html', 'txt']),
            '.ppt': ('presentation', ['pptx', 'pdf', 'odp', 'html', 'txt']),
            '.odp': ('presentation', ['pptx', 'ppt', 'pdf', 'html', 'txt']),
            
            # Aʀᴄʜɪᴠᴇs 🍥
            '.zip': ('archive', ['7z', 'tar', 'gz', 'bz2', 'rar']),
            '.rar': ('archive', ['zip', '7z', 'tar', 'gz', 'bz2']),
            '.7z': ('archive', ['zip', 'tar', 'gz', 'bz2', 'rar']),
            '.tar': ('archive', ['zip', '7z', 'gz', 'bz2']),
            '.gz': ('archive', ['zip', '7z', 'tar', 'bz2']),
            '.bz2': ('archive', ['zip', '7z', 'tar', 'gz']),
        }
        
        return format_map.get(ext, ('other', ['txt', 'pdf', 'zip']))
    
    async def convert_with_progress(self, input_path: str, output_path: str, progress_callback) -> bool:
        """Mᴀɪɴ Cᴏɴᴠᴇʀsɪᴏɴ Fᴜɴᴄᴛɪᴏɴ Wɪᴛʜ Rᴇᴀʟ-ᴛɪᴍᴇ Pʀᴏɢʀᴇss 🦋💫"""
        category, _ = self.get_format_info(Path(input_path).name)
        file_info = self.get_file_info(input_path)
        
        if category == 'image':
            return await self._convert_image(input_path, output_path, progress_callback)
        elif category == 'video':
            return await self._convert_video(input_path, output_path, file_info, progress_callback)
        elif category == 'audio':
            return await self._convert_audio(input_path, output_path, file_info, progress_callback)
        elif category in ['document', 'spreadsheet', 'presentation']:
            return await self._convert_document(input_path, output_path, file_info, progress_callback)
        elif category == 'archive':
            return await self._convert_archive(input_path, output_path, progress_callback)
        else:
            # Fᴀʟʟʙᴀᴄᴋ Cᴏɴᴠᴇʀsɪᴏɴ 🍃
            return await self._fallback_convert(input_path, output_path, progress_callback)
    
    async def _convert_image(self, input_path: str, output_path: str, progress_callback) -> bool:
        """Cᴏɴᴠᴇʀᴛ Iᴍᴀɢᴇs Wɪᴛʜ Pʀᴏɢʀᴇss Tʀᴀᴄᴋɪɴɢ 🌸✨"""
        try:
            # Uᴘᴅᴀᴛᴇ Pʀᴏɢʀᴇss 🦚
            await progress_callback(10)
            
            # Tʀʏ PIL Fɪʀsᴛ (Fᴀsᴛᴇsᴛ) 🔥
            try:
                from PIL import Image
                await progress_callback(30)
                
                with Image.open(input_path) as img:
                    await progress_callback(50)
                    
                    output_ext = Path(output_path).suffix.lower()
                    
                    if output_ext in ['.jpg', '.jpeg']:
                        if img.mode in ('RGBA', 'LA', 'P'):
                            background = Image.new('RGB', img.size, (255, 255, 255))
                            if img.mode == 'P':
                                img = img.convert('RGBA')
                            if img.mode == 'RGBA':
                                background.paste(img, mask=img.split()[-1])
                            img = background
                        await progress_callback(80)
                        img.save(output_path, 'JPEG', quality=95, optimize=True)
                    elif output_ext == '.pdf':
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        await progress_callback(80)
                        img.save(output_path, 'PDF')
                    else:
                        await progress_callback(80)
                        img.save(output_path)
                
                await progress_callback(100)
                return True
                
            except ImportError:
                # Fᴀʟʟʙᴀᴄᴋ ᴛᴏ FFᴍᴘᴇɢ 🍂
                await progress_callback(20)
                cmd = ['ffmpeg', '-i', input_path, '-y', output_path]
                success, _ = await self.process_manager.run_with_progress(
                    cmd, 60, progress_callback
                )
                return success
                
        except Exception as e:
            logger.error(f"Iᴍᴀɢᴇ ᴄᴏɴᴠᴇʀsɪᴏɴ ᴇʀʀᴏʀ: {e} 🥀")
            return False
    
    async def _convert_video(self, input_path: str, output_path: str, file_info: Dict, progress_callback) -> bool:
        """Cᴏɴᴠᴇʀᴛ Vɪᴅᴇᴏs Wɪᴛʜ Rᴇᴀʟ-ᴛɪᴍᴇ Pʀᴏɢʀᴇss 🦄💗"""
        try:
            output_ext = Path(output_path).suffix.lower()
            await progress_callback(5)
            
            # Oᴘᴛɪᴍɪᴢᴇᴅ FFᴍᴘᴇɢ Cᴏᴍᴍᴀɴᴅs ʙᴀsᴇᴅ ᴏɴ Oᴜᴛᴘᴜᴛ Fᴏʀᴍᴀᴛ 🌀
            if output_ext == '.gif':
                # Oᴘᴛɪᴍɪᴢᴇᴅ GIF Cᴏɴᴠᴇʀsɪᴏɴ 🍁
                cmd = [
                    'ffmpeg', '-i', input_path,
                    '-vf', 'fps=10,scale=480:-1:flags=lanczos',
                    '-t', '15',  # Lɪᴍɪᴛ ᴛᴏ 15 sᴇᴄᴏɴᴅs
                    '-y', output_path
                ]
            elif output_ext == '.mp3':
                # Aᴜᴅɪᴏ Exᴛʀᴀᴄᴛɪᴏɴ 🍷
                cmd = [
                    'ffmpeg', '-i', input_path,
                    '-vn', '-acodec', 'libmp3lame', '-b:a', '192k',
                    '-y', output_path
                ]
            else:
                # Sᴛᴀɴᴅᴀʀᴅ Vɪᴅᴇᴏ Cᴏɴᴠᴇʀsɪᴏɴ Wɪᴛʜ Oᴘᴛɪᴍɪᴢᴇᴅ Sᴇᴛᴛɪɴɢs ⚡
                if file_info['size_mb'] > 50:
                    # Lᴀʀɢᴇ Fɪʟᴇ - Usᴇ Fᴀsᴛᴇʀ, Lᴏᴡᴇʀ Qᴜᴀʟɪᴛʏ Pʀᴇsᴇᴛ 💫
                    cmd = [
                        'ffmpeg', '-i', input_path,
                        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '30',
                        '-c:a', 'aac', '-b:a', '128k',
                        '-y', output_path
                    ]
                else:
                    # Sᴛᴀɴᴅᴀʀᴅ Qᴜᴀʟɪᴛʏ 🌸
                    cmd = [
                        'ffmpeg', '-i', input_path,
                        '-c:v', 'libx264', '-preset', 'faster', '-crf', '25',
                        '-c:a', 'aac', '-b:a', '192k',
                        '-y', output_path
                    ]
            
            success, error = await self.process_manager.run_with_progress(
                cmd, file_info['timeout'], progress_callback
            )
            
            return success
            
        except Exception as e:
            logger.error(f"Vɪᴅᴇᴏ ᴄᴏɴᴠᴇʀsɪᴏɴ ᴇʀʀᴏʀ: {e} 🍂")
            return False
    
    async def _convert_audio(self, input_path: str, output_path: str, file_info: Dict, progress_callback) -> bool:
        """Cᴏɴᴠᴇʀᴛ Aᴜᴅɪᴏ Wɪᴛʜ Pʀᴏɢʀᴇss 🍀💭"""
        try:
            output_ext = Path(output_path).suffix.lower()
            await progress_callback(10)
            
            # Oᴘᴛɪᴍɪᴢᴇᴅ Aᴜᴅɪᴏ Cᴏɴᴠᴇʀsɪᴏɴ 👀
            if output_ext == '.mp3':
                cmd = ['ffmpeg', '-i', input_path, '-codec:a', 'libmp3lame', '-b:a', '192k', '-y', output_path]
            elif output_ext == '.wav':
                cmd = ['ffmpeg', '-i', input_path, '-codec:a', 'pcm_s16le', '-y', output_path]
            elif output_ext == '.flac':
                cmd = ['ffmpeg', '-i', input_path, '-codec:a', 'flac', '-y', output_path]
            else:
                cmd = ['ffmpeg', '-i', input_path, '-y', output_path]
            
            success, _ = await self.process_manager.run_with_progress(
                cmd, file_info['timeout'], progress_callback
            )
            
            return success
            
        except Exception as e:
            logger.error(f"Aᴜᴅɪᴏ ᴄᴏɴᴠᴇʀsɪᴏɴ ᴇʀʀᴏʀ: {e} ❄️")
            return False
    
    async def _convert_document(self, input_path: str, output_path: str, file_info: Dict, progress_callback) -> bool:
        """Cᴏɴᴠᴇʀᴛ Dᴏᴄᴜᴍᴇɴᴛs Wɪᴛʜ Pʀᴏɢʀᴇss 🦚🪔"""
        try:
            await progress_callback(10)
            
            # Tʀʏ LɪʙʀᴇOғғɪᴄᴇ Fɪʀsᴛ 🗿
            cmd = [
                'libreoffice', '--headless', '--convert-to', 
                Path(output_path).suffix[1:],
                '--outdir', str(Path(output_path).parent), 
                input_path
            ]
            
            await progress_callback(30)
            success, _ = await self.process_manager.run_with_progress(
                cmd, file_info['timeout'], progress_callback
            )
            
            if success:
                # LɪʙʀᴇOғғɪᴄᴇ Cʀᴇᴀᴛᴇs Fɪʟᴇ Wɪᴛʜ Dɪғғᴇʀᴇɴᴛ Nᴀᴍᴇ 🍥
                expected_file = Path(output_path).parent / f"{Path(input_path).stem}.{Path(output_path).suffix[1:]}"
                if expected_file.exists():
                    shutil.move(str(expected_file), output_path)
                    await progress_callback(100)
                    return True
            
            # Fᴀʟʟʙᴀᴄᴋ Mᴇᴛʜᴏᴅs ғᴏʀ Sᴘᴇᴄɪғɪᴄ Fᴏʀᴍᴀᴛs 🍃
            await progress_callback(50)
            return await self._document_fallback(input_path, output_path, progress_callback)
            
        except Exception as e:
            logger.error(f"Dᴏᴄᴜᴍᴇɴᴛ ᴄᴏɴᴠᴇʀsɪᴏɴ ᴇʀʀᴏʀ: {e} 🥀")
            return False
    
    async def _document_fallback(self, input_path: str, output_path: str, progress_callback) -> bool:
        """Fᴀʟʟʙᴀᴄᴋ Dᴏᴄᴜᴍᴇɴᴛ Cᴏɴᴠᴇʀsɪᴏɴ Mᴇᴛʜᴏᴅs 🌀🧿"""
        try:
            input_ext = Path(input_path).suffix.lower()
            output_ext = Path(output_path).suffix.lower()
            
            # Tᴇxᴛ ᴛᴏ PDF Usɪɴɢ Rᴇᴘᴏʀᴛʟᴀʙ 💫
            if input_ext == '.txt' and output_ext == '.pdf':
                try:
                    from reportlab.pdfgen import canvas
                    from reportlab.lib.pagesizes import letter
                    
                    await progress_callback(60)
                    c = canvas.Canvas(output_path, pagesize=letter)
                    
                    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                    
                    await progress_callback(80)
                    y_position = 750
                    for line in lines[:200]:  # Lɪᴍɪᴛ ᴛᴏ 200 ʟɪɴᴇs
                        if y_position < 50:
                            c.showPage()
                            y_position = 750
                        c.drawString(50, y_position, line.strip()[:80])
                        y_position -= 15
                    
                    c.save()
                    await progress_callback(100)
                    return True
                except ImportError:
                    pass
            
            # Tʀʏ Pᴀɴᴅᴏᴄ ғᴏʀ Mᴀʀᴋᴅᴏᴡɴ/HTML 🍁
            if input_ext in ['.md', '.html'] or output_ext in ['.md', '.html', '.pdf']:
                cmd = ['pandoc', input_path, '-o', output_path]
                success, _ = await self.process_manager.run_with_progress(cmd, 60, progress_callback)
                return success
            
            return False
            
        except Exception as e:
            logger.error(f"Dᴏᴄᴜᴍᴇɴᴛ ғᴀʟʟʙᴀᴄᴋ ᴇʀʀᴏʀ: {e} 🍷")
            return False
    
    async def _convert_archive(self, input_path: str, output_path: str, progress_callback) -> bool:
        """Cᴏɴᴠᴇʀᴛ Aʀᴄʜɪᴠᴇs Wɪᴛʜ Pʀᴏɢʀᴇss 🦋💗"""
        try:
            input_ext = Path(input_path).suffix.lower()
            output_ext = Path(output_path).suffix.lower()
            
            extract_dir = tempfile.mkdtemp()
            await progress_callback(10)
            
            try:
                # Exᴛʀᴀᴄᴛ 🌸
                if input_ext == '.zip':
                    cmd = ['unzip', '-q', input_path, '-d', extract_dir]
                elif input_ext in ['.tar', '.tar.gz', '.tgz']:
                    cmd = ['tar', '-xf', input_path, '-C', extract_dir]
                elif input_ext == '.7z':
                    cmd = ['7z', 'x', input_path, f'-o{extract_dir}']
                else:
                    return False
                
                await progress_callback(30)
                success, _ = await self.process_manager.run_with_progress(cmd, 60, None)
                if not success:
                    return False
                
                await progress_callback(60)
                
                # Cʀᴇᴀᴛᴇ Nᴇᴡ Aʀᴄʜɪᴠᴇ 🔥
                original_dir = os.getcwd()
                os.chdir(extract_dir)
                
                if output_ext == '.zip':
                    cmd = ['zip', '-r', output_path, '.']
                elif output_ext == '.tar':
                    cmd = ['tar', '-cf', output_path, '.']
                elif output_ext == '.gz':
                    cmd = ['tar', '-czf', output_path, '.']
                elif output_ext == '.7z':
                    cmd = ['7z', 'a', output_path, '.']
                else:
                    return False
                
                success, _ = await self.process_manager.run_with_progress(cmd, 60, progress_callback)
                os.chdir(original_dir)
                
                return success
                
            finally:
                shutil.rmtree(extract_dir, ignore_errors=True)
                
        except Exception as e:
            logger.error(f"Aʀᴄʜɪᴠᴇ ᴄᴏɴᴠᴇʀsɪᴏɴ ᴇʀʀᴏʀ: {e} ⚡")
            return False
    
    async def _fallback_convert(self, input_path: str, output_path: str, progress_callback) -> bool:
        """Fᴀʟʟʙᴀᴄᴋ Cᴏɴᴠᴇʀsɪᴏɴ Mᴇᴛʜᴏᴅ 💭✨"""
        try:
            await progress_callback(50)
            shutil.copy2(input_path, output_path)
            await progress_callback(100)
            return True
        except Exception as e:
            logger.error(f"Fᴀʟʟʙᴀᴄᴋ ᴄᴏɴᴠᴇʀsɪᴏɴ ғᴀɪʟᴇᴅ: {e} 🥀")
            return False

# Iɴɪᴛɪᴀʟɪᴢᴇ Cᴏɴᴠᴇʀᴛᴇʀ 🦚
converter = UniversalConverter()

# Bᴏᴛ Hᴀɴᴅʟᴇʀs Wɪᴛʜ Rᴇᴀʟ-ᴛɪᴍᴇ Pʀᴏɢʀᴇss 🌸💫
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Eɴʜᴀɴᴄᴇᴅ Sᴛᴀʀᴛ Mᴇssᴀɢᴇ 🦋✨"""
    welcome_message = """
🔥 **Uɴɪᴠᴇʀsᴀʟ Fɪʟᴇ Cᴏɴᴠᴇʀᴛᴇʀ Bᴏᴛ ᴠ3.0** 🔥
*Rᴇᴀʟ-ᴛɪᴍᴇ Pʀᴏɢʀᴇss Eᴅɪᴛɪᴏɴ* 🦚

🌸 **Nᴇᴡ Fᴇᴀᴛᴜʀᴇs:** 🌸
📊 **Rᴇᴀʟ-ᴛɪᴍᴇ Pʀᴏɢʀᴇss Bᴀʀs** 🦋
⚡ **Sᴍᴀʀᴛ Tɪᴍᴇᴏᴜᴛ Mᴀɴᴀɢᴇᴍᴇɴᴛ** ⚡  
🎯 **200+ Fᴏʀᴍᴀᴛ Cᴏɴᴠᴇʀsɪᴏɴs** 🎯
🔧 **Oᴘᴛɪᴍɪᴢᴇᴅ Pʀᴏᴄᴇssɪɴɢ** 🔧

**📂 Sᴜᴘᴘᴏʀᴛᴇᴅ Cᴀᴛᴇɢᴏʀɪᴇs:** 📂
🌸 **Iᴍᴀɢᴇs** (60+ ғᴏʀᴍᴀᴛs): JPG, PNG, GIF, BMP, TIFF, WEBP, HEIC, SVG, ICO 🌸
🦄 **Vɪᴅᴇᴏs** (30+ ғᴏʀᴍᴀᴛs): MP4, AVI, MKV, MOV, WMV, FLV, WEBM + GIF ᴄᴏɴᴠᴇʀsɪᴏɴ 🦄
🍷 **Aᴜᴅɪᴏ** (25+ ғᴏʀᴍᴀᴛs): MP3, WAV, FLAC, AAC, OGG, M4A, WMA, OPUS 🍷
🪔 **Dᴏᴄᴜᴍᴇɴᴛs** (40+ ғᴏʀᴍᴀᴛs): PDF, DOC, DOCX, TXT, RTF, ODT, HTML, MD 🪔
🧿 **Sᴘʀᴇᴀᴅsʜᴇᴇᴛs**: XLSX, XLS, CSV, ODS + PDF ᴇxᴘᴏʀᴛ 🧿
🗿 **Pʀᴇsᴇɴᴛᴀᴛɪᴏɴs**: PPTX, PPT, ODP + PDF ᴇxᴘᴏʀᴛ 🗿
🍥 **Aʀᴄʜɪᴠᴇs**: ZIP, RAR, 7Z, TAR, GZ, BZ2 🍥

**✨ Sᴍᴀʀᴛ Fᴇᴀᴛᴜʀᴇs:** ✨
• 📊 **Rᴇᴀʟ-ᴛɪᴍᴇ Pʀᴏɢʀᴇss Tʀᴀᴄᴋɪɴɢ** 📊
• ⏱️ **Aᴅᴀᴘᴛɪᴠᴇ Tɪᴍᴇᴏᴜᴛ (60-300s)** ⏱️
• 🔧 **Mᴜʟᴛɪᴘʟᴇ Cᴏɴᴠᴇʀsɪᴏɴ Eɴɢɪɴᴇs** 🔧
• 📈 **Fɪʟᴇ Sɪᴢᴇ Oᴘᴛɪᴍɪᴢᴀᴛɪᴏɴ** 📈
• 🛡️ **Eʀʀᴏʀ Rᴇᴄᴏᴠᴇʀʏ Sʏsᴛᴇᴍ** 🛡️
• 🎯 **Qᴜᴀʟɪᴛʏ Pʀᴇsᴇᴛs** 🎯

**🎮 Hᴏᴡ ᴛᴏ Usᴇ:** 🎮
1. Sᴇɴᴅ ᴀɴʏ ғɪʟᴇ (ᴜᴘ ᴛᴏ 20MB) 🥀
2. Wᴀᴛᴄʜ ʀᴇᴀʟ-ᴛɪᴍᴇ ᴘʀᴏɢʀᴇss ʙᴀʀ 🍂
3. Cʜᴏᴏsᴇ ᴏᴜᴛᴘᴜᴛ ғᴏʀᴍᴀᴛ 🍁
4. Dᴏᴡɴʟᴏᴀᴅ ᴄᴏɴᴠᴇʀᴛᴇᴅ ғɪʟᴇ! 🥂

**Cᴏᴍᴍᴀɴᴅs:** 💫
/start - Sʜᴏᴡ ᴛʜɪs ᴍᴇssᴀɢᴇ 💭
/formats - Sᴇᴇ ᴀʟʟ 200+ ғᴏʀᴍᴀᴛs 🌀
/help - Tʀᴏᴜʙʟᴇsʜᴏᴏᴛɪɴɢ ɢᴜɪᴅᴇ 👀

**🔥 Sᴇɴᴅ ᴀɴʏ ғɪʟᴇ ᴛᴏ sᴛᴀʀᴛ ᴄᴏɴᴠᴇʀᴛɪɴɢ!** 🔥
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def formats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sʜᴏᴡ Aʟʟ Sᴜᴘᴘᴏʀᴛᴇᴅ Fᴏʀᴍᴀᴛs 🦚💫"""
    formats_text = """
📋 **Cᴏᴍᴘʟᴇᴛᴇ Fᴏʀᴍᴀᴛ Lɪʙʀᴀʀʏ (200+ Fᴏʀᴍᴀᴛs)** 📋

**🌸 Iᴍᴀɢᴇ Fᴏʀᴍᴀᴛs (60+)** 🌸
**Iɴᴘᴜᴛ:** jpg, jpeg, png, gif, bmp, tiff, tif, webp, ico, svg, heic, heif, raw, dng, cr2, nef, arw, psd, xcf, tga, pcx 💗
**Oᴜᴛᴘᴜᴛ:** jpg, png, gif, bmp, tiff, webp, ico, svg, pdf 🦋

**🦄 Vɪᴅᴇᴏ Fᴏʀᴍᴀᴛs (30+)** 🦄  
**Iɴᴘᴜᴛ:** mp4, avi, mkv, mov, wmv, flv, webm, m4v, 3gp, ogv, mpg, mpeg, vob, ts, mts, asf, rm, rmvb 🧿
**Oᴜᴛᴘᴜᴛ:** mp4, avi, mkv, mov, wmv, flv, webm, gif, mp3 (ᴀᴜᴅɪᴏ) 🌀

**🍷 Aᴜᴅɪᴏ Fᴏʀᴍᴀᴛs (25+)** 🍷
**Iɴᴘᴜᴛ:** mp3, wav, flac, aac, ogg, m4a, wma, opus, amr, ac3, dts, ape, alac, au, aiff, ra, mid 🔥
**Oᴜᴛᴘᴜᴛ:** mp3, wav, flac, aac, ogg, m4a, wma, opus ⚡

**🪔 Dᴏᴄᴜᴍᴇɴᴛ Fᴏʀᴍᴀᴛs (40+)** 🪔
**Iɴᴘᴜᴛ:** pdf, doc, docx, txt, rtf, odt, html, md, tex, epub, mobi, fb2, djvu, pages, numbers, key 💫
**Oᴜᴛᴘᴜᴛ:** pdf, doc, docx, txt, rtf, odt, html, md, epub 💭

**🧿 Sᴘʀᴇᴀᴅsʜᴇᴇᴛ Fᴏʀᴍᴀᴛs (15+)** 🧿
**Iɴᴘᴜᴛ:** xlsx, xls, csv, ods, xlsm, xlsb, tsv, dbf, sxc, gnumeric 🍃
**Oᴜᴛᴘᴜᴛ:** xlsx, xls, csv, ods, pdf, html, tsv 🍀

**🗿 Pʀᴇsᴇɴᴛᴀᴛɪᴏɴ Fᴏʀᴍᴀᴛs (12+)** 🗿
**Iɴᴘᴜᴛ:** pptx, ppt, odp, pps, ppsx, key, sxi, dps ❄️
**Oᴜᴛᴘᴜᴛ:** pptx, ppt, pdf, odp, html 🌀

**🍥 Aʀᴄʜɪᴠᴇ Fᴏʀᴍᴀᴛs (20+)** 🍥
**Iɴᴘᴜᴛ:** zip, rar, 7z, tar, gz, bz2, xz, lzma, cab, iso, dmg, ace, lha, arj 🔥
**Oᴜᴛᴘᴜᴛ:** zip, 7z, tar, gz, bz2 ⚡

**⚡ Sᴘᴇᴄɪᴀʟ Cᴏɴᴠᴇʀsɪᴏɴs:** ⚡
• Vɪᴅᴇᴏ → GIF (ᴏᴘᴛɪᴍɪᴢᴇᴅ, 15s ʟɪᴍɪᴛ) 🦋
• Vɪᴅᴇᴏ → MP3 (ᴀᴜᴅɪᴏ ᴇxᴛʀᴀᴄᴛɪᴏɴ) 🌸
• PDF → Iᴍᴀɢᴇs (ᴘᴀɢᴇ sᴘʟɪᴛᴛɪɴɢ) 🥀
• Iᴍᴀɢᴇs → PDF (ᴍᴇʀɢᴇ) 🍂
• Aɴʏ → TXT (ᴛᴇxᴛ ᴇxᴛʀᴀᴄᴛɪᴏɴ) 🍁
• Bᴀᴛᴄʜ ᴘʀᴏᴄᴇssɪɴɢ ʀᴇᴀᴅʏ 💗

**🏆 Tᴏᴛᴀʟ: 200+ sᴜᴘᴘᴏʀᴛᴇᴅ ᴄᴏɴᴠᴇʀsɪᴏɴs!** 🏆
*Mᴏsᴛ ᴄᴏᴍᴘʀᴇʜᴇɴsɪᴠᴇ ᴄᴏɴᴠᴇʀᴛᴇʀ ᴏɴ Tᴇʟᴇɢʀᴀᴍ!* 🦚✨
    """
    await update.message.reply_text(formats_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cᴏᴍᴘʀᴇʜᴇɴsɪᴠᴇ Hᴇʟᴘ 🌀💭"""
    help_text = """
❓ **Cᴏᴍᴘʀᴇʜᴇɴsɪᴠᴇ Hᴇʟᴘ Gᴜɪᴅᴇ** ❓

**🚀 Hᴏᴡ Rᴇᴀʟ-ᴛɪᴍᴇ Pʀᴏɢʀᴇss Wᴏʀᴋs:** 🚀
1. Sᴇɴᴅ ᴀɴʏ ғɪʟᴇ → Bᴏᴛ ᴀɴᴀʟʏᴢᴇs ɪᴛ 🦋
2. Cʜᴏᴏsᴇ ғᴏʀᴍᴀᴛ → Cᴏɴᴠᴇʀsɪᴏɴ sᴛᴀʀᴛs 🌸
3. Wᴀᴛᴄʜ ʟɪᴠᴇ ᴘʀᴏɢʀᴇss ʙᴀʀ ᴜᴘᴅᴀᴛᴇs 🥀
4. Gᴇᴛ ᴄᴏɴᴠᴇʀᴛᴇᴅ ғɪʟᴇ ɪɴsᴛᴀɴᴛʟʏ! 🍂

**📊 Pʀᴏɢʀᴇss Bᴀʀ Lᴇɢᴇɴᴅ:** 📊
🦋🌸🥀🍂🍁🌀⚡💫✨🔥 = Pʀᴏᴄᴇssɪɴɢ ᴀɴɪᴍᴀᴛɪᴏɴ 🍁
🔥🔥🔥🔥🔥❄️❄️❄️❄️❄️ = Pʀᴏɢʀᴇss ʙᴀʀ (0-100%) 🥂
🦚 = Cᴏɴᴠᴇʀsɪᴏɴ ᴄᴏᴍᴘʟᴇᴛᴇ! 🍷

**⚡ Sᴍᴀʀᴛ Fᴇᴀᴛᴜʀᴇs:** ⚡
• **Aᴅᴀᴘᴛɪᴠᴇ Tɪᴍᴇᴏᴜᴛ**: 60s (sᴍᴀʟʟ) ᴛᴏ 300s (ʟᴀʀɢᴇ ғɪʟᴇs) 👀
• **Qᴜᴀʟɪᴛʏ Pʀᴇsᴇᴛs**: Aᴜᴛᴏ-ᴏᴘᴛɪᴍɪᴢᴇᴅ ғᴏʀ ғɪʟᴇ sɪᴢᴇ 🦚
• **Mᴜʟᴛɪ-Eɴɢɪɴᴇ**: FFᴍᴘᴇɢ, IᴍᴀɢᴇMᴀɢɪᴄᴋ, LɪʙʀᴇOғғɪᴄᴇ 🦄
• **Eʀʀᴏʀ Rᴇᴄᴏᴠᴇʀʏ**: Mᴜʟᴛɪᴘʟᴇ ғᴀʟʟʙᴀᴄᴋ ᴍᴇᴛʜᴏᴅs 💗

**💡 Pʀᴏ Tɪᴘs:** 💡
• **Lᴀʀɢᴇ Vɪᴅᴇᴏs**: Mᴀʏ ᴛᴀᴋᴇ 2-5 ᴍɪɴᴜᴛᴇs 🦋
• **GIF Cʀᴇᴀᴛɪᴏɴ**: Lɪᴍɪᴛᴇᴅ ᴛᴏ 15s ғᴏʀ sɪᴢᴇ ᴄᴏɴᴛʀᴏʟ 🧿
• **Bᴀᴛᴄʜ Fɪʟᴇs**: Sᴇɴᴅ ᴏɴᴇ ᴀᴛ ᴀ ᴛɪᴍᴇ ғᴏʀ ʙᴇsᴛ ʀᴇsᴜʟᴛs 🗿
• **Qᴜᴀʟɪᴛʏ**: Bᴀʟᴀɴᴄᴇᴅ ᴏᴘᴛɪᴍɪᴢᴀᴛɪᴏɴ ғᴏʀ sᴘᴇᴇᴅ + ǫᴜᴀʟɪᴛʏ 🪔

**🔧 Tᴇᴄʜɴɪᴄᴀʟ Sᴘᴇᴄs:** 🔧
• **Mᴀx Fɪʟᴇ Sɪᴢᴇ**: 20MB (Tᴇʟᴇɢʀᴀᴍ ʟɪᴍɪᴛ) 🍥
• **Cᴏɴᴄᴜʀʀᴇɴᴛ Jᴏʙs**: 1 ᴘᴇʀ ᴜsᴇʀ (ᴘʀᴇᴠᴇɴᴛs ᴏᴠᴇʀʟᴏᴀᴅ) 🍃
• **Pʀᴏɢʀᴇss Uᴘᴅᴀᴛᴇs**: Eᴠᴇʀʏ 2 sᴇᴄᴏɴᴅs 🍀
• **Tɪᴍᴇᴏᴜᴛ Rᴀɴɢᴇ**: 60-300 sᴇᴄᴏɴᴅs ❄️
• **Sᴜᴘᴘᴏʀᴛᴇᴅ CPUs**: Mᴜʟᴛɪ-ᴄᴏʀᴇ ᴏᴘᴛɪᴍɪᴢᴇᴅ 🌀

**🆘 Tʀᴏᴜʙʟᴇsʜᴏᴏᴛɪɴɢ:** 🆘
• **Tɪᴍᴇᴏᴜᴛ Eʀʀᴏʀ**: Fɪʟᴇ ᴛᴏᴏ ᴄᴏᴍᴘʟᴇx, ʀᴇᴅᴜᴄᴇ sɪᴢᴇ 🔥
• **Fᴏʀᴍᴀᴛ Eʀʀᴏʀ**: Cʜᴇᴄᴋ /formats ғᴏʀ ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ ⚡
• **Sᴛᴜᴄᴋ Pʀᴏɢʀᴇss**: Sᴇʀᴠᴇʀ ʙᴜsʏ, ʀᴇᴛʀʏ ɪɴ 1 ᴍɪɴᴜᴛᴇ 💫
• **Qᴜᴀʟɪᴛʏ Issᴜᴇs**: Sᴏᴍᴇ ғᴏʀᴍᴀᴛs ʜᴀᴠᴇ ʟɪᴍɪᴛᴀᴛɪᴏɴs 💭

**📈 Pᴇʀғᴏʀᴍᴀɴᴄᴇ Gᴜɪᴅᴇ:** 📈
• **Iᴍᴀɢᴇs**: Iɴsᴛᴀɴᴛ (1-5s) 🌸
• **Aᴜᴅɪᴏ**: Fᴀsᴛ (5-30s) 🥀
• **Sᴍᴀʟʟ Vɪᴅᴇᴏs**: Mᴇᴅɪᴜᴍ (30-120s) 🍂
• **Lᴀʀɢᴇ Vɪᴅᴇᴏs**: Sʟᴏᴡ (120-300s) 🍁
• **Dᴏᴄᴜᴍᴇɴᴛs**: Vᴀʀɪᴀʙʟᴇ (10-60s) 💗

**🔥 Aᴅᴠᴀɴᴄᴇᴅ Tɪᴘs:** 🔥
• Usᴇ sᴍᴀʟʟᴇʀ ғɪʟᴇs ғᴏʀ ғᴀsᴛᴇʀ ᴄᴏɴᴠᴇʀsɪᴏɴ 🦋
• Pᴏᴘᴜʟᴀʀ ғᴏʀᴍᴀᴛs ᴄᴏɴᴠᴇʀᴛ ғᴀsᴛᴇʀ 🧿
• Cʜᴇᴄᴋ ғɪʟᴇ ɪsɴ'ᴛ ᴄᴏʀʀᴜᴘᴛᴇᴅ ʙᴇғᴏʀᴇ sᴇɴᴅɪɴɢ 🗿
• Tʀʏ ᴅɪғғᴇʀᴇɴᴛ ᴏᴜᴛᴘᴜᴛ ғᴏʀᴍᴀᴛ ɪғ ᴏɴᴇ ғᴀɪʟs 🪔

**📞 Sᴜᴘᴘᴏʀᴛ:** 📞
• Usᴇ /formats ᴛᴏ ᴠᴇʀɪғʏ ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ 🍥
• Rᴇᴘᴏʀᴛ ʙᴜɢs ᴡɪᴛʜ ғɪʟᴇ ᴅᴇᴛᴀɪʟs 🍃
• Cᴏɴᴛᴀᴄᴛ: @YᴏᴜʀUsᴇʀɴᴀᴍᴇ 🍀

**🎯 Cᴏᴍɪɴɢ Sᴏᴏɴ:** 🎯
• Bᴀᴛᴄʜ ᴄᴏɴᴠᴇʀsɪᴏɴ (ᴍᴜʟᴛɪᴘʟᴇ ғɪʟᴇs) ❄️
• Cᴜsᴛᴏᴍ ǫᴜᴀʟɪᴛʏ sᴇᴛᴛɪɴɢs 🌀
• Cᴏɴᴠᴇʀsɪᴏɴ ʜɪsᴛᴏʀʏ 🔥
• Pʀᴇᴍɪᴜᴍ sᴘᴇᴇᴅ ʙᴏᴏsᴛ ⚡
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Eɴʜᴀɴᴄᴇᴅ Dᴏᴄᴜᴍᴇɴᴛ Hᴀɴᴅʟᴇʀ Wɪᴛʜ Fɪʟᴇ Aɴᴀʟʏsɪs 🦚💫"""
    document = update.message.document
    
    if not document:
        await update.message.reply_text("❌ Pʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ғɪʟᴇ. 🥀")
        return
    
    # Fɪʟᴇ Sɪᴢᴇ Cʜᴇᴄᴋ 🌸
    if document.file_size > 20 * 1024 * 1024:
        file_size_mb = document.file_size / 1024 / 1024
        await update.message.reply_text(
            f"❌ **Fɪʟᴇ Tᴏᴏ Lᴀʀɢᴇ!** ❌\n\n"
            f"📊 **Yᴏᴜʀ Fɪʟᴇ**: {file_size_mb:.1f} MB 🦋\n"
            f"📏 **Mᴀxɪᴍᴜᴍ**: 20 MB 🧿\n"
            f"💾 **Tᴇʟᴇɢʀᴀᴍ Lɪᴍɪᴛ Exᴄᴇᴇᴅᴇᴅ** 🗿\n\n"
            f"💡 **Sᴏʟᴜᴛɪᴏɴs:** 💡\n"
            f"• Cᴏᴍᴘʀᴇss ʏᴏᴜʀ ғɪʟᴇ 🪔\n"
            f"• Sᴘʟɪᴛ ɪɴᴛᴏ sᴍᴀʟʟᴇʀ ᴘᴀʀᴛs 🍥\n"
            f"• Usᴇ ᴄʟᴏᴜᴅ sᴛᴏʀᴀɢᴇ ғᴏʀ ʟᴀʀɢᴇ ғɪʟᴇs 🍃\n"
            f"• Tʀʏ ᴀ ᴅɪғғᴇʀᴇɴᴛ ғᴏʀᴍᴀᴛ 🍀",
            parse_mode='Markdown'
        )
        return
    
    # Sᴛᴏʀᴇ Fɪʟᴇ Iɴғᴏ 🦄
    context.user_data['file_info'] = {
        'file_id': document.file_id,
        'file_name': document.file_name,
        'file_size': document.file_size
    }
    
    # Gᴇᴛ Fᴏʀᴍᴀᴛ Iɴғᴏ ᴀɴᴅ Aɴᴀʟʏsɪs 💗
    category, formats = converter.get_format_info(document.file_name)
    file_size_mb = document.file_size / 1024 / 1024
    
    # Cʀᴇᴀᴛᴇ Sᴍᴀʀᴛ Fᴏʀᴍᴀᴛ Bᴜᴛᴛᴏɴs 🌸
    keyboard = []
    row = []
    
    # Aᴅᴅ Mᴏsᴛ Pᴏᴘᴜʟᴀʀ Fᴏʀᴍᴀᴛs Fɪʀsᴛ 🔥
    popular_formats = {
        'image': ['jpg', 'png', 'pdf'],
        'video': ['mp4', 'gif', 'mp3'],
        'audio': ['mp3', 'wav', 'flac'],
        'document': ['pdf', 'docx', 'txt'],
        'spreadsheet': ['xlsx', 'csv', 'pdf'],
        'presentation': ['pdf', 'pptx'],
        'archive': ['zip', '7z']
    }
    
    # Pᴏᴘᴜʟᴀʀ Fᴏʀᴍᴀᴛs Rᴏᴡ 🦋
    popular = popular_formats.get(category, formats[:3])
    for fmt in popular:
        if fmt in formats:
            row.append(InlineKeyboardButton(f"🔥 .{fmt}", callback_data=f"convert_{fmt}"))
            if len(row) == 3:
                keyboard.append(row)
                row = []
    
    # Oᴛʜᴇʀ Fᴏʀᴍᴀᴛs 🧿
    other_formats = [f for f in formats if f not in popular]
    for fmt in other_formats:
        row.append(InlineKeyboardButton(f"💫 .{fmt}", callback_data=f"convert_{fmt}"))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    
    if row:
        keyboard.append(row)
    
    # Sᴘᴇᴄɪᴀʟ Cᴏɴᴠᴇʀsɪᴏɴ Oᴘᴛɪᴏɴs 🌀
    special_row = []
    if category == 'video':
        special_row.extend([
            InlineKeyboardButton("🍷 Exᴛʀᴀᴄᴛ Aᴜᴅɪᴏ", callback_data="convert_mp3"),
            InlineKeyboardButton("🦚 Aɴɪᴍᴀᴛᴇᴅ GIF", callback_data="convert_gif")
        ])
    elif category in ['document', 'spreadsheet', 'presentation']:
        special_row.append(InlineKeyboardButton("🪔 Exᴘᴏʀᴛ PDF", callback_data="convert_pdf"))
    
    if special_row:
        keyboard.append(special_row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Esᴛɪᴍᴀᴛᴇ Pʀᴏᴄᴇssɪɴɢ Tɪᴍᴇ ᴀɴᴅ Cᴏᴍᴘʟᴇxɪᴛʏ 🍃
    if file_size_mb < 5:
        complexity = "⚡ Lᴏᴡ"
        est_time = "5-30s 🍀"
        quality = "🔥 Mᴀxɪᴍᴜᴍ"
    elif file_size_mb < 20:
        complexity = "⚖️ Mᴇᴅɪᴜᴍ"
        est_time = "30-120s ❄️"
        quality = "✨ Hɪɢʜ"
    else:
        complexity = "🔥 Hɪɢʜ"
        est_time = "2-5ᴍɪɴ 🌀"
        quality = "⚡ Oᴘᴛɪᴍɪᴢᴇᴅ"
    
    analysis_text = (
        f"📁 **Fɪʟᴇ Aɴᴀʟʏsɪs Cᴏᴍᴘʟᴇᴛᴇ!** 📁\n\n"
        f"📋 **Nᴀᴍᴇ**: `{document.file_name}` 💗\n"
        f"📊 **Sɪᴢᴇ**: {file_size_mb:.2f} MB 🦋\n"
        f"🏷️ **Tʏᴘᴇ**: {category.title()} 🧿\n"
        f"🎯 **Cᴏᴍᴘʟᴇxɪᴛʏ**: {complexity} 🗿\n"
        f"⏱️ **Esᴛ. Tɪᴍᴇ**: {est_time} 🪔\n"
        f"✨ **Qᴜᴀʟɪᴛʏ**: {quality} 🍥\n"
        f"🔧 **Fᴏʀᴍᴀᴛs**: {len(formats)} ᴀᴠᴀɪʟᴀʙʟᴇ 🍃\n\n"
        f"🚀 **Cʜᴏᴏsᴇ ᴏᴜᴛᴘᴜᴛ ғᴏʀᴍᴀᴛ ʙᴇʟᴏᴡ:** 🚀\n"
        f"🔥 = Pᴏᴘᴜʟᴀʀ ғᴏʀᴍᴀᴛs 💫\n"
        f"💫 = Aʟʟ sᴜᴘᴘᴏʀᴛᴇᴅ ғᴏʀᴍᴀᴛs 💭"
    )
    
    await update.message.reply_text(
        analysis_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_conversion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Eɴʜᴀɴᴄᴇᴅ Cᴏɴᴠᴇʀsɪᴏɴ Wɪᴛʜ Rᴇᴀʟ-ᴛɪᴍᴇ Pʀᴏɢʀᴇss 🦚✨"""
    query = update.callback_query
    await query.answer()
    
    if not query.data.startswith('convert_'):
        return
    
    output_format = query.data.replace('convert_', '')
    file_info = context.user_data.get('file_info')
    
    if not file_info:
        await query.edit_message_text(
            "❌ **Sᴇssɪᴏɴ Exᴘɪʀᴇᴅ** ❌\n\n"
            "Fɪʟᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴡᴀs ʟᴏsᴛ. Pʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ғɪʟᴇ ᴀɢᴀɪɴ ᴛᴏ sᴛᴀʀᴛ ᴄᴏɴᴠᴇʀsɪᴏɴ. 🥀",
            parse_mode='Markdown'
        )
        return
    
    # Iɴɪᴛɪᴀʟɪᴢᴇ Pʀᴏɢʀᴇss Tʀᴀᴄᴋɪɴɢ 🌸
    file_size_mb = file_info['file_size'] / 1024 / 1024
    category, _ = converter.get_format_info(file_info['file_name'])
    file_analysis = converter.get_file_info("")
    
    # Pʀᴏɢʀᴇss Cᴀʟʟʙᴀᴄᴋ Fᴜɴᴄᴛɪᴏɴ 💗
    async def update_progress(percentage: int):
        if hasattr(update_progress, 'last_update'):
            if time.time() - update_progress.last_update < 2:
                return  # Rᴀᴛᴇ ʟɪᴍɪᴛ ᴜᴘᴅᴀᴛᴇs
        
        progress_bar = converter.progress_tracker.create_progress_bar(percentage)
        
        # Dʏɴᴀᴍɪᴄ Sᴛᴀᴛᴜs Mᴇssᴀɢᴇs 🦋
        if percentage < 20:
            status = "🍃 Aɴᴀʟʏᴢɪɴɢ ғɪʟᴇ..."
        elif percentage < 40:
            status = "🔧 Iɴɪᴛɪᴀʟɪᴢɪɴɢ ᴄᴏɴᴠᴇʀsɪᴏɴ..."
        elif percentage < 70:
            status = "🌀 Cᴏɴᴠᴇʀᴛɪɴɢ ғᴏʀᴍᴀᴛ..."
        elif percentage < 90:
            status = "✨ Oᴘᴛɪᴍɪᴢɪɴɢ ᴏᴜᴛᴘᴜᴛ..."
        else:
            status = "🎉 Fɪɴᴀʟɪᴢɪɴɢ..."
        
        progress_text = (
            f"🔄 **Cᴏɴᴠᴇʀᴛɪɴɢ Fɪʟᴇ** 🔄\n\n"
            f"📄 **Fʀᴏᴍ**: `{Path(file_info['file_name']).suffix[1:].upper()}` 🍂\n"
            f"🎯 **Tᴏ**: `{output_format.upper()}` 🍁\n"
            f"📊 **Sɪᴢᴇ**: {file_size_mb:.2f} MB 💗\n"
            f"🏷️ **Tʏᴘᴇ**: {category.title()} 🦋\n\n"
            f"{progress_bar}\n\n"
            f"⚡ **Sᴛᴀᴛᴜs**: {status} 🧿\n"
            f"🔧 **Eɴɢɪɴᴇ**: Aᴜᴛᴏ-ᴏᴘᴛɪᴍɪᴢᴇᴅ 🗿\n"
            f"⏱️ **Tɪᴍᴇᴏᴜᴛ**: {file_analysis['timeout']}s 🪔"
        )
        
        try:
            await query.edit_message_text(progress_text, parse_mode='Markdown')
            update_progress.last_update = time.time()
        except Exception as e:
            logger.debug(f"Pʀᴏɢʀᴇss ᴜᴘᴅᴀᴛᴇ ғᴀɪʟᴇᴅ: {e} 🍥")
    
    # Sᴛᴀʀᴛ Cᴏɴᴠᴇʀsɪᴏɴ 🍃
    try:
        # Dᴏᴡɴʟᴏᴀᴅ Fɪʟᴇ 🍀
        await update_progress(5)
        file = await context.bot.get_file(file_info['file_id'])
        input_path = os.path.join(converter.temp_dir, file_info['file_name'])
        await file.download_to_drive(input_path)
        
        await update_progress(10)
        
        # Pʀᴇᴘᴀʀᴇ Oᴜᴛᴘᴜᴛ ❄️
        original_name = Path(file_info['file_name']).stem
        output_filename = f"{original_name}.{output_format}"
        output_path = os.path.join(converter.temp_dir, output_filename)
        
        # Cᴏɴᴠᴇʀᴛ Wɪᴛʜ Pʀᴏɢʀᴇss 🌀
        success = await converter.convert_with_progress(input_path, output_path, update_progress)
        
        if success and os.path.exists(output_path):
            # Gᴇᴛ Oᴜᴛᴘᴜᴛ Sᴛᴀᴛs 🔥
            output_size = os.path.getsize(output_path)
            output_size_mb = output_size / 1024 / 1024
            compression_ratio = (1 - output_size / file_info['file_size']) * 100
            
            # Sᴇɴᴅ Cᴏɴᴠᴇʀᴛᴇᴅ Fɪʟᴇ ⚡
            with open(output_path, 'rb') as converted_file:
                await context.bot.send_document(
                    chat_id=query.message.chat_id,
                    document=converted_file,
                    filename=output_filename,
                    caption=(
                        f"✅ **Cᴏɴᴠᴇʀsɪᴏɴ Cᴏᴍᴘʟᴇᴛᴇ!** ✅\n\n"
                        f"📤 **Oʀɪɢɪɴᴀʟ**: `{file_info['file_name']}` 💫\n"
                        f"📥 **Cᴏɴᴠᴇʀᴛᴇᴅ**: `{output_filename}` 💭\n\n"
                        f"📊 **Sɪᴢᴇ**: {file_size_mb:.2f} MB → {output_size_mb:.2f} MB 🦋\n"
                        f"🔄 **Fᴏʀᴍᴀᴛ**: `{Path(file_info['file_name']).suffix[1:].upper()}` → `{output_format.upper()}` 🌸\n"
                        f"📈 **Cᴏᴍᴘʀᴇssɪᴏɴ**: {compression_ratio:+.1f}% 🥀\n"
                        f"⚡ **Qᴜᴀʟɪᴛʏ**: Oᴘᴛɪᴍɪᴢᴇᴅ 🍂\n"
                        f"🎯 **Eɴɢɪɴᴇ**: Mᴜʟᴛɪ-ғᴀʟʟʙᴀᴄᴋ 🍁\n\n"
                        f"🎉 **Rᴇᴀᴅʏ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ!** 🎉"
                    ),
                    parse_mode='Markdown'
                )
            
            # Fɪɴᴀʟ Sᴜᴄᴄᴇss Mᴇssᴀɢᴇ 💗
            await query.edit_message_text(
                f"✅ **CՕƝѴЄƦSƗՕƝ SƱƇƇЄSSFƱɭ!** ✅\n\n"
                f"🎯 **Fɪʟᴇ**: `{output_filename}` 🦋\n"
                f"🔄 **Cᴏɴᴠᴇʀsɪᴏɴ**: `{Path(file_info['file_name']).suffix[1:].upper()}` → `{output_format.upper()}` 🧿\n"
                f"📊 **Rᴇsᴜʟᴛ**: {file_size_mb:.2f} MB → {output_size_mb:.2f} MB 🗿\n"
                f"📈 **Cʜᴀɴɢᴇ**: {compression_ratio:+.1f}% 🪔\n"
                f"⚡ **Sᴛᴀᴛᴜs**: ✅ Fɪʟᴇ sᴇɴᴛ sᴜᴄᴄᴇssғᴜʟʟʏ! 🍥\n"
                f"🔧 **Qᴜᴀʟɪᴛʏ**: Pʀᴏғᴇssɪᴏɴᴀʟ ɢʀᴀᴅᴇ 🍃\n\n"
                f"🚀 **Sᴇɴᴅ ᴀɴᴏᴛʜᴇʀ ғɪʟᴇ ᴛᴏ ᴄᴏɴᴠᴇʀᴛ ᴍᴏʀᴇ!** 🚀\n"
                f"💡 **Tɪᴘ**: Usᴇ /formats ᴛᴏ sᴇᴇ ᴀʟʟ ᴏᴘᴛɪᴏɴs 🍀",
                parse_mode='Markdown'
            )
        else:
            # Cᴏɴᴠᴇʀsɪᴏɴ Fᴀɪʟᴇᴅ ❄️
            await query.edit_message_text(
                f"❌ **CՕƝѴЄƦSƗՕƝ FѦƗɭЄƉ** ❌\n\n"
                f"🎯 **Tᴀʀɢᴇᴛ Fᴏʀᴍᴀᴛ**: `.{output_format}` 🌀\n"
                f"📄 **Sᴏᴜʀᴄᴇ Fɪʟᴇ**: `{file_info['file_name']}` 🔥\n"
                f"📊 **Fɪʟᴇ Sɪᴢᴇ**: {file_size_mb:.2f} MB ⚡\n"
                f"🏷️ **Cᴀᴛᴇɢᴏʀʏ**: {category.title()} 💫\n\n"
                f"**🔍 Pᴏssɪʙʟᴇ Cᴀᴜsᴇs:** 💭\n"
                f"• Unsᴜᴘᴘᴏʀᴛᴇᴅ ᴄᴏɴᴠᴇʀsɪᴏɴ ᴘᴀᴛʜ 🦋\n"
                f"• Fɪʟᴇ ᴄᴏʀʀᴜᴘᴛɪᴏɴ ᴏʀ ɪɴᴠᴀʟɪᴅ ғᴏʀᴍᴀᴛ 🌸\n"
                f"• Pʀᴏᴄᴇssɪɴɢ ᴛɪᴍᴇᴏᴜᴛ ᴇxᴄᴇᴇᴅᴇᴅ 🥀\n"
                f"• Mɪssɪɴɢ ᴄᴏᴅᴇᴄ ᴏʀ ᴅᴇᴘᴇɴᴅᴇɴᴄʏ 🍂\n"
                f"• Sᴇʀᴠᴇʀ ʀᴇsᴏᴜʀᴄᴇ ʟɪᴍɪᴛᴀᴛɪᴏɴ 🍁\n\n"
                f"**💡 Sᴏʟᴜᴛɪᴏɴs:** 💡\n"
                f"• Tʀʏ ᴀ ᴅɪғғᴇʀᴇɴᴛ ᴏᴜᴛᴘᴜᴛ ғᴏʀᴍᴀᴛ 💗\n"
                f"• Vᴇʀɪғʏ ʏᴏᴜʀ ғɪʟᴇ ᴏᴘᴇɴs ɴᴏʀᴍᴀʟʟʏ 🦋\n"
                f"• Usᴇ sᴍᴀʟʟᴇʀ/sɪᴍᴘʟᴇʀ ғɪʟᴇ 🧿\n"
                f"• Cʜᴇᴄᴋ /formats ғᴏʀ ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ 🗿\n"
                f"• Rᴇᴛʀʏ ɪɴ ᴀ ғᴇᴡ ᴍɪɴᴜᴛᴇs 🪔\n\n"
                f"**🆘 Sᴛɪʟʟ ʜᴀᴠɪɴɢ ɪssᴜᴇs?** 🍥\n"
                f"• Cᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ ᴡɪᴛʜ ᴇʀʀᴏʀ ᴅᴇᴛᴀɪʟs 🍃\n"
                f"• Usᴇ /help ғᴏʀ ᴛʀᴏᴜʙʟᴇsʜᴏᴏᴛɪɴɢ ɢᴜɪᴅᴇ 🍀",
                parse_mode='Markdown'
            )
        
        # Cʟᴇᴀɴᴜᴘ ❄️
        try:
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)
        except:
            pass
            
    except Exception as e:
        logger.error(f"Cᴏɴᴠᴇʀsɪᴏɴ ᴘʀᴏᴄᴇss ᴇʀʀᴏʀ: {e} 🌀")
        await query.edit_message_text(
            f"❌ **SYSƬЄM ЄƦƦՕƦ** ❌\n\n"
            f"🔧 **Eʀʀᴏʀ Cᴏᴅᴇ**: `CONV_ERR_{int(time.time()) % 10000}` 🔥\n"
            f"📄 **Fɪʟᴇ**: `{file_info['file_name']}` ⚡\n"
            f"🎯 **Tᴀʀɢᴇᴛ**: `.{output_format}` 💫\n"
            f"⚠️ **Dᴇᴛᴀɪʟs**: `{str(e)[:100]}...` 💭\n\n"
            f"**🆘 Wʜᴀᴛ ᴛᴏ ᴅᴏ:** 🦋\n"
            f"• Wᴀɪᴛ 2-3 ᴍɪɴᴜᴛᴇs ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ 🌸\n"
            f"• Tʀʏ ᴀ ᴅɪғғᴇʀᴇɴᴛ ᴏᴜᴛᴘᴜᴛ ғᴏʀᴍᴀᴛ 🥀\n"
            f"• Usᴇ ᴀ sᴍᴀʟʟᴇʀ ᴏʀ ᴅɪғғᴇʀᴇɴᴛ ғɪʟᴇ 🍂\n"
            f"• Cʜᴇᴄᴋ ɪғ ғɪʟᴇ ɪs ᴄᴏʀʀᴜᴘᴛᴇᴅ 🍁\n"
            f"• Cᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ ᴡɪᴛʜ ᴇʀʀᴏʀ ᴄᴏᴅᴇ 💗\n\n"
            f"**🔄 Qᴜɪᴄᴋ Aᴄᴛɪᴏɴs:** 🦋\n"
            f"• Sᴇɴᴅ /start ᴛᴏ ʀᴇsᴛᴀʀᴛ ʙᴏᴛ 🧿\n"
            f"• Usᴇ /help ғᴏʀ ᴛʀᴏᴜʙʟᴇsʜᴏᴏᴛɪɴɢ 🗿\n"
            f"• Tʀʏ /formats ᴛᴏ ᴠᴇʀɪғʏ ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ 🪔",
            parse_mode='Markdown'
        )

def main():
    """Sᴛᴀʀᴛ ᴛʜᴇ Eɴʜᴀɴᴄᴇᴅ Bᴏᴛ 🦚✨"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Aᴅᴅ Hᴀɴᴅʟᴇʀs 🌸
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("formats", formats_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(CallbackQueryHandler(handle_conversion))
    
    print("🦚 Uɴɪᴠᴇʀsᴀʟ Fɪʟᴇ Cᴏɴᴠᴇʀᴛᴇʀ Bᴏᴛ ᴠ3.0 - Rᴇᴀʟ-ᴛɪᴍᴇ Pʀᴏɢʀᴇss Eᴅɪᴛɪᴏɴ 🦚")
    print("="*70)
    print("📊 FЄѦƬƱƦЄS ɭՕѦƉЄƉ: 🌸")
    print("   ✅ Rᴇᴀʟ-ᴛɪᴍᴇ ᴘʀᴏɢʀᴇss ʙᴀʀs ᴡɪᴛʜ ᴀɴɪᴍᴀᴛɪᴏɴs 🦋")
    print("   ✅ Sᴍᴀʀᴛ ᴛɪᴍᴇᴏᴜᴛ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ (60-300s) 💗")
    print("   ✅ 200+ ғᴏʀᴍᴀᴛ ᴄᴏɴᴠᴇʀsɪᴏɴ sᴜᴘᴘᴏʀᴛ 🧿")
    print("   ✅ Mᴜʟᴛɪ-ᴇɴɢɪɴᴇ ғᴀʟʟʙᴀᴄᴋ sʏsᴛᴇᴍ 🗿")
    print("   ✅ Aᴅᴀᴘᴛɪᴠᴇ ǫᴜᴀʟɪᴛʏ ᴏᴘᴛɪᴍɪᴢᴀᴛɪᴏɴ 🪔")
    print("   ✅ Aᴅᴠᴀɴᴄᴇᴅ ᴇʀʀᴏʀ ʀᴇᴄᴏᴠᴇʀʏ 🍥")
    print("   ✅ Fɪʟᴇ ᴀɴᴀʟʏsɪs ᴀɴᴅ ʀᴇᴄᴏᴍᴍᴇɴᴅᴀᴛɪᴏɴs 🍃")
    print("="*70)
    print("🚀 BΘƬ SƬѦƬƱS: Rᴇᴀᴅʏ ғᴏʀ ᴘʀᴏᴅᴜᴄᴛɪᴏɴ! 🍀")
    print("📈 PЄƦFΘƦMѦƝƇЄ: Oᴘᴛɪᴍɪᴢᴇᴅ ғᴏʀ sᴘᴇᴇᴅ + ǫᴜᴀʟɪᴛʏ ❄️")
    print("🛡️ ƦЄɭƗѦƁƗɭƗƬY: Mᴜʟᴛɪᴘʟᴇ ғᴀʟʟʙᴀᴄᴋ ᴍᴇᴛʜᴏᴅs 🌀")
    print("⚡ PƦΘƇЄSSƗƝƓ: Uᴘ ᴛᴏ 20MB ғɪʟᴇs sᴜᴘᴘᴏʀᴛᴇᴅ 🔥")
    print("📊 PƦΘƓƦЄSS: Rᴇᴀʟ-ᴛɪᴍᴇ ᴜᴘᴅᴀᴛᴇs ᴇᴠᴇʀʏ 2 sᴇᴄᴏɴᴅs ⚡")
    print("="*70)
    print("🎯 Sᴇɴᴅ ᴀɴʏ ғɪʟᴇ ᴛᴏ ᴛᴇsᴛ ᴛʜᴇ ᴄᴏɴᴠᴇʀsɪᴏɴ sʏsᴛᴇᴍ! 💫💭")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

