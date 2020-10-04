from kivymd.app import MDApp
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy import utils

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from accounts import account_sid, auth_token
from datetime import datetime
import time

from accounts import twilio_number
from utils.call import MakeCall


class Content(BoxLayout):
    pass


class Recent(BoxLayout):
    pass


class Developer(BoxLayout):
    pass


class License(BoxLayout):
    pass


class Message(MDBoxLayout):
    def action(self):
        time.sleep(1)
        self.ids.to_send.text = ''
        self.ids.msg.text = ''

    def send_sms(self):
        msg_client = Client(account_sid, auth_token)
        if self.ids.to_send.text != '' and self.ids.msg.text != '':
            try:
                message = msg_client.messages.create(
                    to=self.ids.to_send.text,
                    from_=twilio_number,
                    body=self.ids.msg.text,
                    status_callback='https://postb.in/b/1594000410504-2666337494738')
                toast("Message sent")
            except TwilioRestException:
                toast("something went wrong")
        elif self.ids.to_send.text == '' or self.ids.msg.text == '':
            toast("Enter Correct info")
        else:
            toast("Message sent")


class HomeScreen(BoxLayout):
    dialog = None
    client = Client(account_sid, auth_token)

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        self.get_keypad()
        Clock.schedule_interval(self.real_time, 1)
        # self.auto_end()
        # self.get_recent()
        # self.get_balance()

    # create keypads
    def get_keypad(self, dt=0):
        keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '+']
        letters = ['~', 'abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz', '', '', '']
        for key, letter in zip(keys, letters):
            btn = TwoLineListItem(
                text=f"                 [size=26]{key}[/size]",
                secondary_text=f"               {letter}",
                divider=None,
                on_release=self.display
            )
            self.ids.keypads.add_widget(btn)

    # create input/ display
    def display(self, instance):
        num = self.ids.display_n
        if len(num.text) <= 12:
            num.text += instance.text[26]
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
                timeout=10,
                to=self.ids.display_n.text,
                twiml="<Response><Dial>+254723818567</Dial></Response>"
                # url='http://demo.twilio.com/docs/voice.xml'
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

    def auto_end(self):
        cl = self.client.calls.list()
        if cl[0].status == 'canceled':
            print("canceled")
            self.ids.manager.current = 'home'
        else:
            return self.call_hangup

# get call log
    def recent_calls(self):
        log = Recent()
        pop = Popup(
            title="Call Logs",
            title_color=[0, 0, 0, 1],
            title_size=28,
            content=log,
            background='',
            size_hint=(0.8, 0.8))
        pop.open()
        logs = self.client.calls.list(limit=20)
        for lg in logs:
            lis = TwoLineListItem(
                text=f"[size=22]{lg.to}[/size]",
                secondary_text=f"{lg.date_created.strftime('%d %B %Y')}     {lg.start_time.strftime('%H:%M:%S')}      {lg.duration}Sec"
            )
            log.ids.recent.add_widget(lis)

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

    def new_message(self):
        show = Message()
        pop = Popup(
            title="New Message",
            title_color=[0, 0, 0, 1],
            title_size=30,
            content=show,
            background='',
            size_hint=(0.8, 0.8))
        pop.open()

    # create time object to be updated by kivy Clock for real time
    def real_time(self, dt=0):
        tm = datetime.now().strftime('%H:%M:%S')
        self.ids.backdrop.header_text = tm

    # settings: update api account details
    def update_number(self):
        un = None
        if not un:
            un = MDDialog(
                title="[size=14]Update Details *[/size]",
                type="custom",
                size_hint=[0.9, 1],
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="No!", text_color=[1, 0, 0, 1],
                        on_release=lambda x: toast("Canceled"),
                        on_press=lambda x: un.dismiss()),
                    MDFlatButton(
                        text="Update", text_color=[0, 1, 0, 1],
                        on_release=lambda x: toast("Number updated"))])
        un.open()

    def developer_info(self):
        dev = Developer()
        devpop = Popup(
            title="New Message",
            title_color=[0, 0, 0, 1],
            title_size=30,
            content=dev,
            background='',
            size_hint=(0.6, 0.5))
        devpop.open()

    def licenses(self):

        tl = License()
        lncpop = Popup(
            title="",
            title_color=[0, 0, 0, 1],
            title_size=30,
            content=tl,
            background='',
            size_hint=(0.8, 0.8))
        lncpop.open()


class UpdateApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        return HomeScreen()


UpdateApp().run()
