# Environment Variables

이 템플릿은 `.env` 파일 또는 시스템 환경 변수로 설정을 주입한다. 새 프로젝트를 만들 때는 `.env.example`을 기준으로 `.env`를 구성한다.

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `APP_NAME` | `FastAPI DDD Template` | FastAPI 앱 제목과 로그에 표시되는 애플리케이션 이름 |
| `APP_ENV` | `local` | 실행 환경. `local`, `dev`, `staging`, `prod` 중 하나 |
| `DEBUG` | `true` | FastAPI debug 모드 활성화 여부 |
| `LOG_LEVEL` | `INFO` | 출력할 최소 로그 레벨. `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` 중 하나 |

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
