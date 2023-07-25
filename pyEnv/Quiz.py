import wx

#Global Variables]
score = 0
attempts = 1
questionNum = 0

class MyApp(wx.App):
   def OnInit(self):
        welcome_frame = WelcomeFrame()
        welcome_frame.Show()
        
        return True
    
class WelcomeFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Welcome", size=(400, 150))

        panel = wx.Panel(self)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
    
        self.label = wx.StaticText(panel, label="Welcome! Would you like to play?", pos=(50, 50))
        mainSizer.Add(self.label, 0, wx.ALL | wx.CENTER, 5)

        self.yesButton = wx.Button(panel, label='Yes', pos=(50, 100))
        self.yesButton.Bind(wx.EVT_BUTTON, self.onYes)
        btnSizer.Add(self.yesButton, 1, wx.ALL | wx.EXPAND, 5)

        self.noButton = wx.Button(panel, label='No', pos=(150, 100))
        self.noButton.Bind(wx.EVT_BUTTON, self.onNo)
        btnSizer.Add(self.noButton, 1, wx.ALL | wx.EXPAND, 5)

        mainSizer.Add(btnSizer, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(mainSizer)
    
    def onYes(self, event):
        self.Close()
        quiz_frame = QuizFrame1()
        quiz_frame.Show()

    def onNo(self, event):
        self.Close()

class RetryFrame(wx.Frame):
        global questionNum
        global attempts
        def __init__(self):
            wx.Frame.__init__(self, None, title="Retry?", size=(300, 200))
            
            panel = wx.Panel(self)

            mainSizer = wx.BoxSizer(wx.VERTICAL)
            btnSizer = wx.BoxSizer(wx.HORIZONTAL)
            
            self.label = wx.StaticText(panel, label="Would you like to try again?", pos=(50, 50))
            mainSizer.Add(self.label, 0, wx.ALL | wx.CENTER, 5)

            self.yesButton = wx.Button(panel, label='Yes', pos=(50, 100))
            self.yesButton.Bind(wx.EVT_BUTTON, self.onYes)
            btnSizer.Add(self.yesButton, 1, wx.ALL | wx.EXPAND, 5)
            
            self.noButton = wx.Button(panel, label='No', pos=(150, 100))
            self.noButton.Bind(wx.EVT_BUTTON, self.onNo)
            btnSizer.Add(self.noButton, 1, wx.ALL | wx.EXPAND, 5)

            mainSizer.Add(btnSizer, 0, wx.ALL | wx.EXPAND, 5)
            panel.SetSizer(mainSizer)

        def onYes(self, event):
            global attempts
            global questionNum
            self.Close()
            print(attempts)
            print(questionNum)
            attempts -= 1
            if questionNum == 1:
                quiz_frame = QuizFrame1()
                quiz_frame.Show()
            elif questionNum == 2:
                quiz_frame2 = QuizFrame2()
                quiz_frame2.Show()
            elif questionNum ==3:
                quiz_frame3 = QuizFrame3()
                quiz_frame3.Show()
            elif questionNum ==4:
                quiz_frame4 = QuizFrame4()
                quiz_frame4.Show()
    
        def onNo(self, event):
            
            if questionNum == 1:
                quiz_frame2 = QuizFrame2()
                quiz_frame2.Show()
            elif questionNum == 2:
                quiz_frame3 = QuizFrame3()
                quiz_frame3.Show()
            elif questionNum ==3:
                quiz_frame4 = QuizFrame4()
                quiz_frame4.Show()
            elif questionNum ==4:
                results_frame = resultFrame()
                results_frame.Show()
            self.Close()   

class QuizFrame1(wx.Frame):
    global score
    global attempts
    global questionNum
    questionNum = 1
    def __init__(self):
        wx.Frame.__init__(self, None, title="Quiz", size=(400, 200))

        panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.label = wx.StaticText(panel, label="What does CPU stand for?", pos=(50, 50))
        sizer.Add(self.label,0,wx.ALL | wx.CENTER, 5)

        self.answer = wx.TextCtrl(panel, pos=(50, 80))
        sizer.Add(self.answer,0,wx.ALL | wx.CENTER,5)

        self.submitButton = wx.Button(panel, label='Submit', pos=(50, 120))
        self.submitButton.Bind(wx.EVT_BUTTON, self.onSubmit1)
        sizer.Add(self.submitButton, 0,wx.ALL | wx.CENTER,5)

        panel.SetSizer(sizer)
    def onSubmit1(self, event):
        global score
        global attempts
        global questionNum
        answer = self.answer.GetValue()
        if answer.lower() == 'central processing unit':
            wx.MessageBox('Correct answer!')
            score += 1
            self.Close()
            quiz_frame2 = QuizFrame2()
            quiz_frame2.Show()
            print(score)
        elif answer.lower() != 'central processing unit' and attempts == 1:
            print("retry")
            questionNum = 1
            self.Close()
            retry_frame = RetryFrame()
            retry_frame.Show()
        else:
            wx.MessageBox('Sorry, wrong answer and no additional attempts')
            self.Close()
            quiz_frame2 = QuizFrame2()
            quiz_frame2.Show()

class QuizFrame2(wx.Frame):
    global score
    global attempts
    global questionNum
    def __init__(self):
        wx.Frame.__init__(self, None, title="Quiz", size=(400, 200))

        panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.label = wx.StaticText(panel, label="What does GPU stand for?", pos=(50, 50))
        sizer.Add(self.label,0,wx.ALL | wx.CENTER, 5)

        self.answer = wx.TextCtrl(panel, pos=(50, 80))
        sizer.Add(self.answer,0,wx.ALL | wx.CENTER, 5)

        self.submitButton = wx.Button(panel, label='Submit', pos=(50, 120))
        self.submitButton.Bind(wx.EVT_BUTTON, self.onSubmit2)
        sizer.Add(self.submitButton,0,wx.ALL | wx.CENTER, 5)

        panel.SetSizer(sizer)
    def onSubmit2(self, event):
        global score
        global attempts
        global questionNum
        answer = self.answer.GetValue()
        if answer.lower() == 'graphics processing unit':
            wx.MessageBox('Correct answer!')
            score += 1
            self.Close()
            quiz_frame3 = QuizFrame3()
            quiz_frame3.Show()
            print(score)
        elif answer.lower() != 'graphics processing unit' and attempts == 1:
            print("retry")
            questionNum = 2
            self.Close()
            retry_frame = RetryFrame()
            retry_frame.Show()
        else:
            wx.MessageBox('Sorry, wrong answer and no additional attempts')
            self.Close()
            quiz_frame3 = QuizFrame3()
            quiz_frame3.Show()

class QuizFrame3(wx.Frame):
    global score
    global attempts
    global questionNum
    def __init__(self):
        wx.Frame.__init__(self, None, title="Quiz", size=(400, 200))

        panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.label = wx.StaticText(panel, label="What does RAM stand for?", pos=(50, 50))
        sizer.Add(self.label,0,wx.ALL | wx.CENTER, 5)

        self.answer = wx.TextCtrl(panel, pos=(50, 80))
        sizer.Add(self.answer,0,wx.ALL | wx.CENTER, 5)

        self.submitButton = wx.Button(panel, label='Submit', pos=(50, 120))
        self.submitButton.Bind(wx.EVT_BUTTON, self.onSubmit3)
        sizer.Add(self.submitButton,0,wx.ALL | wx.CENTER, 5)

        panel.SetSizer(sizer)
    def onSubmit3(self, event):
        global score
        global attempts
        global questionNum
        answer = self.answer.GetValue()
        if answer.lower() == 'random access memory':
            wx.MessageBox('Correct answer!')
            score += 1
            self.Close()
            quiz_frame4 = QuizFrame4()
            quiz_frame4.Show()
            print(score)
        elif answer.lower() != 'random access memory' and attempts == 1:
            print("retry")
            questionNum = 3
            self.Close()
            retry_frame = RetryFrame()
            retry_frame.Show()
        else:
            wx.MessageBox('Sorry, wrong answer and no additional attempts')

            self.Close()
            quiz_frame4 = QuizFrame4()
            quiz_frame4.Show()

class QuizFrame4(wx.Frame):
    global score
    global attempts
    global questionNum
    def __init__(self):
        wx.Frame.__init__(self, None, title="Quiz", size=(400, 200))

        panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.label = wx.StaticText(panel, label="What does PSU stand for?", pos=(50, 50))
        sizer.Add(self.label,0,wx.ALL | wx.CENTER, 5)

        self.answer = wx.TextCtrl(panel, pos=(50, 80))
        sizer.Add(self.answer,0,wx.ALL | wx.CENTER, 5)

        self.submitButton = wx.Button(panel, label='Submit', pos=(50, 120))
        self.submitButton.Bind(wx.EVT_BUTTON, self.onSubmit4)
        sizer.Add(self.submitButton,0,wx.ALL | wx.CENTER, 5)

        panel.SetSizer(sizer)

    def onSubmit4(self, event):
        global score
        global attempts
        global questionNum
        answer = self.answer.GetValue()
        if answer.lower() == 'power supply':
            wx.MessageBox('Correct answer!')
            score += 1
            self.Close()
            results_frame = resultFrame()
            results_frame.Show()
            print(score)
        elif answer.lower() != 'power supply' and attempts == 1:
            print("retry")
            questionNum = 4
            self.Close()
            retry_frame = RetryFrame()
            retry_frame.Show()
        else:
            wx.MessageBox('Sorry, wrong answer and no additional attempts')
            self.Close()
            results_frame = resultFrame()
            results_frame.Show()

class resultFrame(wx.Frame):
    global score
    def __init__(self):
        wx.Frame.__init__(self, None, title="Score", size=(400, 200))
        if score != 0:
            totalScore = score/4
        else:
            totalScore = 0
            
        grade = "{:.2%}".format(totalScore)
        gradeStr = str(grade)
        panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.label = wx.StaticText(panel, label="Total Score is ", pos=(50, 50))
        sizer.Add(self.label,0,wx.ALL | wx.CENTER, 5)
        self.label.SetLabel(self.label.GetLabel()+gradeStr)

        panel.SetSizer(sizer)

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()