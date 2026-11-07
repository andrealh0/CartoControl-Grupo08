import datos_cartocontrol as datos


# Consultar el historial de trazabilidad de una orden
def consultar_historial():
    print("\n--- HISTORIAL DE TRAZABILIDAD ---")

    #buscar la orden
    codigo = datos.pedir_texto("Codigo de orden: ").upper()
    orden = datos.buscar_orden(codigo)

    #verificar que la orden exista
    if orden is None:
        print("La orden no existe.")
        return

    #buscar los registros asociados con la orden
    encontrados = 0

    print("\nHISTORIAL DE LA ORDEN:", codigo)
    print("-" * 100)
    print(f"{'FECHA Y HORA':<20} | EVENTO")
    print("-" * 100)

    for registro in datos.historial:
        if registro[0] == codigo:
            print(f"{registro[1]:<20} | {registro[2]}")
            encontrados = encontrados + 1

    #informar si la orden aun no tiene movimientos registrados
    if encontrados == 0:
        print("La orden no tiene registros en el historial.")

    print("-" * 100)