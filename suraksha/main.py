from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.utils import platform
from kivy.uix.screenmanager import Screen, ScreenManager

if platform == 'android':
    ON_ANDROID = True

if ON_ANDROID:
    from jnius import autoclass
    activity = autoclass('org.renpy.android.PythonActivity').mActivity



class LaunchScreen(Screen):
    pass


class SurakshaApp(App):
    '''
    Suraksha is an app for helping people send messages to their emergency
    contacts in case of some trouble
    '''

    def build(self):
        sm = ScreenManager()
        ls = LaunchScreen()
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
        but.bind(on_release=self.save_emergency_contacts)
        
        bx.add_widget(em_name)
        bx.add_widget(self.cont_name)
        bx.add_widget(em_num)
        bx.add_widget(self.cont_num)
        bx.add_widget(but)
        ls.add_widget(bx)
        sm.add_widget(ls)
        return sm


    def save_emergency_contacts(self, instance):
        if self.cont_name is None:
            if ON_ANDROID:
                activity.toastError('Please provide a contact name!')
            return
        if self.cont_num is None:
            if ON_ANDROID:
                activity.toastError('Oops! You forgot to provide a contact number.')
            return

        with open('data/contact_list', 'w+') as fd:
            fd.write(self.cont_name.text + ': ' + self.cont_num.text)


        if ON_ANDROID:
            from plyer import sms
            sms.send(self.cont_num, "Hi! I have added you as an emergency contact on"
                    "Suraksha. Please download Suraksha app here: to help me in"
                    "the need of emergency.")


if __name__ == '__main__':
    SurakshaApp().run()