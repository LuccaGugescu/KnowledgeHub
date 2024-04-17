from moviepy.editor import CompositeVideoClip, VideoFileClip, TextClip, ColorClip
import os


class VideoEditor:

    def __init__(self, script_directory):
        self.script_directory = script_directory

    def run_converter(self):
        directory_name = "video"
        filename = "convert_assets_to_video.ps1"
        file_path = os.path.join(self.script_directory, directory_name, filename)
        try:
            os.system(f'powershell.exe -File "{file_path}"')
            print("PowerShell script executed successfully.")
        except Exception as e:
            print("Error running PowerShell script:", e)

    def generate_text_clip(self, text_file, duration, font_path, font_size, color='white', video_width=390,
                           video_height=844,
                           position='bottom', margin_top=0, padding=10):
        text = []
        with open(text_file, 'r') as file:
            for line in file:
                text.append(line.strip())
        n_texts = len(text)
        text_clips = []
        for i, txt in enumerate(text):
            # Create a TextClip with the text
            txt_clip = TextClip(txt, fontsize=font_size, color=color,
                                size=(video_width * 3 / 4, None), font=font_path, method='caption')

            # Add padding to the text clip
            padded_txt_clip = self.add_padding_to_clip(txt_clip, padding)

            # Calculate the duration of each text clip
            clip_duration = duration / n_texts

            # Set duration, start, and end time
            padded_txt_clip = padded_txt_clip.set_duration(clip_duration)
            padded_txt_clip = padded_txt_clip.set_start(i * clip_duration)
            padded_txt_clip = padded_txt_clip.set_end((i + 1) * clip_duration)

            # Set position
            if position == 'center':
                padded_txt_clip = padded_txt_clip.set_position(('center', 'center'), relative=True)
            elif position == 'top':
                # Calculate position with margin from the top
                margin = margin_top / video_height
                padded_txt_clip = padded_txt_clip.set_position(('center', margin), relative=True)

            # Add fade-in and fade-out effects
            fade_duration = min(0.1, clip_duration * 0.2)
            padded_txt_clip = padded_txt_clip.fadein(fade_duration).fadeout(fade_duration)

            text_clips.append(padded_txt_clip)
        return text_clips

    def add_padding_to_clip(self, clip, padding):
        # Calculate the dimensions of the padding clip
        padded_clip_width = clip.size[0] + 2 * padding
        padded_clip_height = clip.size[1] + 2 * padding

        # Create a ColorClip for padding
        padding_color_clip = ColorClip(size=(int(padded_clip_width), int(padded_clip_height)),
                                       color=(0, 0, 0))  # Adjust color as needed

        # Composite text clip with padding
        padded_clip = CompositeVideoClip([padding_color_clip.set_opacity(0.7), clip.set_position('center')])

        return padded_clip

    def generate_title(self, title_file, duration, font_path, font_size, color='white', video_width=390,
                       video_height=844,
                       position='top', margin_top=0, padding=10):
        # Read title text from file
        with open(title_file, 'r') as file:
            title_text = file.read().strip()

        # Create a TextClip with the title text
        title_clip = TextClip(title_text, fontsize=font_size, color=color,
                              size=(video_width * 3 / 4, None), font=font_path, method='caption')

        # Calculate title clip dimensions
        title_width, title_height = title_clip.size

        # Create a ColorClip for padding
        padding_color_clip = ColorClip(size=(int(title_width + 2 * padding), int(title_height + 2 * padding)),
                                       color=(0, 0, 0))

        # Composite title clip with padding
        title_clip_with_padding = CompositeVideoClip([padding_color_clip.set_opacity(0.1), title_clip.set_position('center')])

        # Set duration and position
        title_clip_with_padding = title_clip_with_padding.set_duration(duration)
        if position == 'top':
            # Calculate position with margin from the top
            margin = margin_top / video_height
            title_clip_with_padding = title_clip_with_padding.set_position(('center', margin), relative=True)

        # Add fade-in and fade-out effects
        fade_duration = min(0.1, duration * 0.2)
        title_clip_with_padding = title_clip_with_padding.fadein(fade_duration).fadeout(fade_duration)

        return title_clip_with_padding

    def add_text_to_video(self, video_file, text_file, title_file, output_file, font_path, font_size, color='white'):
        video_clip = VideoFileClip(video_file)
        video_width = video_clip.size[0]  # Get video width
        video_height = video_clip.size[1]  # Get video height

        # Adjust margin top according to your preference
        margin_top = 150  # Adjust as needed

        text_clips = self.generate_text_clip(text_file, video_clip.duration, font_path, font_size, color,
                                             video_width=video_width, video_height=video_height,
                                             position="center")
        title_clip = self.generate_title(title_file, 3, font_path, font_size, "#8723D7",
                                         video_width=video_width, video_height=video_height,
                                         position="top", margin_top=margin_top)

        final_clip = CompositeVideoClip([video_clip] + [title_clip] + text_clips)

        final_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')
