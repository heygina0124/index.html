# Remotion Guide (이 파이프라인용)

설치된 Remotion 공식 스킬(remotion-dev/skills)의 API 규칙이 우선이다. 이 문서는 프로젝트 구조와 관례만 정한다.

## 생성
```
cd projects/<name>/06_remotion
npx create-video@latest . --blank   # TypeScript, blank
npm i
```
생성 명령이나 옵션이 바뀌었으면 공식 문서를 따른다.

## 구조
```
06_remotion/
  public/
    screens/   ← 01_research/screens 복사
    audio/     ← 05_audio의 vo/ music/ sfx/ 복사
    logo.svg
  src/
    Root.tsx          ← 컴포지션 2개 등록
    Main.tsx          ← <Series>로 장면 배치, 오디오 레이어
    brand.ts          ← 컬러/폰트/로고 토큰
    timing.json       ← 05_audio/timing.json 복사
    motion.ts         ← 공통 애니메이션 헬퍼 (fadeUp, slideIn, countUp, highlight)
    scenes/
      Scene01Hook.tsx
      Scene02Problem.tsx
      ...
    ui/               ← rebuild 화면의 재구성 컴포넌트
```

## 관례
- 모든 장면 컴포넌트는 `{ layout: "landscape" | "portrait" }` prop을 받는다.
- 시간 값은 초 단위로 생각하고 `fps`로 변환: `const f = (s: number) => Math.round(s * fps)`.
- 애니메이션은 `useCurrentFrame()` + `interpolate()` / `spring()`만 사용. CSS transition, setTimeout 금지.
- 이미지는 `staticFile()` + `<Img>`, 오디오는 `<Audio>`.
- 폰트는 `@remotion/google-fonts` 또는 `public/`의 로컬 폰트를 로드하고 렌더 전에 로드 완료를 보장.
- 장면 길이는 `timing.json`의 `frames`를 그대로 쓴다. 장면 안에서 길이를 하드코딩하지 않는다.

## 오디오
- VO: 각 장면 `<Series.Sequence>` 안에 `<Audio src=vo/scene-XX.mp3 volume={1} />`.
- 음악: 최상위에 전체 길이로 깔고, VO 구간에서 0.15, VO 사이 공백에서 0.25로 interpolate 덕킹. 마지막 1.5초 페이드아웃.
- SFX: 해당 장면 Sequence 안에서 `<Sequence from={f(at)}>`로 배치, volume 0.4~0.6.

## 미리보기 / 확인
- 스틸: `npx remotion still Main16x9 ../07_renders/stills/s03.png --frame=<n>`
- 9:16도 같은 프레임으로 한 장씩 뽑아 비교.
- 렌더 전 `npx tsc --noEmit`으로 타입 에러 확인.
