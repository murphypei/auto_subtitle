from whisper_tool import WhisperProcessor
from ffmpeg_tool import add_subtitle_to_video, audio_extract


if __name__ == "__main__":
    # 输入的视频文件
    input_video = "input.mp4"
    # 输出的视频文件
    output_video = "output.mp4"
    # 提取的音频文件
    output_audio = "output.wav"
    # 提取的字幕文件
    srt_file = "subtitle.srt"

    # 提取的字幕ass文件
    # ass_file = "subtitle.ass"

    # 如果需要翻译
    # target_language = "ru"

    # 部分语言需要自定义字体
    # font_path = ""

    # 提取音频文件
    audio_extract(input_video, output_audio)

    # 音转文
    whisper_processor = WhisperProcessor()
    whisper_processor.extract_subtitle(output_audio, srt_path=srt_file)
    # whisper_processor.extract_subtitle(output_audio, srt_path=srt_file, target_language=target_language)

    # 合成视频
    add_subtitle_to_video(input_video, srt_file, output_video)
    # add_subtitle_to_video(input_video, srt_file, output_video, font_path)
