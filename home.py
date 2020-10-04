from kivymd.app import MDApp
from kivymd.uix.list import TwoLineIconListItem, \
    IconLeftWidget, TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton, MDRaisedButton

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior

from kivy import utils

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from accounts import account_sid, auth_token

from accounts import twilio_number
from utils.call import MakeCall

class Content(BoxLayout):
    pass


class Message(BoxLayout):
    pass


class CustomButton(MDCard, ButtonBehavior):
    pass


class HomeScreen(BoxLayout):
    dialog = None
    client = Client(account_sid, auth_token)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.get_keypad()
        # self.get_recent()
        self.get_balance()

    # create keypads
    def get_keypad(self, dt=0):
        keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '+']
        letters = ['~', 'abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz', '', '', '']
        for key, letter in zip(keys, letters):
            btn = TwoLineListItem(
                text=key,
                secondary_text=letter,
                # border='Inset',
                on_release=self.display
            )
            self.ids.keypads.add_widget(btn)

    # create input/ display
    def display(self, instance):
        num = self.ids.display_n
        if len(num.text) <= 12:
            num.text += instance.text[16]
        else:
            num.text = num.text

    # create backspace callback
    def delete(self):
        num = self.ids.display_n
        num.text = num.text[:-1]
        return num

    # make call
    def call(self):
        try:
            return MakeCall.make_call(
                from_=twilio_number,
                to=self.ids.display_n.text,
                url='http://demo.twilio.com/docs/voice.xml'
            )
        except TwilioRestException:
            pass

    # hangup call
    def call_hangup(self):
        end_call = self.client.calls.list()
        end_call[0].update(status="completed")

    # Check if display is not empty and has required phone number length
    def action(self):
        if self.ids.display_n.text != "" and len(self.ids.display_n.text) >= 8:
            self.ids.manager.current = 'active'
        else:
            self.ids.manager.current = 'home'

    # get call logs
    def get_recent(self, dt=0):
        logs = self.client.calls.list()
        for log in logs:
            self.ids.time.text = str(log.start_time)
            dc = log.date_created.strftime("%d:%m:%y")
            tm = log.end_time.strftime("%H:%M:%S")
            recent = TwoLineIconListItem(
                text=f"        [font=RobotoLight]{log.to}[/font]",
                text_color=[0, 0, 0, 1],
                secondary_text=f"         {log.duration}sec               {dc}      {tm}",
                secondary_text_color=[0, 1, 0, 1],
                bg_color=[1, 1, 1, 1],
                divider='Inset'
            )
            im = IconLeftWidget(icon='account')
            recent.add_widget(im)
            recent.size_hint_max_y = 2
            self.ids.recent.add_widget(recent)

    # Fetch account balance
    def get_balance(self):
        account = self.client.api.accounts(account_sid).fetch()
        tls = [bl for bl in (account.subresource_uris['balance'])]

    # Create account top up function
    def top_up(self):
        mc = utils.get_color_from_hex('#0000ff')
        paypal = MDFlatButton(
            text="Cancel",
            text_color=mc,
            on_release=lambda x: toppup_dialog.dismiss())
        mpesa = MDFlatButton(
            markup=True,
            text="[color=#00cc00]M_Pesa[/color]",
            on_release=lambda x: self.loader)
        toppup_dialog = MDDialog(
            title="[size=14]Account Top-Up[/size]",
            size_hint=[0.8, .6],
            radius=[30, 5, 30, 5],
            text="To top up your account use send desired amount to (00000) or one option below",
            buttons=[paypal, mpesa])
        toppup_dialog.open()

    # close dialog box
    def dialog_close(self, obj):
        return self.dialog.dismiss()

    # create new message. Will use dialog box instead of separate screen
    def new_message(self):
        self.dialog = MDDialog(
            title="New Message",
            type="custom",
            size_hint=[0.8, 1],
            content_cls=Message(),
            buttons=[
                MDFlatButton(
                    text="Cancel!", text_color=[1, 0, 0, 1],
                    on_release=lambda x: toast("Canceled"),
                    on_press=self.dialog_close),
                MDRaisedButton(
                    text="Send", md_bg_color=[0, 0, 1, 1])])
        self.dialog.open()

    # settings: update api account details
    def update_number(self):
        un = None
        if not un:
            un = MDDialog(
                title="[size=14]Update Details *[/size]",
                type="custom",
                radius=[30, 5, 30, 5],
                size_hint=[0.9, 1],
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="No!", text_color=[1, 0, 0, 1],
                        on_release=lambda x: toast("Canceled"),
                        on_press=lambda x: un.dismiss()),
                    MDFlatButton(
                        markup=True,
                        text="[b]Update[/b]", text_color=[0, 1, 0, 1],
                        on_release=lambda x: toast("Number updated"))])
        un.open()


class HomeApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        return HomeScreen()

    def on_start(self):
        return True

    def on_pause(self):
        return True


if __name__ == '__main__':
    HomeApp().run()


