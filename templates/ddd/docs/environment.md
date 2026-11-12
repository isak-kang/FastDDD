# Environment Variables

이 템플릿은 `.env` 파일 또는 시스템 환경 변수로 설정을 주입한다. 새 프로젝트를 만들 때는 `.env.example`을 기준으로 `.env`를 구성한다.

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `APP_NAME` | `FastAPI DDD Template` | FastAPI 앱 제목과 로그에 표시되는 애플리케이션 이름 |
| `APP_ENV` | `local` | 실행 환경. `local`, `dev`, `staging`, `prod` 중 하나 |
| `DEBUG` | `true` | `settings.app.debug`로 읽을 수 있는 플래그. FastAPI 앱의 `debug`에는 연결하지 않는다 (Starlette debug 모드는 전역 예외 핸들러를 우회해 raw traceback을 반환하므로, 통일된 에러 응답 계약과 충돌한다) |
| `LOG_LEVEL` | `INFO` | 출력할 최소 로그 레벨. `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` 중 하나 |
| `CORS_ALLOW_ORIGINS` | (비어 있음) | 브라우저에서 이 API를 호출할 수 있는 origin 목록. **콤마로 구분**한다(예: `http://localhost:3000,https://app.example.com`). 비우면 CORS 미들웨어를 아예 붙이지 않는다 |

## LOG_LEVEL

로그 레벨은 낮은 단계부터 높은 단계까지 다음 순서다.

```text
DEBUG < INFO < WARNING < ERROR < CRITICAL
```

- `DEBUG`: 개발 중 상세 흐름 확인
- `INFO`: 일반 실행 흐름 확인
- `WARNING`: 사용자 입력 오류나 복구 가능한 문제 확인
- `ERROR`: 처리 실패나 서버 오류 확인
- `CRITICAL`: 즉시 대응이 필요한 치명적 오류 확인

기본값은 `INFO`다. 운영 환경에서는 보통 `INFO` 또는 `WARNING`을 사용하고, 문제를 자세히 추적할 때만 `DEBUG`를 사용한다.
