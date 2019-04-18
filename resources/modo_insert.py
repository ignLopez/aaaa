from tkinter import LabelFrame, Label, ttk, Entry, CENTER, NO, StringVar, Toplevel, DoubleVar, W, E, Button
import sqlite3

from config.config import yet, yet2, SqlSentence as sqls
from resources import base_paths

class ModoInsert:

    # Principal modo insert view
    def __init__(self, newWindow, tipo, window):
        self.db = base_paths.db_file
        self.tipo = tipo
        self.window1 = newWindow
        self.window = window
        self.columnas = ('id', 'Fecha', 'Cuenta', 'Categoría', ' Subcategoría ', 'Descripción', '€', 'TipoMov', 'Notas')
        self.frameBottons = LabelFrame(self.window1, borderwidth=3, relief='groove', bg='blue')
        self.frameTable = LabelFrame(self.window1, borderwidth=3, relief='ridge', bg='blue')
        self.message = Label(self.window1, borderwidth=3, relief='ridge')
        self.message['text'] = ''
        self.titulo = Label(self.frameBottons, text='Insertar un Movimiento').pack()
        # self.message = Label(self.frameTable,text='',fg='red').pack( expand=True, fill='both')

        self.tree = ttk.Treeview(self.frameTable)
        self.tree['columns'] = self.columnas
        self.tree['show'] = 'headings'
        for i in self.columnas:
            self.tree.heading(i, text=i, anchor=CENTER)
            self.tree.column(i, minwidth=0, width=90, stretch=NO)

        self.fechaEtiqueta = Label(self.frameBottons, text='Fecha: ')
        self.fecha = Entry(self.frameBottons, textvariable=StringVar(self.frameBottons, yet))
        self.cuentaEtiqueta = Label(self.frameBottons, text='Cuenta: ')
        self.cuenta = ttk.Combobox(self.frameBottons, state="readonly", width=17)
        self.cuenta["values"] = ''
        self.categoriaEtiqueta = Label(self.frameBottons, text='Categoria: ')
        self.categoria = ttk.Combobox(self.frameBottons, state="readonly", width=17)
        self.categoria["values"] = ''
        self.subcategoriaEtiqueta = Label(self.frameBottons, text='Subcategoria: ')
        self.subcategoria = Entry(self.frameBottons)
        self.descripcionEtiqueta = Label(self.frameBottons, text='Descripcion: ')
        self.descripcion = Entry(self.frameBottons)
        self.eurEtiqueta = Label(self.frameBottons, text='€: ')
        self.eur = Entry(self.frameBottons)
        self.tipoEtiqueta = Label(self.frameBottons, text='tipo: ')
        self.tipo = Entry(self.frameBottons, textvariable=StringVar(self.frameBottons, tipo), state='readonly')
        self.notaEtiqueta = Label(self.frameBottons, text='Nota: ')
        self.nota = Entry(self.frameBottons)
        self.botonInsertarMov = ttk.Button(self.frameBottons, text='Aceptar',
                                           command=lambda: self.insertarMovimiento(tipo))
        self.editar = ttk.Button(self.frameBottons, text='Editar', command=lambda: self.g_editar(tipo))
        self.borrar = ttk.Button(self.frameBottons, text='Borrar', command=lambda: self.g_borrar(tipo))
        self.quitButton = ttk.Button(self.frameBottons, text='Quit', width=25, command=self.close_windows)

        self.quitButton.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.borrar.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.editar.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.botonInsertarMov.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.nota.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.notaEtiqueta.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.tipo.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.tipoEtiqueta.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.eur.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.eurEtiqueta.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.descripcion.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.descripcionEtiqueta.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.subcategoria.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.subcategoriaEtiqueta.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.categoria.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.categoriaEtiqueta.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.cuenta.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.cuentaEtiqueta.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.fecha.pack(side='bottom', expand=True, fill='both', ipady=2)
        self.fechaEtiqueta.pack(side='bottom', expand=True, fill='both', ipady=2)

        self.tree.pack(side='bottom', expand=True, fill='both', pady=5)
        # self.message.pack(side='bottom', expand=True, fill='both', pady=5)

        self.frameBottons.grid(column=0, row=0, sticky="nsew")
        self.frameTable.grid(column=1, row=0, sticky="nsew")
        self.message.grid(column=0, row=1, sticky="ew", columnspan=10)

        self.getMovimiento(tipo)
        self.getCuenta()
        self.getCategoria(tipo)
        self.insertarMovimiento(tipo)


    # Get sqlitle connection
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
            return result

    # get sql query
    def getMovimiento(self, tipo):
        # Limpia la tabla
        tipo = str(tipo)
        registrosAntiguos = self.tree.get_children()
        for registro in registrosAntiguos:
            self.tree.delete(registro)
        query = sqls.select_pruebas.format(tipo)
        print(query)
        movimientos = self.run_query(query)
        for movimiento in movimientos:
            self.tree.insert('', 0, text=movimiento[0], values=movimiento[0:])

    def getMovimiento2(self):
        # Limpia la tabla
        registrosAntiguos = self.tree.get_children()
        for registro in registrosAntiguos:
            self.tree.delete(registro)
        query = 'SELECT * FROM pruebas'
        movimientos = self.run_query(query)
        for movimiento in movimientos:
            self.tree.insert('', 0, text=movimiento[0], values=movimiento[1:])

    # show list of cuenta order by historic frequency
    def getCuenta(self):
        query = """SELECT cuenta FROM
                  (SELECT  cuenta ,count(cuenta) as  freq
                  FROM facts_table
                  GROUP BY cuenta
                  order by count(cuenta) desc) as T1"""
        elemntos = self.run_query(query)
        lista = [elemento[0] for elemento in elemntos]
        self.cuenta["values"] = lista

    # show list of category order by historic frequency
    def getCategoria(self, tipo):
        query = 'SELECT distinct categoria from facts_table Where tipo="' + tipo + '"'
        elemntos = self.run_query(query)
        lista = [elemento[0] for elemento in elemntos]
        self.categoria["values"] = lista
    # form validation
    def validacion(self):
        "result =  len(self.fecha.get())!=0 and \
                  len(self.eur.get())!=0ç2"""
        # ('.' in self.eur.get())
        return True
    # insert data form in sqllitle
    def insertarMovimiento(self, tipo):
        if self.validacion():
            query = "INSERT INTO pruebas VALUES(NULL,?,?,?,?,?,?,?,?,?)"
            parameters = (
                self.fecha.get(),
                self.cuenta.get(),
                self.categoria.get(),
                self.subcategoria.get(),
                self.descripcion.get(),
                self.eur.get(),
                self.tipo.get(),
                self.nota.get(),
                yet2)
            self.run_query(query, parameters)
            self.message['text'] = 'Datos Salvados'
        else:
            self.message['text'] = 'Algo hay mal, mira a ver!'
        self.getMovimiento(tipo)

    def getLista(self):
        query = """SELECT cuenta FROM
                  (SELECT  cuenta ,count(cuenta) as  freq
                  FROM facts_table
                  GROUP BY cuenta
                  order by count(cuenta) desc) as T1"""
        querGasto = """SELECT distinct categoria from facts_table Where tipo='Gasto'"""
        elemntos = self.run_query(query)
        lista = [elemento[0] for elemento in elemntos]
        self.cuenta["values"] = lista

    # delete form registry
    def g_borrar(self, tipo):
        self.message['text'] = ''  # Vaciamos el texto del mensaje
        try:
            self.tree.item(self.tree.selection())['text']

        except IndexError:
            self.message['text'] = 'Selecciona un movimiento simpló!!'
            return
        self.message['text'] = ''
        id = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM pruebas WHERE id=?'
        self.run_query(query, (id,))
        self.message['text'] = 'yiaaass!!! La armaste'
        self.getMovimiento(tipo)

    # create edit window form registry
    def g_editar(self, tipo):
        self.message['text'] = ''  # Vaciamos el texto del mensaje
        try:
            self.tree.item(self.tree.selection())['values'][0]

        except IndexError:
            self.message['text'] = 'Selecciona un movimiento simpló!!'
            return

        id = self.tree.item(self.tree.selection())['text']
        fecha = self.tree.item(self.tree.selection())['values'][0]
        cuenta = self.tree.item(self.tree.selection())['values'][1]
        categoria = self.tree.item(self.tree.selection())['values'][2]
        subcategoria = self.tree.item(self.tree.selection())['values'][3]
        descripcion = self.tree.item(self.tree.selection())['values'][4]
        eur = self.tree.item(self.tree.selection())['values'][5]
        tipo2 = self.tree.item(self.tree.selection())['values'][6]
        nota = self.tree.item(self.tree.selection())['values'][7]

        self.edit_wind = Toplevel()
        self.edit_wind.title = "Editar movimiento"

        # Show ID
        Label(self.edit_wind, text='Old Name: ').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=id), state='readonly').grid(row=0, column=2)

        # old fecha
        Label(self.edit_wind, text='Fecha: ').grid(row=1, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=fecha), state='readonly').grid(row=1,
                                                                                                          column=2)
        # New fecha
        Label(self.edit_wind, text='Nueva Fecha: ').grid(row=1, column=3)
        newFecha = Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=fecha))
        newFecha.grid(row=1, column=4)

        # old Cuenta
        Label(self.edit_wind, text='Cuenta: ').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=cuenta), state='readonly').grid(row=2,
                                                                                                           column=2)

        # New cuenta
        Label(self.edit_wind, text=' New Cuenta: ').grid(row=2, column=3)
        newCuenta = Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=cuenta))
        newCuenta.grid(row=2, column=4)

        # old categoria
        Label(self.edit_wind, text='Categoria: ').grid(row=3, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=categoria), state='readonly').grid(row=3,
                                                                                                              column=2)

        # New categoría
        Label(self.edit_wind, text=' New Categoria: ').grid(row=3, column=3)
        newCategoria = Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=categoria))
        newCategoria.grid(row=3, column=4)

        # old SubCategoría
        Label(self.edit_wind, text='Subcategoria: ').grid(row=4, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=subcategoria), state='readonly').grid(row=4,
                                                                                                                 column=2)

        # New SubCategoría
        Label(self.edit_wind, text=' New SubCategoría: ').grid(row=4, column=3)
        newSubCategoria = Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=subcategoria))
        newSubCategoria.grid(row=4, column=4)

        # old descripcion
        Label(self.edit_wind, text='descripcion: ').grid(row=5, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=descripcion), state='readonly').grid(row=5,
                                                                                                                column=2)

        # New descripcion
        Label(self.edit_wind, text=' New descripcion: ').grid(row=5, column=3)
        newdescripcion = Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=descripcion))
        newdescripcion.grid(row=5, column=4)

        # old eur
        Label(self.edit_wind, text='Euros: ').grid(row=6, column=1)
        Entry(self.edit_wind, textvariable=DoubleVar(self.edit_wind, value=eur), state='readonly').grid(row=6, column=2)

        # New eur
        Label(self.edit_wind, text=' New Euros: ').grid(row=6, column=3)
        newEur = Entry(self.edit_wind, textvariable=DoubleVar(self.edit_wind, value=eur))
        newEur.grid(row=6, column=4)

        # old tipo
        Label(self.edit_wind, text='Tipo: ').grid(row=7, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=tipo2), state='readonly').grid(row=7,
                                                                                                          column=2)

        # New tipo
        Label(self.edit_wind, text=' New Tipo: ').grid(row=7, column=3)
        newtipo = Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=tipo2))
        newtipo.grid(row=7, column=4)

        # old Notas
        Label(self.edit_wind, text='Notas: ').grid(row=8, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=nota), state='readonly').grid(row=8,
                                                                                                         column=2)

        # New Notas
        Label(self.edit_wind, text=' New Notas: ').grid(row=8, column=3)
        newNota = Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=nota))
        newNota.grid(row=8, column=4)

        Button(self.edit_wind, text='Refresh',
               command=lambda: self.editar_registro(id, newFecha.get(), newCuenta.get(), newCategoria.get(),
                                                    newSubCategoria.get(), newdescripcion.get(), newEur.get(),
                                                    newtipo.get(), newNota.get(), tipo)).grid(row=9, columns=2,
                                                                                              sticky=W + E)

    # edit form registry in window edit
    def editar_registro(self, id, newFecha, newCuenta, newCategoria, newSubCategoria, newdescripcion, newEur, newtipo,
                        newNota, tipo):
        query = 'UPDATE pruebas SET Fecha =?, Cuenta =?,Categoria =?,Subcategoria =?,Descripcion =?,Total =?,' \
                'TipoMov =?,Notas =?  Where id=?'
        parameters = (newFecha, newCuenta, newCategoria, newSubCategoria, newdescripcion, newEur, newtipo, newNota, id)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'El Registro nº{} se ha actualizado'.format(id)
        self.getMovimiento(tipo)

    # close window
    def close_windows(self):
        self.window1.destroy()
        self.window.deiconify()
