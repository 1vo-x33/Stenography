import cv2
import numpy as np

def bin_to_text(bin_data):
    text = ''
    for i in range(0, len(bin_data), 8):
        byte = bin_data[i:i+8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    return text

def decode_video(video_path):
    cap = cv2.VideoCapture(video_path)
    binary_data = ""
    found = False
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        height, width, _ = frame.shape
        for y in range(height):
            for x in range(width):
                pixel = frame[y, x]
                for c in range(3):
                    binary_data += str(pixel[c] & 1)
                
                if len(binary_data) % 800 == 0:
                    decoded = bin_to_text(binary_data)
                    if "####" in decoded:
                        print(f"GEHEIM BERICHT GEVONDEN: {decoded.split('####')[0]}")
                        found = True
                        break
            if found: break
        if found: break
        break
        
    cap.release()
    if not found:
        print("Geen bericht gevonden.")

if __name__ == "__main__":
    decode_video("encoded_video.mkv")
