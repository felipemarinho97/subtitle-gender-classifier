import argparse
import srt
import ffmpeg
import os
from datetime import timedelta
import torch
from model import ECAPA_gender
import tempfile
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_audio_segment(video_file, start_time, duration, output_file):
    # Run ffmpeg command to extract audio and suppress output
    ffmpeg.input(video_file, ss=start_time, t=duration).output(output_file).run(quiet=True, overwrite_output=True)

def detect_gender(audio_file: str, model, device: torch.device) -> str:
    with torch.no_grad():
        output = model.predict(audio_file, device=device)
        return output

def process_subtitles_with_gender(srt_file, video_file, output_srt_file, model, device):
    with open(srt_file, 'r', encoding='utf-8') as f:
        subtitles = list(srt.parse(f.read()))

    output_subtitles = []
    tmp_dir = tempfile.mkdtemp(prefix='/tmp/')

    def process_subtitle(subtitle):
        start_time = subtitle.start.total_seconds()
        duration = (subtitle.end - subtitle.start).total_seconds()
        audio_file = f"{tmp_dir}/temp_audio_{subtitle.index}.wav"

        # Extract the audio segment for the current subtitle
        extract_audio_segment(video_file, start_time, duration, audio_file)

        # Detect gender for the extracted audio
        gender = detect_gender(audio_file, model, device)

        # Tag the subtitle text with the detected gender
        tagged_text = f"<{gender}>{subtitle.content}</{gender}>"
        subtitle.content = tagged_text

        # Remove temporary audio file
        os.remove(audio_file)

        return subtitle

    # Use ThreadPoolExecutor to process subtitles in parallel
    with ThreadPoolExecutor() as executor:
        future_to_subtitle = {executor.submit(process_subtitle, subtitle): subtitle for subtitle in subtitles}
        
        # Use tqdm to show the progress bar
        for future in tqdm(as_completed(future_to_subtitle), total=len(subtitles), desc="Processing subtitles"):
            output_subtitles.append(future.result())

    # Sort subtitles by index to maintain original order
    output_subtitles.sort(key=lambda x: x.index)

    # Write the modified subtitles to a new .srt file
    with open(output_srt_file, 'w', encoding='utf-8') as f:
        f.write(srt.compose(output_subtitles))

def main():
    parser = argparse.ArgumentParser(description="Detect gender for each subtitle segment and tag it.")
    parser.add_argument("srt_file", type=str, help="Path to the .srt subtitle file.")
    parser.add_argument("video_file", type=str, help="Path to the video file.")
    parser.add_argument("output_srt_file", type=str, help="Path to save the tagged .srt subtitle file.")
    
    args = parser.parse_args()

    # Load the gender detection model
    model = ECAPA_gender.from_pretrained("JaesungHuh/ecapa-gender")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Process subtitles and tag them with gender
    process_subtitles_with_gender(args.srt_file, args.video_file, args.output_srt_file, model, device)

if __name__ == "__main__":
    main()
