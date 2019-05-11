from tkinter import Frame, ttk, Button, filedialog, CENTER, NO
import sqlite3
from resources import base_paths
import pandas as pd
import datetime as dt

class ModoBalance:
    def __init__(self, newWindow, window):
        self.db = 'C://Users//Ignacio//Desktop//proyecto_conta//contaProyect//resources//db//HOST_CON.db'
        self.newWindow = newWindow
        self.window = window
        self.newWindow.geometry("735x628+370+63")
        self.font = ("Helvetica", 10, 'bold')
        self.frameBottons = Frame(self.newWindow, borderwidth=3, relief='groove', bg='#4863a0')
        self.frameTable = Frame(self.newWindow, borderwidth=3, relief='ridge', bg='white')

        self.tree = ttk.Treeview(self.frameTable)
        self.tree['columns']=['Grupo Cuentas','Saldo']
        self.tree['show'] = 'headings'
        for i in ['Grupo Cuentas','Saldo']:
            self.tree.heading(i,text=i,anchor=CENTER)
            self.tree.column(i,minwidth= 2, width=200,stretch=NO)

        self.button1 = Button(self.frameBottons, text='boton', width=15,
                              bg='#4863a0', activebackground='#fff', activeforeground='#4863a0', fg='#fff',
                              font=self.font)
        self.button2 = Button(self.frameBottons, text='Quit',  width=15,command=self.close_windows,
                              bg='#4863a0', activebackground='#fff', activeforeground='#4863a0', fg='#fff',
                              font=self.font)
        self.button2.pack(side='left', expand=True, fill='both')
        self.button1.pack(side='left', expand=True, fill='both')

        self.tree.place(relx=0.014, rely=0.019, relheight=0.966 , relwidth=0.979)
        self.frameBottons.place(relx=0.014, rely=0.016, relheight=0.10, relwidth=0.973)
        self.frameTable.place(relx=0.014, rely=0.127, relheight=0.852, relwidth=0.973)

        self.get_tree_values()

    def run_query(self, query):
        cnx = sqlite3.connect(self.db)
        data = pd.read_sql_query(query, cnx)
        return data

    def get_multiplicador(self,cuenta,tipo,eur,i):
        condicion1=(cuenta==i and tipo=='Traspaso')
        condicion2=(tipo=='Gasto')
        if condicion1 | condicion2:
            return (-1)*float(eur)
        else:
            return 1*float(eur)

    def prepare_data(self,data):
        data['fecha'] = pd.to_datetime(data['fecha'])
        data['year']=data['fecha'].apply(lambda x: x.year)
        data['eur']=data['eur'].apply(lambda x: float(str(x).replace(',','.')))
        data_prep = data
        return data_prep

    def get_tree_values(self):
        query_tipoCuentas="SELECT descript from dimCuentas_tipo order by orden"
        lista_tipo=self.run_query(query_tipoCuentas)
        query_lista = 'SELECT * FROM dimCuentas'
        lista_cuentas = self.run_query(query_lista)
        query1 = 'SELECT * FROM facts_table '  #'+"'"+str(cuenta)+"'"
        data=self.run_query(query1)
        data_prep=self.prepare_data(data)
        for index,row in lista_tipo.iterrows():
            abuelo=self.tree.insert('','end',values=(row['descript'],))
            for index,row in lista_cuentas[lista_cuentas['tipo_cuenta']==row['descript']].iterrows():
                resta= data_prep[ ( (data_prep['cuenta']==row['descrip']) & (data_prep['tipo']=='Traspaso') ) | ( (data_prep['cuenta']==row['descrip']) & (data_prep['tipo']== 'Gasto'))]['eur'].sum()
                suma=data_prep[ ( (data_prep['cuenta']==row['descrip']) & (data_prep['tipo']=='Ingreso') ) | ( (data_prep['categoria']==row['descrip']) & (data_prep['tipo']== 'Traspaso'))]['eur'].sum()
                saldo=round(suma-resta,2)
                self.tree.insert(abuelo,'end',values=('       ' + row['descrip']+' '+'€',saldo))

    def close_windows(self):
        self.newWindow.destroy()
        self.window.deiconify()






