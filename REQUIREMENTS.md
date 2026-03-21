# REQUIREMENTS.md

## 1. Descripción del producto
La API REST para gestión de inspecciones NDT es un sistema diseñado para facilitar y automatizar el proceso de inspección no destructiva de materiales y componentes. Su propósito principal es ofrecer una plataforma eficiente y segura para registrar, gestionar y analizar los resultados de estas inspecciones, mejorando así la calidad y la seguridad de los productos finales.

## 2. Usuarios objetivo
Los usuarios finales de este sistema serán principalmente inspectores de calidad, técnicos de mantenimiento y gerentes de producción en industrias que requieren inspecciones NDT, como la aeroespacial, la energía y la construcción. Estos usuarios necesitan ser capaces de interactuar con el sistema de manera intuitiva para ingresar, consultar y analizar datos de inspecciones de forma eficiente.

## 3. Casos de uso
UC-01 — Registro de Inspección
**Actor:** Inspector de calidad
**Precondición:** El usuario debe estar autenticado en el sistema y tener permisos para registrar inspecciones.
**Flujo:**
1. El usuario selecciona el tipo de inspección que desea registrar.
2. El sistema solicita los detalles de la inspección, incluyendo el componente inspeccionado, el método de inspección y los resultados.
3. El usuario ingresa los detalles y sube cualquier evidencia o documentación relevante.
4. El sistema valida la información y la almacena en la base de datos.
**Criterios de aceptación:**
- El sistema debe permitir el registro de diferentes tipos de inspecciones NDT.
- Los datos de inspección deben ser validados para asegurar la consistencia y la completitud.
- El sistema debe generar un identificador único para cada inspección registrada.

UC-02 — Consulta de Resultados de Inspección
**Actor:** Técnico de mantenimiento
**Precondición:** El usuario debe estar autenticado en el sistema y tener permisos para consultar resultados de inspecciones.
**Flujo:**
1. El usuario busca inspecciones por fecha, componente o método de inspección.
2. El sistema muestra los resultados de las inspecciones que coinciden con los criterios de búsqueda.
3. El usuario selecciona una inspección para ver los detalles completos.
**Criterios de aceptación:**
- El sistema debe permitir la búsqueda de inspecciones por diferentes criterios.
- Los resultados de la búsqueda deben mostrarse de manera clara y organizada.
- El sistema debe mostrar todos los detalles relevantes de la inspección seleccionada.

UC-03 — Generación de Informes
**Actor:** Gerente de producción
**Precondición:** El usuario debe estar autenticado en el sistema y tener permisos para generar informes.
**Flujo:**
1. El usuario selecciona el tipo de informe que desea generar (por ejemplo, resumen de inspecciones por período).
2. El sistema solicita los parámetros adicionales necesarios para el informe (como fechas o componentes específicos).
3. El sistema genera el informe en un formato adecuado para su visualización o descarga.
**Criterios de aceptación:**
- El sistema debe ofrecer diferentes tipos de informes predefinidos.
- Los informes deben ser fáciles de entender y deben contener toda la información relevante solicitada.
- El sistema debe permitir la descarga de los informes en formatos comunes como PDF o Excel.

## 4. Requisitos no funcionales
| ID | Requisito |
|----|-----------|
| RNF-01 | La API debe ser capaz de manejar al menos 100 solicitudes concurrentes sin una disminución significativa en el rendimiento. |
| RNF-02 | Todos los datos de inspección deben ser almacenados de manera segura, utilizando protocolos de cifrado adecuados para proteger la información sensible. |
| RNF-03 | La API debe ser compatible con diferentes navegadores web y dispositivos móviles para asegurar la accesibilidad. |
| RNF-04 | El sistema debe tener una tasa de disponibilidad del 99.9% en un período de un mes, permitiendo un máximo de 45 minutos de tiempo de inactividad programada para mantenimiento mensual. |

## 5. Modelo de datos (conceptual)
- Inspección: ID, fecha, tipo de inspección, componente inspeccionado, método de inspección, resultados, evidencia/documentación.
- Componente: ID, nombre, descripción, ubicación.
- Usuario: ID, nombre, correo electrónico, rol.

## 6. APIs / Interfaces externas (si aplica)
- **/inspecciones**: Endpoint para registrar nuevas inspecciones.
- **/inspecciones/{id}**: Endpoint para consultar detalles de una inspección específica.
- **/informes**: Endpoint para generar informes de inspecciones.
- **/auth**: Endpoint para la autenticación de usuarios.