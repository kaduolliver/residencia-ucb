import requests
import time
import json
import os
from yt_dlp import YoutubeDL
from dotenv import load_dotenv

# ===================================
# CONFIGURAÇÃO INICIAL
# ===================================

load_dotenv()

# Crie em https://www.assemblyai.com/dashboard/signup

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
if not ASSEMBLYAI_API_KEY:
    raise ValueError("A variável ASSEMBLYAI_API_KEY não está definida!") 

VIDEO_URL = "https://www.youtube.com/watch?v=_1ok4o9GXzA"  # Link do youtube
ARQ_AUDIO = "audio_temp.mp3"

# ===================================
# BAIXAR ÁUDIO DO YOUTUBE
# ===================================

print("Baixando áudio do YouTube...")
ydl_opts = {
    "format": "bestaudio",
    "outtmpl": "audio_temp.%(ext)s",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192"
    }],
    "paths": {"home": "."},
}

with YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(VIDEO_URL, download=True)
    ARQ_AUDIO = f"audio_temp.mp3"

if not os.path.exists(ARQ_AUDIO):
    print("Erro: o arquivo de áudio não foi criado. Verifique se o vídeo tem áudio disponível.")
    exit(1)

print("Áudio baixado com sucesso!")

# ===================================
# ENVIAR ÁUDIO PARA ASSEMBLYAI
# ===================================

headers = {"authorization": ASSEMBLYAI_API_KEY}

print("Enviando áudio para a API...")
with open(ARQ_AUDIO, "rb") as f:
    upload_response = requests.post("https://api.assemblyai.com/v2/upload", headers=headers, data=f)
if upload_response.status_code != 200:
    print("Falha no upload:", upload_response.text)
    exit(1)
audio_url = upload_response.json().get("upload_url")

print(f"Upload concluído: {audio_url}")

# ===================================
# SOLICITAR TRANSCRIÇÃO
# ===================================

transcript_request = {
    "audio_url": audio_url,
    "speaker_labels": True,  
    "language_code": "pt"
}
response = requests.post("https://api.assemblyai.com/v2/transcript", json=transcript_request, headers=headers)
transcript_id = response.json()["id"]

print(f"Transcrição iniciada (ID: {transcript_id})")

# ===================================
# AGUARDAR CONCLUSÃO
# ===================================

while True:
    status = requests.get(f"https://api.assemblyai.com/v2/transcript/{transcript_id}", headers=headers).json()
    if status.get("status") == "completed":
        print("Transcrição concluída!")
        break
    elif status.get("status") == "error":
        print("Erro:", status.get("error"))
        exit(1)
    else:
        print(f"Status: {status.get('status')}...")
    time.sleep(5)


# ===================================
# SALVAR RESULTADOS
# ===================================

with open("transcricao.json", "w", encoding="utf-8") as f:
    json.dump(status, f, ensure_ascii=False, indent=4)

with open("transcricao.txt", "w", encoding="utf-8") as f:
    if "utterances" in status:
        for utt in status["utterances"]:
            start = utt["start"] / 1000
            end = utt["end"] / 1000
            speaker = utt["speaker"]
            text = utt["text"]
            f.write(f"[{start:.2f}s → {end:.2f}s] {speaker}: {text}\n")
    else:
        f.write(status.get("text", ""))

print("Arquivos salvos: transcricao.txt e transcricao.json")
