# Cursor 어댑터

## 새 프로젝트

템플릿을 복사해 시작한다. DDD 예시:

```bash
curl -fsSL https://raw.githubusercontent.com/isak-kang/FastDDD/main/scripts/create.sh \
  | bash -s -- ddd ./my-backend --with-shared-skills
```

카탈로그 레포를 clone한 경우:

```bash
./scripts/create.sh ddd /path/to/my-backend --with-shared-skills
```

템플릿에 포함된 `.cursor/rules/`와 `.cursor/skills/`가 프로젝트 규칙이다.

## 기존 프로젝트에 공통 문서 skill 추가

```bash
./scripts/sync-shared-skills.sh /path/to/your-project
```

API 명세, 에러코드 문서, 릴리즈 노트, 블로그 등 **스택 무관 skill**만 복사한다.

## FastDDD 카탈로그 레포 자체

이 저장소 루트를 Cursor로 열 때는 `.cursor/rules/00-catalog.mdc`가 적용된다.
앱 아키텍처 규칙은 `templates/{template}/` 내부에만 둔다.
