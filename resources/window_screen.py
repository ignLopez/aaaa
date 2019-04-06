from tkinter import Frame, Button, Toplevel, Label
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3

from resources.modo_insert import ModoInsert
from resources.lectura_inteligente import LecturaInteligente
from resources.modo_report import ModoReport
from resources import base_paths
from config.config import SqlSentence as sqls

import seaborn as sns
sns.set()

class MainWindow:
    def __init__(self, window):
        self.db = base_paths.db_file
        self.window = window
        self.columnas = ('id', 'Fecha', 'Cuenta', 'Categoría', ' Subcategoría ', 'Descripción', '€', 'TipoMov', 'Notas')
        self.frameBottons = Frame(self.window, borderwidth=3, relief='groove', bg='blue')
        self.frameTable = Frame(self.window, borderwidth=3, relief='ridge', bg='blue')
        self.titulo = Label(self.frameBottons, text='Insertar un Movimiento').pack()
        self.titulo2 = Label(self.frameTable, text='Últimos Movimiento').pack(expand=1)

        #      self.tree = ttk.Treeview(self.frameTable)
        #        self.tree['columns'] = self.columnas
        #        self.tree['show'] = 'headings'
        #       for i in self.columnas:
        #            self.tree.heading(i, text=i, anchor=CENTER)
        #            self.tree.column(i, minwidth=0, width=90, stretch=NO)

        self.botonReport = Button(self.frameBottons, text='Mostrat Informe', command=self.create_report, width=15)
        self.button1 = Button(self.frameBottons, text='Gasto', command=lambda: self.getInsert('Gasto'), width=15)
        self.button2 = Button(self.frameBottons, text='Ingreso', command=lambda: self.getInsert('Ingreso'), width=15)
        self.button3 = Button(self.frameBottons, text='Traspaso', command=lambda: self.getInsert('Traspaso'), width=15)
        self.button4 = Button(self.frameBottons, text='Importar Movimientos', command=self.importarMov, width=15)
        self.fundaGraph = Figure(figsize=(10, 5), dpi=100)
        self.subploti = self.fundaGraph.add_subplot(111)
        self.subploti.set_title('Histórico')
        self.canvas = FigureCanvasTkAgg(self.fundaGraph, self.frameTable)
        self.canvas.get_tk_widget().pack(side='bottom', expand=True, fill='both', pady=5)

        self.botonReport.pack(side='bottom', expand=True, fill='both')
        self.button4.pack(side='bottom', expand=True, fill='both')
        self.button3.pack(side='bottom', expand=True, fill='both')
        self.button2.pack(side='bottom', expand=True, fill='both')
        self.button1.pack(side='bottom', expand=True, fill='both')

        # self.tree.pack(side='bottom', expand=True, fill='both', pady=5)

        self.frameBottons.grid(column=0, row=0, sticky="nsew")
        self.frameTable.grid(column=1, row=0, sticky="nsew")

        self.get_data()

    def getInsert(self, tipo):
        self.newWindow = Toplevel(self.window)
        self.app = ModoInsert(self.newWindow, tipo, self.window)
        self.window.withdraw()

    def importarMov(self):
        self.newWindow = Toplevel(self.window)
        self.app = LecturaInteligente(self.newWindow, self.window)
        self.window.withdraw()

    def create_report(self):
        self.newWindow = Toplevel(self.window)
        self.app = ModoReport(self.newWindow, self.window)
        self.window.withdraw()

    def get_data(self):

        def limpiar_eur(x):
            if type(x) == float:
                return x
            else:
                return float(x.replace(',', '.'))

        cnx = sqlite3.connect(self.db)
        cnx_cursor = cnx.cursor()
        cnx_cursor.execute(sqls.create_fact_table)
        cnx_cursor.execute(sqls.create_prueba_table)
        query = sqls.select_fact
        data = pd.read_sql_query(query, cnx)
        if not data.empty:
            data['fecha'] = pd.to_datetime(data['fecha'], format="%d/%m/%Y")
            data['mes'] = data['fecha'].apply(lambda x: x.month)
            data['anio'] = data['fecha'].apply(lambda x: x.year)
            data['eur'] = data['eur'].apply(lambda x: limpiar_eur(x))
            data.loc[data.tipo == 'Gasto', 'eur2'] = data['eur'] * -1
            data.loc[data.tipo != 'Gasto', 'eur2'] = data['eur']
            tablita = data[data['tipo'] != 'Traspaso'].pivot_table('eur2', index=['anio', 'mes'], columns='tipo',
                                                                   aggfunc='sum')
            tablita.index = [pd.datetime(anio, mes, 1).date().strftime('%m/%y') for (anio, mes) in tablita.index]
            df2 = pd.DataFrame(tablita.to_records())
            df2['ahorro_mensual'] = df2['Gasto'] + df2['Ingreso']
            df2['k'] = df2['ahorro_mensual'].cumsum()
            df2['index'] = pd.to_datetime(df2['index'], format="%m/%y")
            df2.index = [pd.to_datetime(i).date().strftime('%m/%y') for i in df2['index']]
            df2[['Gasto', 'Ingreso']].plot.bar(color=['red', 'green'])
            self.subploti.plot(df2['index'], df2['Gasto'] * -1)
            self.subploti.plot(df2['index'], df2['Ingreso'])
            self.subploti.plot(df2['index'], df2['k'])
