import pytube
import subprocess
import os
import cv2
import moviepy.editor as mp
from TaskMatrix.visual_chatgpt import ConversationBot
from dotenv import load_dotenv

load_dotenv() 


def download_youtube_video(video_url, download_path, filename="video.mp4"):
  """Downloads a YouTube video to a specified path.

  Args:
    video_url: The URL of the YouTube video to download.
    download_path: The path to save the downloaded video to.
  """

  # Create a YouTube object from the video URL.
  yt = pytube.YouTube(video_url)

  # Get the highest quality stream of the video.
  #stream = yt.streams.get_highest_resolution()
  stream = yt.streams.filter(res='360p').first()

  # Download the video to the specified path.
  stream.download(download_path, filename)

  # Return the path to the downloaded video.
  return download_path

def preprocess(video_path, output_path, video_length=30):
  """Preprocesses a video.

  Args:
    video_path: The path to the video to preprocess.
  """

  subprocess.run(["ffmpeg", "-ss", "0", "-i", video_path, "-c", "copy", "-t",  str(video_length), output_path])
  subprocess.run(["rm", video_path])
  return output_path


# Function to extract frames from the video and save them as thumbnails
def extract_frames(video_file, output_folder, num_frames):
    clip = mp.VideoFileClip(video_file)
    frame_rate = clip.fps
    duration = clip.duration
    interval = duration / num_frames

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(num_frames):
        time = i * interval
        frame = clip.get_frame(time)
        thumbnail_path = os.path.join(output_folder, f"frame_{i}.jpg")
        cv2.imwrite(thumbnail_path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    return [os.path.join(output_folder, f"frame_{i}.jpg") for i in range(num_frames)]

#if __name__ == "__main__":
#    video_file = 'output.mp4'
#    output_folder = './thumbnails'
#    num_frames = 10  # Number of frames/thumbnails to generate

    # Extract frames from the video
#    image_paths = extract_frames(video_file, output_folder, num_frames)


def generate_description(img):
  # load = "ImageCaptioning_cuda:0,Text2Image_cuda:0"
  #load = "Text2Box_cuda:0,Segmenting_cuda:0,Inpainting_cuda:0,ImageCaptioning_cuda:0"
  load = "ImageCaptioning_cuda:0"
  load_dict = {e.split('_')[0].strip(): e.split('_')[1].strip() for e in load.split(',')}

  bot = ConversationBot(load_dict=load_dict)
  state = []

  bot.init_agent('English')
  bot.run_image(img, state, '', 'English')
  bot.run_text('Describe the image as vividly as possible in no more than 2 paragraphs', state)

  output = bot.memory.buffer
  bot.memory.clear()
  return output.split('\n')[-1].split(':')[-1].strip()


def generate_descriptions(directory, desc_file='descriptions.txt'):
    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(f'Generating descriptions for {f}')
            d = generate_description(f)
            with open(desc_file, "a") as a_file:
                a_file.write(d)
                a_file.write("\n")