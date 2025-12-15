# 2026-CT-AllOfUsAreProfessor
CT
Markdown# 🏫 All of Us Are Professor (지금 우리 교수님은)
> **"컴퓨팅 사고" 기말 프로젝트: 2D 방탈출 포인트 앤 클릭 어드벤처 게임**

---

## 🚨 [필독] 게임 실행 전 필수 설정 (Urgent Setup) 🚨

**GitHub 용량 문제로 인해 리소스 파일들이 분산 업로드되어 있습니다.**
**게임을 정상적으로 실행하려면 반드시 아래 순서대로 폴더를 정리해주세요!**

1. 다운로드 받은 폴더 안에 **새 폴더**를 만들고 이름을 **`assets`** 로 지정합니다.
2. 흩어져 있는 모든 **리소스 파일들**을 **`assets` 폴더 안으로 이동**시켜주세요.
   * **이미지 파일:** `.png`, `.jpg` (Background, Character, Item, UI 등)
   * **사운드 파일:** `.mp3`, `.ogg`, `.wav`
3. 정리가 끝나면 폴더 구조가 아래와 같아야 합니다.

```text
MyEscapeGame/
 ├── assets/           <-- (여기에 모든 이미지/소리 파일이 들어있어야 함!)
 │    ├── backgrounds
 │    ├── characters
 │    ├── items
 │    └── ...
 ├── main.py
 ├── settings.py
 ├── game_state.py
 └── ...
``` 
📖 게임 소개 (Introduction)"잠들었다 깨어나니 밤 12시의 강의실... 문은 잠겼고, 교수님의 논리 퍼즐만 남았다."본 프로젝트는 '컴퓨팅 사고(Computational Thinking)' 과목의 기말 과제로 제작된 파이썬 기반의 방탈출 게임입니다. 화려한 액션보다는 문제 분해와 논리적 사고를 통해 해결해야 하는 퍼즐 요소에 집중하였습니다.

🎯 게임 목표강의실 곳곳에 숨겨진 단서(아이템, 쪽지)를 찾고 논리적으로 조합하여, 잠긴 문인 디지털 도어락의 비밀번호 4자리를 알아내 탈출하세요.

🛠️ 설치 및 실행 방법 (Installation)이 게임은 Python과 Pygame 라이브러리가 필요합니다.
1. 필수 요구 사항Python 3.x 설치Pygame 라이브러리 설치
2. 라이브러리 설치 명령어터미널(CMD 또는 PowerShell)에 아래 명령어를 입력하세요.Bashpip install pygame
3. 게임 실행assets 폴더 정리가 끝났다면, 아래 명령어로 게임을 시작합니다. python main.py

🎮 조작 방법 (Controls)마우스 왼쪽 클릭: 조사하기, 아이템 획득, UI 조작키보드: 최종 비밀번호 입력구분설명조사 (Inspect)수상한 물건(책상, 서랍 등)을 클릭하여 확대하거나 상태를 확인합니다.획득 (Get)열쇠나 쪽지 같은 아이템을 클릭하면 인벤토리에 저장됩니다.사용 (Use)인벤토리의 아이템을 활성화한 상태로 특정 사물을 클릭하면 상호작용합니다.

🧩 개발 환경 및 사용 기술Language: Python 3.12Library: PygameIDE: PyCharmStructure:main.py: 게임의 메인 루프 및 이벤트 처리game_state.py: 아이템 획득 여부, 문 열림 상태 등 전역 상태 관리 (State Management)settings.py: 해상도, 색상, FPS 등 상수 데이터 관리

💡 프로젝트 후기 (Developer's Note)본 프로젝트는 단순히 코드를 작성하는 것을 넘어, 문제를 작은 단위로 나누어 해결하는 **'분해(Decomposition)'**와 게임의 상태를 체계적으로 관리하는 **'알고리즘 설계'**에 중점을 두었습니다.개발 과정에서 라이브러리 호환성 문제와 리소스 최적화 등 기술적 난관이 있었으나, 이를 해결하며 컴퓨팅 사고 역량을 기를 수 있었습니다.

ⓒ 2025 All rights reserved.
