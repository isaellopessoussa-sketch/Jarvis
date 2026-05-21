import os
import datetime
import webbrowser
import wikipedia
import pyjokes
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import google.generativeai as genai

# Configurações iniciais
wikipedia.set_lang("pt")
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))

class JarvisHUD(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 12
        self.spacing = 10

        # Título do Sistema
        self.add_widget(Label(
            text="JARVIS - PROTOCOLO MOBILE V1", 
            size_hint_y=0.08, 
            font_size='20sp', 
            bold=True, 
            color=(0, 0.8, 1, 1)
        ))

        # Chat Log
        self.scroll = ScrollView(size_hint_y=0.80)
        self.chat_logs = Label(
            text=f"Jarvis: {self.obter_saudacao()}\n",
            alignment=('left', 'top'),
            size_hint_y=None,
            valign='top',
            halign='left',
            font_size='16sp',
            markup=True
        )
        self.chat_logs.bind(size=self.ajustar_texto)
        self.scroll.add_widget(self.chat_logs)
        self.add_widget(self.scroll)

        # Entrada de comandos
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=0.12, spacing=8)
        
        self.txt_input = TextInput(
            hint_text="Insira sua ordem, Senhor...", 
            multiline=False,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.4, 0.4, 0.4, 1),
            font_size='16sp'
        )
        self.txt_input.bind(on_text_validate=self.executar_comando)
        
        btn_enviar = Button(
            text="EXECUTAR", 
            size_hint_x=0.28, 
            background_color=(0, 0.6, 0.9, 1),
            font_size='14sp',
            bold=True
        )
        btn_enviar.bind(on_release=self.executar_comando)

        input_layout.add_widget(self.txt_input)
        input_layout.add_widget(btn_enviar)
        self.add_widget(input_layout)

    def obter_saudacao(self):
        # Saudação com base na hora atual (igual ao código do print)
        hora = datetime.datetime.now().hour
        if 0 <= hora < 12:
            return "Bom dia, Senhor. Todos os sistemas iniciados."
        elif 12 <= hora < 18:
            return "Boa tarde, Senhor. Banco de dados atualizado."
        else:
            return "Boa noite, Senhor. Protocolo de segurança ativo."

    def ajustar_texto(self, instance, value):
        self.chat_logs.text_size = (instance.width, None)
        self.chat_logs.height = self.chat_logs.texture_size[1]

    def executar_comando(self, instance):
        comando = self.txt_input.text.strip()
        if not comando:
            return

        self.chat_logs.text += f"\n[b]Você:[/b] {comando}\n"
        self.txt_input.text = ""
        cmd_lower = comando.lower()

        # --- FUNÇÕES CLÁSSICAS DO PROJETO ORIGINAL ---

        # 1. Abrir YouTube
        if "abrir youtube" in cmd_lower or "youtube" in cmd_lower:
            self.chat_logs.text += "Jarvis: Abrindo a plataforma do YouTube, Senhor.\n"
            webbrowser.open("https://www.youtube.com")
            return

        # 2. Abrir Google
        if "abrir google" in cmd_lower or "google" in cmd_lower:
            self.chat_logs.text += "Jarvis: Inicializando o mecanismo de busca Google, Senhor.\n"
            webbrowser.open("https://www.google.com")
            return

        # 3. Pesquisa na Wikipédia
        if "pesquisar" in cmd_lower or "wikipedia" in cmd_lower:
            busca = cmd_lower.replace("pesquisar", "").replace("na wikipedia", "").strip()
            self.chat_logs.text += f"Jarvis: Buscando por '{busca}' nos registros...\n"
            try:
                resumo = wikipedia.summary(busca, sentences=2)
                self.chat_logs.text += f"Jarvis: Encontrei isto: {resumo}\n"
            except Exception:
                self.chat_logs.text += "Jarvis: Não localizei registros sobre este assunto na Wikipédia.\n"
            return

        # 4. Hora Certa
        if "hora" in cmd_lower or "horas" in cmd_lower:
            agora = datetime.datetime.now().strftime("%H:%M")
            self.chat_logs.text += f"Jarvis: São exatamente {agora}, Senhor.\n"
            return

        # 5. Data Atual
        if "data" in cmd_lower or "hoje" in cmd_lower:
            hoje = datetime.datetime.now().strftime("%d/%m/%Y")
            self.chat_logs.text += f"Jarvis: Hoje é dia {hoje}, Senhor.\n"
            return

        # 6. Piadas (Igual ao módulo pyjokes do original)
        if "piada" in cmd_lower or "conte uma piada" in cmd_lower:
            # Pega uma piada técnica do pyjokes
            piada = pyjokes.get_joke(lang='en') # pyjokes foca mais em inglês, mas o Gemini traduz abaixo se falhar
            self.chat_logs.text += f"Jarvis (Piada Nerd): {piada}\n"
            return

        # --- SE NÃO FOR NENHUM COMANDO DIRETO, USA O GEMINI ---
        try:
            model = genai.GenerativeModel('gemini-pro')
            prompt_contexto = (
                "Você é o JARVIS, a inteligência artificial do Homem de Ferro. "
                "Responda ao usuário com tom altamente tecnológico, prestativo e chame-o de 'Senhor'. "
                f"Mensagem do Senhor: {comando}"
            )
            response = model.generate_content(prompt_contexto)
            self.chat_logs.text += f"Jarvis: {response.text}\n"
        except Exception:
            self.chat_logs.text += "Jarvis: Conexão com o núcleo de inteligência indisponível. Verifique a API Key.\n"

class JarvisApp(App):
    def build(self):
        return JarvisHUD()

if __name__ == '__main__':
    JarvisApp().run()
