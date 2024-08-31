import argparse
import srt
import ffmpeg
import os
from datetime import timedelta

def extract_audio_segment(video_file, start_time, duration, output_file):
    # Usa o ffmpeg para extrair um segmento de áudio
    ffmpeg.input(video_file, ss=start_time, t=duration).output(output_file).run()

def process_subtitles(srt_file, video_file, output_dir):
    # Ler o arquivo de legendas
    with open(srt_file, 'r', encoding='utf-8') as f:
        subtitles = list(srt.parse(f.read()))
    
    # Criar diretório de saída se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Processar cada segmento de legenda
    for subtitle in subtitles:
        start_time = subtitle.start.total_seconds()
        duration = (subtitle.end - subtitle.start).total_seconds()
        output_file = os.path.join(output_dir, f"{subtitle.index}.wav")
        
        extract_audio_segment(video_file, start_time, duration, output_file)
        print(f"Extracted audio segment {subtitle.index} to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Extract audio segments from a video file based on subtitles.")
    parser.add_argument("srt_file", type=str, help="Path to the .srt subtitle file.")
    parser.add_argument("video_file", type=str, help="Path to the video file.")
    parser.add_argument("output_dir", type=str, help="Directory to save the extracted audio segments.")
    
    args = parser.parse_args()

    process_subtitles(args.srt_file, args.video_file, args.output_dir)

if __name__ == "__main__":
    main()

