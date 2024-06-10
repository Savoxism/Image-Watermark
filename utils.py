from PIL import Image, ImageDraw, ImageFont
import io

def add_watermark(image_stream, watermark_text):
    # Open the image file
    img = Image.open(image_stream).convert("RGBA")
    
    # Create a transparent overlay for the watermark
    txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
    
    # Add watermark
    draw = ImageDraw.Draw(txt)
    
    # Specify the path to the Arial font file
    font_path = "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf"  # Change this to your system's Arial font path
    font = ImageFont.truetype(font_path, 120)  # Increase the font size
    
    # Calculate text size
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    textwidth, textheight = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    # Position the text at the center
    width, height = img.size
    x = (width - textwidth) / 2
    y = (height - textheight) / 2
    
    # Draw the text with transparency
    draw.text((x, y), watermark_text, fill=(255, 255, 255, 128), font=font)  # 128 for semi-transparency
    
    # Rotate the overlay
    txt = txt.rotate(45, expand=1)
    
    # Resize the rotated overlay to match the original image size
    txt = txt.resize(img.size, resample=Image.BICUBIC)
    
    # Composite the watermark with the original image
    watermarked = Image.alpha_composite(img, txt)
    
    # Save the watermarked image to a BytesIO object
    img_io = io.BytesIO()
    watermarked = watermarked.convert("RGB")  # Convert back to RGB
    watermarked.save(img_io, 'JPEG', quality=85)
    img_io.seek(0)
    
    return img_io