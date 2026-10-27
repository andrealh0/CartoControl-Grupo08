import modulo_completoProyecto

#INICIO SUBMENU 1
def submenu_gestion_planificacion():
    opPlan = 0

    while opPlan != 4:
        print("\nGestión y planificación de órdenes")
        print("1. Registrar y actualizar una orden de producción")
        print("2. Organizar la secuencia diaria de producción")
        print("3. Registrar cambios de prioridad")
        print("4. Regresar al menú principal")

        try:
            opPlan = int(input("Ingrese una opción: "))
        except ValueError:
            opPlan = 0

        if opPlan >= 1 and opPlan <= 4:
            if opPlan == 1:
                # Registrar y actualizar una orden de producción
                print("Funcionalidad pendiente de implementación")

            elif opPlan == 2:
                # Organizar la secuencia diaria de producción
                print("Funcionalidad pendiente de implementación")

            elif opPlan == 3:
                # Registrar cambios de prioridad
                print("Funcionalidad pendiente de implementación")        

            # si es 4, el ciclo termina

        else:
            print("Opción invalida. Intente nuevamente.")

#FIN SUBMENU 1

#INICIO SUBMENU 2
def submenu_control_materia_prima():
    opMat = 0 

    while opMat != 3:
        print("\nCONTROL DE MATERIA PRIMA")
        print("1. Consultar y reservar materia prima")
        print("2. Registrar movimientos de material entre órdenes")
        print("3. Regresar al menú principal")

        try:
            opMat = int(input("Ingrese una opción: "))
        except ValueError:
            opMat = 0

        if opMat >= 1 and opMat <= 3:
            if opMat == 1:
                # Consultar y reservar materia prima
                print("Funcionalidad pendiente de implementación")

            elif opMat == 2:
                # Registrar movimientos de material entre órdenes
                print("Funcionalidad pendiente de implementación")        

            # si es 3, el ciclo termina
        
        else:
            print("Opción invalida. Intente nuevamente.")         
#FIN SUBMENU 2

#INICIO SUBMENU 3
def submenu_seguimiento_produccion():
    opProd = 0

    while opProd != 3:
        print("\nSEGUIMIENTO DE PRODUCCIÓN")
        print("1. Actualizar etapa y estado de una orden")
        print("2. Registrar producción, rechazos y paros")
        print("3. Regresar al menú principal")

        try:
            opProd = int(input("Ingrese una opción: "))
        except ValueError:
            opProd = 0

        if opProd >= 1 and opProd <= 3:
            if opProd == 1:
                modulo_completoProyecto.actualizar_etapa_estado()

            elif opProd == 2:
                modulo_completoProyecto.registrar_produccion_rechazos_paros()  
        else: 
            print("opción invalida. Intente de nuevamente")              

            # si es 3, el ciclo termina    
#FIN SUBMENU 3

#INICIO SUBMENU 4
def submenu_aprobaciones_control_calidad():
    opCal = 0

    while opCal != 3:
        print("\nAPROBACIONES Y CONTROL DE CALIDAD")
        print("1. Registrar y verificar aprobación del arte")
        print("2. Registrar inspecciones y resultados de calidad")
        print("3. Regresar al menú principal")

        try:
            opCal = int(input("Ingrese una opción: "))
        except ValueError:
            opCal = 0

        if opCal >= 1 and opCal <= 3:
            if opCal == 1:
                # Registrar y verificar aprobación del arte
                print("Funcionalidad pendiente de implementación")

            elif opCal == 2:
                # Registrar inspecciones y resultados de calidad
                print("Funcionalidad pendiente de implementación") 


            # si es 3, el ciclo termina
        else:
            print("Opción inválida. Intente nuevamente.")    
#FIN SUBMENU 4

#INICIO SUBMENU 5
def submenu_identificacion_despacho():
    opDesp = 0

    while opDesp != 3:
        print("\nIDENTIFICACIÓN Y PREPARACIÓN PARA DESPACHO")
        print("1. Generar y registrar identificación del producto")
        print("2. Validar y preparar una orden para despacho")
        print("3. Regresar al menú principal")

        try:
            opDesp = int(input("Ingrese una opción: "))
        except ValueError:
            opDesp = 0

        if opDesp >= 1 and opDesp <= 3:
            if opDesp == 1:
                # Generar y registrar identificación del producto
                print("Funcionalidad pendiente de implementación")

            elif opDesp == 2:
                # Validar y preparar una orden para despacho
                print("Funcionalidad pendiente de implementación")

            # si es 3, el ciclo termina  
        else:
            print("Opción inválida. Intente nuevamente.")              
#FIN SUBMENU 5           

#cargar datos iniciales de ordenes y materiales

opcion = 0

while opcion != 7:
    print("\nCARTOCONTROL")
    print("1. Gestión y planificación de órdenes")
    print("2. Control de materia prima")
    print("3. Seguimiento de producción")
    print("4. Aprobaciones y control de calidad")
    print("5. Identificación y preparación para despacho")
    print("6. Historial de trazabilidad")
    print("7. Salir")

    try:
        opcion = int(input("Ingrese una opción: "))
    except ValueError:
        opcion = 0

    if opcion >= 1 and opcion <= 7:
        if opcion == 1:
            submenu_gestion_planificacion()

        elif opcion == 2:
            submenu_control_materia_prima()

        elif opcion == 3:
            submenu_seguimiento_produccion()

        elif opcion == 4:
            submenu_aprobaciones_control_calidad()

        elif opcion == 5:
            # Aquí se llamará al submenú correspondiente a la identificación y preparación para despacho
            submenu_identificacion_despacho()
        
        elif opcion == 6:
            # Aquí se llamará al submenú correspondiente al historial de trazabilidad
            print("Submenú de Historial de trazabilidad")        

        # si es 7, el ciclo termina

    else:
        print("Opción invalida. Intente nuevamente.")        