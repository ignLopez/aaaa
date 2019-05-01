from tkinter import Frame, ttk, Button, filedialog, CENTER, NO
import sqlite3
import pandas as pd

from config.config import params as dicti, yet2


class LecturaInteligente:

    def __init__(self, newWindow, window):
        self.db = 'HOST_CON.db'
        self.newWindow = newWindow
        self.window = window

        # self.newWindow.geometry("800x600")
        self.columnas = ('id', 'Fecha', 'Cuenta', 'Categoría', 'Subcategoría', 'Descripción', '€', 'TipoMov', 'Notas')
        self.columnasP = ('id', '€')
        self.columnasG = ('Descripción', 'Notas')
        self.frameBottons = Frame(self.newWindow, borderwidth=3, relief='groove', bg='blue')
        self.frameTable = Frame(self.newWindow, borderwidth=3, relief='ridge', bg='blue')

        self.tree = ttk.Treeview(self.frameTable)
        self.tree['columns'] = self.columnas
        self.tree['show'] = 'headings'
        for i in self.columnas:
            if i in self.columnasP:
                self.tree.heading(i, text=i, anchor=CENTER)
                self.tree.column(i, minwidth=0, width=60, stretch=NO)
            elif i in self.columnasG:
                self.tree.heading(i, text=i, anchor=CENTER)
                self.tree.column(i, minwidth=0, width=150, stretch=NO)
            else:
                self.tree.heading(i, text=i, anchor=CENTER)
                self.tree.column(i, minwidth=0, width=90, stretch=NO)

        self.tree2 = ttk.Treeview(self.frameTable)
        self.tree2['columns'] = self.columnas
        self.tree2['show'] = 'headings'
        for i in self.columnas:
            if i in self.columnasP:
                self.tree2.heading(i, text=i, anchor=CENTER)
                self.tree2.column(i, minwidth=0, width=60, stretch=NO)
            elif i in self.columnasG:
                self.tree2.heading(i, text=i, anchor=CENTER)
                self.tree2.column(i, minwidth=0, width=150, stretch=NO)
            else:
                self.tree2.heading(i, text=i, anchor=CENTER)
                self.tree2.column(i, minwidth=0, width=90, stretch=NO)

        self.button1 = Button(self.frameBottons, text='Importar Datos', command=self.importExcel, width=15)
        self.button2 = Button(self.frameBottons, text='Insertar', command=self.pasaraTabla, width=15)
        self.button3 = Button(self.frameBottons, text='Editar', command=self.editarEntabla, width=15)
        self.quitButton = Button(self.frameBottons, text='Editar', command=self.close_windows, width=15)

        # self.custName.set(filename)
        self.quitButton.pack(side='bottom', expand=False, fill='both')
        self.button3.pack(side='bottom', expand=True, fill='both')
        self.button2.pack(side='bottom', expand=True, fill='both')
        self.button1.pack(side='bottom', expand=True, fill='both')

        self.tree.pack(side='bottom', expand=True, fill='both', pady=5)
        self.tree2.pack(side='bottom', expand=True, fill='both', pady=5)

        self.frameBottons.grid(column=0, row=0, sticky="nsew")
        self.frameTable.grid(column=1, row=0, sticky="nsew")

        self.getMovimiento()

    def importExcel(self):
        filename = filedialog.askopenfilename(parent=self.frameBottons, title='Choose a file')
        self.impReadData(filename)

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
            return result

    def getMovimiento(self):
        # Limpia la tabla
        registrosAntiguos = self.tree.get_children()
        for registro in registrosAntiguos:
            self.tree.delete(registro)
        query = 'SELECT * FROM pruebas'
        movimientos = self.run_query(query)
        for movimiento in movimientos:
            self.tree.insert('', 0, values=movimiento)

    def getCategoria(self, concepto):
        minilist_tipo = []
        minilist_cate = []
        for i in dicti['categoria'].keys():
            for j in dicti['categoria'][i].keys():
                if concepto in dicti['categoria'][i][j]:
                    minilist_tipo.append(i)
                    minilist_cate.append(j)
                else:
                    continue

        if len(minilist_cate) > 1:
            return 'ERR', 'ERR', 'ERR'
        elif len(minilist_cate) == 1:
            if minilist_cate[0] == 'Traspaso desde cuenta':
                return minilist_tipo[0], minilist_cate[0]
            else:
                return minilist_tipo[0], minilist_cate[0]
        elif len(minilist_tipo) == 0:
            return 888, 888

    def getCuenta(self, movimiento):

        for i in dicti['cuenta']:
            if movimiento in dicti['cuenta'][i]:
                return i

    def leer_dict(self,concepto,movimiento):
        for i in dicti['categoria'].keys():
            for j in dicti['categoria'][i].keys():
                for t in dicti['categoria'][i][j]:
                    # si concepto está en la rama de las categorías
                    if  concepto.upper().rstrip().lstrip()==t.upper().rstrip().lstrip():
                        if i in ['Ingreso','Gasto','Traspaso']:
                            return 'bbva',j,i
                        elif i in ['Traspaso2']:
                            for i in dicti['Movimiento'].keys():
                                for a in dicti['Movimiento'][i].keys():
                                    for z in dicti['Movimiento'][i][a]:
                                        if (movimiento.upper().rstrip().lstrip()== z.upper().rstrip().lstrip()) or (z in movimiento.split()):
                                            return a,'bbva','Traspaso'

                        elif i in ['Traspaso3']:
                            for i in dicti['Movimiento'].keys():
                                for a in dicti['Movimiento'][i].keys():
                                    for z in dicti['Movimiento'][i][a]:
                                        if (movimiento.upper().rstrip().lstrip()== z.upper().rstrip().lstrip()) or (z in movimiento.split()):
                                            return 'bbva',a,'Traspaso'




    def impReadData(self, ruta):
        mov = pd.read_excel(ruta, encoding='latin1').iloc[:, 1:]
        for index, row in mov.iterrows():
            if self.leer_dict(row['Concepto'],row['Movimiento'])!=None:
                cuenta,categoria,tipo  = self.leer_dict(row['Concepto'],row['Movimiento'])
                self.tree2.insert('', 0, values=(index, row['F.Valor'], cuenta, categoria, row['Concepto'], abs(row['Importe']), tipo,row['Movimiento']))
            else:
                self.tree2.insert('', 0, values=(index, row['F.Valor'], '888', '888', row['Concepto'], abs(row['Importe']),'888',row['Movimiento']))

        del mov

    def deleteRow(self):
        selected_item = self.tree2.selection()[0]  # get selected item
        self.tree2.delete(selected_item)

    def pasaraTabla(self):

        fecha = self.tree2.item(self.tree2.selection())['values'][1]
        cuenta = self.tree2.item(self.tree2.selection())['values'][2]
        categoria = self.tree2.item(self.tree2.selection())['values'][3]
        subcategoria = self.tree2.item(self.tree2.selection())['values'][4]
        descripcion = self.tree2.item(self.tree2.selection())['values'][5]
        eur = self.tree2.item(self.tree2.selection())['values'][6]
        tipo = self.tree2.item(self.tree2.selection())['values'][7]
        nota = self.tree2.item(self.tree2.selection())['values'][8]
        query = "INSERT INTO pruebas VALUES(NULL,?,?,?,?,?,?,?,?,?)"
        parameters = (fecha, cuenta, categoria, subcategoria, descripcion, eur, tipo, nota, yet2)
        self.run_query(query, parameters)
        self.deleteRow()
        self.getMovimiento()

    def editarEntabla(self):
        print(self.tree2.item(self.tree2.selection())['values'])

    # for item in x:  ## Changing all children from root item
    #    tree.item(item, text="blub", values=("foo", "bar"))
    # Método Cerrar Ventana
    def close_windows(self):
        self.newWindow.destroy()
        self.window.deiconify()
