import datetime

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
                {'IngresoTrabajo': ['Abono de nómina']
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
