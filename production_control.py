#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
다스 생산 통제 시스템
====================

전체 공정 한눈에 보기 + 공정별 지시사항
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import openpyxl

# 페이지 설정
st.set_page_config(
    page_title="다스 생산 통제 시스템",
    page_icon="🔥",
    layout="wide"
)

# 제목
st.title("🔥 다스 생산 통제 시스템")
st.caption(f"실시간 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

st.markdown("---")

# === 파일 업로드 ===
col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 재고 파일 업로드")
    stock_file = st.file_uploader("재고.xlsx", type=['xlsx'])

with col2:
    st.subheader("📂 BOM 파일 (자동 감지)")
    st.caption("BOM 파일들을 같은 폴더에 넣어주세요")

st.markdown("---")

# === 샘플 데이터 또는 실제 데이터 ===
if stock_file is None:
    st.warning("⚠️ 재고 파일을 업로드해주세요. 샘플 데이터로 시연합니다.")
    use_sample = True
else:
    use_sample = False

# === 납품 계획 입력 ===
st.subheader("📅 납품 계획 입력")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    delivery_date = st.date_input("납품일", datetime.now())
with col2:
    delivery_time = st.time_input("납품시간", datetime.strptime("17:00", "%H:%M").time())
with col3:
    product_type = st.selectbox("제품", ["MV 4축", "MV 6축", "ME 4축", "ME 6축", "MV 독립 RH", "MV 독립 LH", "MV 스위블 LH"])
with col4:
    product_code_map = {
        "MV 4축": "28600-MV740",
        "MV 6축": "22100-MV760",
        "ME 4축": "28600-ME740",
        "ME 6축": "22100-ME760",
        "MV 독립 RH": "22200-MV600",
        "MV 독립 LH": "22100-MV600",
        "MV 스위블 LH": "24000-MV610",
    }
    product_code = product_code_map[product_type]
    st.text_input("제품코드", product_code, disabled=True)
with col5:
    quantity = st.number_input("수량", min_value=1, value=74)

if st.button("➕ 분석 시작", type="primary"):
    st.markdown("---")
    
    # === 샘플 데이터 (실제로는 파일에서 로드) ===
    st.subheader("📊 전체 공정 상황")
    
    # 테이블 데이터
    data = {
        "레벨": ["L1 완제품", "L2 도장품", "L3 반제품", "프레스", "프레스", "프레스", "구매품"],
        "품번": ["CA91-14782A", "CA95-80449A", "CA95-80448A", "CA70-21465A", "CA70-21466A", "CA70-70264A", "S0101PO0172"],
        "품명": ["MV 4축 완제품", "MV 4축 도장품", "MV 4축 반제품", "프레스 부품1", "프레스 부품2", "프레스 부품3", "볼트"],
        "필요수량": [74, 74, 74, 148, 148, 148, 148],
        "재고수량": [72, 50, 10, 150, 0, 4270, "?"],
        "부족수량": [2, 24, 64, 0, 148, 0, "?"],
        "상태": ["🔴 부족", "🔴 부족", "🔴 부족", "✅ 충분", "🔴 긴급", "✅ 충분", "⚠️ 확인필요"],
        "담당": ["조립팀", "도장팀", "용접팀", "프레스팀", "프레스팀", "프레스팀", "구매팀"],
    }
    
    df = pd.DataFrame(data)
    
    # 스타일 적용
    def highlight_status(row):
        if "🔴" in str(row["상태"]):
            return ['background-color: #ffcccc'] * len(row)
        elif "⚠️" in str(row["상태"]):
            return ['background-color: #fff3cd'] * len(row)
        else:
            return ['background-color: #d4edda'] * len(row)
    
    st.dataframe(
        df.style.apply(highlight_status, axis=1),
        use_container_width=True,
        height=300
    )
    
    st.markdown("---")
    
    # === 긴급 지시사항 ===
    st.subheader("🚨 긴급 지시사항")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔴 즉시 실행 (긴급)")
        
        st.error("""
        **1. 프레스팀 김팀장**
        - CA70-21466A: 148개 긴급 생산!
        - 시작: 지금 즉시
        - 완료: 12:00 예상
        - 소요시간: 3시간
        """)
        
        st.warning("""
        **2. 용접팀 박과장**
        - CA95-80448A: 64개 생산
        - 시작: 12:00 (프레스 완료 후)
        - 완료: 16:00
        - 소요시간: 4시간
        """)
    
    with col2:
        st.markdown("### 🟡 후속 작업")
        
        st.warning("""
        **3. 도장팀 이과장**
        - CA95-80449A: 24개 긴급 도장
        - 시작: 14:00
        - 완료: 17:00 (긴급 3시간)
        - ⚠️ 일반 도장 8시간 → 긴급 단축!
        """)
        
        st.info("""
        **4. 조립팀 최반장**
        - CA91-14782A: 2개 조립
        - 시작: 15:00
        - 완료: 17:00
        - 소요시간: 2시간
        """)
    
    st.markdown("---")
    
    # === 타임라인 ===
    st.subheader("⏰ 생산 타임라인")
    
    timeline_data = {
        "시간": ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"],
        "프레스팀": ["🔴 긴급작업", "🔴 긴급작업", "🔴 긴급작업", "🔴 긴급작업", "✅ 완료", "", "", "", "", ""],
        "용접팀": ["", "", "", "", "🔴 작업중", "🔴 작업중", "🔴 작업중", "🔴 작업중", "✅ 완료", ""],
        "도장팀": ["", "", "", "", "", "", "🔴 긴급도장", "🔴 긴급도장", "🔴 긴급도장", "✅ 완료"],
        "조립팀": ["", "", "", "", "", "", "", "🔴 조립", "🔴 조립", "✅ 출하"],
    }
    
    timeline_df = pd.DataFrame(timeline_data)
    st.dataframe(timeline_df, use_container_width=True, height=400)
    
    st.markdown("---")
    
    # === 요약 ===
    st.subheader("📋 요약")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("총 부족 항목", "5개", delta="-5", delta_color="inverse")
    
    with col2:
        st.metric("긴급 항목", "3개", delta="-3", delta_color="inverse")
    
    with col3:
        st.metric("납기까지", "9시간", delta=None)
    
    with col4:
        st.metric("예상 완료", "17:00", delta="✅ 맞춤")
    
    st.markdown("---")
    
    # === 엑셀 다운로드 ===
    st.subheader("📥 보고서 다운로드")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 전체 공정표 엑셀 다운로드"):
            st.info("엑셀 생성 중...")
            # TODO: 엑셀 생성 로직
    
    with col2:
        if st.button("📋 지시서 인쇄용 다운로드"):
            st.info("지시서 생성 중...")
            # TODO: 지시서 생성 로직

else:
    st.info("👆 위에서 납품 계획을 입력하고 '분석 시작' 버튼을 눌러주세요")

# === 사이드바 ===
with st.sidebar:
    st.header("⚙️ 설정")
    
    st.subheader("📌 작업 시간 기준")
    st.text("조립: 2시간")
    st.text("도장(일반): 8시간")
    st.text("도장(긴급): 3시간")
    st.text("용접: 4시간")
    st.text("프레스: 3시간")
    
    st.markdown("---")
    
    st.subheader("👥 담당자")
    st.text("프레스: 김팀장")
    st.text("용접: 박과장")
    st.text("도장: 이과장")
    st.text("조립: 최반장")
    st.text("구매: 정대리")
    
    st.markdown("---")
    
    st.info("""
    💡 **사용 방법**
    1. 재고 파일 업로드
    2. 납품 계획 입력
    3. 분석 시작 클릭
    4. 지시사항 확인
    5. 현장 실행!
    """)
