# Streamlit Cloud 배포 가이드

## 준비물
1. GitHub 계정 (없으면 github.com에서 무료 가입)
2. production_control.py 파일
3. requirements.txt 파일

## 배포 순서

### 1단계: GitHub에 코드 올리기

1. GitHub.com 접속
2. 오른쪽 위 '+' 클릭 → 'New repository'
3. Repository name: das-production-control
4. Public 선택
5. 'Create repository' 클릭

6. 파일 업로드:
   - 'uploading an existing file' 클릭
   - production_control.py 드래그
   - requirements.txt 드래그
   - 'Commit changes' 클릭

### 2단계: Streamlit Cloud 연결

1. share.streamlit.io 접속
2. 'Sign up' → GitHub로 로그인
3. 'New app' 클릭
4. Repository: das-production-control 선택
5. Main file path: production_control.py
6. 'Deploy!' 클릭

### 3단계: 완료!

- 2~3분 기다리면 배포 완료
- URL 생성됨: https://das-production-control.streamlit.app
- 이 URL을 북마크하거나 공유!

## 업데이트 방법

파일 수정 후:
1. GitHub에서 파일 클릭
2. 연필 아이콘(Edit) 클릭
3. 수정
4. 'Commit changes' 클릭
→ 자동으로 재배포됨!

## 주의사항

- 재고 파일은 매번 업로드해야 함
- 또는 Google Drive 연동 가능
- 무료 플랜: 1GB 저장공간, 충분함
