from tkinter import LabelFrame, Button
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import pandas as pd

from resources import base_paths

class ModoReport:
    def __init__(self, newWindow, window):
        query = "SELECT fecha,categoria,eur FROM facts_table WHERE tipo='Gasto'"
        query2 = "SELECT fecha,categoria,eur FROM facts_table WHERE tipo='Gasto' AND categoria='alquiler'"
        self.db = base_paths.db_file
        self.newWindow = newWindow
        self.window = window
        self.frameBottons = LabelFrame(self.newWindow, borderwidth=3, relief='groove', bg='blue')
        self.frameTable = LabelFrame(self.newWindow, borderwidth=3, relief='ridge', bg='blue')

        self.button1 = Button(self.frameBottons, text='Resfrescar Report', width=15)
        self.fundaGraph = Figure(figsize=(10, 5), dpi=100)
        self.fundaGraph.tight_layout(pad=1, w_pad=1.0, h_pad=1.0)
        self.subploti1 = self.fundaGraph.add_subplot(221)
        self.subploti1.axis('equal')
        self.subploti2 = self.fundaGraph.add_subplot(222)

        self.subploti3 = self.fundaGraph.add_subplot(223)

        self.subploti4 = self.fundaGraph.add_subplot(224)

        self.canvas = FigureCanvasTkAgg(self.fundaGraph, self.frameTable)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='bottom', expand=True, fill='both', pady=5)

        self.button1.pack(side='bottom', expand=True, fill='both')

        self.frameBottons.grid(column=0, row=0, sticky="nsew")
        self.frameTable.grid(column=1, row=0, sticky="nsew")
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
