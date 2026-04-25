# Flask 게시판 Render 배포 준비 설계 (SQLite 유지)

## 목표
- 기존 Flask 게시판을 최소 변경으로 Render에 배포 가능한 상태로 만든다.
- SQLite를 유지하되, Render Persistent Disk를 통해 데이터 유실 위험을 줄인다.

## 범위
- 애플리케이션 코드 최소 수정 (`app.py`)
- 배포 필수 파일 추가 (`requirements.txt`, `Procfile`)
- Render 환경 설정 가이드 확정

## 아키텍처
- Flask 앱 구조는 유지한다.
- 프로세스 실행은 Render에서 `gunicorn app:app`를 사용한다.
- DB 경로는 환경변수 `DATABASE_PATH`를 우선 읽고, 미지정 시 기존 `board.db`를 기본값으로 사용한다.

## 파일 변경 설계
1. `app.py`
   - `os.getenv("DATABASE_PATH")` 값이 있으면 해당 경로 사용
   - 없으면 기존 경로(`Path(__file__).with_name("board.db")`) 사용

2. `requirements.txt` (신규)
   - `Flask`
   - `gunicorn`
   - `pytest` (기존 테스트 실행용)

3. `Procfile` (신규)
   - `web: gunicorn app:app`

## Render 설정 설계
- 서비스 타입: Web Service
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Persistent Disk 연결 경로: `/var/data`
- 환경변수:
  - `DATABASE_PATH=/var/data/board.db`

## 검증 계획
### 로컬 검증
1. `python -m pytest -q` 통과
2. `gunicorn app:app` 실행 성공 확인

### Render 배포 후 검증
1. `/posts` 페이지 접속 확인
2. 글 생성/수정/삭제 기능 정상 동작 확인
3. 재배포 후 기존 게시글 데이터 유지 확인

## 비목표
- PostgreSQL 전환
- Docker 배포 구성
- 인증/권한 및 CSRF 도입
- 대규모 리팩토링
