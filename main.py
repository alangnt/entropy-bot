import whisper
import ollama
import wave
import sounddevice as sd
import scipy.io.wavfile as scipy_wav
from piper import PiperVoice, SynthesisConfig

class EntropyBot:
    def __init__(self):
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

        # TODO: repair the prompt
        # initial prompt
        #self.init_prompt = "You are my second brain, acting like a human with feelings"

    def record(self, duration=5, sr=16000):
        audio = sd.rec(int(duration * sr), samplerate=sr, channels=1)
        print("Start talking for 5 seconds")
        sd.wait()
        scipy_wav.write("io/input.wav", sr, audio)

    def listen(self):
        # transcribe the record
        recorded = self.model.transcribe("io/input.wav", verbose=True)
        return recorded["text"]

    def reply(self, recorded_text):
        # send to ollama
        response = ollama.chat(model="llama3.1", messages=[
            #{"role": "user", "content": self.init_prompt},
            {"role": "user", "content": recorded_text}
        ])
        reply = response["message"]["content"]

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
            self.reply(recorded_text)

assistant = EntropyBot()
assistant.main()