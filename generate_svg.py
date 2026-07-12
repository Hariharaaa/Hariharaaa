import sys

def main():
    with open("ascii_art.txt", "r") as f:
        lines = f.readlines()
    
    font_size = 12
    line_height = 14
    width = max(len(l) for l in lines) * 7.5 + 40
    height = len(lines) * line_height + 40
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
    <style>
        .ascii {{
            font-family: 'Courier New', Courier, monospace;
            font-size: {font_size}px;
            fill: #6e40c9;
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
    
    for i in range(len(lines)):
        delay = i * 0.05
        svg += f'        .line-{i} {{ animation-delay: {delay}s; }}\n'
        
    svg += '''    </style>
    <g class="ascii">
'''
    
    y = 20
    for i, line in enumerate(lines):
        line = line.rstrip('\n').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        svg += f'        <text x="20" y="{y}" class="line line-{i}">{line}</text>\n'
        y += line_height
        
    svg += '''    </g>
</svg>'''

    with open("ascii_animation.svg", "w") as f:
        f.write(svg)

if __name__ == "__main__":
    main()
