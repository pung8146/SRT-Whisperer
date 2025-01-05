# README (Korean)

## Fast-Whisper 소개

Fast-Whisper는 OpenAI의 Whisper 모델을 CTranslate2를 이용하여 재구현한 버전입니다. CTranslate2는 Transformer 모델을 위한 고속 추론 엔진으로, 이를 통해 기존 Whisper 모델보다 최대 4배 빠른 성능을 자랑하며 메모리 사용량도 적습니다. 특히, CPU와 GPU에서 8비트 양자화를 적용함으로써 성능 효율을 더욱 끌어올릴 수 있습니다.

**프로그램은 사용자의 컴퓨터 성능을 활용하여 작동하므로, 사양이 낮은 경우 Whisper-WebUI를 이용하거나 다른 번역 프로그램을 고려하는 것이 좋습니다.**

[Fast-Whisper GitHub 페이지 바로가기](https://github.com/SYSTRAN/faster-whisper)

---

## 설치 필요 사항

### 1. 파이썬 설치

Fast-Whisper 사용을 위해서는 Python 3.8 이상이 필요합니다. 파이썬 버전을 확인하려면 터미널에서 다음 명령어를 실행하세요.

```bash
python --version
```

또는

```bash
python3 --version
```

**권장 버전:** Python 3.10 이상

[파이썬 공식 다운로드 페이지](https://www.python.org/downloads/)

### 2. NVIDIA 라이브러리 설치 (GPU 사용 시 필수)

GPU를 사용하여 음성 인식 처리 속도를 향상시키기 위해서는 NVIDIA의 cuBLAS와 cuDNN 라이브러리 설치가 필요합니다. GPU가 없거나 해당 라이브러리 설치가 어려운 경우, CPU만을 사용하는 방식으로도 작동하지만, 속도 면에서 제한이 있을 수 있습니다.

#### cuBLAS 설치 방법

1. [cuBLAS for CUDA 11](https://developer.nvidia.com/cublas) 페이지로 이동합니다.
2. **Download Now**를 클릭합니다.
3. 사용 중인 운영체제에 맞는 버전을 선택하여 설치합니다.
   - **주의:** 현재 Windows에서는 프로그램이 지원되지 않습니다.

#### cuDNN 설치 방법

1. [cuDNN 8 for CUDA 11](https://developer.nvidia.com/cudnn) 페이지로 이동합니다.
2. **Download Library** 목록을 확인합니다.
3. 사용 중인 운영체제에 맞는 라이브러리를 선택하여 설치합니다.

---

## Fast-Whisper 설치 방법

### 1. 라이브러리 설치

터미널을 열고 다음 명령어를 실행하여 `faster-whisper` 라이브러리를 설치합니다.

```bash
pip install faster-whisper
```

### 2. 작업 디렉토리 준비

자신이 작업하고 싶은 디렉토리로 이동하여 `transcribe_audio.py` 파일을 생성하고, 자막이 생성되어 저장될 폴더를 만듭니다.

### 3. transcribe_audio.py 파일 생성

아래 코드를 복사하여 `transcribe_audio.py` 파일을 생성합니다.

```python
# 코드 동일 내용 (위 영어 README의 transcribe_audio.py 예시와 동일)
```

---

## 언어 설정

기본 설정은 영어(`language="en"`)입니다. 원하는 언어 코드를 설정하여 다양한 언어로 음성 인식을 수행할 수 있습니다.

- `en`: 영어
- `ja`: 일본어
- `ko`: 한국어

---

## Fast-Whisper 사용 방법

자막을 생성할 오디오 파일들을 `transcribe_audio.py` 파일이 있는 디렉토리에 위치시킨 후, 다음 명령어를 실행합니다.

```bash
python transcribe_audio.py
```

---

## 참고 사항

- GPU 사용 시에는 `cuBLAS`와 `cuDNN`이 올바르게 설치되어 있어야 합니다.
- CPU만 사용할 경우 `device="cpu"`로 설정할 수 있습니다.

---

Fast-Whisper 프로젝트를 통해 오디오 파일을 빠르게 텍스트 자막으로 변환하여 생산성을 향상시켜 보세요!
