from tkinter import LabelFrame,Label,Frame, Button
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import pandas as pd
from tkinter import font  as tkfont

from resources import base_paths

class ModoReport:
    def __init__(self, newWindow, window):

        self.newWindow = newWindow
        self.window = window
        self.db = base_paths.db_file

        self.frameBottons = Frame(self.newWindow, borderwidth=3, relief='groove', bg='blue')
        self.frameTable = Frame(self.newWindow, borderwidth=3, relief='ridge', bg='blue')
        self.frameBottons.grid(column=0, row=0, sticky="nsew")
        self.frameTable.grid(column=1, row=0, sticky="nsew")

        self.button1 = Button(self.frameBottons, text='Gasto', command=lambda: self.show_frame(1))
        self.button2 = Button(self.frameBottons, text='Ingreso', command=lambda: self.show_frame(2))

        self.button2.pack(side='bottom', expand=True, fill='both')
        self.button1.pack(side='bottom', expand=True, fill='both')

        self.show_frame(1)

    #Función que cambia dinamicamente el frame

    def show_frame(self,pag):
        if pag == 1:
            self.frameTable1 = StartPage(parent=self.frameTable, controller=self.newWindow)
            self.frameTable1.grid(row=1, column=0, sticky="nsew")
            actual_frame=self.frameTable1
            actual_frame.tkraise()
        elif pag==2:
            self.frameTable2 = PageOne(parent=self.frameTable, controller=self.newWindow)
            self.frameTable2.grid(row=1, column=0, sticky="nsew")
            actual_frame=self.frameTable2
            actual_frame.tkraise()

class StartPage(Frame):
    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        query = "SELECT fecha,categoria,eur FROM facts_table WHERE tipo='Gasto'"
        query2 = "SELECT fecha,categoria,eur FROM facts_table WHERE tipo='Gasto' AND categoria='alquiler'"
        self.controller = controller
        self.db = base_paths.db_file
        self.figura = Figure(figsize=(10, 5), dpi=100)
        self.sub1 = self.figura.add_subplot(1,2,1)
        self.sub2 = self.figura.add_subplot(1,2,2)
        canvas = FigureCanvasTkAgg(self.figura, self)
        canvas.show()
        canvas.get_tk_widget().pack(expand=True)
        self.datos=self.get_data2(query)
        self.get_pie(self.datos)
        self.datos2 = self.get_data2(query)
        self.get_cat_time(self.datos2)
        self.figura.tight_layout()
#Conect to SQLite and return  query  in DataFrame
    def get_data2(self, query):

        cnx = sqlite3.connect(self.db)
        data = pd.read_sql_query(query, cnx)
        data['fecha'] = pd.to_datetime(data['fecha'], format="%d/%m/%Y")
        return data
# Create a pie chart
    def get_pie(self, data):
        def limpiar_eur(x):
                if type(x) == float:
                    return x
                else:
                    return float(x.replace(',', '.'))

        data['fecha'] = pd.to_datetime(data['fecha'], format="%d/%m/%Y")
        data['mes'] = data['fecha'].apply(lambda x: x.month)
        data['anio'] = data['fecha'].apply(lambda x: x.year)
        data['eur'] = data['eur'].apply(lambda x: limpiar_eur(x))
        tablita = data[['categoria', 'eur']].pivot_table('eur', index='categoria', aggfunc='sum')
        self.sub1.pie(tablita.sort_values(by='eur', ascending=False).head(5),labels=tablita.sort_values(by='eur', ascending=False).head(5).index,autopct='%1.1f%%',shadow=True, startangle=90)
        labels=tablita.sort_values(by='eur', ascending=False).head(5).index
        self.sub1.legend( labels, loc=3)
# plot selected category by month
    def get_cat_time(self, data):
        def limpiar_eur(x):
            if type(x) == float:
                return x
            else:
                return float(x.replace(',', '.'))
        data['fecha'] = pd.to_datetime(data['fecha'], format="%d/%m/%Y")
        data['mes'] = data['fecha'].apply(lambda x: x.month)
        data['anio'] = data['fecha'].apply(lambda x: x.year)
        data['eur'] = data['eur'].apply(lambda x: limpiar_eur(x))
        tablita = data.pivot_table('eur', index=['anio', 'mes'], aggfunc='sum')
        tablita.index = [pd.datetime(anio, mes, 1).date().strftime('%y/%m') for (anio, mes) in tablita.index]
        tablita = pd.DataFrame(tablita.to_records())
        self.sub2.plot(tablita['index'].sort_values(), tablita['eur'])
        self.sub2.set_xticklabels(tablita['index'].sort_values(), rotation=60)
        self.sub2.tick_params()

class PageOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Informe en Construcción")
        label.pack(side="top", fill="x", pady=10)


