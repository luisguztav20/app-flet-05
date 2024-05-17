import pandas as pd
import sympy as sp
from sympy import *
import flet as ft
# import graficador as grafico

# x = sp.symbols('x')
# cifras_sig = 3
# x1 = 0
# xu = 1
# fx = (sp.E**-x)-x


def biseccion(x1, xu, f_x, cifras_sig, lbl_resultados, resultados, page):
    
    def eval_infx(xn, fx):
        return fx.subs(x, xn)
    
    def tolerancia(cifras_sig):
        Es = 0.5 * 10 ** (2 - cifras_sig)
        return Es
    
    def headers(df : pd.DataFrame) -> list:
        return [ft.DataColumn(ft.Text(header)) for header in df.columns]

#    Función para generar las filas de la DataTable
    def rows(df : pd.DataFrame) -> list:
        rows = []
        for index, row in df.iterrows():
            rows.append(ft.DataRow(cells = [ft.DataCell(ft.Text(str(row[header]))) for header in df.columns]))
        return rows
    
    x = sp.symbols('x')
    
    fx = sp.sympify(f_x)
    
    Es = tolerancia(cifras_sig)
    
    iteracion = 1
    aprox_anterior = 0
    aprox_actual = 0
    # def f(x):
    #     return (( e**-x)-x) 
    df = pd.DataFrame(columns=["Iteracion", "x1", "xu", "xr", "f(x1)", "f(xu)", "f(xr)", "f(x1)*f(xr)", "Condicion", "Error Aproximado"])

    #print('Intervalo [', x1,',',xu,']')

    while True:

        xr = (x1 + xu)/ 2
        fx1 = eval_infx(x1, fx)
        fxu = eval_infx(xu, fx)
        fxr = eval_infx(xr, fx)
        producto = fx1*fxr

        if producto < 0:
            condicon = '< 0'
        else:
            condicon = '> 0'
        Ea = abs(((xr - aprox_anterior)/xr)*100)
        df.loc[iteracion-1] = [iteracion, x1, xu, xr, fx1, fxu, fxr, producto, condicon,  Ea]
    
        if producto < 0:
            xu = xr
        elif producto > 0:
            x1 = xr
        else:
            break
        if Ea < Es:
            break
        
        aprox_anterior = xr
        iteracion += 1 
    
    lbl_resultados.value = f"La Raiz es: {xr} \nCon un error de: {Ea}% \nCon {iteracion} iteraciones"
    resultados.visible = True
    # grafico.graficar(fx, page)
    
    tbl_dataTable = ft.DataTable(
        columns=headers(df),
        rows=rows(df)
    )
    
    
    tbl = ft.Row(
            [
                ft.Container(
                    #width=500,
                    #bgcolor='#565656',  #ft.colors.BLUE_100,
                    border_radius=ft.border_radius.all(20),
                    padding=20,
                    content=ft.Row(
                        [
                        tbl_dataTable
                        ]
                        
                    ),
                )   
            ], 
            scroll=ft.ScrollMode.ALWAYS #Permite el scroll
        
    )
    
    listview = ft.ListView(expand=1, auto_scroll=True )
    listview.controls.append(tbl)
    page.add(listview)
    
    
    page.update()
    