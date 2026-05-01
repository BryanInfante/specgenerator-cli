# REQUIREMENTS.md

## 1. Descripción del producto
El sistema de inventario para la ferretería es un proyecto diseñado para gestionar y controlar los productos en stock, permitiendo una gestión eficiente y precisa de los mismos. Su propósito principal es ofrecer una herramienta para que los empleados de la ferretería puedan realizar un seguimiento detallado de los productos disponibles, gestionar las existencias y optimizar el proceso de reposición.

## 2. Usuarios objetivo
Los usuarios finales del sistema de inventario son los empleados de la ferretería, que incluyen:
- Gerentes de tienda
- Empleados de ventas
- Encargados de almacén
- Administradores de sistemas

## 3. Casos de uso
UC-01 — Registro de producto
**Actor:** Empleado de almacén
**Precondición:** El empleado debe tener acceso al sistema y permisos para registrar productos.
**Flujo:**
1. El empleado inicia sesión en el sistema.
2. Selecciona la opción de registrar un nuevo producto.
3. Introduce la información del producto, incluyendo nombre, descripción, precio y cantidad.
4. Confirma el registro del producto.
**Criterios de aceptación:**
- El sistema debe permitir el registro de productos con toda la información necesaria.
- El sistema debe validar que la información introducida sea correcta y completa.

UC-02 — Actualización de existencias
**Actor:** Empleado de almacén
**Precondición:** El empleado debe tener acceso al sistema y permisos para actualizar existencias.
**Flujo:**
1. El empleado selecciona el producto a actualizar.
2. Introduce la nueva cantidad en stock.
3. Confirma la actualización.
**Criterios de aceptación:**
- El sistema debe permitir la actualización de las existencias de un producto.
- El sistema debe validar que la cantidad introducida sea numérica y no negativa.

UC-03 — Búsqueda de productos
**Actor:** Empleado de ventas
**Precondición:** El empleado debe tener acceso al sistema.
**Flujo:**
1. El empleado introduce el nombre o código del producto a buscar.
2. El sistema muestra los resultados de la búsqueda, incluyendo la descripción y cantidad en stock.
**Criterios de aceptación:**
- El sistema debe permitir la búsqueda de productos por nombre o código.
- El sistema debe mostrar los resultados de la búsqueda de manera clara y concisa.

## 4. Requisitos no funcionales
| ID | Requisito |
|----|-----------|
| RNF-01 | El sistema debe ser compatible con navegadores web modernos. |
| RNF-02 | El sistema debe tener una respuesta máxima de 2 segundos para cualquier solicitud. |
| RNF-03 | El sistema debe ser capaz de manejar al menos 100 usuarios concurrentes. |
| RNF-04 | El sistema debe cumplir con los estándares de seguridad para proteger la información de los productos y los usuarios. |

## 5. Modelo de datos (conceptual)
- **Productos**: id, nombre, descripción, precio, cantidad_en_stock
- **Categorías**: id, nombre
- **Proveedores**: id, nombre, dirección
- **Pedidos**: id, fecha, total, estado

## 6. APIs / Interfaces externas (si aplica)
- **API de pago**: Permite a los clientes realizar pagos en línea de manera segura.
- **API de envío**: Permite calcular el costo de envío y realizar el seguimiento de los pedidos.
- **API de inventario**: Permite a los empleados actualizar y consultar el inventario de manera remota.