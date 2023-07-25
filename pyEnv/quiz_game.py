print("welcome to my computer quiz!")
print("The rules are simple, answer each question correctly, you get one do over on one of the four questions, choose wisely!")

playing = input("Do you want to play? ")

if playing.lower() != 'yes':
    quit()
else:
    print("Okay! Let's play")
    score=0
    doOver=1

answer = input("What does CPU stand for? ")
if answer.lower() == "central processing unit":
    print("Correct!")
    score+=1
else:
    repeatQ = input("Incorrect, Try Again? ")
    if repeatQ.lower() == 'yes' and doOver==1:
        doOver -=1
        answer = input("What does CPU stand for? ")
        if answer.lower() == "central processing unit":
            print("Correct!")
            score+=1


answer = input("What does GPU stand for? ")
if answer.lower() == "graphics processing unit":
    print("Correct!")
    score+=1
else:
    repeatQ = input("Incorrect, Try Again? ")
    if repeatQ.lower() == 'yes' and doOver==1:
        doOver -=1
        answer = input("What does GPU stand for? ")
        if answer.lower() == "central processing unit":
            print("Correct!")
            score+=1

answer = input("What does RAM stand for? ")
if answer.lower() == "random access memory":
    print("Correct!")
    score+=1
else:
    print("Incorrect, Try Again!")

answer = input("What does PSU stand for? ")
if answer.lower() == "power supply":
    print("Correct!")
    score+=1
else:
    print("Incorrect, Try Again!")

Grade = score/4
Grade = "{:.2%}".format(Grade)
print(f"Your final score is: {Grade}")