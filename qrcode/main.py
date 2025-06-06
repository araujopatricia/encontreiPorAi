from flask import Flask, request, send_file, render_template_string
import qrcode
from PIL import Image
import io
import os

app = Flask(__name__)
ARQUIVO_SAIDA = "qrcode_gerado.png"
TAMANHO_IMAGEM = (200, 200)
COR_FUNDO = "white"
COR_QR = "black"


def gerar_qrcode(texto: str) -> Image.Image:
    qr_code = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=4,
    )
    qr_code.add_data(texto)
    qr_code.make(fit=True)
    imagem = qr_code.make_image(fill_color=COR_QR, back_color=COR_FUNDO)
    return imagem


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        texto = request.form.get('texto', '').strip()
        if not texto:
            return render_template_string(TEMPLATE, erro="Por favor, digite um link ou texto!", imagem=None)

        try:
            imagem = gerar_qrcode(texto)

            imagem_redimensionada = imagem.resize(TAMANHO_IMAGEM, Image.Resampling.LANCZOS)

            img_io = io.BytesIO()
            imagem_redimensionada.save(img_io, 'PNG')
            img_io.seek(0)

            imagem.save(ARQUIVO_SAIDA)

            import base64
            img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
            return render_template_string(TEMPLATE, erro=None, imagem=img_base64, texto=texto)
        except Exception as e:
            return render_template_string(TEMPLATE, erro=f"Erro ao gerar QR Code: {str(e)}", imagem=None)

    return render_template_string(TEMPLATE, erro=None, imagem=None)


TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Gerador de QR Code</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }
        .error { color: red; }
        .success { color: green; }
        img { margin-top: 20px; }
        input[type="text"] { width: 300px; padding: 10px; }
        input[type="submit"] { padding: 10px 20px; margin: 10px; }
    </style>
</head>
<body>
    <h1>Gerador de QR Code</h1>
    <p>Digite o link ou texto para gerar o QR Code:</p>
    <form method="post">
        <input type="text" name="texto" placeholder="Ex: https://www.google.com">
        <br>
        <input type="submit" value="Gerar QR Code">
    </form>
    {% if erro %}
        <p class="error">{{ erro }}</p>
    {% endif %}
    {% if imagem %}
        <p class="success">✅ QR Code gerado com sucesso! Texto: {{ texto|truncate(30, true, '...') }}</p>
        <img src="data:image/png;base64,{{ imagem }}" alt="QR Code">
    {% endif %}
    {% if not erro and not imagem %}
        <p style="color: gray;">O QR Code aparecerá aqui após ser gerado.</p>
    {% endif %}
</body>
</html>
"""

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))