from tkinter.font import BOLD
import requests
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
import json
import base64

win = Tk()
win.title("My Simple IDE")
win.geometry('1200x650')
win.resizable(0,0)

#Variables
userInput = StringVar()
wrap = IntVar()
integer = IntVar()
string = IntVar()
float = IntVar()
boolean = IntVar()
API_KEY = "" #get a free api key at https://rapidapi.com/judge0-official/api/judge0-ce/

def Base64_encode(element):
    element_bytes = element.encode('ascii')
    base64_bytes = base64.b64encode(element_bytes)
    base64_string = base64_bytes.decode('ascii')
    return base64_string 

def Base64_decode(element):
    element_bytes = element.encode('ascii')
    base64_bytes = base64.b64decode(element_bytes)
    base64_string = base64_bytes.decode('ascii')
    return base64_string 

def submissions():
    global userInput, string, integer, boolean, float

    stdin = userInput.get()
    """stringInput = string.get()
    integerInput = integer.get()
    booleanInput = boolean.get()
    floatInput = float.get()"""
    source_code = text.get('1.0', 'end-1c')
    language = list.get(first='active')

    if( language == "Python 3"):
        lang = 71
    elif(language == "Python 2"):
        lang = 70
    elif(language == "Java"):
        lang = 62
    elif(language == "Javascript"):
        lang = 63
    elif(language == "C#"):
        lang = 51
    elif(language == "C++ (GCC 9.2.0)"):
        lang = 54
    elif(language == "C++ (Clang 7.0.1)"):
        lang = 76
    elif(language == "C (GCC 9.2.0)"):
        lang = 50
    elif(language == "C (Clang 7.0.1)"):
        lang = 75
    submit(lang, source_code, stdin)

def submit(language, source_code, stdin):
    url = "https://judge0-ce.p.rapidapi.com/submissions?base64_encoded=true&fields=*"
    payload = {
	    "language_id": int(language),
	    "source_code": Base64_encode(source_code),
	    "stdin": Base64_encode(stdin)
    }
    headers = {
	    "content-type": "application/json",
	    "Content-Type": "application/json",
	    "X-RapidAPI-Key": API_KEY,
	    "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    token = response.text
    tokens = json.loads(token)
    output(tokens['token'])

def output(token):
    url = "https://judge0-ce.p.rapidapi.com/submissions/" + token 
    querystring = {"base64_encoded":"true","fields":"*"}

    headers = {
	"X-RapidAPI-Key": API_KEY,
	"X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    output_json = response.text
    output_string = json.loads(output_json)
    output = output_string['stdout']
    output = Base64_decode(output)
    outputText.configure(state='normal')
    length=int(outputText.index('end').split('.')[0])
    print(length)
    outputText.delete("1.0","end")
    outputText.insert('end', output)
    outputText.configure(state='disabled')


#Canvas
edit_canvas = Canvas(win, width=600, height=650, background='#f7f7f7')
edit_canvas.pack(side=LEFT)
other_canvas = Canvas(win, width=600, height=650)
other_canvas.pack(side=RIGHT)
input_canvas = Canvas(other_canvas, width=600, height=200, background='#f7f7f7')
input_canvas.pack(side=TOP)
output_canvas = Canvas(other_canvas, width=600, height=450, background='#3d3a50')
output_canvas.pack(side=BOTTOM)

#Lables
Label(win, text="katroid Code Playground", fg='#1a1c22', bg="#f7f7f7", font=("Arial, Helvetica, sans-serif", 25, "bold") ).place(relx=0.35, rely=0.01)
Label(edit_canvas, text='Code Input', fg='#1a1c22', bg="#f7f7f7", font=("Verdana, Geneva, Tahoma, sans-serif", 16, "bold")).place(relx=0.05, rely=0.1)
Label(edit_canvas, text='Language', fg='#1a1c22', bg="#f7f7f7", font=("Verdana, Geneva, Tahoma, sans-serif", 13)).place(relx=0.57,rely=0.93)
Label(input_canvas, text='User Input (If Required)', fg='#1a1c22', bg="#f7f7f7", font=("Verdana, Geneva, Tahoma, sans-serif", 16,"bold")).place(relx=0.1, rely=0.3)
Label(output_canvas, text='Code Output', fg='#f7f7f7', bg="#3d3a50", font=("Verdana, Geneva, Tahoma, sans-serif", 16, "bold")).place(relx=0.05, rely=0.05)
    
#ScrolledText
text = ScrolledText(edit_canvas,font=("Segoe UI', Tahoma, Geneva, Verdana, sans-serif", 13, BOLD), state='normal', height=25, width=60, wrap='word', pady=2, padx=3, undo=True)
text.place(relx =0.05, rely=0.15)
outputText = ScrolledText(output_canvas,font=("Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial,sans-serif", 13, "italic"), state='normal', height=18, width=57, wrap='word', pady=2, padx=3, undo=True)
outputText.place(relx =0.05, rely=0.15)
outputText.insert('1.0', """// This Code Playground was developed by SpiderSplinter
// See code at github.com/spidersplinter
    """)
outputText.configure(state='disabled')

#listView
list = Listbox(edit_canvas, bg='#f7f7f7', fg="#1a1c22", font=("Verdana, Geneva, Tahoma, sans-serif", 14), width=13, height=1, activestyle='dotbox')
list.insert(0, "Python 3")
list.insert(1, "Python 2")
list.insert(2, "Java")
list.insert(3, "Javascript")
list.insert(4, "C#")
list.insert(5, "C++ (GCC 9.2.0)")
list.insert(5, "C++ (Clang 7.0.1)")
list.insert(5, "C (GCC 9.2.0)")
list.insert(5, "C (Clang 7.0.1)")
list.activate(0)
list.place(relx=0.7, rely=0.93)

#Checkbutton
c5 = Checkbutton(input_canvas, text='String',variable=string, onvalue=1, offvalue=0)
c5.select()
c5.place(relx=0.55, rely=0.7)
c1 = Checkbutton(edit_canvas, text='Wrap',variable=wrap, onvalue=1, offvalue=0)
c1.select()
c1.place(relx=0.05, rely=0.93)
c2 = Checkbutton(input_canvas, text='Integer', variable=integer, onvalue=1, offvalue=0)
c2.place(relx=0.1, rely=0.7)
c3 = Checkbutton(input_canvas, text='Float',variable=float, onvalue=1, offvalue=0)
c3.place(relx=0.25, rely=0.7)
c4 = Checkbutton(input_canvas, text='Boolean',variable=boolean, onvalue=1, offvalue=0)
c4.place(relx=0.4, rely=0.7)

#Button
Button(edit_canvas, text="RUN", bg='#3d3a50', fg="#f7f7f7", width=10, height=2, font=("Verdana, Geneva, Tahoma, sans-serif", 13,"bold"), padx=0, pady=0, command=submissions).place(relx=0.76, rely=0.06)
Button(input_canvas, text="SUBMIT", bg='#3d3a50', fg="#f7f7f7", width=13, height=1, font=("Verdana, Geneva, Tahoma, sans-serif", 13, "bold"), padx=0, pady=2).place(relx=0.7, rely=0.7)

#Entry
Entry(input_canvas, textvariable=userInput, width=40, font=("Verdana, Geneva, Tahoma, sans-serif", 16), borderwidth=1).place(relx=0.1, rely=0.5)

win.mainloop()
