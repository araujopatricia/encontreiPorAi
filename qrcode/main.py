import qrcode
import customtkinter
from tkinter import messagebox
from PIL import Image, ImageTk

ARQUIVO_SAIDA = "qrcode_gerado.png"
TAMANHO_IMAGEM = (200, 200)
COR_FUNDO = "white"
COR_QR = "black"
TEMA_APARENCIA = "dark"
TEMA_CORES = "blue"

def gerar_qrcode(texto: str, nome_arquivo: str) -> Image.Image:
    """Gera e salva um QR Code com o texto informado."""
    qr_code = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=4,
    )
    qr_code.add_data(texto)
    qr_code.make(fit=True)
    imagem = qr_code.make_image(fill_color=COR_QR, back_color=COR_FUNDO)
    imagem.save(nome_arquivo)
    return imagem

def gerar_qrcode_gui():
    entrada = entrada_usuario.get().strip()

    if not entrada:
        messagebox.showerror("Erro", "Por favor, digite um link ou texto!")
        return

    try:
        imagem = gerar_qrcode(entrada, ARQUIVO_SAIDA)
        imagem_redimensionada = imagem.resize(TAMANHO_IMAGEM, Image.Resampling.LANCZOS)
        foto = ImageTk.PhotoImage(imagem_redimensionada)

        label_imagem.configure(image=foto, text="")
        label_imagem.image = foto
        label_imagem.pack(padx=20, pady=20)

        label_status.configure(
            text=f"✅ QR Code gerado com sucesso!\nTexto: {entrada[:30]}{'...' if len(entrada) > 30 else ''}",
            text_color="green"
        )

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar QR Code: {str(e)}")
        label_status.configure(text="❌ Erro ao gerar QR Code", text_color="red")

def limpar_qrcode():
    label_imagem.pack_forget()
    entrada_usuario.delete(0, 'end')
    resetar_status()

def resetar_status():
    label_status.configure(
        text="Digite um texto ou link e clique em 'Gerar QR Code'",
        text_color="gray"
    )

def criar_interface():
    global entrada_usuario, label_imagem, label_status

    customtkinter.set_appearance_mode(TEMA_APARENCIA)
    customtkinter.set_default_color_theme(TEMA_CORES)

    janela = customtkinter.CTk()
    janela.title("Gerador QR Code")
    janela.geometry("400x700")

    customtkinter.CTkLabel(
        janela,
        text="Gerador de QR Code",
        font=customtkinter.CTkFont(size=20, weight="bold")
    ).pack(padx=20, pady=20)

    customtkinter.CTkLabel(
        janela,
        text="Digite o link ou texto para gerar o QR Code:",
        font=customtkinter.CTkFont(size=14)
    ).pack(padx=20, pady=(0, 10))

    entrada_usuario = customtkinter.CTkEntry(
        janela,
        placeholder_text="Ex: https://www.google.com",
        width=300,
        height=40
    )
    entrada_usuario.pack(padx=20, pady=10)

    customtkinter.CTkButton(
        janela,
        text="Gerar QR Code",
        command=gerar_qrcode_gui,
        width=200,
        height=40,
        font=customtkinter.CTkFont(size=16, weight="bold")
    ).pack(padx=20, pady=20)

    label_imagem = customtkinter.CTkLabel(
        janela,
        text="O QR Code aparecerá aqui após ser gerado",
        font=customtkinter.CTkFont(size=14),
        text_color="gray"
    )

    label_status = customtkinter.CTkLabel(
        janela,
        text="",
        font=customtkinter.CTkFont(size=12)
    )
    label_status.pack(padx=20, pady=10)
    resetar_status()

    customtkinter.CTkButton(
        janela,
        text="Limpar",
        command=limpar_qrcode,
        width=100,
        height=30,
        font=customtkinter.CTkFont(size=14)
    ).pack(padx=20, pady=10)

    customtkinter.CTkLabel(
        janela,
        text="O QR Code também é salvo como 'qrcode_gerado.png'",
        font=customtkinter.CTkFont(size=11),
        text_color="gray"
    ).pack(padx=20, pady=(10, 20))

    entrada_usuario.bind('<Return>', lambda event: gerar_qrcode_gui())

    janela.mainloop()

if __name__ == "__main__":
    criar_interface()
