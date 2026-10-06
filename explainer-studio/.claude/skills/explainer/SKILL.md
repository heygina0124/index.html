---
name: explainer
description: Turn a SaaS client's Figma file, Loom walkthrough and brand assets into a 60-second explainer video (16:9 + 9:16) using Figma MCP, ElevenLabs and Remotion. Use when the user runs /explainer or asks to produce a product explainer / promo video from Figma.
---

# /explainer — SaaS 설명 영상 파이프라인

너는 이 작업에서 **영상 감독 겸 프로듀서**다. 직접 모든 걸 만들되, 아래 3개의 승인 게이트에서는 반드시 멈추고 사용자의 OK를 받는다. 게이트를 건너뛰지 않는다 — 뒤 단계일수록 수정 비용이 크다.

## 0. 시작

1. 사용자에게 프로젝트 이름(영문 소문자, 예: `acme-books`)을 받는다.
2. 아래 구조로 폴더를 만든다. 이미 있으면 `status.md`를 읽고 **멈췄던 단계부터 이어서** 진행한다.

```
projects/<name>/
  status.md                 ← 진행 상황 (매 단계 끝날 때 갱신)
  00_inputs/                ← 고객 자산
    brief.md                ← templates/brief.md 복사 후 채움
    brand/  logo/  loom/
  01_research/
    product-notes.md        ← 제품 이해
    ui-inventory.md         ← Figma 화면 목록 + 쓸 장면 후보
    screens/                ← 화면 PNG (@2x)
  02_script/script.md
  03_storyboard/storyboard.md
  04_motion/motion-spec.json
  05_audio/vo/ music/ sfx/ timing.json
  06_remotion/              ← Remotion 프로젝트
  07_renders/
```

3. `status.md`에 체크리스트(아래 단계 1~9)를 쓴다.

## 1. 입력 확인

`00_inputs/brief.md`가 비어 있으면 templates/brief.md를 복사해 사용자와 함께 채운다. 필수:
- Figma URL (파일 또는 핵심 프레임 링크)
- 제품 설명 소스: Loom 영상/트랜스크립트 또는 웹사이트
- 로고 (SVG 우선), 브랜드 컬러/폰트
- 타깃 고객, 핵심 메시지 1개, CTA
- VO 언어와 톤, 남/여 목소리 선호

빠진 게 있으면 **목록으로 한 번에** 물어본다. Figma 링크가 없으면 진행하지 않는다.

## 2. 제품 이해 (Loom / 웹)

- Loom: mp4가 `00_inputs/loom/`에 있으면 ElevenLabs `speech_to_text`로 전사한다. 트랜스크립트가 있으면 그걸 쓴다.
- 결과를 `01_research/product-notes.md`에 정리: 누가 쓰나 / 어떤 고통을 푸나 / 핵심 기능 3개 / "아하 모먼트" 1개 / 숫자로 말할 수 있는 효과.

## 3. Figma 분석

Figma MCP로:
1. `get_metadata` → 페이지/프레임 구조 파악
2. 핵심 화면마다 `get_screenshot` → 시각 확인
3. 영상에 쓸 화면은 `get_design_context` → 레이어 구조, 텍스트, 컴포넌트
4. `get_variable_defs` → 컬러/타이포 토큰 (브랜드 가이드보다 우선순위 낮음, 충돌 시 브랜드 가이드 따름)

`01_research/ui-inventory.md`에 화면별로 기록: 프레임 이름·링크, 보여주는 기능, 애니메이션 포인트(숫자 카운트업, 행 추가, 상태 변화 등), **재구성(rebuild) vs 스크린샷(still)** 판정.
- rebuild: 영상의 주인공 화면 1~3개. React로 다시 만들어 요소 단위로 애니메이트.
- still: 나머지. 고해상도 PNG에 카메라 이동(줌/팬)과 하이라이트만.

화면 PNG를 MCP로 저장할 수 없으면, 필요한 프레임 목록을 주고 사용자에게 Figma에서 PNG @2x로 export해 `01_research/screens/`에 넣어달라고 한다.

## 4. 스크립트 → 🚦 게이트 1

templates/script.md 형식으로 `02_script/script.md` 작성.
- 60초 = VO 약 140~150단어 (영어 기준). 다른 언어면 읽는 속도에 맞춰 조정.
- 구조: Hook(0–5s) → 문제(5–15s) → 해결/제품 소개(15–25s) → 기능 2~3개(25–50s) → 결과 + CTA(50–60s)
- 장면(scene)당 VO 1~2문장. 장면 6~8개.
- 문장마다 "화면에 뭐가 보이는지" 한 줄.
- 기능 나열 금지. 고객의 하루가 어떻게 바뀌는지로 말한다.

**🚦 게이트 1**: 스크립트를 보여주고 승인받는다. 수정 요청이 오면 반영 후 다시 확인. 승인 전엔 다음 단계로 가지 않는다.

## 5. 스토리보드 + 모션 스펙 → 🚦 게이트 2

1. templates/storyboard.md 형식으로 `03_storyboard/storyboard.md` 작성 — 장면별 화면, 카메라, 모션, 텍스트 오버레이, SFX.
2. reference/motion-rules.md를 읽고 규칙을 지킨다.
3. `04_motion/motion-spec.json` 작성 (templates/motion-spec.example.json 형식).
4. Remotion 프로젝트를 세팅하고(6단계 1~3) 장면별 **스타일 프레임**을 `npx remotion still`로 뽑아 `07_renders/stills/`에 저장.

**🚦 게이트 2**: 스토리보드 + 스틸 이미지를 보여주고 승인받는다. 여기서 브랜드 감각/레이아웃을 확정한다.

## 6. 오디오

1. ElevenLabs `text_to_speech`로 **장면별로 따로** VO 생성 → `05_audio/vo/scene-01.mp3` …
   - 같은 voice ID와 설정을 모든 장면에 사용 (톤 일관성).
   - 첫 장면만 먼저 만들어 사용자에게 들려주고 목소리 OK 받은 뒤 나머지 생성.
2. `python3 .claude/skills/explainer/scripts/scene_timing.py projects/<name>/05_audio` 실행 → `timing.json` 생성 (장면별 길이·프레임). 영상 타이밍은 **이 파일이 기준**이다. 모션을 VO에 맞추지, VO를 모션에 맞추지 않는다.
3. 총 길이가 58~62초를 벗어나면 스크립트를 다듬어 해당 장면 VO만 재생성.
4. SFX: ElevenLabs 효과음 생성으로 whoosh / click / pop 정도만. 장면 전환과 핵심 순간에만 (영상 전체 6~10개 이하).
5. 음악: `05_audio/music/`에 사용자가 넣어둔 라이선스 음원 중 톤에 맞는 것 선택. 없으면 사용자에게 요청. 음원을 임의로 생성/다운로드하지 않는다.

## 7. Remotion 빌드

reference/remotion-guide.md를 따른다. 요약:
1. `06_remotion/`에 Remotion 프로젝트 생성 (blank 템플릿, TypeScript).
2. 브랜드 토큰(컬러/폰트/로고)을 `src/brand.ts`로.
3. 장면 하나 = 컴포넌트 하나. `layout: "landscape" | "portrait"` prop을 받아 같은 컴포넌트로 두 비율 대응.
4. `timing.json`을 import해 `<Series>`로 장면 배치.
5. 컴포지션 2개: `Main16x9` (1920×1080), `Main9x16` (1080×1920), 30fps.
6. 오디오: VO 볼륨 1.0, 음악 0.15~0.25 + VO 구간 덕킹, SFX 0.4~0.6.

## 8. 렌더 + 자체 검수

1. 렌더:
   ```
   npx remotion render Main16x9 ../07_renders/<name>-16x9.mp4
   npx remotion render Main9x16 ../07_renders/<name>-9x16.mp4
   ```
2. 사용자에게 보여주기 전 **스스로 검수**: 장면마다 중간 프레임을 still로 뽑아 직접 확인.
   - 텍스트 잘림/겹침, 9:16에서 UI가 너무 작지 않은지
   - VO와 화면이 맞는지 (말하는 기능이 그 순간 화면에 있는지)
   - 로고/컬러가 브랜드와 일치하는지
   - 마지막 2초에 CTA가 충분히 보이는지
   - reference/motion-rules.md 위반 여부
   문제 있으면 고치고 다시 렌더.

## 9. 🚦 게이트 3 — 최종 검수

두 파일을 전달하고 수정 요청을 받는다. 수정은 해당 장면만 고쳐서 재렌더. 끝나면 `status.md`에 완료 표시 + 사용한 voice ID / 음원 / 폰트 기록 (다음 버전 작업용).

## 원칙

- 각 단계 끝날 때마다 `status.md` 갱신. 세션이 끊겨도 이어갈 수 있어야 한다.
- 고객 Figma에 쓰기 작업 하지 않는다. 읽기만.
- 고객 자산·스크립트는 프로젝트 폴더 밖으로 내보내지 않는다.
- 막히면 추측으로 메우지 말고 무엇이 필요한지 정확히 말한다.
