
import os
import time
import shutil
from deep_translator import GoogleTranslator

def batch_translate_srt_fast(input_folder, output_folder, batch_size=20):
    # 1. 문제 진단 및 환경 설정: 폴더 경로 정규화 및 생성
    input_folder = os.path.normpath(input_folder)
    output_folder = os.path.normpath(output_folder)
    translator = GoogleTranslator(source='ja', target='ko')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"📂 {output_folder} 폴더를 생성했습니다.")

    files = [f for f in os.listdir(input_folder) if f.endswith('.srt')]
    
    for filename in files:
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        print(f"\n🚀 [번역 시작] {filename}")
        
        # 파일 읽기
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"❌ 파일 읽기 실패 ({filename}): {e}")
            continue

        content_indices = []
        to_translate = []
        translated_lines = lines[:]

        # 대사 추출 로직
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped and not stripped.isdigit() and '-->' not in stripped:
                content_indices.append(idx)
                to_translate.append(stripped)

        # 2. 구체적인 해결 방안: 배치 번역 및 예외 처리
        for i in range(0, len(to_translate), batch_size):
            batch = to_translate[i:i + batch_size]
            combined_text = "\n".join(batch)
            
            try:
                translated_text = translator.translate(combined_text)
                if not translated_text:
                    raise ValueError("번역 결과가 비어있음")
                
                translated_batch = translated_text.split("\n")
                
                if len(translated_batch) == len(batch):
                    for j, res_text in enumerate(translated_batch):
                        translated_lines[content_indices[i + j]] = res_text + "\n"
                else:
                    # 결과 개수 불일치 시 개별 번역 수행 (안전 모드)
                    for j, orig_text in enumerate(batch):
                        translated_lines[content_indices[i + j]] = translator.translate(orig_text) + "\n"
                
                print(f" > 진행률: {min(i + batch_size, len(to_translate))}/{len(to_translate)} 문장 완료", end='\r')
                time.sleep(0.6) # 구글 차단 방지 및 시스템 안정화

            except Exception as e:
                print(f"\n⚠️ 번역 중 오류 발생(일부 건너뜀): {e}")
                time.sleep(1)

        # 3. 예상 결과 반영: 안전한 파일 저장 프로세스
        save_success = False
        # 최대 3번 저장 시도 (권한 오류 대비)
        for attempt in range(3):
            try:
                # 기존 파일이 있으면 권한 해제 후 삭제 시도
                if os.path.exists(output_path):
                    os.chmod(output_path, 0o777) 
                    os.remove(output_path)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.writelines(translated_lines)
                print(f"\n✅ {filename} 저장 완료!")
                save_success = True
                break
            except PermissionError:
                print(f"\n⚠️ 권한 오류 재시도 중 ({attempt+1}/3)...")
                time.sleep(2)
        
        # 끝까지 저장 실패 시 대체 이름으로 저장
        if not save_success:
            alt_path = os.path.join(output_folder, f"FIXED_{int(time.time())}_{filename}")
            with open(alt_path, 'w', encoding='utf-8') as f:
                f.writelines(translated_lines)
            print(f"\n⚠️ 점유 문제로 인해 다른 이름으로 저장됨: {alt_path}")

if __name__ == "__main__":
    # 폴더명 확인: 실제 폴더명과 일치하는지 확인하세요.
    batch_translate_srt_fast("Untranslated2", "Translated_Sub2")

    # python translate_srt.py