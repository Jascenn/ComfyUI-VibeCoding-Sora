"""
Custom Sora Video Node - 完整版
包含4个输出：text_result, thumbnail, video, video_path
完美匹配工作流需求
"""

import os
import requests
import json
import torch
import numpy as np
from PIL import Image
from io import BytesIO
import time
import re
import base64
import folder_paths


class CustomSoraVideoNode:
    """
    自定义 Sora 视频生成节点
    支持4个输出，完全匹配工作流参数

    生成模式：
    - 文生视频 (Text-to-Video): 仅使用提示词生成视频
    - 图生视频 (Image-to-Video): 连接图片输入，基于图片生成视频

    模型时长支持：
    - sora-2: 4-15秒（推荐10-15秒）
    - sora-2-pro: 4-25秒（推荐15-25秒）
    - sora-2-hd: 4-12秒
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_url": ("STRING", {
                    "default": "https://vibecodingapi.ai/v1/chat/completions",
                    "multiline": False,
                    "tooltip": "API 端点地址 / API endpoint URL"
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "留空使用环境变量 VIBECODING_API_KEY",
                    "tooltip": "API 密钥，可留空使用环境变量 VIBECODING_API_KEY / API Key, leave blank to use environment variable"
                }),
                "model": (["sora-2", "sora-2-pro", "sora-2-hd"], {
                    "tooltip": "选择模型 / Select model: sora-2 (标准), sora-2-pro (长视频), sora-2-hd (高清)"
                }),
                "prompt": ("STRING", {
                    "default": "A beautiful sunset over mountains",
                    "multiline": True,
                    "tooltip": "视频描述，必须使用英文 / Video description, English required"
                }),
                "size": (["1280x720", "1920x1080", "720x1280", "1080x1920", "1024x576"], {
                    "tooltip": "视频尺寸 / Video resolution"
                }),
                "duration": ("INT", {
                    "default": 8,
                    "min": 4,
                    "max": 25,
                    "step": 1,
                    "tooltip": "视频时长（秒）/ Video duration (seconds) | sora-2: 4-15s | sora-2-pro: 4-25s | sora-2-hd: 4-12s"
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "tooltip": "随机种子，控制生成结果 / Random seed, controls generation output"
                }),
                "control": (["fixed", "randomize"], {
                    "tooltip": "种子控制模式 / Seed control: fixed (固定种子) | randomize (随机生成)"
                }),
            },
            "optional": {
                "image": ("IMAGE", {
                    "tooltip": "可选图片输入，用于图生视频模式 / Optional image input for Image-to-Video mode"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "IMAGE", "VIDEO", "STRING")
    RETURN_NAMES = ("text_result", "thumbnail", "video", "video_path")
    FUNCTION = "generate_video"
    CATEGORY = "video/sora"

    def generate_video(self, api_url, api_key, model, prompt, size, duration, seed, control, image=None):
        """生成视频"""

        # 处理 seed
        if control == "randomize":
            seed = int(time.time() * 1000) % 0xffffffffffffffff

        # 使用环境变量 API Key
        if not api_key:
            api_key = os.getenv("VIBECODING_API_KEY", "")

        if not api_key:
            return self._error_output("❌ 错误: API Key 未设置\n请在节点中填入 API Key 或设置环境变量 VIBECODING_API_KEY")

        # 验证时长是否符合模型限制
        duration_limits = {
            "sora-2": (4, 15, "推荐10-15秒"),
            "sora-2-pro": (4, 25, "推荐15-25秒"),
            "sora-2-hd": (4, 12, "")
        }

        if model in duration_limits:
            min_dur, max_dur, recommend = duration_limits[model]
            if duration < min_dur or duration > max_dur:
                warning = f"⚠️ 警告: {model} 支持的时长范围是 {min_dur}-{max_dur}秒"
                if recommend:
                    warning += f"（{recommend}）"
                warning += f"\n当前设置: {duration}秒，可能会导致生成失败或效果不佳"
                print(warning)

        print(f"\n{'='*60}")
        print(f"🎬 CustomSoraVideo - 开始生成视频")
        print(f"{'='*60}")
        print(f"   模型: {model}")
        print(f"   提示词: {prompt[:100]}...")
        print(f"   尺寸: {size}")
        print(f"   时长: {duration}秒")
        print(f"   种子: {seed}")

        # 处理图片输入
        has_image = image is not None
        if has_image:
            print(f"   🖼️  图片输入: 已提供（图生视频模式）")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # 构建请求数据（与 API 文档保持一致）
        if has_image:
            # 图生视频模式：使用多模态消息格式
            image_base64 = self._image_to_base64(image)
            data = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            }
        else:
            # 文生视频模式：使用简单文本格式
            data = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }

        try:
            # 禁用代理（避免代理导致的连接问题）
            proxies = {
                "http": None,
                "https": None
            }

            print(f"🚀 发送请求到 API...")
            print(f"   URL: {api_url}")
            start_time = time.time()

            # 根据模型调整超时时间
            timeout_settings = {
                "sora-2": 600,      # 10分钟
                "sora-2-pro": 900,  # 15分钟（长视频需要更多时间）
                "sora-2-hd": 600    # 10分钟
            }
            timeout = timeout_settings.get(model, 600)

            response = requests.post(
                api_url,
                headers=headers,
                json=data,
                timeout=timeout,
                proxies=proxies
            )
            elapsed = time.time() - start_time

            print(f"⏱️  请求耗时: {elapsed:.1f} 秒")
            print(f"📊 响应状态码: {response.status_code}")

            if response.status_code == 200:
                result = response.json()

                # 提取视频 URL 或任务 ID
                video_url = None
                task_id = None
                task_url = None

                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0].get('message', {}).get('content', '')

                    # 提取视频链接（如果已经完成）
                    video_urls = re.findall(r'https://[^\s\)]+\.mp4', content)
                    if video_urls:
                        video_url = video_urls[0]
                        print(f"🎥 找到视频 URL: {video_url}")
                    else:
                        # 提取任务 ID（异步任务）
                        task_id_match = re.search(r'task_[a-z0-9]+', content)
                        if task_id_match:
                            task_id = task_id_match.group()
                            print(f"📋 检测到异步任务: {task_id}")

                            # 提取 Source Data URL
                            source_url_match = re.search(r'https://asyncdata\.net/source/([^\s\)]+)', content)
                            if source_url_match:
                                task_url = source_url_match.group(0)
                                print(f"🔗 任务数据链接: {task_url}")

                # 如果没有直接的视频 URL，尝试轮询任务
                if not video_url and task_id and task_url:
                    print(f"⏳ 等待视频生成完成...")
                    video_url = self._poll_task_completion(task_url, max_wait=600)

                if not video_url:
                    error_msg = "❌ 错误: 未找到视频URL\n\n完整响应:\n" + json.dumps(result, indent=2, ensure_ascii=False)
                    print(error_msg)
                    return self._error_output(error_msg)

                # 下载视频
                print(f"📥 开始下载视频...")
                video_path = self._download_video(video_url, model, seed)
                if not video_path:
                    return self._error_output("❌ 错误: 视频下载失败")

                # 生成缩略图
                print(f"🖼️  生成缩略图...")
                thumbnail = self._generate_thumbnail(video_path)

                # 生成文本结果
                text_result = self._format_text_result(
                    model, prompt, size, duration, seed,
                    video_url, video_path, elapsed, result
                )

                # 生成 VIDEO 元数据 (VHS 兼容格式)
                # 提取文件名（不含路径）
                filename = os.path.basename(video_path)

                video_meta = {
                    "filename": filename,
                    "subfolder": "",
                    "type": "output",
                    "format": "video/h264-mp4",
                    "frame_rate": 30
                }

                print(f"{'='*60}")
                print(f"✅ 视频生成成功！")
                print(f"📁 保存路径: {video_path}")
                print(f"{'='*60}\n")

                return (text_result, thumbnail, video_meta, video_path)

            else:
                error_msg = f"❌ API 错误 {response.status_code}\n\n错误信息:\n{response.text}"
                print(error_msg)
                return self._error_output(error_msg)

        except requests.exceptions.Timeout:
            timeout_minutes = timeout / 60
            error_msg = f"❌ 请求超时: 视频生成时间过长（>{timeout_minutes:.0f}分钟）\n"
            error_msg += f"模型: {model}\n"
            error_msg += f"建议: \n- 检查 API 服务状态\n- 尝试生成更短的视频\n- 稍后重试"
            print(error_msg)
            return self._error_output(error_msg)

        except requests.exceptions.RequestException as e:
            error_msg = f"❌ 网络请求失败: {str(e)}\n\n可能原因:\n- 网络连接问题\n- API 服务器不可达\n- 代理设置问题"
            print(error_msg)
            return self._error_output(error_msg)

        except Exception as e:
            error_msg = f"❌ 请求异常: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            return self._error_output(error_msg)

    def _poll_task_completion(self, task_url, max_wait=600):
        """
        轮询任务完成状态

        Args:
            task_url: 任务数据 URL（如 https://asyncdata.net/source/task_xxx）
            max_wait: 最大等待时间（秒），默认 10 分钟

        Returns:
            video_url: 视频 URL，如果失败返回 None
        """
        start_time = time.time()
        poll_interval = 5  # 每 5 秒轮询一次
        attempt = 0

        proxies = {"http": None, "https": None}

        while time.time() - start_time < max_wait:
            attempt += 1
            elapsed = time.time() - start_time

            try:
                print(f"   🔄 轮询 #{attempt} (已等待 {elapsed:.0f}秒)...", end=' ')

                # 请求任务状态
                response = requests.get(task_url, timeout=30, proxies=proxies)

                if response.status_code == 200:
                    content = response.text

                    # 尝试提取视频 URL
                    video_urls = re.findall(r'https://[^\s\)"<]+\.mp4', content)

                    if video_urls:
                        video_url = video_urls[0]
                        print(f"✅ 完成！")
                        print(f"🎥 视频 URL: {video_url}")
                        return video_url
                    else:
                        # 检查是否还在生成中
                        if 'Progress' in content or 'Generating' in content or 'Queuing' in content:
                            print(f"⏳ 生成中...")
                        else:
                            print(f"⏳ 等待中...")
                else:
                    print(f"⚠️  HTTP {response.status_code}")

            except Exception as e:
                print(f"⚠️  请求失败: {str(e)}")

            # 等待后再次轮询
            time.sleep(poll_interval)

        # 超时
        print(f"\n❌ 轮询超时: 等待了 {max_wait} 秒仍未完成")
        return None

    def _download_video(self, url, model, seed):
        """下载视频到本地"""
        try:
            # 生成文件名
            timestamp = int(time.time())
            filename = f"custom_sora_{model}_{timestamp}.mp4"

            # 获取 output 目录
            output_dir = folder_paths.get_output_directory()
            video_path = os.path.join(output_dir, filename)

            print(f"   保存位置: {video_path}")

            # 下载视频（禁用代理）
            proxies = {"http": None, "https": None}
            response = requests.get(url, timeout=300, stream=True, proxies=proxies)

            if response.status_code == 200:
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0

                with open(video_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)

                        # 显示下载进度
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r   下载进度: {progress:.1f}%", end='', flush=True)

                print()  # 换行

                file_size = os.path.getsize(video_path)
                print(f"✅ 视频下载完成: {filename} ({file_size / 1024 / 1024:.2f} MB)")
                return video_path
            else:
                print(f"❌ 下载失败: HTTP {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ 下载异常: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def _generate_thumbnail(self, video_path):
        """从视频提取第一帧作为缩略图"""
        try:
            import cv2

            # 打开视频
            cap = cv2.VideoCapture(video_path)
            ret, frame = cap.read()
            cap.release()

            if ret:
                # 转换为 RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # 转换为 PIL Image
                pil_image = Image.fromarray(frame_rgb)

                # 转换为 ComfyUI IMAGE 格式 (B, H, W, C)
                image_np = np.array(pil_image).astype(np.float32) / 255.0
                image_tensor = torch.from_numpy(image_np)[None,]

                print(f"✅ 缩略图生成成功 (尺寸: {frame_rgb.shape[1]}x{frame_rgb.shape[0]})")
                return image_tensor
            else:
                print(f"⚠️  无法提取视频帧，使用占位图")
                return self._create_placeholder_image()

        except ImportError:
            print(f"⚠️  opencv-python 未安装，使用占位图")
            print(f"   安装方法: pip install opencv-python")
            return self._create_placeholder_image()

        except Exception as e:
            print(f"⚠️  缩略图生成失败: {str(e)}，使用占位图")
            return self._create_placeholder_image()

    def _create_placeholder_image(self):
        """创建占位图"""
        # 创建 512x512 灰色图片，中间显示文字
        img = Image.new('RGB', (512, 512), color=(64, 64, 64))
        image_np = np.array(img).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np)[None,]
        return image_tensor

    def _image_to_base64(self, image_tensor):
        """
        将 ComfyUI IMAGE tensor 转换为 base64 编码字符串

        Args:
            image_tensor: ComfyUI IMAGE 格式 (B, H, W, C)，值范围 [0, 1]

        Returns:
            base64_str: base64 编码的图片字符串
        """
        try:
            # 从 tensor 转换为 numpy 数组
            # ComfyUI IMAGE 格式: (Batch, Height, Width, Channels)，值范围 [0, 1]
            image_np = image_tensor[0].cpu().numpy()  # 取第一张图片

            # 转换为 0-255 范围的 uint8
            image_np = (image_np * 255).astype(np.uint8)

            # 转换为 PIL Image
            pil_image = Image.fromarray(image_np)

            # 转换为 base64
            buffered = BytesIO()
            pil_image.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

            print(f"   ✅ 图片转换成功 (尺寸: {pil_image.size[0]}x{pil_image.size[1]})")
            return image_base64

        except Exception as e:
            print(f"   ⚠️  图片转换失败: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

    def _format_text_result(self, model, prompt, size, duration, seed, video_url, video_path, elapsed, api_result):
        """格式化文本结果"""

        # 提取任务信息
        task_id = "N/A"
        timestamp = int(time.time())

        if 'choices' in api_result and len(api_result['choices']) > 0:
            content = api_result['choices'][0].get('message', {}).get('content', '')
            task_id_match = re.search(r'task_[a-z0-9]+', content)
            if task_id_match:
                task_id = task_id_match.group()

        # 提取 token 使用
        tokens = api_result.get('usage', {}).get('total_tokens', 0)

        # 获取文件信息
        file_size = 0
        filename = os.path.basename(video_path)
        if os.path.exists(video_path):
            file_size = os.path.getsize(video_path) / 1024 / 1024  # MB

        # 生成时间
        from datetime import datetime
        gen_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        # 格式化输出
        output = []
        output.append("✅ 视频生成成功！")
        output.append("")
        output.append("📋 生成信息:")
        output.append(f"- 模型: {model}")
        output.append(f"- 提示词: {prompt[:80]}...")
        output.append(f"- 尺寸: {size}")
        output.append(f"- 时长: {duration}秒")
        output.append(f"- 种子: {seed}")
        output.append("")
        output.append("🆔 任务信息:")
        output.append(f"- Task ID: {task_id}")
        output.append(f"- 生成时间: {gen_time}")
        output.append(f"- API 时间戳: {timestamp}")
        if tokens > 0:
            output.append(f"💰 Token 使用: {tokens} tokens")
        output.append("")
        output.append("🔗 视频 URL:")
        output.append(video_url)
        output.append("")
        output.append("📁 本地路径:")
        output.append(video_path)
        output.append("")
        output.append("📄 文件信息:")
        output.append(f"- 文件名: {filename}")
        output.append(f"- 文件大小: {file_size:.2f} MB")
        output.append(f"- 格式: MP4")

        return "\n".join(output)

    def _error_output(self, error_msg):
        """返回错误输出"""
        placeholder_image = self._create_placeholder_image()
        video_meta = {"source_path": "", "frame_rate": 0, "duration": 0}
        return (error_msg, placeholder_image, video_meta, "")


# 节点注册
NODE_CLASS_MAPPINGS = {
    "CustomSoraVideo": CustomSoraVideoNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CustomSoraVideo": "Custom Sora Video",
}
