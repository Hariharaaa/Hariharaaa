import sys
from PIL import Image

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.5)
    return image.resize((new_width, new_height))

def main(image_path, new_width=80):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(e)
        return

    image = resize_image(image, new_width)
    
    image_rgb = image.convert("RGB")
    pixels = image_rgb.getdata()
    
    grayscale = image.convert("L").getdata()
    
    chars_with_color = []
    for (rgb, gray) in zip(pixels, grayscale):
        char = ASCII_CHARS[min(gray // 25, len(ASCII_CHARS) - 1)]
        chars_with_color.append((char, rgb))
    
    width, height = image.size
    
    font_size = 12
    line_height = 14
    svg_width = width * 7.2 + 40
    svg_height = height * line_height + 40
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="100%" height="100%">
    <style>
        .ascii {{
            font-family: 'Courier New', Courier, monospace;
            font-size: {font_size}px;
            white-space: pre;
        }}
        @keyframes fadeIn {{
            0% {{ opacity: 0; transform: translateY(5px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
        .line {{
            opacity: 0;
            animation: fadeIn 0.4s ease-out forwards;
        }}
'''
    
    for i in range(height):
        delay = i * 0.05
        svg += f'        .line-{i} {{ animation-delay: {delay}s; }}\n'
        
    svg += '''    </style>
    <rect width="100%" height="100%" fill="#0D1117" />
    <g class="ascii">
'''
    
    y = 20
    idx = 0
    for i in range(height):
        svg += f'        <text x="20" y="{y}" class="line line-{i}">'
        
        current_color = None
        span_text = ""
        
        for j in range(width):
            char, (r, g, b) = chars_with_color[idx]
            idx += 1
            
            char = char.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            
            if hex_color == current_color:
                span_text += char
            else:
                if current_color is not None:
                    svg += f'<tspan fill="{current_color}">{span_text}</tspan>'
                current_color = hex_color
                span_text = char
                
        if current_color is not None:
            svg += f'<tspan fill="{current_color}">{span_text}</tspan>'
            
        svg += '</text>\n'
        y += line_height
        
    svg += '''    </g>
</svg>'''

    with open("ascii_animation.svg", "w") as f:
        f.write(svg)
    print("Generated colored ASCII animation.")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "Screenshot 2026-07-12 at 8.55.31 PM.png", 80)
