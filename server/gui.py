import os
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.config import Config
from tkinter import Tk, filedialog
from web_server import iniciar_servidor_web, parar_servidor_web

# Desabilitar a redimensionamento da janela
Config.set('graphics', 'resizable', False)

class RshareApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.1, 1)  # Background color
        Window.size = (800, 600)  # Definir o tamanho da janela
        Window.minimum_width, Window.minimum_height = Window.size  # Tamanho mínimo
        
        self.server_thread = None
        self.pasta_selecionada = None
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(text='Rshare 1.0', font_size='24sp', color=(0.5, 0.7, 1, 1))
        layout.add_widget(title)
        
        self.pasta_label = Label(text='Nenhuma pasta selecionada', color=(1, 1, 1, 1))
        layout.add_widget(self.pasta_label)
        
        btn_selecionar = Button(text='Selecionar Pasta', size_hint_y=None, height=50, background_color=(0.5, 0.7, 1, 1))
        btn_selecionar.bind(on_release=self.selecionar_pasta)
        layout.add_widget(btn_selecionar)
        
        self.status_label = Label(text='Servidor Offline', font_size='24sp', color=(1, 0, 0, 1))
        
        status_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=100)
        status_layout.add_widget(Widget())  # Add empty widget for centering
        status_layout.add_widget(self.status_label)
        status_layout.add_widget(Widget())  # Add empty widget for centering
        
        layout.add_widget(status_layout)
        
        btn_iniciar = Button(text='Iniciar Servidor', size_hint_y=None, height=50, background_color=(0.5, 0.7, 1, 1))
        btn_iniciar.bind(on_release=self.iniciar_servidor)
        layout.add_widget(btn_iniciar)
        
        btn_parar = Button(text='Parar Servidor', size_hint_y=None, height=50, background_color=(0.5, 0.7, 1, 1))
        btn_parar.bind(on_release=self.parar_servidor)
        layout.add_widget(btn_parar)
        
        arquivos_label = Label(text='Arquivos Compartilhados:', color=(0.5, 0.7, 1, 1))
        layout.add_widget(arquivos_label)
        
        self.caixa_arquivos = GridLayout(cols=1, spacing=20, size_hint_y=None)
        self.caixa_arquivos.bind(minimum_height=self.caixa_arquivos.setter('height'))
        
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, 200))
        scroll_view.add_widget(self.caixa_arquivos)
        
        layout.add_widget(scroll_view)
        
        return layout
    
    def selecionar_pasta(self, instance):
        # Usar tkinter para abrir o diálogo de seleção de pastas
        root = Tk()
        root.withdraw()  # Ocultar a janela principal do Tkinter
        pasta = filedialog.askdirectory()
        root.destroy()  # Destruir a janela do Tkinter
        
        if pasta:
            self.pasta_selecionada = pasta
            self.pasta_label.text = f'Pasta: {self.pasta_selecionada}'
            self.listar_arquivos()
    
    def listar_arquivos(self):
        if self.pasta_selecionada:
            arquivos = os.listdir(self.pasta_selecionada)
            self.caixa_arquivos.clear_widgets()
            for arquivo in arquivos:
                self.caixa_arquivos.add_widget(Label(text=arquivo, color=(1, 1, 1, 1)))
    
    def iniciar_servidor(self, instance):
        if self.pasta_selecionada:
            self.server_thread = threading.Thread(target=iniciar_servidor_web, args=(self.pasta_selecionada,))
            self.server_thread.start()
            self.status_label.text = 'Servidor Online'
            self.status_label.color = (0, 1, 0, 1)  # Verde fluorescente
    
    def parar_servidor(self, instance):
        if self.server_thread:
            parar_servidor_web()
            self.server_thread.join()
            self.status_label.text = 'Servidor Offline'
            self.status_label.color = (1, 0, 0, 1)  # Vermelho

if __name__ == '__main__':
    RshareApp().run()

