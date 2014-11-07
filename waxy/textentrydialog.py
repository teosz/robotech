# textentrydialog.py
# Simple dialog for entering a string.
# Note: Not based on wxPython's TextEntryDialog.

from dialog import Dialog
from textbox import TextBox
from label import Label
from keys import keys
import string

class TextEntryDialog(Dialog):

    def __init__(self, parent, title="Enter some text", prompt="Enter some text",
     default="", cancel_button=1):
        self.prompt = prompt
        self.default = default
        Dialog.__init__(self, parent, title, cancel_button=cancel_button)

    def Body(self):
        label = Label(self, self.prompt)
        self.AddComponent(label, expand='h', border=7)

        self.text = TextBox(self, size=(100,25), process_enter=1)
        self.text.SetValue(self.default)
        self.text.OnChar = self.OnTextBoxChar
        self.AddComponent(self.text, expand='h', border=5)

    def OnTextBoxChar(self, event=None):
        # pressing Enter in the TextBox is the same as clicking OK
        if event.GetKeyCode() == keys.enter:
            self.OnClickOKButton(event)
        else:
            event.Skip()

    def GetValue(self):
        return self.text.GetValue()




class IntegerInputDialog(TextEntryDialog):

    def __init__(self, parent, title='Enter some text', 
                 prompt='Enter some text', default='', cancel_button=1):

        TextEntryDialog.__init__(self, parent, title=title,
                 prompt=prompt, default=str(default), 
                 cancel_button=cancel_button)


    def GetValue(self):

        try:
            val=TextEntryDialog.GetValue(self)
        except ValueError:
            return None

        try:
            int_val=eval("int("+val+")")
        except (SyntaxError,NameError):
            int_val=None

        return int_val


    def OnCharHook(self, event):
        key = event.KeyCode()

        if key == wx.WXK_ESCAPE:
            self.OnClickCancelButton()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return


        good_chars=string.digits+'+*-()'
        if chr(key) in good_chars:
            event.Skip()
            return

        if not wx.Validator_IsSilent():
            wx.Bell()

        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return



    def Validate(self):
        val = TextEntryDialog.GetValue(self)  # make sure the get a string

        good_chars=string.digits+'+*-()'
        for x in val:
            if x not in good_chars:
                return False

        try:
            int_val=eval("int("+val+")")
        except (SyntaxError,NameError):
            Error("Syntax Error")
            return False

        return True


def Input_Integer(title,
                 prompt, default=None,parent=None):


    a=IntegerInputDialog(parent,title,prompt,default)
    result=a.ShowModal()

    if result=='ok':
        r=a.GetValue()
    else:
        r=None

    a.Destroy()

    return r


class FloatInputDialog(TextEntryDialog):

    def __init__(self, parent, title='Enter some text', 
                 prompt='Enter some text', default=None, cancel_button=1):

        TextEntryDialog.__init__(self, parent, title=title,
                 prompt=prompt, default=str(default), 
                 cancel_button=cancel_button)


    def GetValue(self):

        try:
            val=TextEntryDialog.GetValue(self)
        except ValueError:
            return None

        try:
            float_val=eval("float("+val+")")
        except SyntaxError:
            float_val=None

        return float_val



    def Validate(self):
        val = TextEntryDialog.GetValue(self)  # make sure the get a string

        try:
            float_val=eval("float("+val+")")
        except (SyntaxError,NameError):
            Error("Syntax Error")
            return False

        return True



def Input_Float(title,
                 prompt, default=None,parent=None):

    a=FloatInputDialog(parent,title,prompt,default)
    result=a.ShowModal()

    if result=='ok':
        r=a.GetValue()
    else:
        r=None

    a.Destroy()

    return r


