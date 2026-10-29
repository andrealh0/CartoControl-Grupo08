import datos_cartocontrol as datos

#registrar y verificar la aprobación del arte de una orden
def registrar_verificar_arte():
    print("\n--- REGISTRAR Y VERIFICAR APROBACION DEL ARTE ---")

    codigo = datos.pedir_texto("Codigo de orden: ").upper()
    orden = datos.buscar_orden(codigo)

    #verificar que la orden exista
    if orden is None:
        print("La orden no existe.")
        return

    #registrar los datos de la aprobación del arte
    version = datos.pedir_texto("Ingrese la version del arte o cliche: ")
    aprobado = datos.pedir_si_no("¿El arte esta aprobado? (si/no): ")
    responsable = datos.pedir_texto("Ingrese el responsable de la revision: ").title()
    fecha = datos.fecha_hora_actual()

    #actualizar el estado de aprobación del arte
    orden[13] = aprobado

    #guardar los detalles de la revisión del arte
    datos.agregar_registro_extra(
        "APROBACION_ARTE",
        codigo,
        [version, aprobado, responsable, fecha]
    )

    #istrar la aprobación del arte en el historial
    descripcion = "Arte version " + version + ". Aprobado: " + aprobado
    descripcion = descripcion + ". Responsable: " + responsable

    datos.registrar_historial(codigo, descripcion)

    #mostrar el resultado de la revisión
    if aprobado == "si":
        print("Arte aprobado. La orden puede continuar.")
    else:
        print("Arte no aprobado. La orden queda pendiente.")
