import openai
from apikey import APIKEY
import wx
import pickle

# set API Key for the service
openai.api_key = APIKEY

response = ''
prompt = ''
messages = []

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
        wx.Frame.__init__(self, None, title="Prompt",size= (400, 400))
        
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

        
        self.submitButton = wx.Button(panel, label='Submit', pos=(50, 120))
        self.submitButton.Bind(wx.EVT_BUTTON, self.onSubmit)
        self.mainSizer.Add(self.submitButton, 0,wx.ALL | wx.CENTER,5)

        self.responseBox = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY, pos=(50, 150))
        self.mainSizer.Add(self.responseBox, 0, wx.ALL | wx.CENTER, 5)
        self.responseBox.SetValue(response)
        self.responseBox.SetMinSize((400, 200))

        panel.SetSizer(self.mainSizer)
        
    def onSubmit(self,event):
        global response
        global prompt
        global messages
        
        # get prompt from text box
        prompt = self.prompt.GetValue()
        print(prompt)
        
        # create messages dict with prompt from text box
        new_message = {"role":"user","content":prompt}
        
        messages.append(new_message)

        # send message to chatGPT
        output = openai.ChatCompletion.create(
        model='gpt-3.5-turbo', 
        messages=messages
        )
    
        response = output['choices'][0]['message']['content']
        self.responseBox.SetValue(response)
        
        new_response = {"role":"assistant", "content":response}
        messages.append(new_response)
        print(f"messages:{messages}")

#class progressFrame(wx.Frame):
#    def __init__(self):
#        wx.Frame.__init__(self, None, title="Prompt",size= (100, 100))
#        overlay = wx.Panel(self)

       

if __name__ == "__main__":
    app = chatApp()
    app.MainLoop()