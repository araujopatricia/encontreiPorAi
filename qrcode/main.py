
import qrcode
import customtkinter

def qr():
    entrada = entrada_usuario.get()
    print(entrada)

    imagem = qrcode.make()
    imagem.save("qrcode2.png")

    print("qrCode Gerado com Sucesso")


janela = customtkinter.CTk()
#Muda titulo
janela.title("Gerador QrCode")

#Muda tamanho da janela
janela.geometry("300x400")

#label para exebir na interface
label_text = customtkinter.CTkLabel(janela, text="Digite o link do QRCODE")
label_text.pack(padx=20, pady=20)

#Entrada usuario
entrada_usuario = customtkinter.CTkEntry(janela, placeholder_text="digite o link")
entrada_usuario.pack(padx=20, pady=20)

#botão
buttom = customtkinter.CTkButton(janela, text="Gerar", command=qr())
buttom.pack(padx=10, pady=20)

janela.mainloop()