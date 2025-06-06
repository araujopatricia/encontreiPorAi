import qrcode
import customtkinter
from tkinter import messagebox
import os


def qr():
    # Pega o valor da entrada
    entrada = entrada_usuario.get().strip()

    # Verifica se a entrada não está vazia
    if not entrada:
        messagebox.showerror("Erro", "Por favor, digite um link ou texto!")
        return

    try:
        # Cria o QR Code com os dados da entrada
        qr_code = qrcode.QRCode(
            version=1,  # Controla o tamanho do QR Code
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # Adiciona os dados ao QR Code
        qr_code.add_data(entrada)
        qr_code.make(fit=True)

        # Cria a imagem
        imagem = qr_code.make_image(fill_color="black", back_color="white")

        # Salva a imagem
        nome_arquivo = "qrcode_gerado.png"
        imagem.save(nome_arquivo)

        # Mostra mensagem de sucesso
        messagebox.showinfo("Sucesso", f"QR Code gerado com sucesso!\nSalvo como: {nome_arquivo}")
        print(f"QR Code gerado para: {entrada}")

        # Limpa o campo de entrada
        entrada_usuario.delete(0, 'end')

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar QR Code: {str(e)}")


# Configuração da janela
janela = customtkinter.CTk()
janela.title("Gerador QR Code")
janela.geometry("350x450")

# Configura o tema
customtkinter.set_appearance_mode("dark")  # ou "light"
customtkinter.set_default_color_theme("blue")  # ou "green", "dark-blue"

# Label para título
label_titulo = customtkinter.CTkLabel(
    janela,
    text="Gerador de QR Code",
    font=customtkinter.CTkFont(size=20, weight="bold")
)
label_titulo.pack(padx=20, pady=20)

# Label para instruções
label_text = customtkinter.CTkLabel(
    janela,
    text="Digite o link ou texto para gerar o QR Code:",
    font=customtkinter.CTkFont(size=14)
)
label_text.pack(padx=20, pady=(0, 10))

# Entrada do usuário
entrada_usuario = customtkinter.CTkEntry(
    janela,
    placeholder_text="Ex: https://www.google.com",
    width=300,
    height=40
)
entrada_usuario.pack(padx=20, pady=10)

# Botão para gerar QR Code
buttom = customtkinter.CTkButton(
    janela,
    text="Gerar QR Code",
    command=qr,  # Sem os parênteses!
    width=200,
    height=40,
    font=customtkinter.CTkFont(size=16, weight="bold")
)
buttom.pack(padx=20, pady=20)

# Adiciona informações
info_label = customtkinter.CTkLabel(
    janela,
    text="O QR Code será salvo como 'qrcode_gerado.png'\nna mesma pasta do programa",
    font=customtkinter.CTkFont(size=12),
    text_color="gray"
)
info_label.pack(padx=20, pady=(20, 10))

# Permite pressionar Enter para gerar
entrada_usuario.bind('<Return>', lambda event: qr())

janela.mainloop()