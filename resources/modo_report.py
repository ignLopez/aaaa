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



        query = "SELECT fecha,categoria,eur FROM facts_table WHERE tipo='Gasto'"
        query2 = "SELECT fecha,categoria,eur FROM facts_table WHERE tipo='Gasto' AND categoria='alquiler'"
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
        self.controller = controller
        #label = Label(self, text="This is the start page")
        #label.pack(side="top", fill="x", pady=10)
        f = Figure(figsize=(5,5), dpi=100)
        f.tight_layout(pad=1, w_pad=1.0, h_pad=1.0)
        a = f.add_subplot(221)
        b = f.add_subplot(222)
        c = f.add_subplot(223)
        d = f.add_subplot(224)


        a.plot([1,2,3,4,5,6,7,8],[10,6,1,3,6,9,3,5])
        b.plot([1,2,3,4,5,6,7,8],[8,6,1,3,8,9,3,5])
        c.plot([1,2,3,4,5,6,7,8],[7,6,1,3,5,3,9,5])
        d.plot([1,2,3,4,5,6,7,8],[4,2,1,3,8,9,9,5])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(expand=True)


        def get_data2(self, query):

            cnx = sqlite3.connect(self.db)
            data = pd.read_sql_query(query, cnx)
            data['fecha'] = pd.to_datetime(data['fecha'], format="%d/%m/%Y")
            return data
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
            self.subploti1.pie(tablita.sort_values(by='eur', ascending=False).head(5),labels=tablita.sort_values(by='eur', ascending=False).head(5).index, autopct='%1.1f%%',shadow=True, startangle=90)






class PageOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is page 1")
        label.pack(side="top", fill="x", pady=10)


        ############## Pantalla principal #############


class princilapReport(Frame) :
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        query = "SELECT fecha,categoria,eur FROM facts_table WHERE tipo='Gasto'"
        query2 = "SELECT fecha,categoria,eur FROM facts_table WHERE tipo='Gasto' AND categoria='alquiler'"
        self.fundaGraph = Figure(figsize=(10, 5), dpi=100)
        self.fundaGraph.tight_layout(pad=1, w_pad=1.0, h_pad=1.0)
        self.subploti1 = self.fundaGraph.add_subplot(221)
        self.subploti1.axis('equal')
        self.subploti2 = self.fundaGraph.add_subplot(222)

        self.subploti3 = self.fundaGraph.add_subplot(223)

        self.subploti4 = self.fundaGraph.add_subplot(224)

        self.canvas = FigureCanvasTkAgg(self.fundaGraph,self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='bottom', expand=True, fill='both', pady=5)




        self.datos = self.get_data2(query)
        self.datos2 = self.get_data2(query2)
        self.get_pie(self.datos)
        self.get_cat_time(self.datos2, 'alquiler')

    def get_data2(self, query):

        cnx = sqlite3.connect(self.db)
        data = pd.read_sql_query(query, cnx)
        data['fecha'] = pd.to_datetime(data['fecha'], format="%d/%m/%Y")
        return data

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
        self.subploti1.pie(tablita.sort_values(by='eur', ascending=False).head(5),labels=tablita.sort_values(by='eur', ascending=False).head(5).index, autopct='%1.1f%%',shadow=True, startangle=90)

    def get_cat_time(self, data, cat):
        def limpiar_eur(x):
            if type(x) == float:
                return x
            else:
                return float(x.replace(',', '.'))

        data['fecha'] = pd.to_datetime(data['fecha'], format="%d/%m/%Y")
        data['mes'] = data['fecha'].apply(lambda x: x.month)
        data['anio'] = data['fecha'].apply(lambda x: x.year)
        data['eur'] = data['eur'].apply(lambda x: limpiar_eur(x))
        tablita = data[data['categoria'] == cat].pivot_table('eur', index=['anio', 'mes'], aggfunc='sum')
        tablita.index = [pd.datetime(anio, mes, 1).date().strftime('%y/%m') for (anio, mes) in tablita.index]
        tablita = pd.DataFrame(tablita.to_records())
        self.subploti2.plot(tablita['index'].sort_values(), tablita['eur'])
        self.subploti2.set_xticklabels(tablita['index'].sort_values(), rotation=60)
        self.subploti2.tick_params()
        print(tablita['index'].sort_values(), tablita['eur'])

class princilapOtro(Frame) :
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        query = "SELECT fecha,categoria,eur FROM facts_table WHERE tipo='Gasto'"
        query2 = "SELECT fecha,categoria,eur FROM facts_table WHERE tipo='Gasto' AND categoria='blackone'"
        self.fundaGraph = Figure(figsize=(10, 5), dpi=100)
        self.fundaGraph.tight_layout(pad=1, w_pad=1.0, h_pad=1.0)
        self.subploti1 = self.fundaGraph.add_subplot(221)
        self.subploti1.axis('equal')
        self.subploti2 = self.fundaGraph.add_subplot(222)

        self.subploti3 = self.fundaGraph.add_subplot(223)

        self.subploti4 = self.fundaGraph.add_subplot(224)

        self.canvas = FigureCanvasTkAgg(self.fundaGraph,self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='bottom', expand=True, fill='both', pady=5)




        self.datos = self.get_data2(query)
        self.datos2 = self.get_data2(query2)
        self.get_pie(self.datos)
        self.get_cat_time(self.datos2, 'alquiler')

    def get_data2(self, query):

        cnx = sqlite3.connect(self.db)
        data = pd.read_sql_query(query, cnx)
        data['fecha'] = pd.to_datetime(data['fecha'], format="%d/%m/%Y")
        return data

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
        self.subploti1.pie(tablita.sort_values(by='eur', ascending=False).head(5),
                           labels=tablita.sort_values(by='eur', ascending=False).head(5).index, autopct='%1.1f%%',
                           shadow=True, startangle=90)

    def get_cat_time(self, data, cat):
        def limpiar_eur(x):
            if type(x) == float:
                return x
            else:
                return float(x.replace(',', '.'))

        data['fecha'] = pd.to_datetime(data['fecha'], format="%d/%m/%Y")
        data['mes'] = data['fecha'].apply(lambda x: x.month)
        data['anio'] = data['fecha'].apply(lambda x: x.year)
        data['eur'] = data['eur'].apply(lambda x: limpiar_eur(x))
        tablita = data[data['categoria'] == cat].pivot_table('eur', index=['anio', 'mes'], aggfunc='sum')
        tablita.index = [pd.datetime(anio, mes, 1).date().strftime('%y/%m') for (anio, mes) in tablita.index]
        tablita = pd.DataFrame(tablita.to_records())
        self.subploti2.plot(tablita['index'].sort_values(), tablita['eur'])
        self.subploti2.set_xticklabels(tablita['index'].sort_values(), rotation=60)
        self.subploti2.tick_params()
        print(tablita['index'].sort_values(), tablita['eur'])



