from moviepy.editor import VideoFileClip
import pygame
import sys

def play_video(video_path):
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption("MoviePy Video Playback")

    # Load the video
    clip = VideoFileClip(video_path)
    screen = pygame.display.set_mode(clip.size)
    
    # Play the video
    for frame in clip.iter_frames(fps=clip.fps, dtype="uint8"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Convert frame to surface and blit to screen
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()

    # Close the video
    clip.reader.close()
    if clip.audio is not None:
        clip.audio.reader.close_proc()

    pygame.quit()

# Example usage
if __name__ == "__main__":
    video_path = "./src/intro_r.mp4"
    play_video(video_path)
