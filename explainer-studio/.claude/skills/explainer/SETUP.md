# /explainer 설치 가이드

한 번만 하면 된다. 순서대로.

## 1. 기본 도구
- **Claude Code** — 데스크톱 앱의 Code 탭 또는 터미널
- **Node.js** (LTS 버전)
- **ffmpeg** — macOS: `brew install ffmpeg` / Windows: `winget install ffmpeg`
- **Python 3** + **uv** — `pip install uv` (ElevenLabs MCP 실행용)

## 2. 작업 폴더
```
mkdir ~/explainer-studio && cd ~/explainer-studio
mkdir -p .claude/skills projects
```
이 `explainer` 폴더 전체를 `.claude/skills/explainer/`에 넣는다.
(모든 프로젝트에서 쓰려면 `~/.claude/skills/explainer/`)

## 3. Figma
```
claude plugin install figma@claude-plugins-official
```
Claude Code에서 `/mcp` → figma → 로그인. Full 또는 Dev 시트 필요.

## 4. Remotion 스킬
`~/explainer-studio`에서:
```
npx skills add remotion-dev/skills
```
명령이 바뀌었을 수 있으니 remotion.dev/docs/ai 에서 현재 명령 확인.
상업 작업 전 Remotion 라이선스 조건(회사 규모별) 확인.

## 5. ElevenLabs
API 키 발급 (elevenlabs.io → Profile → API Keys) 후:
```
claude mcp add elevenlabs --scope user \
  -e ELEVENLABS_API_KEY=여기에_키 \
  -e ELEVENLABS_MCP_BASE_PATH=$HOME/explainer-studio \
  -- uvx elevenlabs-mcp
```
`/mcp`에서 elevenlabs가 connected인지 확인.

## 6. 음악
`~/explainer-studio/library/music/`에 라이선스 있는 음원 5~10곡 (밝음/차분/테크 등 분위기별). 파일명에 분위기와 BPM을 넣어두면 Claude가 고르기 쉽다 — 예: `upbeat-tech_118bpm.mp3`.

## 7. 실행
```
cd ~/explainer-studio
claude
```
그리고:
```
/explainer
```
Claude가 프로젝트 이름을 묻고 폴더를 만든 뒤 brief를 같이 채운다.

## 확인 체크
- [ ] `/mcp`에 figma, elevenlabs 둘 다 connected
- [ ] `ffprobe -version` 동작
- [ ] `/explainer` 입력 시 스킬이 뜸
