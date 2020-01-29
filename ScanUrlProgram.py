from tkinter import *
from StopWatch import *
from extractAllUrlComposite import *
import multitasking

class ScanGui:
    def __init__(self, root):

        self.urlStr = StringVar()
        self.urlStr.set("")

        self.root = root
        root.title("Scan a URL :")

        self.Scanlbl = Label(root, text= "Enter the url : ")
        self.Scanlbl.pack()

        # register a function into the window
        validate_command = root.register(self.validate)

        self.inputText = Entry(root,
                               width=50,
                               validate="key",
                               validatecommand=(validate_command, '%P'))
        self.inputText.pack()

        self.mylbl = Label(root, text="The Url is: ")
        self.mylbl.pack()
        Label(root, textvariable=self.urlStr).pack()

        self.sw = StopWatch(root)
        self.sw.pack(side=TOP)

        BtnsFrame = Frame(root)
        BtnsFrame.pack()
        self.S1Btn = Button(BtnsFrame, text='StartT', command=self.sw.Start)
        self.S1Btn.bind("<Button-1>", self.StartTheScan)
        self.S1Btn.pack(side=LEFT)
        self.S2Btn = Button(BtnsFrame, text='Stop', command=self.sw.Stop)
        self.S2Btn.bind("<Button-1>", self.StopTheScan)
        self.S2Btn.pack(side=LEFT)
        Button(BtnsFrame, text='Quit', command=root.quit).pack(side=LEFT)

        frameListBx = Frame(root)
        frameListBx.pack()

        Label(root , text="The result of the scan is :").pack()
        self.OutputListBx = Listbox(frameListBx,width="100")
        self.OutputListBx.pack(side="left", fill="y")
        scrollbar = Scrollbar(frameListBx, orient="vertical")
        scrollbar.config(command=self.OutputListBx.yview)
        scrollbar.pack(side="right", fill="y")

        self.OutputListBx.config(yscrollcommand=scrollbar.set)

        MODES = [
            ("InnerLinks", "OnlyInner"),
            ("OuterLinks", "OnlyOuter"),
            ("BothInnerNOuterLinks", "Both")
        ]

        Label(root, text="Choose scan mode :").pack()
        self.con = StringVar()
        self.con.set("OnlyInner")  # initialize
        for text, mode in MODES:
            self.b = Radiobutton(root, text=text,
                                 variable=self.con, value=mode,
                                 indicatoron=0,
                                 width=30)
            self.b.pack()
        self.modebtn = Button(root, text="Print", command=lambda: print(self.con.get()))
        self.modebtn.pack()

    @multitasking.task
    def StartTheScan(self, event=""):
        try:
            print("Starting !!")
            if self.urlStr.get() != "":
                crawl(self.urlStr.get())
                if self.con.get() == "OnlyInner":
                    for n in range(len(internal_urls)):
                        self.OutputListBx.insert(END, list(internal_urls)[n])
                elif self.con.get() == "OnlyOuter":
                    for n in range(len(external_urls)):
                        self.OutputListBx.insert(END, list(external_urls)[n])
                else: # - Both
                    for n in range(len(internal_urls)):
                        self.OutputListBx.insert(END, list(internal_urls)[n])
                    for n in range(len(external_urls)):
                        self.OutputListBx.insert(END, list(external_urls)[n])

                print("[+] Total External links:", len(external_urls))
                print("[+] Total Internal links:", len(internal_urls))
                print("[+] Total:", len(external_urls) + len(internal_urls))
        except ValueError:
            print(ValueError)

    @multitasking.task
    def StopTheScan(self, event=""):
        print("Stoping !!")
        StopCrawl()

    def validate(self, new_text):
        try:
            if new_text == "":
                self.urlStr.set("")
                return True
            fl = str(new_text)
            self.urlStr.set(fl)
            return True
        except ValueError:
            return False



root = Tk()
#root.geometry("400x300")
my_window = ScanGui(root)


root.mainloop()  # blocking

