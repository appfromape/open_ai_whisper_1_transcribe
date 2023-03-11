import json
import openai

openai.api_key = "你的 openai api 金鑰"

with open("audio.mp3", "rb") as audio_file:
    try:
        transcription = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file,
            response_format="srt",
            language="zh",
        )
        try:
            text = json.loads(transcription)
            lines = text.split('\n')
            new_lines = [line.replace(')', '') for line in lines if not line.startswith('HTTP')]
            new_text = "1" + "\n" + '\n'.join(new_lines).strip() + '\n'
            with open("out.srt", "w") as f:
                f.write(new_text)
        except json.decoder.JSONDecodeError as e:
            print(f"JSON 解碼出錯：{e}")
            # print(f"響應文本：{transcription}")
            text = transcription
            lines = text.split('\n')
            new_lines = [line.replace(')', '') for line in lines if not line.startswith('HTTP')]
            new_text = '\n'.join(new_lines).strip() + '\n'
            with open("out.srt", "w") as f:
                f.write(new_text)
    except openai.error.APIError as e:
        text = str(e)
        lines = text.split('\n')
        new_lines = [line.replace(')', '') for line in lines if not line.startswith('HTTP')]
        new_text = "1" + "\n" + '\n'.join(new_lines).strip() + '\n'
        with open('out.srt', 'w') as f:
            f.write(new_text)
