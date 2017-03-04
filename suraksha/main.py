from kivy.app import App
from kivy.lang import Builder
# from jnius import autoclass
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager

# activity = autoclass('org.renpy.android.PythonActivity').mActivity

app = App.get_running_app()


class LaunchScreen(Screen):
    pass


class SurakshaApp(App):
    '''
    Suraksha is an app for helping people send messages to their emergency
    contacts in case of some trouble
    '''
#     Builder.load_string('''
# <LaunchScreen>
#     name: 'Launch Screen'
#     BoxLayout
#         padding: dp(12)
#         orientation: 'vertical'
#         spacing:dp(5)
#         Label:
#             text: 'Emergency contact name'
#         TextInput:
#             id: contact_name
#             height: dp(72)
#             size: dp(32), dp(32)
#             size_hint: 1, None
#             text: ''
#             multiline: False
#         Label:
#             text: 'Emergency contact number'
#         TextInput:
#             id: contact_num
#             height: dp(72)
#             size: dp(32), dp(32)
#             size_hint: 1, None
#             text: ''
#             multiline: False
#         Button:
#             text: 'Add'
#             on_release: save_emergency_contacts(contact_name.text,\
#                                                 contact_num.text)
#         ''')


    cont_name = ''
    cont_num = ''

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LaunchScreen())
        bx = BoxLayout(padding='12dp', orientation='vertical', spacing='5dp')
        em_name = Label(text='Emergency contact name')
        self.cont_name = TextInput(id='contact_name', height='72dp',
                              size=('32dp', '32dp'), size_hint=[1, None],
                              text='', multiline=False)
        em_num = Label(text='Emergency contact number')
        self.cont_num = TextInput(id='contact_num', height='72dp',
                              size=('32dp', '32dp'), size_hint=[1, None],
                              text='', multiline=False)
        but = Button(text='Add')
        
        bx.add_widget(em_name)
        bx.add_widget(self.cont_name)
        bx.add_widget(em_num)
        bx.add_widget(self.cont_num)
        bx.add_widget(but)
        but.bind(on_release=lambda x:self.save_emergency_contacts)
        sm.add_widget(bx)
        return sm


    def save_emergency_contacts(self):
        import json
        if not self.cont_name:
            #activity.toastError('Please provide a contact name!')
            return
        if not self.cont_num:
            #activity.toastError('Oops! You forgot to provide a contact number.')
            return

        with open('suraksha/data/contact_list.json', 'w+'):
            json.dumps(self.cont_name + ': ' + self.cont_num)


        # from plyer import sms
        # sms.send(contact_num, "Hi! I have added you as an emergency contact on"
        #        "Suraksha. Please download Suraksha app here: to help me in"
        #        "the need of emergency.")

SurakshaApp().run()