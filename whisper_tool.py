import torch
import whisper
import json
from googletrans import Translator

# def load_model_bin(model_path, device):
#     def hf_to_whisper_states(text):
#         text = re.sub(".layers.", ".blocks.", text)
#         text = re.sub(".self_attn.", ".attn.", text)
#         text = re.sub(".q_proj.", ".query.", text)
#         text = re.sub(".k_proj.", ".key.", text)
#         text = re.sub(".v_proj.", ".value.", text)
#         text = re.sub(".out_proj.", ".out.", text)
#         text = re.sub(".fc1.", ".mlp.0.", text)
#         text = re.sub(".fc2.", ".mlp.2.", text)
#         text = re.sub(".fc3.", ".mlp.3.", text)
#         text = re.sub(".fc3.", ".mlp.3.", text)
#         text = re.sub(".encoder_attn.", ".cross_attn.", text)
#         text = re.sub(".cross_attn.ln.", ".cross_attn_ln.", text)
#         text = re.sub(".embed_positions.weight", ".positional_embedding", text)
#         text = re.sub(".embed_tokens.", ".token_embedding.", text)
#         text = re.sub("model.", "", text)
#         text = re.sub("attn.layer_norm.", "attn_ln.", text)
#         text = re.sub(".final_layer_norm.", ".mlp_ln.", text)
#         text = re.sub("encoder.layer_norm.", "encoder.ln_post.", text)
#         text = re.sub("decoder.layer_norm.", "decoder.ln.", text)
#         return text

#     # Load HF Model
#     hf_state_dict = torch.load(model_path, map_location=torch.device(device))  # pytorch_model.bin file

#     # Rename layers
#     for key in list(hf_state_dict.keys())[:]:
#         new_key = hf_to_whisper_states(key)
#         hf_state_dict[new_key] = hf_state_dict.pop(key)

#     # Init Whisper Model and replace model weights
#     whisper_model = whisper.load_model("large")
#     whisper_model.load_state_dict(hf_state_dict)
#     return whisper_model


class WhisperProcessor:
    def __init__(self, model_type="large") -> None:
        self.whisper_model = whisper.load_model(model_type)
        print(f"<{model_type}> whisper model loaded")

        self.translator = Translator()

    def write_srt(self, transcribe_seg, srt_path, target_language=None):
        def reformat_time(second):
            m, s = divmod(second, 60)
            h, m = divmod(m, 60)
            hms = "%02d:%02d:%s" % (h, m, str("%.3f" % s).zfill(6))
            hms = hms.replace(".", ",")
            return hms

        srt_lines = []
        for i, data in enumerate(transcribe_seg):
            text = data["text"]
            if target_language:
                text = self.translator.translate(data["text"], dest=target_language).text
            srt_line = f"{str(i + 1)}\n{reformat_time(data['start'])} --> {reformat_time(data['end'])}\n{text}\n\n"
            print(srt_line)
            srt_lines.append(srt_line)

        with open(srt_path, "w", encoding="utf-8") as f:
            f.writelines(srt_lines)

    def detect_language(self, audio_file):
        print("reading the audio file")
        audio = whisper.load_audio(audio_file)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(self.whisper_model.device)
        det_lang_res = self.whisper_model.detect_language(mel)
        print(det_lang_res)

    def whisper_transcribe(self, audio_file, language=None):
        print("Start whisper transcribing...")
        result = self.whisper_model.transcribe(audio_file, language=language)
        print(f"Transcribe language: {result['language']}, {len(result['text'])}")
        with open("whisper_transcribe_result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        return result

    def extract_subtitle(self, audio_file, language=None, target_language=None, srt_path="subtitle.srt"):
        result = self.whisper_transcribe(audio_file, language)
        self.write_srt(result["segments"], srt_path, target_language)


def test_translate():
    translator = Translator()
    print(translator.translate("There is no people", dest="zh-CN"))


if __name__ == "__main__":
    processor = WhisperProcessor()
    processor.extract_subtitle("dress_en.wav", "en", "id", "id.srt")
