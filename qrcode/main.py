import qrcode
import customtkinter
from tkinter import messagebox
from PIL import Image, ImageTk


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
            box_size=8,  # Reduzido para caber melhor na tela
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

        # Redimensiona a imagem para exibir na interface
        imagem_redimensionada = imagem.resize((120, 120), Image.Resampling.LANCZOS)

        # Converte para formato que o CustomTkinter pode usar
        foto = ImageTk.PhotoImage(imagem_redimensionada)

        # Atualiza o label da imagem
        label_imagem.configure(image=foto, text="")
        label_imagem.image = foto  # Mantém uma referência da imagem

        # Mostra o label da imagem se estava oculto
        label_imagem.pack(padx=20, pady=20)

        # Atualiza o label de status
        label_status.configure(
            text=f"✅ QR Code gerado com sucesso!\nTexto: {entrada[:30]}{'...' if len(entrada) > 30 else ''}",
            text_color="green")

        print(f"QR Code gerado para: {entrada}")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar QR Code: {str(e)}")
        label_status.configure(text="❌ Erro ao gerar QR Code", text_color="red")


# Configuração da janela
janela = customtkinter.CTk()
janela.title("Gerador QR Code")
janela.geometry("400x700")  # Aumentado para acomodar a imagem

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

# Label para exibir a imagem do QR Code
label_imagem = customtkinter.CTkLabel(
    janela,
    text="\nO QR Code aparecerá aqui\napós ser gerado",
    font=customtkinter.CTkFont(size=14),
    text_color="gray"
)
# Inicialmente não mostra o label da imagem
# label_imagem.pack(padx=20, pady=20)

# Label para status
label_status = customtkinter.CTkLabel(
    janela,
    text="Digite um texto ou link e clique em 'Gerar QR Code'",
    font=customtkinter.CTkFont(size=12),
    text_color="gray"
)
label_status.pack(padx=20, pady=10)


# Função para limpar QR Code
def limpar_qr():
    label_imagem.pack_forget()  # Remove a imagem da tela
    entrada_usuario.delete(0, 'end')  # Limpa o campo
    label_status.configure(text="Digite um texto ou link e clique em 'Gerar QR Code'",
                           text_color="gray")


# Botão para limpar
buttom_limpar = customtkinter.CTkButton(
    janela,
    text="Limpar",
    command=limpar_qr,
    width=100,
    height=30,
    font=customtkinter.CTkFont(size=14)
)
buttom_limpar.pack(padx=20, pady=10)

# Adiciona informações
info_label = customtkinter.CTkLabel(
    janela,
    text=" O QR Code também é salvo como 'qrcode_gerado.png'",
    font=customtkinter.CTkFont(size=11),
    text_color="gray"
)
info_label.pack(padx=20, pady=(10, 20))

# Permite pressionar Enter para gerar
entrada_usuario.bind('<Return>', lambda event: qr())

janela.mainloop()