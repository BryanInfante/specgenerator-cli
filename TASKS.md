# TASKS.md

## Leyenda
- [ ] Pendiente
- [~] En progreso
- [x] Completado

---

## FASE 1 — Configuración inicial
(agrupa tareas relacionadas)

- [ ] **T-01** Configurar el entorno de desarrollo (Node.js, MongoDB)
  - Instalar Node.js y MongoDB en el sistema de desarrollo
  - Configurar las variables de entorno para Node.js y MongoDB
- [ ] **T-02** Crear el proyecto y estructura de carpetas
  - Inicializar el proyecto con `npm init`
  - Crear la estructura de carpetas para el proyecto (backend, frontend, etc.)
- [ ] **T-03** Instalar dependencias iniciales (Express, Mongoose)
  - Instalar Express y Mongoose con `npm install`
  - Configurar la conexión a la base de datos con Mongoose

---

## FASE 2 — Modelos y esquema de datos
- [ ] **T-04** Definir el modelo de datos para productos
  - Crear el esquema de datos para productos con Mongoose
  - Definir las validaciones y relaciones con otros modelos
- [ ] **T-05** Definir el modelo de datos para categorías
  - Crear el esquema de datos para categorías con Mongoose
  - Definir las validaciones y relaciones con otros modelos
- [ ] **T-06** Definir el modelo de datos para proveedores
  - Crear el esquema de datos para proveedores con Mongoose
  - Definir las validaciones y relaciones con otros modelos

---

## FASE 3 — Lógica de negocio y API
- [ ] **T-07** Implementar la lógica de negocio para productos (crear, leer, actualizar, eliminar)
  - Crear los controladores para productos
  - Implementar la lógica de negocio para cada acción
- [ ] **T-08** Implementar la lógica de negocio para categorías (crear, leer, actualizar, eliminar)
  - Crear los controladores para categorías
  - Implementar la lógica de negocio para cada acción
- [ ] **T-09** Implementar la API para productos (GET, POST, PUT, DELETE)
  - Crear los endpoints para productos
  - Implementar la lógica de negocio para cada endpoint
- [ ] **T-10** Implementar la API para categorías (GET, POST, PUT, DELETE)
  - Crear los endpoints para categorías
  - Implementar la lógica de negocio para cada endpoint

---

## FASE 4 — Tests y deployment
- [ ] **T-11** Implementar tests unitarios para la lógica de negocio
  - Crear tests unitarios para cada controlador
  - Implementar la lógica de negocio para cada test
- [ ] **T-12** Implementar tests de integración para la API
  - Crear tests de integración para cada endpoint
  - Implementar la lógica de negocio para cada test
- [ ] **T-13** Desplegar la aplicación en un entorno de producción
  - Configurar el entorno de producción (servidor, base de datos, etc.)
  - Desplegar la aplicación en el entorno de producción