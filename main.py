from editor import VideoEditor
import os

if __name__ == '__main__':
    # Get the directory of the current script
    curr_dir = os.path.dirname(os.path.abspath(__file__))

    sm = VideoEditor.VideoEditor(curr_dir)
    sm.run_converter()
    # Define file paths and parameters
    video_file = os.path.join(curr_dir, "video", "converted_video.mp4")
    text_file = os.path.join(curr_dir, "editor", "text.txt")
    title_file = os.path.join(curr_dir, "editor", "title.txt")

    font_path = os.path.join(curr_dir, "editor", "font.ttf")  # Provide path to your font file

    output_file = 'output_video.mp4'
    font_size = 20
    color = 'white'  # Text color
    sm.add_text_to_video(video_file, text_file, title_file, output_file, font_path, font_size, color)
