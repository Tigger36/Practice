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
        self.label = wx.StaticText(panel, label="Welcome to the chatGPT Assistant!", pos=(50,50))
        self.mainSizer.Add(self.label, 0, wx.ALL | wx.CENTER, 5)

        #Prompt for prompt
        self.label = wx.StaticText(panel, label="Type your question below and then click submit", pos=(50,60))
        self.mainSizer.Add(self.label, 0, wx.ALL | wx.CENTER, 5)

        #Text control for response
        self.prompt = wx.TextCtrl(panel, pos=(50, 80))
        self.mainSizer.Add(self.prompt,0, wx.ALL | wx.CENTER,5)
        self.prompt.SetMinSize((500, 100))
        
        #Submit button
        self.submitButton = wx.Button(panel, label='Submit', pos=(50, 120))
        self.submitButton.Bind(wx.EVT_BUTTON, self.onSubmit)
        self.mainSizer.Add(self.submitButton, 0,wx.ALL | wx.CENTER,5)

        #text box for chat response
        self.responseBox = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY, pos=(50, 150))
        self.mainSizer.Add(self.responseBox, 0, wx.ALL | wx.CENTER, 5)
        self.responseBox.SetValue(response)
        self.responseBox.SetMinSize((400, 200))

        #progress bar
        self.progressBar = wx.Gauge(panel, range=100, pos=(100, 400), size=(300, 25))
        self.mainSizer.Add(self.progressBar, 0, wx.ALL | wx.CENTER, 5)
        self.progressBar.Hide()
        panel.SetSizer(self.mainSizer)
        

    def get_response(self):
        global response
        global prompt
        global messages
        
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

       

if __name__ == "__main__":
    app = chatApp()
    app.MainLoop()