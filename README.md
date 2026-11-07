# CartoControl

CartoControl es un sistema desarrollado en Python para apoyar la gestión y trazabilidad de órdenes de producción de CartoTec Empaques.

El programa permite relacionar la información de una orden durante su recorrido por planificación, materia prima, producción, control de calidad e identificación y preparación para despacho.

## Funcionalidades principales

CartoControl incluye:

- Gestión y planificación de órdenes.
- Control y reserva de materia prima.
- Registro de movimientos de material entre órdenes.
- Seguimiento de producción, rechazos y paros.
- Registro y verificación de aprobación del arte.
- Inspecciones y resultados de calidad.
- Identificación del producto mediante lotes.
- Preparación total o parcial para despacho.
- Registro de autorizaciones.
- Historial de trazabilidad por orden.

## Requisitos

Para ejecutar el programa se necesita:

- Python 3
- Pandas

Antes de ejecutar CartoControl, instalar las dependencias con:

```bash
python -m pip install -r requirements.txt
```

También se puede instalar Pandas directamente con:

```bash
python -m pip install pandas
```

## Ejecución

1. Abrir la carpeta del proyecto.
2. Abrir una terminal dentro de esa carpeta.
3. Instalar las dependencias necesarias.
4. Ejecutar:

```bash
python menus.py
```

El menú principal permitirá acceder a los diferentes módulos de CartoControl.

## Almacenamiento de datos

CartoControl utiliza archivos CSV para conservar la información entre ejecuciones.

Los archivos almacenan información relacionada con:

- órdenes;
- materiales;
- reservas;
- movimientos de material;
- producción;
- historial;
- registros adicionales de calidad, identificaciones y autorizaciones.

Pandas se utiliza para leer y escribir estos archivos desde Python.

## Estructura principal

```text
menus.py
modulos_ordenes_materiales.py
modulo_completoProyecto.py
modulos_calidad_despacho.py
historial_trazabilidad.py
datos_cartocontrol.py
requirements.txt
```

`menus.py` funciona como punto de entrada al sistema y conecta los diferentes módulos.

## Alcance

CartoControl da seguimiento a la información de una orden desde su planificación hasta que el producto queda preparado para despacho.

El sistema organiza y registra información del proceso, pero no controla maquinaria ni sustituye las decisiones y autorizaciones del personal.

El seguimiento del transporte o del producto después de salir de planta no forma parte del alcance actual.

## Equipo

Grupo 08