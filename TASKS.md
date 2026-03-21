# TASKS.md

## Leyenda
- [ ] Pendiente
- [~] En progreso
- [x] Completado

---

## FASE 1 — Configuración Inicial
(agrupa tareas relacionadas con la configuración inicial del proyecto)

- [ ] **T-01** Configurar el entorno de desarrollo (Node.js, npm, MongoDB)
  - Instalar Node.js y npm
  - Instalar MongoDB y configurar el servicio
  - Verificar la instalación y configuración
- [ ] **T-02** Crear el proyecto y estructura de carpetas
  - Inicializar el proyecto con npm
  - Crear la estructura de carpetas y subcarpetas
  - Configurar el archivo `package.json`
- [ ] **T-03** Instalar dependencias iniciales (Express, MongoDB, JSON Web Token)
  - Instalar Express.js
  - Instalar el driver de MongoDB para Node.js
  - Instalar la librería JSON Web Token

---

## FASE 2 — Modelos y Base de Datos
(agrupa tareas relacionadas con la definición de modelos y configuración de la base de datos)

- [ ] **T-04** Definir el modelo de datos para Inspección
  - Definir los campos y tipos de datos para el modelo de Inspección
  - Crear el esquema de la colección en MongoDB
- [ ] **T-05** Definir el modelo de datos para Componente
  - Definir los campos y tipos de datos para el modelo de Componente
  - Crear el esquema de la colección en MongoDB
- [ ] **T-06** Definir el modelo de datos para Usuario
  - Definir los campos y tipos de datos para el modelo de Usuario
  - Crear el esquema de la colección en MongoDB
- [ ] **T-07** Configurar la conexión a la base de datos
  - Importar el driver de MongoDB
  - Establecer la conexión a la base de datos

---

## FASE 3 — Lógica de Negocio y Endpoints
(agrupa tareas relacionadas con la implementación de la lógica de negocio y endpoints)

- [ ] **T-08** Implementar la lógica de negocio para registrar una inspección
  - Crear el controlador para el endpoint de registro de inspecciones
  - Validar los datos de entrada
  - Guardar la inspección en la base de datos
- [ ] **T-09** Implementar la lógica de negocio para consultar inspecciones
  - Crear el controlador para el endpoint de consulta de inspecciones
  - Validar los parámetros de búsqueda
  - Recuperar las inspecciones de la base de datos
- [ ] **T-10** Implementar la lógica de negocio para generar informes
  - Crear el controlador para el endpoint de generación de informes
  - Validar los parámetros del informe
  - Generar el informe en formato adecuado

---

## FASE 4 — Tests y Deploy
(agrupa tareas relacionadas con la implementación de tests y despliegue del proyecto)

- [ ] **T-11** Implementar tests unitarios para la lógica de negocio
  - Seleccionar una librería de testing (por ejemplo, Jest)
  - Escribir tests para cada controlador
- [ ] **T-12** Implementar tests de integración para los endpoints
  - Seleccionar una herramienta de testing de API (por ejemplo, Postman)
  - Escribir tests para cada endpoint
- [ ] **T-13** Desplegar el proyecto en un entorno de producción
  - Seleccionar un proveedor de servicios en la nube (por ejemplo, AWS, Google Cloud)
  - Configurar el despliegue continuo
  - Realizar el despliegue inicial