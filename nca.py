import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import darkdetect
import google.generativeai as genai
import time

isdark = darkdetect.isDark()

if isdark is True:
    ctk.set_appearance_mode("dark") # Modos: "light", "dark", "system"
else:
    ctk.set_appearance_mode("light")

#Chave API
genai.configure(api_key="#######################################")

#PROMPT_TEMPLATE é o que vai dar contexto ao bot e vai fazê-lo ser mais objetivo com seu resultado
PROMPT_TEMPLATE = """Você é um mestre de automação de redes e configuração de roteadores, switchs, firewalls, mikrotiks e servidores linux e windows.

Seu trabalho é converter o INPUT dado em comandos de CLI do determinado equipamento para completar a tarefa dada.

Output:
- CLI script ou comandos CLI passo-a-passo para o determinado equipamento
- Uma separatoria de 4 caracteres "----"
- Uma explicação firme de cada comando (se requisitado)
- Gerar apenas o necessário e nada mais.

--- INPUT START
{input}
--- INPUT END

REPLY:
"""

app = ctk.CTk(fg_color="#000000") # Cria a janela e escolhe um background
app.title("NCA By MorningStar") # Título da janela
app.geometry("700x500") # Escolhe o tamanho da janela
app.resizable(width=False, height=False) # Não permite que mude o tamanho da janela
app.iconbitmap(r"app_icon.ico") # seleciona um icone para o app

frame = ctk.CTkFrame(app, fg_color="#000000")
frame.pack() # Cria o frame do label

label = ctk.CTkLabel(frame, width=650, text="Histórico de conversa:",anchor="w", justify="left", font=("Josefin sans", 12), text_color="#F2F2F2")
label.pack(pady=5) # Cria uma label com texto para ficar em cima do textbox

frame2 = ctk.CTkFrame(app,corner_radius=10, fg_color="transparent", bg_color="transparent")
frame2.pack() # Cria um frame para o textbox

text = ctk.CTkTextbox(frame2, width=650, height=350, fg_color="#333333", corner_radius=10,text_color="#F2F2F2", font=("Josefin sans", 12))
text.pack() # Cria o textbox que serve como histórico da conversa
text.configure(state="disabled") # Desabilita a edição do textbox

frame3 = ctk.CTkFrame(app, width=650, corner_radius=10, fg_color="#000000")
frame3.pack(pady=10, side="bottom") # Cria um frame para o botão de enviar e o input

def addTexto(event=None):
    user_input = inp.get() # Pega o input
    if user_input.strip() != "": # Verifica se o input não está em branco
        text.configure(state="normal") # Muda o tipo da TEXTBOX para ser editavel
        text.insert("end",f"👤 Você: {user_input}\n") # Adiciona o input ao textbox
        text.configure(state="disabled") # Desabilita a edição
        inp.delete(0, "end") # Deleta o input da caixa de entrada

    try:
        prompt = PROMPT_TEMPLATE.format(input=user_input) #Define o prompt com o nosso template e o input do usuario
        model = genai.GenerativeModel(model_name="gemini-2.0-flash") #Escolhe o modelo da i.a
        response = model.generate_content(prompt) #Gera uma resposta de acordo com o template
        reply = response.text.strip() #Transforma a resposta em texto puro
        tempo = time.strftime('%d.%m.%Y.%H_%M_%S') #Cria uma variavel com o tempo atual

        inputf = user_input.split(' ')
        with open(f'{inputf[0]}_{inputf[1]}_{inputf[2]}_{tempo}.txt', 'w') as file: #Modulo para criar um arquivo e usar ele como historico
            cli = response.text.split('----',1) #Cria uma variavel para separar o CLI da explicação
            file.write(f'CLI:\n{cli[0]}') #Escreve cada input e resposta do usuario
            file.close() #Salva o arquivo e fecha após escrever
        text.configure(state="normal") # Muda o tipo da TEXTBOX para ser editavel
        text.insert("end",f"🤖 NCA: {reply}\n") # Adiciona a resposta ao textbox
        text.configure(state="disabled") # Desabilita a edição
    except Exception as e:
        CTkMessagebox(app, fg_color="#000000", bg_color="#000000", text_color="#F2F2F2", title="Erro ao gerar resposta.", message="Ocorreu um erro ao gerar sua resposta, por favor contate o suporte do app.", button_color="#FFD700", button_hover_color="#FFD966", button_text_color="#000000", icon=r"icone_erro_dourado.ico") # Uma janela de erro caso não consiga criar a resposta ao input


inp = ctk.CTkEntry(frame3, width=510, fg_color="#333333", placeholder_text="Digite a configuração desejada:", border_color=None, font=("Josefin sans", 12), text_color="#F2F2F2") # Seção de input
inp.bind("<Return>", command=addTexto) # Faz com que ao apertar enter mande o input
inp.grid(row=0, column=0, padx=5, sticky="nsew")

button = ctk.CTkButton(frame3, text="Enviar", command=addTexto, fg_color="#FFD700",hover_color="#FFD966", text_color="#000000") # Botão de envio do input
button.grid(row=0, column=1, padx=5, sticky="nsew")

app.mainloop() # Roda a janela em loop
