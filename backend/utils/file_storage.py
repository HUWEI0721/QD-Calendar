"""
本地文件存储助手
替代 OSS，使用本地文件系统存储图片
"""
import os
import uuid
from datetime import datetime
from flask import current_app, url_for
from werkzeug.utils import secure_filename
from pathlib import Path


class FileStorage:
    """本地文件存储助手"""
    
    def __init__(self):
        self.upload_folder = None
        self.base_url = None
        self._init_storage()
    
    def _init_storage(self):
        """初始化存储目录"""
        try:
            # 获取上传文件夹路径（相对于项目根目录）
            self.upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
            
            # 如果是相对路径，转换为绝对路径
            if not os.path.isabs(self.upload_folder):
                # 获取项目根目录（backend 的父目录）
                backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                self.upload_folder = os.path.join(backend_dir, self.upload_folder)
            
            # 创建上传目录
            os.makedirs(self.upload_folder, exist_ok=True)
            
            # 获取基础 URL（用于生成访问路径）
            self.base_url = current_app.config.get('FILE_SERVER_URL', '/uploads')
            
            current_app.logger.info("=" * 60)
            current_app.logger.info("文件存储初始化:")
            current_app.logger.info(f"  存储路径: {self.upload_folder}")
            current_app.logger.info(f"  访问路径: {self.base_url}")
            current_app.logger.info("=" * 60)
            current_app.logger.info("✅ 本地文件存储初始化成功!")
            
        except Exception as e:
            current_app.logger.error("=" * 60)
            current_app.logger.error(f"❌ 文件存储初始化失败: {str(e)}")
            import traceback
            current_app.logger.error(f"   详细错误:\n{traceback.format_exc()}")
            current_app.logger.error("=" * 60)
    
    def upload_file(self, file_obj, folder='events'):
        """
        保存文件到本地
        
        Args:
            file_obj: 文件对象
            folder: 子文件夹名称（默认 'events'）
            
        Returns:
            dict: 包含文件访问 URL
                {
                    'url': '/uploads/events/2025/10/30/abc123.jpg',
                    'filename': 'abc123.jpg',
                    'filepath': '/absolute/path/to/file.jpg'
                }
        """
        if not self.upload_folder:
            current_app.logger.error("❌ 文件存储未初始化")
            return None
        
        try:
            # 读取文件内容
            file_content = file_obj.read()
            
            # 生成安全的文件名
            original_filename = secure_filename(file_obj.filename)
            ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
            
            # 生成唯一文件名：日期_UUID.扩展名
            date_str = datetime.now().strftime('%Y%m%d')
            unique_id = uuid.uuid4().hex[:12]  # 使用12位UUID
            new_filename = f"{date_str}_{unique_id}.{ext}"
            
            # 创建子目录结构：uploads/events/2025/10/30/
            date_path = datetime.now().strftime('%Y/%m/%d')
            full_folder = os.path.join(self.upload_folder, folder, date_path)
            os.makedirs(full_folder, exist_ok=True)
            
            # 完整的文件路径
            file_path = os.path.join(full_folder, new_filename)
            
            # 保存文件
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            # 生成访问 URL（相对路径）
            relative_path = f"{folder}/{date_path}/{new_filename}"
            file_url = f"{self.base_url}/{relative_path}"
            
            current_app.logger.info(f"✅ 文件保存成功:")
            current_app.logger.info(f"   文件名: {new_filename}")
            current_app.logger.info(f"   路径: {file_path}")
            current_app.logger.info(f"   URL: {file_url}")
            current_app.logger.info(f"   大小: {len(file_content)} bytes")
            
            return {
                'url': file_url,
                'filename': new_filename,
                'filepath': file_path,
                'size': len(file_content)
            }
            
        except Exception as e:
            current_app.logger.error(f"❌ 文件保存失败: {str(e)}")
            import traceback
            current_app.logger.error(traceback.format_exc())
            return None
    
    def delete_file(self, file_url):
        """
        删除本地文件
        
        Args:
            file_url: 文件 URL（如 '/uploads/events/2025/10/30/abc123.jpg'）
            
        Returns:
            bool: 是否删除成功
        """
        if not file_url:
            return False
        
        try:
            # 从 URL 提取相对路径
            if file_url.startswith(self.base_url):
                relative_path = file_url[len(self.base_url):].lstrip('/')
            else:
                # 尝试提取 /uploads/ 后面的部分
                if '/uploads/' in file_url:
                    relative_path = file_url.split('/uploads/')[1]
                else:
                    current_app.logger.warning(f"无法解析文件 URL: {file_url}")
                    return False
            
            # 构建完整路径
            file_path = os.path.join(self.upload_folder, relative_path)
            
            # 检查文件是否存在
            if os.path.exists(file_path):
                os.remove(file_path)
                current_app.logger.info(f"✅ 文件删除成功: {file_path}")
                
                # 尝试删除空目录
                self._cleanup_empty_dirs(os.path.dirname(file_path))
                return True
            else:
                current_app.logger.warning(f"文件不存在: {file_path}")
                return False
                
        except Exception as e:
            current_app.logger.error(f"❌ 文件删除失败: {str(e)}")
            return False
    
    def file_exists(self, file_url):
        """
        检查文件是否存在
        
        Args:
            file_url: 文件 URL
            
        Returns:
            bool: 文件是否存在
        """
        if not file_url:
            return False
        
        try:
            # 从 URL 提取相对路径
            if file_url.startswith(self.base_url):
                relative_path = file_url[len(self.base_url):].lstrip('/')
            elif '/uploads/' in file_url:
                relative_path = file_url.split('/uploads/')[1]
            else:
                return False
            
            # 构建完整路径
            file_path = os.path.join(self.upload_folder, relative_path)
            
            return os.path.exists(file_path) and os.path.isfile(file_path)
            
        except Exception as e:
            current_app.logger.error(f"检查文件存在性失败: {str(e)}")
            return False
    
    def get_file_path(self, file_url):
        """
        获取文件的完整路径
        
        Args:
            file_url: 文件 URL
            
        Returns:
            str: 文件的完整路径，不存在则返回 None
        """
        if not file_url:
            return None
        
        try:
            # 从 URL 提取相对路径
            if file_url.startswith(self.base_url):
                relative_path = file_url[len(self.base_url):].lstrip('/')
            elif '/uploads/' in file_url:
                relative_path = file_url.split('/uploads/')[1]
            else:
                return None
            
            # 构建完整路径
            file_path = os.path.join(self.upload_folder, relative_path)
            
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return file_path
            return None
            
        except Exception as e:
            current_app.logger.error(f"获取文件路径失败: {str(e)}")
            return None
    
    def _cleanup_empty_dirs(self, dir_path):
        """清理空目录"""
        try:
            # 只清理 uploads 目录下的空文件夹
            if not dir_path.startswith(self.upload_folder):
                return
            
            # 如果目录为空，删除它
            if os.path.isdir(dir_path) and not os.listdir(dir_path):
                os.rmdir(dir_path)
                current_app.logger.info(f"清理空目录: {dir_path}")
                
                # 递归清理父目录
                parent_dir = os.path.dirname(dir_path)
                if parent_dir != self.upload_folder:
                    self._cleanup_empty_dirs(parent_dir)
        except Exception as e:
            # 清理失败不影响主流程
            pass
    
    def get_file_info(self, file_url):
        """
        获取文件信息
        
        Args:
            file_url: 文件 URL
            
        Returns:
            dict: 文件信息（大小、创建时间等）
        """
        file_path = self.get_file_path(file_url)
        if not file_path:
            return None
        
        try:
            stat = os.stat(file_path)
            return {
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'exists': True
            }
        except Exception as e:
            current_app.logger.error(f"获取文件信息失败: {str(e)}")
            return None


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

