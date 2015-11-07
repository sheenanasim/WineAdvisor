#/usr/bin/env python
#-*- coding: utf-8 -*-

import csv, sqlite3
import Tkinter
from PIL import Image, ImageTk
import PIL
import ttk
from Tkinter import *
from ScrolledText import ScrolledText
import copy
import unicodecsv

class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.chosenType = ""
        self.chosenMeal = ""
        self.listWine = []
        self.parent = parent
        self.initialize()
        self.age=0
        self.sex='unknown'
        self.analysis = []
        self.index = 0
        
    def _get_chosenType(self):
        return self.chosenType

    def _get_chosenMeal(self):
        return self.chosenMeal

    def initialize(self):
        self.grid()
        self.grid()

        #ajoute un bouton
        self.button2 = Tkinter.Button(self,text=u"Click me when you're done!", command=self.OnButtonClick2)
        
        #ajoute un label
        self.labelVariableIntro = Tkinter.StringVar()
        self.labelIntro = Tkinter.Label(self,textvariable=self.labelVariableIntro,
                              anchor="w",fg="white",bg="blue")
        self.labelIntro.grid(column=0,row=0,columnspan=2,sticky='EW')
        self.labelVariableIntro.set(u"Hello ! We are here to help you chose your wine! What mode would you like to use?")

        #ajoute un label
        self.labelRadioText = Tkinter.StringVar()
        self.labelRadio = Tkinter.Label(self,textvariable=self.labelRadioText,
                              anchor="w",fg="white",bg="blue")
        self.labelRadioText.set(u"Please, tell us more about yourself:")

        #add canvas with scrollbar for the results
        self.canvas = Tkinter.Canvas(self, borderwidth=0, background="#ffffff")
        self.canvas.config(scrollregion=[0,0,400,400])
        self.canvas.grid(column = 0, row = 10, columnspan = 2)
        self.scrollbar = Scrollbar(self,orient=VERTICAL)
        self.scrollbar.grid(column = 3, row = 10, sticky = N+S)                 
        self.scrollbar.config(command=self.yview)
        
        #add textName
        self.textName = Text(self.canvas, width=55,height=30, yscrollcommand=self.scrollbar.set)
        self.textName.grid(column = 0, row = 0)
        self.textName.bind('<MouseWheel>', self.scrollwheel)

        #add textType
        self.textType = Text(self.canvas, width=15,height=30, yscrollcommand=self.scrollbar.set)
        self.textType.grid(column = 1, row = 0)
        self.textType.bind('<MouseWheel>', self.scrollwheel)

        #add textPrice
        self.textPrice = Text(self.canvas, width=7,height=30, yscrollcommand=self.scrollbar.set)
        self.textPrice.grid(column = 2, row = 0)
        self.textPrice.bind('<MouseWheel>', self.scrollwheel)

        #add textMarket
        self.textMarket = Text(self.canvas, width=12,height=30, yscrollcommand=self.scrollbar.set)
        self.textMarket.grid(column = 3, row = 0)
        self.textMarket.bind('<MouseWheel>', self.scrollwheel)
        
        #add combobox type
        self.combovar1 = Tkinter.StringVar()
        self.combovar1.set("Please Select Main Ingredient ... ")
        self.types1 = ttk.Combobox(self, textvariable=self.combovar1, state= 'readonly')
        self.types1.bind("<<ComboboxSelected>>", self.SelectedCombo1)
        self.types1['values'] = typeMeal
        self.types1.grid(column=0,row=6, columnspan = 2, sticky='EW')

        #add combobox meal
        self.combovar2 = Tkinter.StringVar()
        self.combovar2.set("Please Select Meal ... ")
        self.types2 = ttk.Combobox(self, textvariable=self.combovar2, state='readonly')
        self.types2.bind("<<ComboboxSelected>>", self.SelectedCombo2)

        #add combobox tri
        self.combovar3 = Tkinter.StringVar()
        self.combovar3.set("Sort by Price")
        self.sort = ttk.Combobox(self, textvariable=self.combovar3, state='readonly')
        self.sort.bind("<<ComboboxSelected>>", self.SelectedCombo3)
        self.sort['values'] = ('Price', 'Supermarket', 'Type')

        #add combobox gender
        self.combogender = Tkinter.StringVar()
        self.combogender.set("Tell us what your gender is.")
        self.gender = ttk.Combobox(self, textvariable=self.combogender)
        self.gender['values'] = ('Male', 'Female')

        #editable age
        self.comboage = Tkinter.StringVar()
        self.comboage.set("Please choose age.")
        self.agei = ttk.Combobox(self, textvariable=self.comboage, state='readonly')
        self.agei['values'] = (' < 35 ', '35 - 44','45 - 54', '55 - 64', ' > 64 ' )

        #ajoute un label
        self.labelVariable2 = Tkinter.StringVar()
        self.label2 = Tkinter.Label(self,textvariable=self.labelVariable2,
                              anchor="w",fg="white",bg="blue")
        self.labelVariable2.set(u"Please describe us what kind of food you are planning to have")
        self.label2.grid(column=0,row=5,columnspan=2,sticky='EW')

        #radiobutton
        self.select = IntVar()
        self.select.set(1)
        choices = [("Normal",1),("Advanced",2)]
        c = 0
        for txt, val in choices:
            Radiobutton(self, 
                text=txt,
                padx = 20, 
                variable=self.select, 
                command=self.SelectChoice,
                value=val).grid(column= c, row = 1)
            c += 1

    def scrollwheel(self, event):
        return 'break'

    def yview(self, *args):
        apply(self.textName.yview, args)
        apply(self.textType.yview, args)
        apply(self.textPrice.yview, args)
        apply(self.textMarket.yview, args)

    def SelectChoice(self):
        if self.select.get() == 2:
            #self.e.grid(column=1,row=3, sticky='EW')
            self.gender.grid(column=0, row=3, sticky='EW')
            self.agei.grid(column=1, row=3, sticky='EW')
            self.labelRadio.grid(column=0, row=2,columnspan=2,sticky='EW')
        else:
            #self.e.grid_remove()
            self.gender.grid_remove()
            self.agei.grid_remove()
            self.labelRadio.grid_remove()

    def SelectedCombo1(self, event):
        self.chosenType = self.types1.get()
        self.combovar2.set("Please Select Meal ... ")
        self.types2['values'] = self.getMeals(self.chosenType)
        self.types2.grid(column=0,row=7, sticky='EW', columnspan = 2)
        
        forma = ".jpg"
        address = self.chosenType + forma
        self.img = ImageTk.PhotoImage(PIL.Image.open(address))
        self.panelIm = Label(self, image = self.img)
        self.panelIm.grid(column = 4, row = 9, rowspan = 8)
        
    def SelectedCombo2(self, event):
        self.button2.grid(column=0,row=9, columnspan=2)
        #self.chosenMeal = self.type2.get()

    def SelectedCombo3(self, event):
        by = self.sort.get()
        if by == 'Type':
            realBy = 1
        if by == 'Supermarket':
            realBy = 2
        if by == 'Price':
            realBy = 3
        self.listWine = self.getWinesSorted(self.chosenType, self.chosenMeal, realBy)
        self.textName.config(state=NORMAL)
        self.textPrice.config(state=NORMAL)
        self.textMarket.config(state=NORMAL)
        self.textType.config(state=NORMAL)
        self.textName.delete(1.0, END)
        self.textPrice.delete(1.0, END)
        self.textMarket.delete(1.0, END)
        self.textType.delete(1.0, END)
        self.textName.insert(END, self.prettyString(self.listWine)[0])
        self.textType.insert(END, self.prettyString(self.listWine)[1])
        self.textPrice.insert(END, self.prettyString(self.listWine)[2])
        self.textMarket.insert(END, self.prettyString(self.listWine)[3])
        self.textName.config(state=DISABLED)
        self.textPrice.config(state=DISABLED)
        self.textMarket.config(state=DISABLED)
        self.textType.config(state=DISABLED)

    def takeMeal(self, meal):
        if not "What is" in meal:
            return meal
        else:
            result = "Overall Winner " + (self.chosenType.lower())
            return result

    def OnButtonClick2(self):
        self.chosenMeal = self.takeMeal(self.types2.get())
        #print self.chosenMeal
        self.listWine = self.getWines(self.chosenType, self.chosenMeal)
        self.textName.config(state=NORMAL)
        self.textPrice.config(state=NORMAL)
        self.textMarket.config(state=NORMAL)
        self.textType.config(state=NORMAL)
        self.textName.delete(1.0, END)
        self.textPrice.delete(1.0, END)
        self.textMarket.delete(1.0, END)
        self.textType.delete(1.0, END)
        self.textName.insert(END, self.prettyString(self.listWine)[0])
        self.textType.insert(END, self.prettyString(self.listWine)[1])
        self.textPrice.insert(END, self.prettyString(self.listWine)[2])
        self.textMarket.insert(END, self.prettyString(self.listWine)[3])
        self.textName.config(state=DISABLED)
        self.textPrice.config(state=DISABLED)
        self.textMarket.config(state=DISABLED)
        self.textType.config(state=DISABLED)
        self.sort.grid(column=0,row=8,columnspan=2, sticky='EW')

    def whichRow(self, age, sex):
        for i in range(len(self.analysis)):
            if str(self.analysis[i][0]) in str(sex) and int(self.analysis[i][1]) == int(age):
                return i

    def OnPressEnter(self,event):
        self.labelVariable.set(self.entryVariable.get()+" (You pressed ENTER)")

    def category(self, age):
        if age == " < 35":
            return 25
        if age == "35 - 44":
            return 35
        if age == "45 - 54":
            return 45
        if age == "55 - 64":
            return 55
        else:
            return 65

    def getMeals(self, typ):
        mealList=[]
        for row in cur.execute('SELECT MEAL FROM TYPEMEAL WHERE TYPE LIKE ?', (self.chosenType,)):
            mealList.append(row[0].title())
        for ele in mealList:
            if "Win" in ele:
                cop = copy.deepcopy(ele)
                mealList.remove(ele)
                mealList.append("My meal is not in the list. What is the overvall advice?")
        return mealList

    def selectBest(self, liste):
        result = []
        ret_list = []
        for ele in liste:
            for i in range(len(self.analysis[0])):
                if self.analysis[0][i].lower() == ele.lower():
                    result.append(self.analysis[self.index][i])

        result.sort(reverse=True)
        #print "result:"
        #print result
        
        for ele1 in result:
            for i in range(len(self.analysis[0])):
                if self.analysis[self.index][i] == ele1:
                    ret_list.append(self.analysis[0][i])

        #print "function"
        #print ret_list
                    
        if len(result)>0:
            return ret_list
        else:
            return liste

    def getWines(self, typ, meal):
        result = []
        possibleWines=[]

        cur.execute('DROP TABLE IF EXISTS INTER1')
        cur.execute("CREATE TABLE INTER1(meal TEXT, type TEXT, wine TEXT)")
        cur.execute('INSERT INTO INTER1 SELECT A.MEAL, A.TYPE, B.WINE FROM TYPEMEAL A, MATCHWINEFOOD B WHERE A.TYPE LIKE ? AND A.MEAL = B.MEAL AND A.MEAL LIKE ?', (typ,meal,))
        cur.execute('DROP TABLE IF EXISTS INTER2')
        cur.execute("CREATE TABLE INTER2(kind TEXT, name TEXT, kind2 TEXT, price FLOAT, supermarket TEXT)")
        
        possibleWineTypes=[]
        BestpossibleWineTypes =[]
        
        for row in cur.execute("SELECT DISTINCT WINE FROM INTER1"):
            #print row
            possibleWineTypes.append(row[0])

        #print possibleWineTypes
        if self.select.get() == 2:
            self.age = self.comboage.get()
            self.sex = self.gender.get()
            self.age = self.category(self.age)
            with open('result_analysis.csv','r') as fin:
                reader = unicodecsv.reader(fin, encoding='utf-8', delimiter=';', lineterminator='\n')
                for row in reader:
                    self.analysis.append(row)
            self.index = self.whichRow(self.age, self.sex)
            BestpossibleWineTypes = self.selectBest(possibleWineTypes)
  
            for ele in BestpossibleWineTypes:
                tmp_holder = 0
                cur.execute("SELECT COUNT(*) FROM ALLWINE A JOIN INTER1 B ON A.KIND = B.WINE WHERE A.KIND LIKE ?", (ele,))
                tmp_holder = cur.fetchone()[0]
                if tmp_holder != 0:
                    cur.execute("INSERT INTO INTER2 SELECT A.KIND, A.NAME, A.KIND2, A.PRICE, A.SUPERMARKET FROM ALLWINE A JOIN INTER1 B ON A.KIND = B.WINE WHERE A.KIND LIKE ?", (ele,))
                    break 
        else:
            BestpossibleWineTypes = possibleWineTypes
            for ele in BestpossibleWineTypes:
                cur.execute("INSERT INTO INTER2 SELECT A.KIND, A.NAME, A.KIND2, A.PRICE, A.SUPERMARKET FROM ALLWINE A JOIN INTER1 B ON A.KIND = B.WINE WHERE A.KIND LIKE ?", (ele,))

        print "BestWineTypes: "
        print BestpossibleWineTypes
        
        for row in cur.execute("SELECT DISTINCT KIND, NAME, KIND2, PRICE, SUPERMARKET FROM INTER2 ORDER BY PRICE"):
            possibleWines.append(row)
            
        return possibleWines

    def getWinesSorted(self, typ, meal, sortBy):
        result = []
        possibleWines=[]
        BestpossibleWineTypes= []
        
        cur.execute('DROP TABLE IF EXISTS INTER1')
        cur.execute("CREATE TABLE INTER1(meal TEXT, type TEXT, wine TEXT)")
        cur.execute('INSERT INTO INTER1 SELECT A.MEAL, A.TYPE, B.WINE FROM TYPEMEAL A, MATCHWINEFOOD B WHERE A.TYPE LIKE ? AND A.MEAL = B.MEAL AND A.MEAL LIKE ?', (typ,meal,))
        cur.execute('DROP TABLE IF EXISTS INTER2')
        cur.execute("CREATE TABLE INTER2(kind TEXT, name TEXT, kind2 TEXT, price FLOAT, supermarket TEXT)")
        
        possibleWineTypes=[]
        for row in cur.execute("SELECT DISTINCT WINE FROM INTER1"):
            possibleWineTypes.append(row[0])
            
        possibleWineTypes=[]
        for row in cur.execute("SELECT WINE FROM INTER1 WHERE MEAL LIKE ?", (self.chosenMeal,)):
            possibleWineTypes.append(row[0])
            #print row

        if self.select.get() == 2:
            self.age = self.comboage.get()
            self.sex = self.gender.get()
            self.age = self.category(self.age)
            with open('result_analysis.csv','r') as fin:
                reader = unicodecsv.reader(fin, encoding='utf-8', delimiter=';', lineterminator='\n')
                for row in reader:
                    self.analysis.append(row)
            self.index = self.whichRow(self.age, self.sex)
            BestpossibleWineTypes = self.selectBest(possibleWineTypes)

            for ele in BestpossibleWineTypes:
                tmp_holder = 0
                cur.execute("SELECT COUNT(*) FROM ALLWINE A JOIN INTER1 B ON A.KIND = B.WINE WHERE A.KIND LIKE ?", (ele,))
                tmp_holder = cur.fetchone()[0]
                if tmp_holder != 0:
                    cur.execute("INSERT INTO INTER2 SELECT A.KIND, A.NAME, A.KIND2, A.PRICE, A.SUPERMARKET FROM ALLWINE A JOIN INTER1 B ON A.KIND = B.WINE WHERE A.KIND LIKE ?", (ele,))
                    break
                
        else:
            BestpossibleWineTypes = possibleWineTypes
            for ele in BestpossibleWineTypes:
                cur.execute("INSERT INTO INTER2 SELECT A.KIND, A.NAME, A.KIND2, A.PRICE, A.SUPERMARKET FROM ALLWINE A JOIN INTER1 B ON A.KIND = B.WINE WHERE A.KIND LIKE ?", (ele,))

        #print "BestWineTypes: "
        #print BestpossibleWineTypes
        
        newResult = []
        for row in cur.execute("SELECT DISTINCT KIND, NAME, KIND2, PRICE, SUPERMARKET FROM INTER2 ORDER BY CASE WHEN ? = 1 THEN KIND2 WHEN ? = 2 THEN SUPERMARKET WHEN ? = 3 THEN PRICE END", (sortBy, sortBy, sortBy,)):
            newResult.append(row)

        return newResult
  
    def prettyString(self, liste):
        nameList = []
        priceList = []
        marketList = []
        typeList = []
        for ele1 in liste:
            tmp_name = ele1[1].strip()
            while tmp_name.endswith('#'):
                tmp_name = tmp_name[:-1]
                tmp_name.strip()
            
            nameList.append(tmp_name)
            nameList.append('\n')
            priceList.append('$')
            priceList.append(unicode(ele1[3]))
            priceList.append('\n')
            marketList.append(ele1[4])
            marketList.append('\n')
            typeList.append(ele1[2])
            typeList.append('\n')
        resultName = "".join(nameList)
        resultPrice = "".join(priceList)
        resultMarket = "".join(marketList)
        resultType = "".join(typeList)
        return (resultName, resultType, resultPrice, resultMarket)
        

if __name__ == "__main__":
    
    dataFile ="dataBase.sq3" 
    conn =sqlite3.connect(dataFile)
    cur =conn.cursor()

    #get type
    typeMeal=[]
    for row in cur.execute('SELECT DISTINCT TYPE FROM TYPEMEAL'):
      typeMeal.append(row[0].title())

    app = simpleapp_tk(None)
    app.title('Wine advisor')
    app.minsize(500,400)
    app.mainloop()
