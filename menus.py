import modulo_completoProyecto
import modulos_calidad_despacho
import historial_trazabilidad
import modulos_ordenes_materiales

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
            modulos_ordenes_materiales.menu_gestion_planificacion()

        elif opcion == 2:
            modulos_ordenes_materiales.menu_materia_prima()

        elif opcion == 3:
            submenu_seguimiento_produccion()

        elif opcion == 4:
            modulos_calidad_despacho.menu_calidad()

        elif opcion == 5:
            modulos_calidad_despacho.menu_despacho()
        
        elif opcion == 6:
            historial_trazabilidad.consultar_historial()        

        # si es 7, el ciclo termina

    else:
        print("Opción invalida. Intente nuevamente.")        