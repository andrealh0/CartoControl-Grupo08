import time
from pathlib import Path

import pandas as pd

# Para saber que dato es cada posicion de una orden:
# 0 codigo, 1 cliente, 2 producto, 3 cantidad, 4 entrega, 5 pedido aprobado,
# 6 etapa, 7 estado, 8 prioridad, 9 material, 10 cantidad de material,
# 11 dia planificado, 12 turno, 13 arte aprobado, 14 resultado de calidad,
# 15 identificacion, 16 autorizacion de entrega parcial.
ordenes = []

materiales = []
reservas = []
movimientos = []
producciones = []
historial = []
registros_extra = []

carpeta_datos = Path(__file__).resolve().parent

tablas_csv = [
    ("ordenes.csv", ["codigo", "cliente", "producto", "cantidad_solicitada",
                     "fecha_entrega", "pedido_aprobado", "etapa", "estado",
                     "prioridad", "material", "cantidad_material", "dia_planificado",
                     "turno", "arte_aprobado", "resultado_calidad", "identificacion",
                     "autorizacion_parcial"], ordenes),
    ("materiales.csv", ["codigo", "descripcion", "existencia_fisica"], materiales),
    ("reservas.csv", ["orden", "material", "cantidad"], reservas),
    ("movimientos.csv", ["material", "cantidad", "origen", "destino",
                          "autoriza_planificacion", "autoriza_bodega", "fecha_hora"], movimientos),
    ("producciones.csv", ["orden", "inicio", "fin", "buena", "rechazada",
                           "prueba", "motivo_paro", "responsable", "fecha_hora"], producciones),
    ("historial.csv", ["orden", "fecha_hora", "descripcion"], historial),
    ("registros_extra.csv", ["tipo", "orden"] +
     ["dato_" + str(i) for i in range(1, 21)], registros_extra)
]


def pedir_texto(mensaje):
    dato = input(mensaje).strip()
    while dato == "":
        print("Debe ingresar un dato.")
        dato = input(mensaje).strip()
    return dato


def solo_numeros(dato):
    if dato == "":
        return False
    for caracter in dato:
        if caracter < "0" or caracter > "9":
            return False
    return True


def pedir_cantidad(mensaje):
    while True:
        dato = input(mensaje).strip()
        if solo_numeros(dato):
            return int(dato)
        print("Debe ingresar un numero entero no negativo.")


def pedir_positivo(mensaje):
    cantidad = pedir_cantidad(mensaje)
    while cantidad == 0:
        print("La cantidad debe ser mayor que cero.")
        cantidad = pedir_cantidad(mensaje)
    return cantidad


def pedir_si_no(mensaje):
    dato = pedir_texto(mensaje).lower()
    while dato != "si" and dato != "no":
        print("Escriba si o no.")
        dato = pedir_texto(mensaje).lower()
    return dato


def pedir_fecha(mensaje):
    fecha = pedir_texto(mensaje)
    correcta = False
    while not correcta:
        if len(fecha) == 10 and fecha[2] == "/" and fecha[5] == "/":
            numeros = fecha[0:2] + fecha[3:5] + fecha[6:10]
            if solo_numeros(numeros):
                dia = int(fecha[0:2])
                mes = int(fecha[3:5])
                anio = int(fecha[6:10])
                if anio > 0 and mes >= 1 and mes <= 12:
                    dias = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                    if mes == 2 and anio % 4 == 0:
                        if anio % 100 != 0 or anio % 400 == 0:
                            dias[1] = 29
                    if dia >= 1 and dia <= dias[mes - 1]:
                        correcta = True
        if not correcta:
            print("Fecha invalida. Use DD/MM/AAAA, por ejemplo 25/10/2026.")
            fecha = pedir_texto(mensaje)
    return fecha


def pedir_hora(mensaje):
    while True:
        hora = pedir_texto(mensaje)
        if len(hora) == 5 and hora[2] == ":":
            numeros = hora[0:2] + hora[3:5]
            if solo_numeros(numeros):
                if int(hora[0:2]) <= 23 and int(hora[3:5]) <= 59:
                    return hora
        print("Ingrese una hora valida en formato HH:MM. Ejemplo: 08:00.")


def fecha_hora_actual():
    return time.strftime("%d/%m/%Y %H:%M")


def buscar_orden(codigo):
    for orden in ordenes:
        if orden[0] == codigo:
            return orden
    return None


def buscar_material(codigo):
    for material in materiales:
        if material[0] == codigo:
            return material
    return None


def buscar_reserva(codigo_orden, codigo_material):
    for reserva in reservas:
        if reserva[0] == codigo_orden and reserva[1] == codigo_material:
            return reserva
    return None


def total_reservado(codigo_material):
    total = 0
    for reserva in reservas:
        if reserva[1] == codigo_material:
            total = total + int(reserva[2])
    return total


def registrar_historial(codigo, descripcion):
    historial.append([codigo, fecha_hora_actual(), descripcion])
    guardar_datos()


def agregar_registro_extra(tipo, codigo, datos):
    registro = [tipo, codigo]
    for dato in datos:
        registro.append(str(dato))
    registros_extra.append(registro)
    guardar_datos()


def guardar_datos():
    for nombre, columnas, filas in tablas_csv:
        filas_csv = []
        for fila in filas:
            if len(fila) > len(columnas):
                raise ValueError("Hay demasiados datos para " + nombre)
            fila_csv = []
            for dato in fila:
                fila_csv.append(str(dato))
            while len(fila_csv) < len(columnas):
                fila_csv.append("")
            filas_csv.append(fila_csv)
        tabla = pd.DataFrame(filas_csv, columns=columnas)
        tabla.to_csv(carpeta_datos / nombre, index=False, encoding="utf-8")


def cargar_datos():
    for nombre, columnas, filas in tablas_csv:
        archivo = carpeta_datos / nombre
        if archivo.exists():
            tabla = pd.read_csv(archivo, dtype=str, keep_default_na=False,
                                encoding="utf-8")
            if list(tabla.columns) != columnas:
                raise ValueError("Las columnas no coinciden en " + nombre)
            for fila_csv in tabla.itertuples(index=False, name=None):
                fila = []
                for dato in fila_csv:
                    fila.append(str(dato))
                if nombre == "registros_extra.csv":
                    while len(fila) > 2 and fila[-1] == "":
                        fila.pop()
                filas.append(fila)


cargar_datos()