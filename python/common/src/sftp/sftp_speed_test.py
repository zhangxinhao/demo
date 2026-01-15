# -*- coding: utf-8 -*-
"""
SFTP 上传下载速率测试模块

使用 paramiko 实现 SFTP 连接，测试上传和下载速率
使用 tqdm 显示进度条
"""

import os
import time
from typing import Optional

import paramiko
from tqdm import tqdm

from common.env_var import EnvVar
from common.path_type import PathType
from utils.path_manager import get_path_manager
from utils.settings import get_settings


class SFTPSpeedTest:
    """SFTP 速率测试类"""

    def __init__(self):
        self._settings = get_settings()
        self._path_manager = get_path_manager()
        self._ssh_client: Optional[paramiko.SSHClient] = None
        self._sftp: Optional[paramiko.SFTPClient] = None

        # 加载 SFTP 配置
        self._host = self._settings.get(EnvVar.SFTP_HOST)
        self._port = self._settings.get(EnvVar.SFTP_PORT)
        self._username = self._settings.get(EnvVar.SFTP_USERNAME)
        self._password = self._settings.get(EnvVar.SFTP_PASSWORD)

        # 本地测试数据目录
        self._local_sftp_dir = self._path_manager.get_dir(PathType.SFTP)
        self._path_manager.ensure_dir_exists(PathType.SFTP)

        # 远程测试目录
        self._remote_test_dir = "/tmp/sftp_speed_test"

    def _validate_config(self) -> bool:
        """验证 SFTP 配置"""
        if not self._host:
            print("Error: SFTP_HOST is not configured")
            return False
        if not self._username:
            print("Error: SFTP_USERNAME is not configured")
            return False
        if not self._password:
            print("Error: SFTP_PASSWORD is not configured")
            return False
        return True

    def connect(self) -> bool:
        """建立 SFTP 连接"""
        if not self._validate_config():
            return False

        try:
            print(f"Connecting to {self._host}:{self._port}...")

            # 创建 SSH 客户端
            self._ssh_client = paramiko.SSHClient()
            self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # 连接到服务器
            self._ssh_client.connect(
                hostname=self._host,
                port=self._port,
                username=self._username,
                password=self._password,
                timeout=30
            )

            # 创建 SFTP 客户端
            self._sftp = self._ssh_client.open_sftp()
            print("SFTP connection established successfully")

            # 确保远程测试目录存在
            self._ensure_remote_dir_exists(self._remote_test_dir)

            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False

    def _ensure_remote_dir_exists(self, remote_path: str) -> None:
        """确保远程目录存在"""
        try:
            self._sftp.stat(remote_path)
        except FileNotFoundError:
            self._sftp.mkdir(remote_path)
            print(f"Created remote test directory: {remote_path}")

    def disconnect(self) -> None:
        """断开 SFTP 连接"""
        if self._sftp:
            self._sftp.close()
            self._sftp = None
        if self._ssh_client:
            self._ssh_client.close()
            self._ssh_client = None
        print("SFTP connection closed")

    def generate_test_file(self, size_mb: float = 10) -> str:
        """
        生成测试文件
        
        Args:
            size_mb: 文件大小（MB）
            
        Returns:
            测试文件路径
        """
        filename = f"test_file_{size_mb}mb.bin"
        filepath = os.path.join(self._local_sftp_dir, filename)

        if os.path.exists(filepath):
            existing_size = os.path.getsize(filepath) / (1024 * 1024)
            if abs(existing_size - size_mb) < 0.01:
                print(f"Test file already exists: {filepath}")
                return filepath

        print(f"Generating test file: {filepath} ({size_mb} MB)...")
        size_bytes = int(size_mb * 1024 * 1024)
        chunk_size = 1024 * 1024  # 1MB 块

        with open(filepath, "wb") as f:
            with tqdm(total=size_bytes, unit="B", unit_scale=True, desc="生成测试文件") as pbar:
                remaining = size_bytes
                while remaining > 0:
                    write_size = min(chunk_size, remaining)
                    # 生成随机数据
                    data = os.urandom(write_size)
                    f.write(data)
                    remaining -= write_size
                    pbar.update(write_size)

        print(f"Test file generated: {filepath}")
        return filepath

    def test_upload(self, local_file: str) -> dict:
        """
        测试上传速率
        
        Args:
            local_file: 本地文件路径
            
        Returns:
            包含测试结果的字典
        """
        if not self._sftp:
            print("Error: Not connected to SFTP server")
            return {}

        if not os.path.exists(local_file):
            print(f"Error: Local file not found: {local_file}")
            return {}

        filename = os.path.basename(local_file)
        remote_file = f"{self._remote_test_dir}/{filename}"
        file_size = os.path.getsize(local_file)

        print(f"\n{'=' * 60}")
        print(f"开始上传测试: {filename}")
        print(f"文件大小: {file_size / (1024 * 1024):.2f} MB")
        print(f"{'=' * 60}")

        try:
            with tqdm(total=file_size, unit="B", unit_scale=True, desc="上传进度") as pbar:
                def callback(transferred: int, total: int) -> None:
                    pbar.n = transferred
                    pbar.refresh()

                start_time = time.time()
                self._sftp.put(local_file, remote_file, callback=callback)
                end_time = time.time()

            duration = end_time - start_time
            speed_mbps = (file_size / (1024 * 1024)) / duration if duration > 0 else 0

            result = {
                "type": "upload",
                "filename": filename,
                "file_size_bytes": file_size,
                "file_size_mb": file_size / (1024 * 1024),
                "duration_seconds": duration,
                "speed_mbps": speed_mbps
            }

            print(f"\n上传完成!")
            print(f"耗时: {duration:.2f} 秒")
            print(f"速率: {speed_mbps:.2f} MB/s")

            return result

        except Exception as e:
            print(f"Upload failed: {e}")
            return {}

    def test_download(self, remote_filename: str) -> dict:
        """
        测试下载速率
        
        Args:
            remote_filename: 远程文件名（在远程测试目录中）
            
        Returns:
            包含测试结果的字典
        """
        if not self._sftp:
            print("Error: Not connected to SFTP server")
            return {}

        remote_file = f"{self._remote_test_dir}/{remote_filename}"
        local_file = os.path.join(self._local_sftp_dir, f"download_{remote_filename}")

        # 获取远程文件大小
        try:
            file_size = self._sftp.stat(remote_file).st_size
        except Exception as e:
            print(f"Error: Remote file not found: {remote_file}")
            return {}

        print(f"\n{'=' * 60}")
        print(f"开始下载测试: {remote_filename}")
        print(f"文件大小: {file_size / (1024 * 1024):.2f} MB")
        print(f"{'=' * 60}")

        try:
            with tqdm(total=file_size, unit="B", unit_scale=True, desc="下载进度") as pbar:
                def callback(transferred: int, total: int) -> None:
                    pbar.n = transferred
                    pbar.refresh()

                start_time = time.time()
                self._sftp.get(remote_file, local_file, callback=callback)
                end_time = time.time()

            duration = end_time - start_time
            speed_mbps = (file_size / (1024 * 1024)) / duration if duration > 0 else 0

            result = {
                "type": "download",
                "filename": remote_filename,
                "file_size_bytes": file_size,
                "file_size_mb": file_size / (1024 * 1024),
                "duration_seconds": duration,
                "speed_mbps": speed_mbps
            }

            print(f"\n下载完成!")
            print(f"耗时: {duration:.2f} 秒")
            print(f"速率: {speed_mbps:.2f} MB/s")

            # 删除下载的临时文件
            if os.path.exists(local_file):
                os.remove(local_file)
                print(f"Cleaned up temporary file: {local_file}")

            return result

        except Exception as e:
            print(f"Download failed: {e}")
            return {}

    def run_speed_test(self, file_sizes_mb: list = None) -> list:
        """
        运行完整的速率测试
        
        Args:
            file_sizes_mb: 测试文件大小列表（MB），默认 [1, 10, 50]
            
        Returns:
            所有测试结果的列表
        """
        if file_sizes_mb is None:
            file_sizes_mb = [1, 10, 50]

        results = []

        if not self.connect():
            return results

        try:
            for size_mb in file_sizes_mb:
                print(f"\n{'#' * 60}")
                print(f"测试文件大小: {size_mb} MB")
                print(f"{'#' * 60}")

                # 生成测试文件
                test_file = self.generate_test_file(size_mb)

                # 测试上传
                upload_result = self.test_upload(test_file)
                if upload_result:
                    results.append(upload_result)

                # 测试下载
                download_result = self.test_download(os.path.basename(test_file))
                if download_result:
                    results.append(download_result)

            # 打印汇总结果
            self._print_summary(results)

        finally:
            self.disconnect()

        return results

    def _print_summary(self, results: list) -> None:
        """打印测试结果汇总"""
        if not results:
            print("\n没有测试结果")
            return

        print(f"\n{'=' * 60}")
        print("测试结果汇总")
        print(f"{'=' * 60}")
        print(f"{'类型':<10} {'文件大小(MB)':<15} {'耗时(秒)':<15} {'速率(MB/s)':<15}")
        print(f"{'-' * 60}")

        for r in results:
            type_str = "上传" if r["type"] == "upload" else "下载"
            print(f"{type_str:<10} {r['file_size_mb']:<15.2f} {r['duration_seconds']:<15.2f} {r['speed_mbps']:<15.2f}")

        # 计算平均速率
        upload_results = [r for r in results if r["type"] == "upload"]
        download_results = [r for r in results if r["type"] == "download"]

        if upload_results:
            avg_upload = sum(r["speed_mbps"] for r in upload_results) / len(upload_results)
            print(f"\n平均上传速率: {avg_upload:.2f} MB/s")

        if download_results:
            avg_download = sum(r["speed_mbps"] for r in download_results) / len(download_results)
            print(f"平均下载速率: {avg_download:.2f} MB/s")

    def cleanup_remote(self) -> None:
        """清理远程测试文件"""
        if not self.connect():
            return

        try:
            try:
                files = self._sftp.listdir(self._remote_test_dir)
                for f in files:
                    remote_path = f"{self._remote_test_dir}/{f}"
                    self._sftp.remove(remote_path)
                    print(f"Deleted remote file: {remote_path}")

                # 删除目录
                self._sftp.rmdir(self._remote_test_dir)
                print(f"Deleted remote directory: {self._remote_test_dir}")
            except FileNotFoundError:
                print(f"Remote directory not found: {self._remote_test_dir}")
        except Exception as e:
            print(f"Cleanup failed: {e}")
        finally:
            self.disconnect()

    def cleanup_local(self) -> None:
        """清理本地测试文件"""
        for filename in os.listdir(self._local_sftp_dir):
            if filename.startswith("test_file_") or filename.startswith("download_"):
                filepath = os.path.join(self._local_sftp_dir, filename)
                os.remove(filepath)
                print(f"Deleted local file: {filepath}")


def main():
    """主函数"""
    tester = SFTPSpeedTest()

    # 运行速率测试（使用 1MB 和 10MB 文件）
    tester.run_speed_test(file_sizes_mb=[1, 10])

    # 可选：清理测试文件
    # tester.cleanup_remote()
    # tester.cleanup_local()


if __name__ == "__main__":
    main()
