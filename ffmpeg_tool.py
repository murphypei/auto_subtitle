import ffmpeg
import subprocess


# def audio_extract(input_video, output_audio):
#     command = ["ffmpeg", "-i", "pipe:0", "-vn -acodec copy", output_audio]

#     with open(input_path, "rb") as f:
#         subprocess.run(command, input=f.read())


def audio_extract(input_video, output_audio):
    command = ["ffmpeg", "-i", input_video, "-vn", "-acodec", "copy", output_audio]
    print(" ".join(command))
    subprocess.run(command)


def srt2ass(srt_file, ass_file):
    assert srt_file.endswith(".srt"), f"{srt_file} not endwith .srt"
    assert ass_file.endswith(".ass"), f"{ass_file} not endwith .ass"
    command = ["ffmpeg", "-i", srt_file, ass_file]
    print(" ".join(command))
    subprocess.run(command)


def add_subtitle_to_video(input_video, subtitle_file, output_video, font_path=None):
    if font_path:
        vf_commnd = f"subtitles={subtitle_file}:force_style='{subtitle_file}'"
    else:
        vf_commnd = f"subtitles={subtitle_file}"
    command = [
        "ffmpeg",
        "-i",
        input_video,
        "-vf",
        vf_commnd,
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-strict",
        "-2",
        output_video,
    ]
    print(" ".join(command))
    subprocess.run(command)


if __name__ == "__main__":
    # audio_extract("dress_en.mp4", "test_ffmpeg.wav")
    # srt2ass("id.srt", "id.ass")
    add_subtitle_to_video("dress_en.mp4", "id.ass", "id_output.mp4")
