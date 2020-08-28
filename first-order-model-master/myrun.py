import imageio
import numpy as np

from skimage.transform import resize
from IPython.display import HTML
import warnings
from demo import load_checkpoints
from demo import make_animation
from skimage import img_as_ubyte
import ffmpeg
import moviepy.editor as mpe

warnings.filterwarnings("ignore")

source_image = imageio.imread('images/2.jpeg')
driving_video = imageio.get_reader('images/driver.mp4')
fps = driving_video.get_meta_data()['fps']
#Resize image and video to 256x256

source_image = resize(source_image, (256, 256))[..., :3]
driving_video = [resize(frame, (256, 256))[..., :3] for frame in driving_video]


#HTML(display(source_image, driving_video).to_html5_video())
print("loaded video")

generator, kp_detector = load_checkpoints(config_path='config/vox-256.yaml', 
                            checkpoint_path='checkpoints/vox-cpk.pth.tar', cpu=True)

print("created model")

predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=True, cpu=True)

print("created predicitions")

#save resulting video

imageio.mimsave('generated.mp4', [img_as_ubyte(frame) for frame in predictions], fps=fps)

video_clip = mpe.VideoFileClip('generated.mp4')

 #extract audio from original driving video
audio_clip = mpe.AudioFileClip('images/driver.mp4')

#set audio into your output video and saving it to your google drive
final_clip = video_clip.set_audio(audio_clip)
final_clip.write_videofile("final.mp4",fps=fps)

video_clip.close()
audio_clip.close()
final_clip.close()

#HTML(predictions.to_html5_video())
print("prepared image animation")
