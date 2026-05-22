import base64
import re
import urllib.request
import os
import zlib

md_file = 'UML_Diagrams.md'
output_dir = '.'

diagram_names = [
    "1_Use_Case_Diagram",
    "2_Class_Diagram",
    "3_Activity_Diagram",
    "4_Sequence_Diagram",
    "5_State_Diagram"
]

try:
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Find all diagram blocks (either mermaid or plantuml)
    blocks = re.findall(r'```(mermaid|plantuml)\n(.*?)\n```', md_content, re.DOTALL)

    for i, (type_, block) in enumerate(blocks):
        name = diagram_names[i] if i < len(diagram_names) else f"diagram_{i+1}"
        print(f"Generating {name}.png as {type_}...")
        
        if type_ == "mermaid":
            # Mermaid rendering via mermaid.ink
            graphbytes = block.encode("utf8")
            base64_bytes = base64.urlsafe_b64encode(graphbytes)
            base64_string = base64_bytes.decode("ascii")
            url = f"https://mermaid.ink/img/{base64_string}?type=png&bgColor=ffffff"
            
        elif type_ == "plantuml":
            # PlantUML rendering via Kroki
            compressed = zlib.compress(block.encode('utf-8'), 9)
            base64_encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
            url = f"https://kroki.io/plantuml/png/{base64_encoded}"

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    out_path = os.path.join(output_dir, f"{name}.png")
                    with open(out_path, "wb") as out_f:
                        out_f.write(response.read())
                    print(f"Successfully saved {out_path}")
                else:
                    print(f"Failed to fetch {name}. HTTP Status: {response.status}")
        except Exception as e:
            print(f"Error fetching image for {name}: {e}")
            
except Exception as e:
    print(f"An error occurred: {e}")
