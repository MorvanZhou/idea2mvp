#!/usr/bin/env python3
"""
邮件通知 - 通过 SMTP 发送邮件通知

将搜索报告或其他文本内容通过邮件发送给用户。
支持从 stdin、文件或命令行参数传入内容。

需要环境变量（在 .env.idea2mvp 中配置）：
  EMAIL_SMTP_HOST     — SMTP 服务器地址（如 smtp.qq.com、smtp.gmail.com）
  EMAIL_SMTP_PORT     — SMTP 端口（默认 465，SSL）
  EMAIL_SENDER        — 发件人邮箱
  EMAIL_PASSWORD       — 邮箱授权码（非登录密码）
  EMAIL_RECEIVER      — 收件人邮箱

使用方式：
  # 发送文本内容
  python3 send_email.py --subject "工具探索报告" --body "报告正文内容..."

  # 从文件读取内容发送
  python3 send_email.py --subject "工具探索报告" --file tmp/ph_results.txt

  # 发送多个文件内容（合并为一封邮件）
  python3 send_email.py --subject "工具探索报告" --file tmp/ph_results.txt tmp/github_results.txt

  # 从 stdin 读取内容
  cat tmp/ph_results.txt | python3 send_email.py --subject "工具探索报告"

  # 指定收件人（覆盖 .env 中的默认收件人）
  python3 send_email.py --subject "报告" --body "内容" --to someone@example.com

结果输出到 stdout，确认发送成功或失败。
"""

import argparse
import os
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_env


def send_email(subject, body, receiver=None):
    """通过 SMTP 发送邮件。

    Args:
        subject: 邮件主题
        body: 邮件正文（纯文本）
        receiver: 收件人邮箱，为 None 时使用 .env 中的 EMAIL_RECEIVER

    Returns:
        True 成功，False 失败
    """
    host = os.environ.get("EMAIL_SMTP_HOST", "")
    port = int(os.environ.get("EMAIL_SMTP_PORT", "465"))
    sender = os.environ.get("EMAIL_SENDER", "")
    password = os.environ.get("EMAIL_PASSWORD", "")
    receiver = receiver or os.environ.get("EMAIL_RECEIVER", "")

    missing = []
    if not host:
        missing.append("EMAIL_SMTP_HOST")
    if not sender:
        missing.append("EMAIL_SENDER")
    if not password:
        missing.append("EMAIL_PASSWORD")
    if not receiver:
        missing.append("EMAIL_RECEIVER")
    if missing:
        print(f"❌ 缺少邮件配置：{', '.join(missing)}", flush=True)
        print("   请在 .env.idea2mvp 中配置邮件相关参数。", flush=True)
        return False

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        if port == 465:
            server = smtplib.SMTP_SSL(host, port, timeout=15)
        else:
            server = smtplib.SMTP(host, port, timeout=15)
            server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        print(f"✅ 邮件已发送至 {receiver}", flush=True)
        return True
    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP 认证失败，请检查邮箱和授权码是否正确。", flush=True)
        return False
    except smtplib.SMTPException as e:
        print(f"❌ 邮件发送失败：{e}", flush=True)
        return False
    except Exception as e:
        print(f"❌ 连接 SMTP 服务器失败：{e}", flush=True)
        return False


def main():
    parser = argparse.ArgumentParser(description="通过 SMTP 发送邮件通知")
    parser.add_argument("--subject", "-s", required=True, help="邮件主题")
    parser.add_argument("--body", "-b", help="邮件正文（纯文本）")
    parser.add_argument("--file", "-f", nargs="+", help="从文件读取正文内容（支持多个文件，合并发送）")
    parser.add_argument("--to", help="收件人邮箱（覆盖 .env 中的 EMAIL_RECEIVER）")
    args = parser.parse_args()

    load_env()

    body_parts = []

    if args.body:
        body_parts.append(args.body)

    if args.file:
        for filepath in args.file:
            if not os.path.exists(filepath):
                print(f"⚠️ 文件不存在，跳过：{filepath}", flush=True)
                continue
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:
                body_parts.append(f"=== {os.path.basename(filepath)} ===\n\n{content}")

    if not body_parts and not sys.stdin.isatty():
        stdin_content = sys.stdin.read().strip()
        if stdin_content:
            body_parts.append(stdin_content)

    if not body_parts:
        print("❌ 没有邮件内容。请通过 --body、--file 或 stdin 提供内容。", flush=True)
        sys.exit(1)

    body = "\n\n".join(body_parts)
    success = send_email(args.subject, body, receiver=args.to)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
