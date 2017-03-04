from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager


Builder.load_string('''
<LaunchScreen>
    name: 'ScreenTicket'
    BoxLayout
        padding: dp(12)
        orientation: 'vertical'
        spacing:dp(5)
	    Label:
	        text: 'Enter your emergency contact here'
	    TextInput:
			height: dp(72)
			size: dp(32), dp(32)
			size_hint: 1, None
			text: ''
			multiline: False

		Button:
		    text: 'Add'
		    on_release: pass
		''')


class LaunchScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(LaunchScreen())


class SurakshaApp(App):
	'''

	'''

	def build(self):
		return sm


SurakshaApp().run()