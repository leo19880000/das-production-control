#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
로컬 네트워크에서 접속 가능하게 실행

실행 방법:
python run_server.py

그러면 같은 와이파이에 연결된 다른 컴퓨터/폰에서도 접속 가능!
"""

import subprocess
import socket

# 내 IP 주소 찾기
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print("=" * 60)
print("🌐 다스 생산 통제 시스템 서버 시작")
print("=" * 60)
print()
print(f"📍 이 컴퓨터에서 접속: http://localhost:8501")
print(f"📍 다른 컴퓨터에서 접속: http://{local_ip}:8501")
print()
print("💡 같은 와이파이에 연결된 모든 기기에서 접속 가능!")
print()
print("종료하려면 Ctrl+C 누르세요")
print("=" * 60)
print()

# Streamlit 실행 (외부 접속 허용)
subprocess.run([
    "streamlit", "run", "production_control.py",
    "--server.address", "0.0.0.0",
    "--server.port", "8501"
])
