import cv2
import numpy as np

def text_to_bin(text):
    return [format(ord(i), '08b') for i in text]

def encode_video(input_video, secret_text, output_video):
    cap = cv2.VideoCapture(input_video)
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
    
    secret_text += "####"
    binary_secret = "".join(text_to_bin(secret_text))
    data_index = 0
    data_len = len(binary_secret)
    
    first_frame = True
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        if first_frame and data_index < data_len:
            for y in range(height):
                for x in range(width):
                    if data_index < data_len:
                        pixel = frame[y, x]
                        for c in range(3):
                            if data_index < data_len:
                                # Ensure we work with integers and keep results in 0-255 range
                                color_val = int(pixel[c])
                                pixel[c] = (color_val & ~1) | int(binary_secret[data_index])
                                data_index += 1
                        frame[y, x] = pixel
                    else:
                        break
                if data_index >= data_len:
                    break
            first_frame = False
            
        out.write(frame)
        
    cap.release()
    out.release()
    print(f"Bericht verstopt in {output_video}")

if __name__ == "__main__":
    encode_video("video.mp4", "GEHEIM_VIDEO_BERICHT", "encoded_video.mkv")


