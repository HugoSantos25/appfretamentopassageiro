# main.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import csv

class Passageiro:
    def __init__(self, nome, cpf, rg, empresa, telefone):
        self.nome = nome
        self.cpf = cpf
        self.rg = rg
        self.empresa = empresa
        self.telefone = telefone

    def __str__(self):
        return f"{self.nome} - CPF: {self.cpf}"

class PassageiroManager(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)
        self.passageiros = []

        self.inputs = {}
        campos = ['Nome', 'CPF', 'RG', 'Empresa', 'Telefone']
        for campo in campos:
            self.inputs[campo] = TextInput(hint_text=campo, size_hint_y=None, height=40)
            self.add_widget(self.inputs[campo])

        btn_add = Button(text='Adicionar Passageiro', size_hint_y=None, height=40)
        btn_add.bind(on_press=self.adicionar_passageiro)
        self.add_widget(btn_add)

        btn_exportar = Button(text='Exportar Lista (CSV)', size_hint_y=None, height=40)
        btn_exportar.bind(on_press=self.exportar_csv)
        self.add_widget(btn_exportar)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.lista_layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.lista_layout.bind(minimum_height=self.lista_layout.setter('height'))
        self.scroll.add_widget(self.lista_layout)
        self.add_widget(self.scroll)

    def adicionar_passageiro(self, instance):
        dados = {k: self.inputs[k].text.strip() for k in self.inputs}
        if dados['Nome'] and dados['CPF']:
            novo = Passageiro(**dados)
            self.passageiros.append(novo)
            self.atualizar_lista()
            for campo in self.inputs.values():
                campo.text = ''

    def remover_passageiro(self, passageiro):
        if passageiro in self.passageiros:
            self.passageiros.remove(passageiro)
            self.atualizar_lista()

    def atualizar_lista(self):
        self.lista_layout.clear_widgets()
        for p in self.passageiros:
            box = BoxLayout(size_hint_y=None, height=40)
            box.add_widget(Label(text=str(p)))
            btn_remover = Button(text="Remover", size_hint_x=None, width=100)
            btn_remover.bind(on_press=lambda instance, p=p: self.remover_passageiro(p))
            box.add_widget(btn_remover)
            self.lista_layout.add_widget(box)

    def exportar_csv(self, instance):
        with open("passageiros.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Nome", "CPF", "RG", "Empresa", "Telefone"])
            for p in self.passageiros:
                writer.writerow([p.nome, p.cpf, p.rg, p.empresa, p.telefone])
        print("Arquivo 'passageiros.csv' exportado com sucesso.")

class LoginScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)
        self.app = app

        self.user_input = TextInput(hint_text='Usuário', size_hint_y=None, height=40)
        self.add_widget(self.user_input)

        self.pass_input = TextInput(hint_text='Senha', password=True, size_hint_y=None, height=40)
        self.add_widget(self.pass_input)

        self.message = Label(text='', size_hint_y=None, height=30)
        self.add_widget(self.message)

        btn_login = Button(text='Entrar', size_hint_y=None, height=40)
        btn_login.bind(on_press=self.verificar_login)
        self.add_widget(btn_login)

    def verificar_login(self, instance):
        usuario = self.user_input.text.strip()
        senha = self.pass_input.text.strip()
        if usuario == 'admin' and senha == '1234':
            self.app.root.clear_widgets()
            self.app.root.add_widget(PassageiroManager())
        else:
            self.message.text = '[color=ff0000]Usuário ou senha incorretos[/color]'
            self.message.markup = True

class PassageiroApp(App):
    def build(self):
        root = BoxLayout()
        login_screen = LoginScreen(app=self)
        root.add_widget(login_screen)
        return root

if __name__ == '__main__':
    PassageiroApp().run()
