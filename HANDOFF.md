# 인수인계: HotelEng (호텔서비스 영어)

기준일: 2026-11-28 · 작성: 프로젝트 "웹앱/ 다국어 학습"에서 옮김 · 사용자: RYU

## 0. 이 문서를 쓰는 방법

- 새 프로젝트 **"웹앱/ 호텔 실무영어"**에 이 문서를 붙여 넣고 "이 문서를 기준으로 이어서 작업해줘"라고 말하면 됩니다.
- 새 프로젝트에 저장소 `insoo-commits/hoteleng-app`을 연결하세요.
- 계정 스킬 `language-app-build`, `language-app-audio`, `language-app-release`를 빌드·음성·배포 전에 불러오세요.

## ⚠️ 원본 소스와 음성 원본

- **원본 소스는 이제 저장소에 있습니다** (2026-11-28, `src/`, `data/phe_areas.json`, `tools/mp3tar.py`, `tools/stats/Code.gs`, `audio/index.json`, `audio/packs.json`). 저장소 루트의 index.html, app.js, data.js, sw.js, audio/p/*.bin은 `src/build.py`가 만든 **결과물**이라, 저장소 루트 파일만 고치면 다음 빌드 때 사라집니다. 항상 `src/`를 고치고 빌드하세요.
- 빌드 준비: `pip install cmudict edge-tts`, node + Playwright(clips.js, helpshots.js가 씀).
- **mp3 원본 `audio/mp3.tar`는 올리지 않아도 됩니다** (2026-11-28). 음성 팩 `audio/p/*.bin`에 mp3가 바이트 그대로 들어 있어서, `audio/mp3.tar`가 없으면 `tools/mp3tar.py`가 팩에서 14,060클립을 모두 꺼내 로컬 캐시(/tmp/mp3cache)에 둡니다. `build.py`와 `make_audio.py`가 이것을 자동으로 씁니다(빌드 출력: `mp3tar: no mp3.tar, 14060 clips taken out of …/audio/p`). 손으로 꺼내려면 `python3 tools/mp3tar.py frompacks audio/p <폴더>`.
- 확인: 팩에서 꺼낸 클립으로 빌드하면 "site audio clips 14060 of 14060"이고 index.html·app.js·sw.js가 v1.77 배포본과 같습니다.
- 그래도 mp3 원본이 하나도 없으면 `build.py`가 `STOP: mp3 원본이 없습니다…`를 출력하고 멈춥니다(음성 팩을 지우지 않도록 막아 둠). 이때 생긴 site/는 음성이 빠져 있으니 배포하지 마세요.
- 그 밖의 자료(예전 프로젝트 폴더): 포스터 `hotel-english-app/poster/`(src/poster.html, PDF·PNG).

## 1. 앱 정보

- **이름:** HotelEng (앱 제목 "호텔서비스 영어"). 전주대 호텔경영학과 학생용. 제목줄에 "호텔경영학과" 문구는 넣지 않음(로고 SVG는 하단과 인트로에 있음, hotel.jj.ac.kr 링크).
- **학생용 주소:** https://hoteleng.pages.dev/ (Cloudflare Pages, 포스터 QR도 이 주소). 보조: https://insoo-commits.github.io/hoteleng-app/
- **저장소:** `insoo-commits/hoteleng-app`. 파일 238개쯤이라 Cloudflare 빌드 설정 불필요.
- **현재 버전:** **v1.77** (PR #10) + 링크 미리보기 og.jpg (PR #11, 버전 그대로). 마지막 커밋 `6388028`.
- **캐릭터:** 호텔경영학과 마스코트(src/introimg/mascot.png, 420×337 투명). 인트로, 퀴즈 결과, 도움말에 나옴.

## 2. 빌드와 배포

1. `src/` 수정 → 저장소 루트에서 `python3 src/build.py` → `site/`와 `preview/`가 생김(둘 다 .gitignore).
2. `build.py`의 `VERSION`을 **배포할 때마다** 올림(app.js?v= 캐시 깨기; RYU가 예전 app.js를 본 적 있음).
3. 다른 스레드에서도 배포한 적이 있으니 **배포 전에 VERSION 확인 + git pull.**
4. 배포 = `site/`의 index.html, app.js, data.js, sw.js, manifest.webmanifest, og.jpg, img/를 저장소 루트로 복사. 음성 팩은 빌드가 `audio/p/*.bin`에 바로 씀. **mp3는 절대 커밋하지 않음**(.gitignore audio/*.mp3). TOEIC 팩 7-01-01..04는 빌드마다 바이트가 바뀌니 data.js와 같이 복사.
5. `claude/...` 브랜치 → PR → main merge. PR에 RYU 지정.
- 음성 만들기: `python3 src/make_audio.py <codes|all>`는 **build.py와 한 명령에 이어 붙이지 말고 따로 실행**(작업 폴더 문제). mp3 원본은 팩에서 자동으로 꺼내 쓰고(위 ⚠️), `make_audio.py`가 새 클립을 만들면 `audio/mp3.tar`(.gitignore)에 전체를 저장합니다. 다른 mp3 폴더를 쓰려면 `HOTELENG_MP3=<폴더>`.
- 도움말 스크린샷: `node src/helpshots.js <outdir>` → webp q62 → 다시 빌드. 캡션에 "]" 금지.

## 3. 콘텐츠 구성 (RYU 결정)

- 메뉴: | 기초회화 · 호텔기본 · 프런트 · 객실·시설 · 식음료 · 고객응대·실무 | TOEIC · 영어면접 | 도움말 |
- **수업 계획 메뉴, 수업 진행 안내, 수업/자율 표시 없음.** 개인 학생도 쓰는 앱이고 수업은 교수가 직접 운영. (학기표 Claude Doc은 참고용: https://claude.ai/artifact/5fjWjKZeQkwntJNx2M9Af5)
- "외웠어요" 체크박스 없음.
- 기초회화 1-01 기본 인사 ~ 1-12. 대화 묶음은 반씩 나눔(5~8줄, src/content/splits.py).
- **TOEIC:** LC 듣기 / RC 읽기 / 빈출 단어(단어만) / 자주 나오는 표현(문장 패턴만, 겹치지 않게) / 모의고사(미니 25문제, 실전 50문제). 문제은행 1,000문항(src/content/tqbank*.py, 정답을 먼저 쓰고 빌드가 섞음). 호텔 분야만이 아니라 여러 분야. Part 1 그림은 pics.py / pics_b.py(새 문제 = 새 그림). 듣기 문제 영어는 체크박스 "듣기 문제 영어 보기" 하나로, 기본 숨김.
- **영어면접:** 7개 소분류(자기소개·지원 동기 / 강점·약점·경험 / 희망 부서별 / 상황 대처 / 면접 흐름·마무리 / 예상 질문·기출(전주대 핸드아웃, 싱가포르 콘래드 기출) / 모의 면접 8-07-01). 모의 면접 원본은 `content/m8d.py`를 손으로 고침(genm8d.py, mkcur.py는 다시 돌리지 말 것). 문장 영어는 원래 묶음과 똑같이 유지해야 음성이 맞음. 학생 이름 넣지 않음. 면접 관련 링크는 "@묶음 제목"으로 씀.
- ※ 단어 메모: 대화·예문 줄 아래 오른쪽 정렬, 넉넉하게(학생이 쉬운 단어도 모른다고 가정). src/gloss.py + content/glossary.py + content/senses.py(그 문장 뜻을 먼저: book(예약하다, 책)).
- 묶음 그림: src/scenes.py 53장(규칙 regex). 새 묶음이 규칙에 맞는지 확인.
- 내용 속 대학 = 전주대학교 / Jeonju University. 전공은 business administration, 외국 도시는 그대로.

## 4. 화면·재생 규칙

- 디자인 A(그라데이션 제목, src/skin_a.css), HotelEng 전용 he.css. PC 본문 1176px, 상단 고정 메뉴 = 페이지 메뉴 줄(스크롤 위치로 전환, v1.72).
- PC 버튼 이름 문장보기·주요단어·복습퀴즈, 폰은 문장·단어·퀴즈. 키 S W E, C 연속 재생, G 묶음 재생.
- 기본 2회 ×1.0, 속도 ×0.7–×1.5. 문장 칸·화자 탭 = 그 줄 무한 반복, 다시 탭하면 멈춤. 좌우 스와이프 = 이전/다음 묶음.
- 목소리: 남 m = en-US-AndrewNeural, m2 = BrianNeural, 여 = JennyNeural 계열(f, f2). ma'am/sir 등으로 화자 성별 자동. 16kbps.
- 배경 재생: 문장 사이에 무음 mp3를 돌림 + 잠금화면 컨트롤.
- sw.js: iPhone Range 요청 2바이트 조각을 저장하던 버그 고침(v1.35). 200 응답 1KB 이상만 저장.

## 5. 공통 기능 (JeyCampus · PhasaKAO · PhasaLAO와 같이)

- 인트로 + 하단 설정(글자 크기, 낮밤, HOME), 제목 탭 = 인트로(sessionStorage he-intro). 사진은 RYU가 고름(환영=hero, 설치 띠, PC 갤러리 6장). 안 쓴 사진: class.jpg, mondrian.jpg, banquet.jpg.
- 인트로 숫자 줄: 메뉴 수 빼고 학습자 수를 끝에(v1.77, 통계 hoteleng-statspage).
- 음량 슬라이더 v1.75–1.76 (src/vol.js, iPhone GainNode). 실제 iPhone 잠금화면 재생은 아직 확인 안 됨.
- 당겨서 새로고침 v1.75 (src/ptr.js, build.py js 줄 마지막).
- 링크 미리보기: build.py OG_TAGS + src/og.jpg. 카카오 캐시는 링크 뒤 ?k=1로 확인.
- 익명 통계·설문: Apps Script 웹앱 URL(v1.70부터, 2026-11-27 재배포)  
  https://script.google.com/macros/s/AKfycbwZNJ6JYJ7GaqgU56WZoAqklaPSX_KnE2viSEPhSdtvfZC3tazNRqRvitklWNiHx5KGdw/exec  
  이벤트 open/lesson/quiz/toeic/play/mock. 묶음 코드 앞에 ' (시트 날짜 변환 방지).

## 6. RYU 작업 방식

- 스레드 제목 앞에 [HotelEng].
- 더 빠르거나 크레딧을 아끼는 방법이 보이면 먼저 한 줄로 알려 줄 것.
- 프로젝트 파일 한도 50,000개: mp3를 낱개로 쌓지 말고 tar 하나로.
- 포스터는 앱이 바뀌면 숫자·버전·주소를 저장소에서 다시 읽어 맞춤. Playwright A4 렌더, 하단이 1123px 안에 들어오는지 확인.

## 7. 남은 일

- 실제 iPhone에서 음량 슬라이더 + 잠금화면 재생 확인.
- 같은 sw.js Range 버그가 다른 앱에 있는지는 확인 안 됨.
