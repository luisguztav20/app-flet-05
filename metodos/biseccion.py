import sympy as sp
import flet as ft

def biseccion(x1, xu, f_x, cifras_sig, lbl_resultados, resultados, page):
    
    def eval_infx(xn, fx):
        return fx.subs(x, xn)
    
    def tolerancia(cifras_sig):
        Es = 0.5 * 10 ** (2 - cifras_sig)
        return Es
    
    def headers(columns):
        return [ft.DataColumn(ft.Text(header)) for header in columns]

    def rows(data):
        rows = []
        for row in data:
            cells = [ft.DataCell(ft.Text(str(cell))) for cell in row]
            rows.append(ft.DataRow(cells=cells))
        return rows
    
    x = sp.symbols('x')
    
    fx = sp.sympify(f_x)
    
    Es = tolerancia(cifras_sig)
    
    iteracion = 1
    aprox_anterior = 0
    aprox_actual = 0
    
    data = []
    while True:
        xr = (x1 + xu)/ 2
        fx1 = eval_infx(x1, fx)
        fxu = eval_infx(xu, fx)
        fxr = eval_infx(xr, fx)
        producto = fx1 * fxr

        if producto < 0:
            condicon = '< 0'
        else:
            condicon = '> 0'
        Ea = abs(((xr - aprox_anterior)/xr)*100)
        
        data.append([iteracion, x1, xu, xr, fx1, fxu, fxr, producto, condicon, Ea])
        
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
    
    tbl_dataTable = ft.DataTable(
        columns=headers(["Iteracion", "x1", "xu", "xr", "f(x1)", "f(xu)", "f(xr)", "f(x1)*f(xr)", "Condicion", "Error Aproximado"]),
        rows=rows(data)
    )
    
    tbl = ft.Row(
        [
            ft.Container(
                border_radius=ft.border_radius.all(20),
                padding=20,
                content=ft.Row([tbl_dataTable])
            )
        ], 
        scroll=ft.ScrollMode.ALWAYS
    )
    
    listview = ft.ListView(expand=1, auto_scroll=True)
    listview.controls.append(tbl)
    page.add(listview)
    page.update()
