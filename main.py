import whisper
import ollama

import sounddevice as sd
import scipy.io.wavfile as scipy_wav

import wave
from piper import PiperVoice, SynthesisConfig

def record(duration=5, sr=16000):
    audio = sd.rec(int(duration * sr), samplerate=sr, channels=1)
    print("Start talking for 5 seconds")
    sd.wait()
    scipy_wav.write("io/input.wav", sr, audio)

# infinite use
while True:
    record()

    # load whisper
    model = whisper.load_model("base")

    # transcribe the record
    recorded = model.transcribe("io/input.wav", verbose=True)
    recorded_text = recorded["text"]

    # send to ollama
    response = ollama.chat(model="llama3.1", messages=[
        {"role": "user", "content": recorded_text}
    ])
    reply = response["message"]["content"]

    print("Reply: ", reply)

    # synthethize the reply from ollama
    syn_config = SynthesisConfig(
        volume=0.5,             # half as loud
        length_scale=0.5,       # higher the slower
        noise_scale=1.0,        # more audio variation
        noise_w_scale=1.0,      # more speaking variation
        normalize_audio=False,  # use raw audio from voice
    )

    voice = PiperVoice.load("voices/en/en_US-amy-low.onnx")
    with wave.open("io/output.wav", "wb") as wav_file:
        voice.synthesize_wav(reply, wav_file, syn_config)

    # play the reply out loud
    sr, data = scipy_wav.read("io/output.wav")
    sd.play(data, sr)
    sd.wait()