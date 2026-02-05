from faster_whisper import WhisperModel
import sys
import os

def seconds_to_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

def process_audio_to_srt(audio_file, model, srt_folder):
    base_name = os.path.splitext(os.path.basename(audio_file))[0]
    srt_file_name = os.path.join(srt_folder, f"{base_name}.srt")

    # 환각 및 무한 루프 방지를 위한 파라미터 최적화
    segments, info = model.transcribe(
        audio_file, 
        beam_size=5,            # beam_size를 너무 높이면 오히려 환각이 늘어날 수 있음 (5~10 권장)
        language="ja", 
        vad_filter=True, 
        vad_parameters=dict(min_silence_duration_ms=1000), # 침묵 판단 기준을 조금 더 길게 설정
        
        # --- 핵심 수정 부분 ---
        condition_on_previous_text=False, # 이전 문맥 참조 해제 (무한 루프 방지의 핵심)
        no_speech_threshold=0.6,          # 음성이 아닐 확률이 60% 이상이면 무시
        log_prob_threshold=-1.0,          # 모델의 확신도가 낮으면 해당 구간 건너뜀
        compression_ratio_threshold=2.4,  # 텍스트가 지나치게 반복(압축률 높음)되면 버림
        # -----------------------
        
        repetition_penalty=1.2,
        best_of=5
    )

    with open(srt_file_name, "w", encoding="utf-8") as file:
        i = 0
        for segment in segments:
            # 신뢰도가 낮은 세그먼트는 자막 파일에 쓰지 않음 (이중 안전장치)
            if segment.no_speech_prob > 0.8:
                continue
                
            text = segment.text.strip()
            if not text:
                continue

            i += 1
            start_time = seconds_to_srt_time(segment.start)
            end_time = seconds_to_srt_time(segment.end)
            
            file.write(f"{i}\n")
            file.write(f"{start_time} --> {end_time}\n")
            file.write(f"{text}\n\n")
            
            sys.stdout.write(f"\r[{os.path.basename(audio_file)}] 세그먼트 {i} 처리 중...")
            sys.stdout.flush()
            
    print(f"\n'{audio_file}' 변환 완료! -> '{srt_file_name}'")

# 모델 설정 (최신 안정 버전인 large-v3-turbo 고려 가능)
model_size = "large-v3"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

audio_folder = "Video"
srt_folder = "SRT"

if not os.path.exists(srt_folder):
    os.makedirs(srt_folder)

for file in os.listdir(audio_folder):
    if file.endswith((".mp3", ".wav", ".m4a", ".mp4")):
        audio_file = os.path.join(audio_folder, file)
        process_audio_to_srt(audio_file, model, srt_folder)
        
        # python transAudio.py