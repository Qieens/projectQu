from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from jnius import autoclass

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.add_widget(Label(text='🔑 Token Discord'))
        self.token_input = TextInput(multiline=False)
        self.add_widget(self.token_input)

        self.add_widget(Label(text='🆔 ID Channel (pisahkan dengan koma)'))
        self.channel_input = TextInput(multiline=False)
        self.add_widget(self.channel_input)

        self.add_widget(Label(text='💬 Pesan'))
        self.message_input = TextInput()
        self.add_widget(self.message_input)

        self.add_widget(Label(text='🔁 Jumlah Kirim'))
        self.total_input = TextInput(text='1', multiline=False)
        self.add_widget(self.total_input)

        self.add_widget(Label(text='⏱️ Delay (detik)'))
        self.delay_input = TextInput(text='5', multiline=False)
        self.add_widget(self.delay_input)

        start_btn = Button(text="🚀 Jalankan")
        start_btn.bind(on_press=self.start_service)
        self.add_widget(start_btn)

    def start_service(self, instance):
        with open("config.txt", "w") as f:
            f.write(f"{self.token_input.text}\n")
            f.write(f"{self.channel_input.text}\n")
            f.write(f"{self.message_input.text}\n")
            f.write(f"{self.total_input.text}\n")
            f.write(f"{self.delay_input.text}\n")

        # Start Android background service
        PythonService = autoclass('org.kivy.android.PythonService')
        PythonService.start('AutoPostService', '')

class AutoPostApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    AutoPostApp().run()