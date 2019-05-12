import datetime
import sqlite3
import pandas as pd
from resources import base_paths

params = {

    'categoria':
        {
            'Gasto':
                {'fuera': ['La tagliatella', 'Pol ind montaæa blanca ca', 'Amaki', 'El hipopotamo',
                           'Bululu', 'Burger king la ballena', 'El dorado las canteras', 'Vaqueria las salinas',
                           'Nyc taxi bar', 'Restaurante nomiya',
                           'Telepizza', 'Mcdonalds nuevo barajas', 'Www.just-eat.es', 'El travieso',
                           'Natural burguer triana', 'Bar tiramisu', 'Mumbai sunset bar', 'El dorado las canteras',
                           'Naturalis']
                    , 'entrenenimiento': ['Monopol', 'Yelmo cines alisios']
                    , 'transporte': ['Anastor las palmas - ceps', 'Cedipsa 77189-1 es sical', 'Dosjotas 2010',
                                     'Cedipsa 77371-1 aeropuert', 'Estacion el goro', 'Estacion bp guanarteme',
                                     'Cepsa tinoca']
                    , 'parking': ['Aparcamientos el rincon']
                    , 'cortepelo': ['Peluqueria aleman']
                    , 'deporte': ['Adeudo macrofit las palmas']
                    , 'orange': ['Adeudo orange-france telecom']
                    ,
                 'tabaco': ['Bazar calle mayor', 'Estanco baza', 'Bazar calle', 'Bazar itaca', 'Tabaqueria bazar itaca']
                 },

            'Ingreso':
                {'salario W': ['Abono de nómina']
                 },
            'Traspaso':
                {'bbva ahorro': ['Traspaso a cuenta'],
                 'casa': ['Hbo*espana', 'Adeudo telefonica de espana, s.a.u.', 'Hiperdino triana'],
                 'cartera': ['Disposicion de efectivo en cajero servired'],
                 'bbva': ['Traspaso desde cuenta', ]
                 }
        },
    'cuenta':
        {'bbva ahorro': ['Rescate'],
         'casa': ['Hbo', 'Hiper', 'Movistar', 'Hipr']

         }
}

yet = str(datetime.datetime.now().date().strftime('%d/%m/%Y'))
yet2 = datetime.datetime.now().date().strftime('%d/%m/%Y , %H:%M:%S')


class SqlSentence:
    create_fact_table = """
        CREATE TABLE IF NOT EXISTS facts_table (
                id integer PRIMARY KEY,
                fecha text,
                cuenta text,
                categoria text,
                subcategoria text,
                descripcion text,
                eur text,
                tipo text,
                nota text
                );"""

    create_prueba_table = """
        CREATE TABLE IF NOT EXISTS pruebas (
                id integer PRIMARY KEY,
                fecha text,
                cuenta text,
                categoria text,
                subcategoria text,
                descripcion text,
                total text,
                tipomov text,
                notas text,
                insertupdate text
                );
        """
    select_fact = """SELECT * FROM facts_table"""
    select_pruebas = """
    SELECT id , fecha , cuenta , categoria , subcategoria, descripcion, total, tipomov, notas FROM pruebas 
    WHERE tipomov='{0}' ORDER BY insertupdate DESC
    """
    lista_cuentas_ordenadas="""SELECT cuenta FROM
                  (SELECT  cuenta ,count(cuenta) as  freq
                  FROM facts_table
                  GROUP BY cuenta
                  order by count(cuenta) desc) as T1"""

class Services:

    def run_query(self):
        db=base_paths.db_file
        cnx = sqlite3.connect(db)
        return cnx

    def close_conn(self,cnx):
        return cnx.commit()

    #Cuando interesa retornar un datos para reporting o para tratarlos
    def get_query(self,query):
        cnx=self.run_query()
        data = pd.read_sql_query(query, cnx)
        self.close_conn(cnx)
        return data

    # Cuando se va a hacer un insert,update,o getmovimientos
    def run_query2(self, query, parameters=()):
        db=base_paths.db_file
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
            return result


class Validador():
    def __init__(self,s):
       self.val_num = self.is_number(s)
       self.val_empty=self.isnot_empty(s)

    def is_number(self,s):
       try:
           float(s)
           return True
       except ValueError:
           return False

    def isnot_empty(self,s):
        if s =='':
            return False
        else:
            return True