---
name: write-error-code-spec
description: API 도메인의 에러코드 정의 문서를 생성하거나 업데이트한다.
---

# 에러코드 명세 작성 (Write Error Code Spec)

## 목적

에러코드 문서를 생성하거나 업데이트한다.

## 필요한 입력

- 기존 에러코드 정의
- API 명세
- 서비스 예외 처리
- AGENTS.md 에러 응답 규칙

## 진행 순서

1. 새로 추가되거나 변경된 에러를 파악한다.
2. HTTP 상태 코드, 에러 코드, 메시지, 원인, 복구 가이드를 확인한다.
3. 네이밍 컨벤션을 확인한다.
4. 제거된 에러 코드를 재사용하지 않는다.
5. 필요한 경우 deprecated 항목을 문서화한다.

## 출력

```text
docs/errors/{domain}.error-codes.md
```
