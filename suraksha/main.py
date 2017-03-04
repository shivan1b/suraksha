from kivy.app import App
from kivy.lang import Builder
# from jnius import autoclass
from kivy.uix.screenmanager import Screen, ScreenManager

# activity = autoclass('org.renpy.android.PythonActivity').mActivity

def save_emergency_contacts(contact_name, contact_num):
    import json
    if not contact_name:
        activity.toastError('Please provide a contact name!')
        return
    if not contact_num:
        activity.toastError('Oops! You forgot to provide a contact number.')
        return

    with open('suraksha/data/contact_list.json', 'w+'):
        json.dumps(contact_name + ': ' + contact_num)


    # from plyer import sms
    # sms.send(contact_num, "Hi! I have added you as an emergency contact on"
    #        "Suraksha. Please download Suraksha app here: to help me in"
    #        "the need of emergency.")


Builder.load_string('''
<LaunchScreen>
    name: 'ScreenTicket'
    BoxLayout
        padding: dp(12)
        orientation: 'vertical'
        spacing:dp(5)
        Label:
            text: 'Emergency contact name'
        TextInput:
            height: dp(72)
            size: dp(32), dp(32)
            size_hint: 1, None
            text: ''
            multiline: False
        Label:
            text: 'Emergency contact number'
        TextInput:
            height: dp(72)
            size: dp(32), dp(32)
            size_hint: 1, None
            text: ''
            multiline: False
        Button:
            text: 'Add'
        ''')


class LaunchScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(LaunchScreen())


class SurakshaApp(App):
    '''
    Suraksha is an app for helping people send signals 
    '''

    def build(self):
        return sm


SurakshaApp().run()