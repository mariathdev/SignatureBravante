import sys
import io
import os
from PIL import Image, ImageDraw, ImageFont

def image_to_byte_array(image: Image.Image) -> bytes:
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    return image_bytes.getvalue()

def main():
    if len(sys.argv) < 5:
        sys.stderr.write("Erro: argumentos insuficientes. Esperado: nome, setor, email, telefone.\n")
        sys.exit(1)

    try:
        # Caminho da imagem
        base_path = os.path.join(os.path.dirname(__file__), 'public', 'assets', 'SignatureBravanteBlank.png')
        if not os.path.exists(base_path):
            sys.stderr.write(f"Imagem base não encontrada: {base_path}\n")
            sys.exit(1)

        image = Image.open(base_path).convert("RGB")
        draw = ImageDraw.Draw(image)

        # Fonte Arial
        font_path = "C:\\Windows\\Fonts\\arial.ttf"
        main_font = ImageFont.truetype(font_path, size=20)
        secondary_font = ImageFont.truetype(font_path, size=18)

        # Dados
        signName = sys.argv[1]
        signSector = sys.argv[2]
        signEmail = sys.argv[3]
        signPhone = sys.argv[4]

        # Posição base
        x = 395
        y_start = 65
        spacing = 26
        extra_spacing = 14  # espaçamento extra entre os blocos

        # Bloco 1
        draw.text((x, y_start), signName, font=main_font, fill=(255, 219, 152))
        draw.text((x, y_start + spacing), signSector, font=main_font, fill=(255, 255, 255))

        # Bloco 2 (com separação extra)
        draw.text((x, y_start + 2 * spacing + extra_spacing), signEmail, font=secondary_font, fill=(255, 255, 255))
        draw.text((x, y_start + 3 * spacing + extra_spacing), signPhone, font=secondary_font, fill=(255, 255, 255))

        sys.stdout.buffer.write(image_to_byte_array(image))

    except Exception as e:
        sys.stderr.write(f"Erro ao gerar imagem: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()