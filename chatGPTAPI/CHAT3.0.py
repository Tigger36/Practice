import openai
from apikey import APIKEY
import wx
import pickle
import threading
import time

# set API Key for the service
openai.api_key = APIKEY

radBtn1 = True
radBtn2 = False
radBtn3 = False

response = ''
prompt = ''
messages = []
print("start")

class chatApp(wx.App):
    def OnInit(self):
        prompt_frame = promptFrame()
        prompt_frame.Show()
        global radBtn1
        global radBtn2
        global radBtn3

        return True
    
    def OnExit(self):
    # Save session data
        if radBtn1 == True:
            data = {'response': response, 'prompt': prompt, 'messages': messages}
            with open('chat_data.pkl', 'wb') as f:
                pickle.dump(data, f)
            return super().OnExit()
        elif radBtn2 == True:
            data = {'response': response, 'prompt': prompt, 'messages': messages}
            with open('therapist_chat_data.pkl', 'wb') as f:
                pickle.dump(data, f)
            return super().OnExit()
        elif radBtn3 == True:
            data = {'response': response, 'prompt': prompt, 'messages': messages}
            with open('professor_chat_data.pkl', 'wb') as f:
                pickle.dump(data, f)
            return super().OnExit()

class settings_frame(wx.Frame):
    global radBtn1
    global radBtn2
    global radBtn3
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

        self.radioButton1.SetValue(radBtn1)
        self.radioButton2.SetValue(radBtn2)
        self.radioButton3.SetValue(radBtn3)

        self.radioButton1.Bind(wx.EVT_RADIOBUTTON, self.onRadioButton)
        self.radioButton2.Bind(wx.EVT_RADIOBUTTON, self.onRadioButton)
        self.radioButton3.Bind(wx.EVT_RADIOBUTTON, self.onRadioButton)

        self.loadButton = wx.Button(settingsPanel, -1, "Load")
        self.loadButton.Bind(wx.EVT_BUTTON, self.onLoad)
        settingsSizer.Add(self.loadButton, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
    def onLoad(self, event):
        if radBtn1 == True:
            try:
                with open('chat_data.pkl', 'rb') as f:
                    data = pickle.load(f)
                    response = data.get('response', '')
                    prompt = data.get('prompt', '')
                    messages = data.get('messages', [])
                    print("Data from previous session has been loaded successfully")
                    wx.MessageBox('Data from previous session has been loaded successfully', 'Info', wx.OK | wx.ICON_INFORMATION)
            except FileNotFoundError:
                    wx.MessageBox('No previous session data found', 'Info', wx.OK | wx.ICON_INFORMATION)
                    print("No previous session data found")
                    pass
        elif radBtn2 == True:
            try:
                with open('therapist_chat_data.pkl', 'rb') as f:
                    data = pickle.load(f)
                    response = data.get('response', '')
                    prompt = data.get('prompt', '')
                    messages = data.get('messages', [])
                    print("Data from previous session has been loaded successfully")
                    wx.MessageBox('Data from previous session has been loaded successfully', 'Info', wx.OK | wx.ICON_INFORMATION)
            except FileNotFoundError:
                    wx.MessageBox('No previous session data found', 'Info', wx.OK | wx.ICON_INFORMATION)
                    print("No previous session data found")
                    pass
        elif radBtn3 == True:
            try:
                with open('professor_chat_data.pkl', 'rb') as f:
                    data = pickle.load(f)
                    response = data.get('response', '')
                    prompt = data.get('prompt', '')
                    messages = data.get('messages', [])
                    wx.MessageBox('Data from previous session has been loaded successfully', 'Info', wx.OK | wx.ICON_INFORMATION)
                    print("Data from previous session has been loaded successfully")
            except FileNotFoundError:
                    wx.MessageBox('No previous session data found', 'Info', wx.OK | wx.ICON_INFORMATION)
                    print("No previous session data found")
                    pass
            
    def onRadioButton(self, event):
        global radBtn1
        global radBtn2
        global radBtn3
        radBtn1 = self.radioButton1.GetValue()
        radBtn2 = self.radioButton2.GetValue()
        radBtn3 = self.radioButton3.GetValue()

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
    global radBtn1
    global radBtn2
    global radBtn3

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
        global radBtn1
        global radBtn2
        global radBtn3
        
        standardOpt = radBtn1
        therapistOpt = radBtn2
        profOpt = radBtn3
        print(radBtn1)
        print(radBtn2)
        print(radBtn3)

        if radBtn1 == True:
            print(radBtn1)
            pass
        elif radBtn2 == True:
            print(radBtn2)
            therapistPrompt = {"role":"user","content":"Answer all future questions like you are my therapist, ok?"}
            messages.append(therapistPrompt)
        elif radBtn3 == True:
            print(radBtn3)
            profPrompt = {"role":"user","content":"Answer all future questions like you are my professor, ok?"}
            messages.append(profPrompt)

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
       

if __name__ == "__main__":
    app = chatApp()
    app.MainLoop()