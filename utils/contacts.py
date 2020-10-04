from jnius import autoclass


class Contacts():

    # contacts.Contacts._ID
    # contacts.Contacts.DISPLAY_NAME_PRIMARY
    name = []
    phoneNumber = []

    def get_permissions(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_CONTACTS,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_PHONE_STATE,
                Permission.INTERNET,
                Permission.VIBRATE,
            ])
            return True
        except ImportError:
            print("Import error")

    def get_contacts(self):

        if self.get_permissions:
            contacts = autoclass(
                "android.provider.ContactsContract.CommonDataKinds")
            try:
                for contact in contacts:
                    self.name.append(contact.Phone.NAME)
                    self.phoneNumber.append(contact.Phone.NUMBER)
            except:
                pass
        else:
            return False
