import argparse
import torch
from model import ECAPA_gender

def detect_gender(audio_file: str):
    # Carregar o modelo pré-treinado
    model = ECAPA_gender.from_pretrained("JaesungHuh/ecapa-gender")
    model.eval()

    # Verificar se há GPU disponível e mover o modelo para o dispositivo apropriado
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Realizar a predição com o modelo
    with torch.no_grad():
        output = model.predict(audio_file, device=device)
        print(f"Gender: {output}")

def main():
    parser = argparse.ArgumentParser(description="Detect gender in an audio file.")
    parser.add_argument("audio_file", type=str, help="Path to the audio file for gender detection.")
    
    args = parser.parse_args()

    detect_gender(args.audio_file)

if __name__ == "__main__":
    main()

