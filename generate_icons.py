from PIL import Image, ImageDraw

def create_icon_home():
    # 128x128 canvas
    size = (128, 128)
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # House Body
    draw.rectangle([30, 60, 98, 110], fill="white")
    # Roof
    draw.polygon([(20, 60), (64, 20), (108, 60)], fill="white")
    # Door
    draw.rectangle([54, 80, 74, 110], fill=(20, 20, 20, 255))
    
    return image

def create_icon_focus():
    size = (128, 128)
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Bolt
    points = [(70, 10), (30, 70), (60, 70), (50, 120), (98, 50), (68, 50)]
    draw.polygon(points, fill="white")
    
    return image

def create_icon_media():
    size = (128, 128)
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Play Button / Screen
    draw.rounded_rectangle([20, 30, 108, 98], radius=15, fill="white")
    # Play triangle
    draw.polygon([(54, 45), (84, 64), (54, 83)], fill="black")
    
    return image

def create_icon_settings():
    size = (128, 128)
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Circle
    draw.ellipse([25, 25, 103, 103], fill="white")
    # Hole
    draw.ellipse([50, 50, 78, 78], fill=(0, 0, 0, 0))
    # Teeth (Simulated via smaller circles around edge)
    # Just simplistic
    
    return image

if __name__ == "__main__":
    create_icon_home().save("assets/icons/sidebar/home.png")
    create_icon_focus().save("assets/icons/sidebar/focus.png")
    create_icon_media().save("assets/icons/sidebar/media.png")
    create_icon_settings().save("assets/icons/sidebar/settings.png")
    print("Generated icons.")
