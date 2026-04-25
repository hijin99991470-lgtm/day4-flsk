# 게시판 수정/삭제(U/D) 기능 설계

## 목표
- 상세 페이지에 `[수정] [삭제]` 버튼을 추가한다.
- 수정 화면은 `templates/write.html` 폼을 재사용한다.
- 삭제 전에 `정말 삭제할까요?` 확인 창을 띄운다.
- 기존 파일은 최소 변경 원칙을 따른다.

## 범위
- 백엔드: `app.py` 라우트 2개 추가
  - `GET/POST /posts/<int:post_id>/edit`
  - `POST /posts/<int:post_id>/delete`
- 템플릿:
  - `templates/post_form.html`의 역할을 `templates/write.html`로 전환
  - `templates/post_detail.html`에 수정/삭제 버튼 추가
- 테스트:
  - 수정/삭제 동작 검증 테스트 2개 추가

## 아키텍처
기존 Flask 단일 파일 구조를 유지하고, 현재 데이터 접근 방식(`get_db`, sqlite 파라미터 바인딩)을 그대로 사용한다. 생성/수정은 같은 폼 템플릿을 공유하고, 삭제는 별도 POST 엔드포인트로 분리한다.

## UI/템플릿 설계
### 1) 공용 폼 템플릿 (`templates/write.html`)
- 생성/수정에서 동일 템플릿 사용
- 분기 변수
  - 화면 제목: 생성(`글쓰기`) / 수정(`글수정`)
  - 제출 버튼 텍스트: 생성(`저장`) / 수정(`수정`)
  - 필드 기본값: 수정 시 기존 `post['title']`, `post['content']` 주입
- 취소 버튼
  - 생성 화면: 목록(`/posts`)으로 이동
  - 수정 화면: 상세(`/posts/<id>`)로 이동

### 2) 상세 템플릿 (`templates/post_detail.html`)
- 기존 본문 하단에 버튼 영역 추가
  - `[수정]` 링크: `/posts/<id>/edit`
  - `[삭제]` 버튼: `POST /posts/<id>/delete` 폼
- 삭제 폼에 브라우저 확인창 적용
  - `onsubmit="return confirm('정말 삭제할까요?')"`

## 라우트/데이터 흐름
### 1) 수정 (`/posts/<id>/edit`)
- GET
  1. `id`로 게시글 조회
  2. 없으면 `abort(404)`
  3. `write.html` 렌더 + 기존 값 전달
- POST
  1. `title`, `content`를 `strip()`
  2. 둘 다 값이 있을 때만 `UPDATE`
  3. 상세 페이지(`/posts/<id>`)로 redirect

### 2) 삭제 (`/posts/<id>/delete`)
- POST만 허용
- `DELETE FROM posts WHERE id = ?`
- 완료 후 목록(`/posts`)으로 redirect

## 보안/에러 처리
- 기존 패턴 유지: 조회 실패 시 `abort(404)`
- SQL은 기존처럼 파라미터 바인딩(`?`)만 사용
- 삭제는 GET이 아닌 POST로만 처리
- confirm 창은 UX 확인 수단이며 서버 로직은 독립적으로 안전하게 동작

## 테스트 계획
`tests/test_board.py`에 최소 추가:
1. `test_edit_post_updates_content`
   - 게시글 생성 → 수정 POST → 상세/목록에서 수정값 확인
2. `test_delete_post_removes_item`
   - 게시글 생성 → 삭제 POST → 목록에서 삭제 확인

실행 기준:
- `python -m pytest -q` 전체 통과

## 비목표
- 권한/인증 기능 추가
- CSRF 프레임워크 도입
- UI 대규모 리디자인
- 데이터 스키마 변경
