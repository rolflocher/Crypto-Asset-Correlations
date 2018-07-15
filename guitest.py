from tkinter import *
import requests
import os
import sys
from urllib.parse import urlencode
import pandas as pd
import numpy as np

class Application(Frame):
    
    staticcloselist=[]
    varcloselist=[]
    globalsymbol= 'test'
    globalsymbol2= 'test'
    globalint= 40
    globalper= '1m'
    globaldic={}
    
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        #self.button_clicks = 0
        self.create_widgets()

        
    def create_widgets(self):
        self.instruction = Label(self, text = "Enter Primary Pair")
        self.instruction.grid(row = 0, column = 0, columnspan = 2, sticky = W)

        self.esymbol = Entry(self)
        self.esymbol.grid(row=1, column = 0, sticky = W)
        

        self.instruction2 = Label(self, text = "Interval")
        self.instruction2.grid(row = 0, column = 1, columnspan = 2, sticky = W)

        self.eint = Entry(self)
        self.eint.grid(row=1, column = 1, sticky = W)
        

        self.instruction3 = Label(self, text = "Period")
        self.instruction3.grid(row = 0, column = 2, columnspan = 2, sticky = W)

        self.eper = Entry(self)
        self.eper.grid(row=1, column = 2, sticky = W)


        self.instruction4 = Label(self, text = "Search Symbol")
        self.instruction4.grid(row = 0, column = 3, columnspan = 2, sticky = W)

        self.esymbol2 = Entry(self)
        self.esymbol2.grid(row=1, column = 3, sticky = W)


        self.search_button = Button(self, text = "Search", command = self.search)
        self.search_button.grid(row = 2, column = 3, sticky = W)        

        
        self.submit_button = Button(self, text = "Submit", command = self.reveal)
        self.submit_button.grid(row = 2, column = 0, sticky = W)

        self.max_button = Button(self, text = "Max", command = self.max)
        self.max_button.grid(row = 4, column = 2, sticky = W)

        self.min_button = Button(self, text = "Min", command = self.min)
        self.min_button.grid(row = 4, column = 3, sticky = W)

        self.text = Text(self, width = 35, height = 25, wrap = WORD)
        self.text.grid(row=3, column = 0, columnspan = 2, sticky = W)

        self.text2 = Text(self, width = 35, height = 25, wrap = WORD)
        self.text2.grid(row=3, column = 2, columnspan = 2, sticky = W)
        
    def get_kline(self, market, limit=20, interval=2):
        path = "https://www.binance.com/api/v1/klines"
        params = {"symbol": market, "limit": limit, "interval": interval}
        return self._get_no_sign(path, params)    

    def _get_no_sign(self, path, params={}):
        query = urlencode(params)
        url = "%s?%s" % (path, query)
        return requests.get(url, timeout=30, verify=True).json()

    def getcloselist(self):
        
        
        kline = self.get_kline(self.globalsymbol, self.globalint, self.globalper)

        closelist =list(range(self.globalint))
        #localint=self.globalint
        
        for x in range(1, self.globalint):
            try:    
                temp= kline[x][4]
                closelist[x]=temp
            except IndexError:
                x= self.globalint
            
            
        dfcloselist=pd.DataFrame(closelist)

        closearray=np.asarray(dfcloselist, dtype=float)

        close_list=closearray.ravel()

        tempnump=close_list
        index=[0]
        fcloselist=np.delete(tempnump, index)
        self.varcloselist=fcloselist
        
    def max(self):
        
        self.text2.delete(0.0, END)
        maxv = sorted(self.globaldic.values(), reverse=True)
        maxn = sorted(self.globaldic, key=self.globaldic.__getitem__, reverse=True)
        for x in range(1, 25):

            message = '%s : %s\n' % (maxn[x], maxv[x])
            self.text2.insert(0.0, message)

    def min(self):
        self.text2.delete(0.0, END)
        minv = sorted(self.globaldic.values())
        minn = sorted(self.globaldic, key=self.globaldic.__getitem__)
        for x in range(1, 25):

            message = '%s : %s\n' % (minn[x], minv[x])
            self.text2.insert(0.0, message)

    def search(self):
        self.globalsymbol2= self.esymbol2.get()
        self.text2.delete(0.0, END)
        message = '%s : %s' % (self.globalsymbol2, self.globaldic[self.globalsymbol2])
        self.text2.insert(0.0, message)

    def reveal(self):
        #content = self.esymbol.get()
        self.globalsymbol = self.esymbol.get()
        self.globalint= int(self.eint.get())
        self.globalper= self.eper.get()

        print('Coefficients for %s with %s interval and history of %s' % (self.globalsymbol, self.globalper, self.globalint))
        #print(self.globalint)
        #print(self.globalper)
        
        #print('%s Symbol Correlations' % symbol)
        self.getcloselist()
        self.staticcloselist=self.varcloselist
        #print(self.staticcloselist)
        
        filename='2018symbols.txt'
        fin=open(filename, 'r')
        #for line in fin.readlines():
        #    slist.append([line])
        slist = [line.split('\t') for line in fin.readlines()]

        #print(slist)
        #print(slist.index("BNBUSDT"))

        dic= {}

        #dic= {'test':'5'}

##        if self.option.mode == 'THOROUGH':
##            self.option.symbol= self.option.symbol2
##            self.getcloselist()
##            tempco= np.corrcoef(self.staticcloselist,self.varcloselist)
##
##            dic[self.option.symbol]=tempco[1][0]
##            print(dic)
##        else :
            #coefflist=list(range(len(slist)))
        for x in range(0,372):
            self.globalsymbol= slist[0][x]
            self.getcloselist()
            #print(self.varcloselist)
            tempco= np.corrcoef(self.staticcloselist,self.varcloselist)

            dic[self.globalsymbol]=tempco[1][0]
            
            #coefflist.append(tempco[1][0])
            message = '%s : %s\n' % (slist[0][x], tempco[1][0])
            self.text.insert(0.0, message)

##            if slist[0][x] == 'MFTBTC':
##                print(tempco[1][0])
            
            #print(slist[0][x])
            #print(tempco[1][0])
        self.globaldic=dic


##        if content == "password":
##            message = "Correct"
##        else:
##            message = "Incorrect"
##        self.text.delete(0.0, END)
##        self.text.insert(0.0, message)
root = Tk()
root.title("RBL Correlation Computer")
root.geometry("600x500")
app = Application(root)
root.mainloop()
