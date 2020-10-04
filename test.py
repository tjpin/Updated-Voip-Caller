
import kivy
kivy.require("1.9.1")
from kivy.app import App
from kivy.uix.vkeyboard import VKeyboard


# Create the vkeyboard
class Test(VKeyboard):
    player = VKeyboard()


# Create the App class
class VkeyboardApp(App):
    def build(self):
        return Test()

    # run the App


if __name__ == '__main__':
    VkeyboardApp().run()


# def list_contacts(self):
#     try:
#         from jnius import autoclass
#         PythonActivity = autoclass("org.renpy.android.PythonActivity")
#         ContactsContract = autoclass("android.provider.ContactsContract")
#
#         cr = PythonActivity.mActivity.getContentResolver()
#         null = None
#         cur = cr.query(ContactsContract.Contacts.CONTENT_URI, null, null, null, null)
#
#         if (cur.getCount() > 0):
#             while cur.moveToNext:
#                 id = cur.getString(cur.getColumnIndex(ContactsContract.Contacts._ID))
#                 name = cur.getString(cur.getColumnIndex(ContactsContract.Contacts.DISPLAY_NAME))
#                 # pnumber = cur.getString(cur.getColumnIndex(ContactsContract.Contacts.
#     except:
#         pass
#     # return Contacts.get_contacts()