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
    responsable = datos.pedir_texto(
        "Ingrese el responsable de la revision: "
    ).title()
    fecha = datos.fecha_hora_actual()

    #actualizar el estado de aprobación del arte
    orden[13] = aprobado

    #guardar los detalles de la revisión del arte
    datos.agregar_registro_extra(
        "APROBACION_ARTE",
        codigo,
        [version, aprobado, responsable, fecha]
    )

    #registrar la aprobación del arte en el historial
    descripcion = "Arte version " + version + ". Aprobado: " + aprobado
    descripcion = descripcion + ". Responsable: " + responsable

    datos.registrar_historial(codigo, descripcion)

    #mostrar el resultado de la revisión
    if aprobado == "si":
        print("Arte aprobado correctamente.")
    else:
        print("Arte no aprobado. La orden queda pendiente.")


#calcular la cantidad buena registrada en produccion
def total_produccion_buena(codigo):
    total = 0

    for produccion in datos.producciones:
        if produccion[0] == codigo:
            total = total + int(produccion[3])

    return total


#calcular las unidades que ya tienen una decision final de calidad
def total_calidad_finalizada(codigo):
    total = 0

    for registro in datos.registros_extra:
        if registro[0] == "INSPECCION_CALIDAD" and registro[1] == codigo:
            resultado = registro[5]

            if resultado == "Aprobado" or resultado == "Rechazado":
                total = total + int(registro[2])

    return total


#calcular las unidades aprobadas por calidad
def total_calidad_aprobada(codigo):
    total = 0

    for registro in datos.registros_extra:
        if registro[0] == "INSPECCION_CALIDAD" and registro[1] == codigo:
            if registro[5] == "Aprobado":
                total = total + int(registro[2])

    return total


#calcular las unidades que ya fueron identificadas
def total_identificado(codigo, clasificacion=""):
    total = 0

    for registro in datos.registros_extra:
        if registro[0] == "IDENTIFICACION_PRODUCTO" and registro[1] == codigo:
            if clasificacion == "" or registro[4] == clasificacion:
                total = total + int(registro[3])

    return total


#calcular las unidades que ya fueron preparadas para despacho
def total_preparado_despacho(codigo):
    total = 0

    for registro in datos.registros_extra:
        if registro[0] == "PREPARACION_DESPACHO" and registro[1] == codigo:
            total = total + int(registro[2])

    return total


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

    #verificar que el pedido este aprobado
    if orden[5] != "si":
        print("El pedido de la orden aun no esta aprobado.")
        return

    #verificar que el arte de la orden este aprobado
    if orden[13] != "si":
        print("El arte de la orden aun no esta aprobado.")
        return

    #verificar que exista produccion registrada
    produccion_buena = total_produccion_buena(codigo)

    if produccion_buena <= 0:
        print("La orden aun no tiene unidades buenas registradas en produccion.")
        return

    #calcular las unidades disponibles para inspeccion
    calidad_finalizada = total_calidad_finalizada(codigo)
    disponible_inspeccion = produccion_buena - calidad_finalizada

    print("Cantidad buena registrada en produccion:", produccion_buena)
    print("Cantidad con resultado final de calidad:", calidad_finalizada)
    print("Cantidad disponible para inspeccionar:", disponible_inspeccion)

    if disponible_inspeccion <= 0:
        print("No hay unidades pendientes de inspeccion.")
        return

    #registrar los datos de la inspeccion
    cant_inspeccionada = datos.pedir_positivo(
        "Ingrese la cantidad inspeccionada: "
    )

    while cant_inspeccionada > disponible_inspeccion:
        print("La cantidad inspeccionada no puede superar las unidades disponibles.")
        cant_inspeccionada = datos.pedir_positivo(
            "Ingrese nuevamente la cantidad inspeccionada: "
        )

    defectos = datos.pedir_texto(
        "Ingrese el defecto encontrado o 'Ninguno': "
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

    #validar la relacion entre defecto y cantidad afectada
    while defectos.strip().lower() == "ninguno" and cant_afectada > 0:
        print("Si hay unidades afectadas, debe indicar el defecto encontrado.")
        defectos = datos.pedir_texto(
            "Ingrese el defecto encontrado: "
        )

    while defectos.strip().lower() != "ninguno" and cant_afectada == 0:
        print("Si se encontro un defecto, debe indicar cuantas unidades fueron afectadas.")
        cant_afectada = datos.pedir_cantidad(
            "Ingrese nuevamente la cantidad afectada: "
        )

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
        decision = input(
            "Seleccione el resultado de calidad: "
        ).strip()

    if decision == "1":
        resultado = "Aprobado"
    elif decision == "2":
        resultado = "Rechazado"
    else:
        resultado = "Necesita correccion"

    #validar que un producto aprobado no tenga unidades afectadas
    if resultado == "Aprobado" and cant_afectada > 0:
        print("No puede aprobarse una inspeccion que tiene unidades afectadas.")
        print("Registre el resultado como Rechazado o Necesita correccion.")
        return

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
    descripcion = descripcion + ". Defecto: " + defectos
    descripcion = descripcion + ". Responsable: " + responsable

    datos.registrar_historial(codigo, descripcion)

    #mostrar el resultado
    print("Inspeccion de calidad registrada correctamente.")
    print("Resultado:", resultado)

    if resultado == "Necesita correccion":
        print("Las unidades pueden corregirse y volver a inspeccionarse.")

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

    #verificar que existan unidades aprobadas por calidad
    cantidad_aprobada = total_calidad_aprobada(codigo)
    cantidad_identificada = total_identificado(codigo)
    cantidad_disponible = cantidad_aprobada - cantidad_identificada

    if cantidad_aprobada <= 0:
        print("El producto aun no cuenta con unidades aprobadas por calidad.")
        print("Resultado actual:", orden[14])
        return

    if cantidad_disponible <= 0:
        print("Todas las unidades aprobadas ya fueron identificadas.")
        return

    print("Cantidad aprobada por calidad:", cantidad_aprobada)
    print("Cantidad ya identificada:", cantidad_identificada)
    print("Cantidad disponible para identificar:", cantidad_disponible)

    #registrar los datos de identificacion
    num_lote = 1

    for registro in datos.registros_extra:
        if registro[0] == "IDENTIFICACION_PRODUCTO" and registro[1] == codigo:
            num_lote = num_lote + 1

    lote = codigo + "-L" + str(num_lote).zfill(2)

    cantidad = datos.pedir_positivo(
        "Ingrese la cantidad a identificar: "
    )

    while cantidad > cantidad_disponible:
        print("La cantidad excede las unidades aprobadas disponibles.")
        cantidad = datos.pedir_positivo(
            "Ingrese nuevamente la cantidad a identificar: "
        )

    print("1. Producto terminado")
    print("2. Muestra")
    print("3. Prueba")

    op_clasificacion = input(
        "Seleccione la clasificacion del producto: "
    ).strip()

    while (
        op_clasificacion != "1"
        and op_clasificacion != "2"
        and op_clasificacion != "3"
    ):
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

    #obtener el estado de calidad ya registrado
    estado_calidad = "Aprobado"
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


#validar y preparar una orden para despacho
def validar_preparar_despacho():
    print("\n--- VALIDAR Y PREPARAR ORDEN PARA DESPACHO ---")

    #buscar la orden
    codigo = datos.pedir_texto("Codigo de orden: ").upper()
    orden = datos.buscar_orden(codigo)

    #verificar que la orden exista
    if orden is None:
        print("La orden no existe.")
        return

    #verificar que exista producto terminado identificado
    cantidad_identificada = total_identificado(
        codigo,
        "Producto terminado"
    )

    if cantidad_identificada <= 0:
        print("No hay producto terminado identificado para preparar para despacho.")
        return

    #calcular cuanto producto ya fue preparado para despacho
    cantidad_despachada = total_preparado_despacho(codigo)

    #calcular la cantidad que todavia queda disponible
    cantidad_pendiente = cantidad_identificada - cantidad_despachada

    print("Cantidad solicitada:", orden[3])
    print("Producto terminado identificado:", cantidad_identificada)
    print("Cantidad ya preparada para despacho:", cantidad_despachada)
    print("Cantidad disponible para preparar:", cantidad_pendiente)

    #verificar si ya se preparo todo lo identificado
    if cantidad_pendiente <= 0:
        print("Todo el producto terminado identificado ya fue preparado para despacho.")
        return

    #pedir la cantidad que se desea despachar
    cantidad_despacho = datos.pedir_positivo(
        "Ingrese la cantidad que se desea despachar: "
    )

    #validar que no se prepare mas de la cantidad pendiente
    while cantidad_despacho > cantidad_pendiente:
        print("La cantidad excede el producto identificado disponible.")
        cantidad_despacho = datos.pedir_positivo(
            "Ingrese nuevamente la cantidad que se desea preparar: "
        )

    #verificar si se trata de una entrega parcial
    cantidad_solicitada = int(orden[3])
    total_preparado_despues = cantidad_despachada + cantidad_despacho

    if total_preparado_despues < cantidad_solicitada:
        print("La cantidad corresponde a una preparacion parcial para despacho.")

        autorizada = datos.pedir_si_no(
            "¿La entrega parcial esta autorizada? (si/no): "
        )

        if autorizada == "no":
            print("La orden no puede prepararse para despacho sin autorizacion.")
            return

        autorizador = datos.pedir_texto(
            "Ingrese el nombre de quien autorizo la entrega parcial: "
        ).title()

        orden[16] = "si"

        datos.agregar_registro_extra(
            "AUTORIZACION_PARCIAL",
            codigo,
            [
                cantidad_despacho,
                autorizador,
                datos.fecha_hora_actual()
            ]
        )

    #registrar la preparacion para despacho
    responsable = datos.pedir_texto(
        "Ingrese el responsable de preparar el despacho: "
    ).title()

    fecha = datos.fecha_hora_actual()

    datos.agregar_registro_extra(
        "PREPARACION_DESPACHO",
        codigo,
        [
            cantidad_despacho,
            responsable,
            fecha
        ]
    )

    #registrar el evento en el historial
    descripcion = "Orden preparada para despacho. Cantidad: "
    descripcion = descripcion + str(cantidad_despacho)
    descripcion = descripcion + ". Responsable: " + responsable

    datos.registrar_historial(codigo, descripcion)

    #actualizar la etapa y estado de la orden
    orden[6] = "Despacho"
    total_preparado = cantidad_despachada + cantidad_despacho

    if total_preparado >= cantidad_solicitada:
        orden[7] = "Terminada"
    else:
        orden[7] = "En Proceso"

    datos.guardar_datos()

    print("La orden cumple los requisitos y esta lista para despacho.")
    print("Cantidad preparada:", cantidad_despacho)
    print("Fecha y hora:", fecha)


#submenu del modulo de aprobaciones y control de calidad
def menu_calidad():
    opcion = ""

    while opcion != "3":
        print("\nAPROBACIONES Y CONTROL DE CALIDAD")
        print("1. Registrar y verificar aprobacion del arte")
        print("2. Registrar inspecciones y resultados de calidad")
        print("3. Regresar al menu principal")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            registrar_verificar_arte()

        elif opcion == "2":
            registrar_inspeccion_calidad()

        elif opcion != "3":
            print("Opcion invalida. Intente nuevamente.")


#submenu del modulo de identificacion y preparacion para despacho
def menu_despacho():
    opcion = ""

    while opcion != "3":
        print("\nIDENTIFICACION Y PREPARACION PARA DESPACHO")
        print("1. Generar y registrar identificacion del producto")
        print("2. Validar y preparar una orden para despacho")
        print("3. Regresar al menu principal")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            generar_identificacion_producto()

        elif opcion == "2":
            validar_preparar_despacho()

        elif opcion != "3":
            print("Opcion invalida. Intente nuevamente.")