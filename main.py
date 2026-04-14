import whisper
import ollama
import wave
import sounddevice as sd
import scipy.io.wavfile as scipy_wav
from piper import PiperVoice, SynthesisConfig

from db_actions import insert_conversation_line

class EntropyBot:
    def __init__(self):
        # messages history
        self.messages = []

        # synthesis configuration
        self.synthesis_config = SynthesisConfig(
            volume=0.5,             # half as loud
            length_scale=0.5,       # higher the slower
            noise_scale=1.0,        # more audio variation
            noise_w_scale=1.0,      # more speaking variation
            normalize_audio=False,  # use raw audio from voice
        )
        # load the model once
        self.model = whisper.load_model("base")
        # load the voice once
        self.voice = PiperVoice.load("voices/en/en_US-amy-low.onnx")

    def record(self, duration=5, sr=16000):
        audio = sd.rec(int(duration * sr), samplerate=sr, channels=1)
        print("Start talking for 5 seconds")
        sd.wait()
        scipy_wav.write("io/input.wav", sr, audio)

    def listen(self):
        # transcribe the record
        recorded = self.model.transcribe("io/input.wav", verbose=True)
        recorded_text = recorded["text"]
        insert_conversation_line("user", recorded_text)
        self.messages.append({ "role": "user", "content": recorded_text })
        return recorded_text

    def reply(self):
        # send to ollama
        response = ollama.chat(model="llama3.1", messages=self.messages)
        reply = response["message"]["content"]
        insert_conversation_line("assistant", reply)
        self.messages.append({ "role": "assistant", "content": reply })

        print("Reply: ", reply)

        with wave.open("io/output.wav", "wb") as wav_file:
            self.voice.synthesize_wav(reply, wav_file, self.synthesis_config)

        # play the reply out loud
        sr, data = scipy_wav.read("io/output.wav")
        sd.play(data, sr)
        sd.wait()

    def main(self):
        # infinite use
        while True:
            self.record()
            recorded_text = self.listen()
            if "stop the program" in recorded_text:
                break
            self.reply()

assistant = EntropyBot()
assistant.main()