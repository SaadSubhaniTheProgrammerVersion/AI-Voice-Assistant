import sounddevice as sd
import numpy as np
import noisereduce as nr
from scipy.io.wavfile import write, read
from huggingsound import SpeechRecognitionModel

from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf


# Choose your microphone device and set duration of recording
duration = 5  # seconds
fs = 44100  # Sample rate

# Record audio
print("Starting recording for {} seconds.".format(duration))
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait()  # Wait for the recording to finish
print("Recording finished.")

# Save recording to a WAV file
write("output.wav", fs, myrecording)  # Save as WAV file 

# Read the WAV file
rate, data = read("output.wav")

# Reduce noise
# Ensure the audio data is in mono format for noise reduction
if len(data.shape) > 1:  # check if audio file is stereo
    data = np.mean(data, axis=1)  # convert to mono

reduced_noise = nr.reduce_noise(y=data, sr=rate)

# Save the cleaned audio to a WAV file
write("clean_output.wav", fs, reduced_noise)

# Perform speech recognition
model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-english")
audio_paths = ["clean_output.wav"]
transcriptions = model.transcribe(audio_paths)

# Print the transcriptions
transcription = transcriptions[0]["transcription"]
print(transcription)



# # Following pip packages need to be installed:
# # !pip install git+https://github.com/huggingface/transformers sentencepiece datasets

processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

inputs = processor(text=transcription, return_tensors="pt")

# load xvector containing speaker's voice characteristics from a dataset
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

sf.write("speech.wav", speech.numpy(), samplerate=16000)
