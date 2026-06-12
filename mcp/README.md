# MCP 배포 가이드

Notion, Google Drive 등 외부 시스템 연동에 MCP를 사용한다.

## 핵심 원칙

Git Markdown이 소스 오브 트루스다. Notion과 Google Drive는 배포 대상이다.

## 커밋하지 않을 것

- API 토큰
- OAuth 자격증명
- 워크스페이스 시크릿
- 민감한 경우 비공개 데이터베이스 ID

## 권장 배포 흐름

1. `docs/` 아래에 문서를 생성한다.
2. 문서를 리뷰한다.
3. 배포 계획을 준비한다.
4. MCP 도구로 Notion 또는 Drive를 생성/업데이트한다.
5. 배포 결과를 기록한다.
