from PIL import Image

def text_to_bin(text):
    return [format(ord(i), '08b') for i in text]

def encode_image(input_filepath, secret_text, output_filepath):
    try:
        img = Image.open(input_filepath)
        if img.mode != 'RGB':
            img = img.convert('RGB')
    except FileNotFoundError:
        return

    secret_text += "####"
    binary_secret = "".join(text_to_bin(secret_text))
    
    data_index = 0
    data_len = len(binary_secret)
    
    encoded_img = img.copy()
    pixels = encoded_img.load()
    width, height = encoded_img.size
    
    total_pixels = width * height
    max_bytes = (total_pixels * 3) // 8
    required_bytes = len(binary_secret) // 8
    
    if required_bytes > max_bytes:
        return

    for y in range(height):
        for x in range(width):
            if data_index < data_len:
                r, g, b = pixels[x, y]
                
                if data_index < data_len:
                    r = (r & ~1) | int(binary_secret[data_index])
                    data_index += 1
                
                if data_index < data_len:
                    g = (g & ~1) | int(binary_secret[data_index])
                    data_index += 1
                    
                if data_index < data_len:
                    b = (b & ~1) | int(binary_secret[data_index])
                    data_index += 1
                    
                pixels[x, y] = (r, g, b)
            else:
                break
        if data_index >= data_len:
            break
            
    encoded_img.save(output_filepath, "PNG")

original_image = "image.png"
encoded_image_file = "encoded.png"
secret_message = "SECRET_AGENT_007"

encode_image(original_image, secret_message, encoded_image_file)

