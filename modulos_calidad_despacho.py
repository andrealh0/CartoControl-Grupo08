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

#registrar inspecciones y resultados de calidad
def registrar_inspeccion_calidad():
    print("\n--- REGISTRAR INSPECCION Y RESULTADO DE CALIDAD ---")

    #buscar la orden que sera inspeccionada
    codigo = datos.pedir_texto("Codigo de orden: ").upper()
    orden = datos.buscar_orden(codigo)

    #verificar que la orden exista
    if orden is None:
        print("La orden no existe.")
        return

    #verificar que el arte de la orden este aprobado
    if orden[13] != "si":
        print("El arte de la orden aun no esta aprobado.")
        return

    #registrar los datos de la inspeccion
    cant_inspeccionada = datos.pedir_positivo(
        "Ingrese la cantidad inspeccionada: "
    )

    defectos = datos.pedir_texto(
        "Ingrese los defectos encontrados o 'Ninguno': "
    )

    cant_afectada = datos.pedir_cantidad(
        "Ingrese la cantidad afectada: "
    )

    #validar que la cantidad afectada no supere la inspeccionada
    while cant_afectada > cant_inspeccionada:
        print("La cantidad afectada no puede ser mayor que la inspeccionada.")
        cant_afectada = datos.pedir_cantidad(
            "Ingrese nuevamente la cantidad afectada: "
        )

    #registrar la decision de calidad
    print("1. Aprobado")
    print("2. Rechazado")
    print("3. Necesita correccion")

    decision = input("Seleccione el resultado de calidad: ").strip()

    while decision != "1" and decision != "2" and decision != "3":
        print("Opcion invalida. Seleccione 1, 2 o 3.")
        decision = input("Seleccione el resultado de calidad: ").strip()

    if decision == "1":
        resultado = "Aprobado"
    elif decision == "2":
        resultado = "Rechazado"
    else:
        resultado = "Necesita correccion"

    #registrar responsable y fecha de la inspeccion
    responsable = datos.pedir_texto(
        "Ingrese el responsable de la inspeccion: "
    ).title()

    fecha = datos.fecha_hora_actual()

    #actualizar el resultado actual de calidad de la orden
    orden[14] = resultado

    #guardar los detalles de la inspeccion
    datos.agregar_registro_extra(
        "INSPECCION_CALIDAD",
        codigo,
        [
            cant_inspeccionada,
            defectos,
            cant_afectada,
            resultado,
            responsable,
            fecha
        ]
    )

    #registrar la inspeccion en el historial
    descripcion = "Inspeccion de calidad. Resultado: " + resultado
    descripcion = descripcion + ". Inspeccionadas: " + str(cant_inspeccionada)
    descripcion = descripcion + ". Afectadas: " + str(cant_afectada)
    descripcion = descripcion + ". Defectos: " + defectos
    descripcion = descripcion + ". Responsable: " + responsable

    datos.registrar_historial(codigo, descripcion)

    #mostrar el resultado
    print("Inspeccion de calidad registrada correctamente.")
    print("Resultado:", resultado)
    print("Fecha y hora:", fecha)

#generar y registrar la identificacion del producto
def generar_identificacion_producto():
    print("\n--- GENERAR Y REGISTRAR IDENTIFICACION DEL PRODUCTO ---")

    #buscar la orden
    codigo = datos.pedir_texto("Codigo de orden: ").upper()
    orden = datos.buscar_orden(codigo)

    #verificar que la orden exista
    if orden is None:
        print("La orden no existe.")
        return

    #verificar que el producto haya sido aprobado por calidad
    if orden[14] != "Aprobado":
        print("El producto aun no cuenta con aprobacion de calidad.")
        print("Resultado actual:", orden[14])
        return

    #registrar los datos de identificacion
    num_lote = 1
    for registro in datos.registros_extra:
        if registro[0] == "IDENTIFICACION_PRODUCTO" and registro[1] == codigo:
            num_lote = num_lote + 1

    lote = codigo + "-L" + str(num_lote).zfill(2)

    cantidad = datos.pedir_positivo("Ingrese la cantidad a identificar: ")
    print("1. Producto terminado")
    print("2. Muestra")
    print("3. Prueba")

    op_clasificacion = input(
        "Seleccione la clasificacion del producto: "
    ).strip()

    while (op_clasificacion != "1"
        and op_clasificacion != "2"
        and op_clasificacion != "3"):
        print("Opcion invalida. Seleccione 1, 2 o 3.")
        op_clasificacion = input(
            "Seleccione la clasificacion del producto: "
        ).strip()

    if op_clasificacion == "1":
        clasificacion = "Producto terminado"
    elif op_clasificacion == "2":
        clasificacion = "Muestra"
    else:
        clasificacion = "Prueba"

    #bbtener el estado de calidad ya registrado
    estado_calidad = orden[14]
    fecha = datos.fecha_hora_actual()

    #generar la etiqueta de identificacion
    etiqueta = (
        "Orden: " + codigo
        + " | Lote: " + lote
        + " | Cantidad: " + str(cantidad)
        + " | Clasificacion: " + clasificacion
        + " | Calidad: " + estado_calidad
    )

    #guardar la identificacion actual de la orden
    orden[15] = etiqueta

    #guardar los detalles de la identificacion
    datos.agregar_registro_extra(
        "IDENTIFICACION_PRODUCTO",
        codigo,
        [
            lote,
            cantidad,
            clasificacion,
            estado_calidad,
            fecha
        ]
    )

    #registrar la identificacion en el historial
    descripcion = "Identificacion generada. Lote: " + lote
    descripcion = descripcion + ". Cantidad: " + str(cantidad)
    descripcion = descripcion + ". Clasificacion: " + clasificacion
    descripcion = descripcion + ". Calidad: " + estado_calidad

    datos.registrar_historial(codigo, descripcion)

    #mostrar la etiqueta generada
    print("\n========================================")
    print("IDENTIFICACION DEL PRODUCTO")
    print("========================================")
    print("Orden:", codigo)
    print("Lote:", lote)
    print("Cantidad:", cantidad)
    print("Clasificacion:", clasificacion)
    print("Estado de calidad:", estado_calidad)
    print("========================================")
    print("Identificacion registrada correctamente.")

