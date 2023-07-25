import openai
from apikey import APIKEY
import wx
import pickle
import threading
import time

# set API Key for the service
openai.api_key = APIKEY

response = ''
prompt = ''
messages = []
print("start")
class chatApp(wx.App):
    def OnInit(self):
        prompt_frame = promptFrame()
        prompt_frame.Show()

        return True
    
    def OnExit(self):
    # Save session data
        data = {'response': response, 'prompt': prompt, 'messages': messages}
        with open('chat_data.pkl', 'wb') as f:
            pickle.dump(data, f)
        return super().OnExit()    
        
# Load previous session data if exists
try:
    with open('chat_data.pkl', 'rb') as f:
        data = pickle.load(f)
        response = data.get('response', '')
        prompt = data.get('prompt', '')
        messages = data.get('messages', [])
        print("Data from previous session has been loaded successfully")
except FileNotFoundError:
        print("No previous session data found")
        pass

class promptFrame(wx.Frame):
    global response
    global prompt
    global messages

    def __init__(self):
        wx.Frame.__init__(self, None, title="AI Assistant",size= (500, 500))

        panel = wx.Panel(self)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        #Welcome message
        self.label = wx.StaticText(panel, label="Welcome to the chatGPT Assistant!", style=wx.ALIGN_CENTER)
        self.mainSizer.Add(self.label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        #Prompt for prompt
        self.label = wx.StaticText(panel, -1, label="Type your question below and then click submit", style=wx.ALIGN_CENTER)
        self.mainSizer.Add(self.label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        #Text control for response
        self.prompt = wx.TextCtrl(panel, -1, style= wx.EXPAND)
        self.mainSizer.Add(self.prompt, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        self.prompt.SetMinSize((500, 100))
        
        #Submit button
        self.submitButton = wx.Button(panel, -1, "Submit")
        self.submitButton.Bind(wx.EVT_BUTTON, self.onSubmit)
        self.mainSizer.Add(self.submitButton, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        #text box for chat response
        self.responseBox = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.EXPAND)
        self.mainSizer.Add(self.responseBox, 0, wx.EXPAND, 5)
        self.responseBox.SetValue(response)
        self.responseBox.SetMinSize((400, 200))

        #progress bar
        self.progressBar = wx.Gauge(panel, range=100, pos=(100, 400), size=(300, 25))
        self.mainSizer.Add(self.progressBar, 0, wx.ALL | wx.CENTER, 5)
        self.progressBar.Hide()

        self.menuBar = wx.MenuBar()

        # Create a menu
        self.menu = wx.Menu()

        # Add a menu item for settings
        self.settingsItem = self.menu.Append(wx.ID_ANY, "Settings", "Open Settings")
        self.Bind(wx.EVT_MENU, self.onSettings, self.settingsItem)

        # Add the menu to the menu bar
        self.menuBar.Append(self.menu, "Options")

        # Set the menu bar for the frame
        self.SetMenuBar(self.menuBar)
        self.Center()
        self.Show(True)
        panel.SetSizer(self.mainSizer)
        
        self.Maximize(True)
        self.Maximize(False)

    def get_response(self):
        global response
        global prompt
        global messages
        
        #settings = settings_frame()
        #standardOpt = settings.radioButton1
        #therapistOpt = settings.radioButton2
        #profOpt = settings.radioButton3

        
        # get prompt from text box
        prompt = self.prompt.GetValue()
        print(prompt)
        
        wx.CallAfter(self.progressBar.SetValue, 10)
        # create messages dict with prompt from text box
        new_message = {"role":"user","content":prompt}
        
        messages.append(new_message)

        wx.CallAfter(self.progressBar.SetValue, 50)

        # send message to chatGPT
        output = openai.ChatCompletion.create(
        model='gpt-3.5-turbo', 
        messages=messages
        )
    
        response = output['choices'][0]['message']['content']
        wx.CallAfter(self.responseBox.SetValue, response)
        
        new_response = {"role":"assistant", "content":response}
        messages.append(new_response)

        wx.CallAfter(self.progressBar.SetValue, 100)
        print(f"messages:{messages}")
        
        while True:
            if self.progressBar.GetValue() <100:
                if not self.progressBar.IsShown():
                    self.progressBar.Show()
            elif self.progressBar.GetValue() == 100:
                time.sleep(1)
                self.progressBar.Hide()
                break
    
    def onSubmit(self, event):
        thread = threading.Thread(target=self.get_response)
        thread.start()
        self.progressBar.Show()
    
    def onSettings(self, event):
        settings = settings_frame()
        settings.Show()
       
class settings_frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Settings",size= (400, 400))

        settingsPanel = wx.Panel(self)
        settingsSizer = wx.BoxSizer(wx.VERTICAL)

        self.label = wx.StaticText(settingsPanel, label="Please select a mode",style =wx.ALIGN_CENTER)
        settingsSizer.Add(self.label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        settingsPanel.SetSizer(settingsSizer)

        self.radioButton1 = wx.RadioButton(settingsPanel, label="Standard")
        self.radioButton2 = wx.RadioButton(settingsPanel, label="Therapist")
        self.radioButton3 = wx.RadioButton(settingsPanel, label="Professor")
        settingsSizer.Add(self.radioButton1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        settingsSizer.Add(self.radioButton2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        settingsSizer.Add(self.radioButton3, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

if __name__ == "__main__":
    app = chatApp()
    app.MainLoop()