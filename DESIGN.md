# DESIGN.md

## 1. Arquitectura general
El sistema de inventario para la ferretería se basa en una arquitectura de microservicios, donde cada componente tiene una función específica y se comunica con los demás a través de APIs RESTful. El sistema consta de tres capas principales: presentación, lógica de negocio y datos. La capa de presentación se encarga de la interfaz de usuario y la interacción con el cliente, la capa de lógica de negocio se encarga de la gestión de los procesos y la capa de datos se encarga del almacenamiento y recuperación de la información.

## 2. Decisiones de arquitectura (ADRs)
### ADR-01: Uso de Node.js como tecnología de backend
**Decisión:** Se decidió utilizar Node.js como tecnología de backend para el sistema de inventario.
**Razón:** Se eligió Node.js por su capacidad para manejar un gran número de conexiones simultáneas, lo que es ideal para un sistema que necesita manejar múltiples solicitudes de usuario al mismo tiempo. Además, Node.js tiene una gran comunidad de desarrolladores y una amplia gama de bibliotecas y frameworks que facilitan el desarrollo de aplicaciones web.
**Consecuencia:** La decisión de utilizar Node.js como tecnología de backend implica que el equipo de desarrollo debe tener experiencia en esta tecnología y que el sistema debe ser diseñado para aprovechar al máximo las características de Node.js.

### ADR-02: Uso de MongoDB como base de datos
**Decisión:** Se decidió utilizar MongoDB como base de datos para el sistema de inventario.
**Razón:** Se eligió MongoDB por su capacidad para manejar grandes cantidades de datos y su flexibilidad en cuanto a la estructura de los datos. MongoDB también es una base de datos NoSQL, lo que significa que no requiere un esquema fijo, lo que facilita la adaptación a cambios en la estructura de los datos.
**Consecuencia:** La decisión de utilizar MongoDB como base de datos implica que el equipo de desarrollo debe tener experiencia en esta tecnología y que el sistema debe ser diseñado para aprovechar al máximo las características de MongoDB.

## 3. Estructura de carpetas/proyecto
```markdown
proyecto-inventario/
├── backend/
│   ├── controllers/
│   │   ├── producto.controller.js
│   │   ├── categoria.controller.js
│   │   └── ...
│   ├── models/
│   │   ├── producto.model.js
│   │   ├── categoria.model.js
│   │   └── ...
│   ├── routes/
│   │   ├── producto.routes.js
│   │   ├── categoria.routes.js
│   │   └── ...
│   ├── services/
│   │   ├── producto.service.js
│   │   ├── categoria.service.js
│   │   └── ...
│   ├── app.js
│   └── package.json
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── ...
│   ├── src/
│   │   ├── components/
│   │   │   ├── producto.component.js
│   │   │   ├── categoria.component.js
│   │   │   └── ...
│   │   ├── containers/
│   │   │   ├── producto.container.js
│   │   │   ├── categoria.container.js
│   │   │   └── ...
│   │   ├── services/
│   │   │   ├── producto.service.js
│   │   │   ├── categoria.service.js
│   │   │   └── ...
│   │   ├── app.js
│   │   └── index.js
│   └── package.json
└── README.md
```

## 4. Modelo de datos detallado
### Producto
- **id**: string — Identificador único del producto
- **nombre**: string — Nombre del producto
- **descripcion**: string — Descripción del producto
- **precio**: number — Precio del producto
- **cantidadEnStock**: number — Cantidad en stock del producto

### Categoria
- **id**: string — Identificador único de la categoría
- **nombre**: string — Nombre de la categoría

### Proveedor
- **id**: string — Identificador único del proveedor
- **nombre**: string — Nombre del proveedor
- **direccion**: string — Dirección del proveedor

### Pedido
- **id**: string — Identificador único del pedido
- **fecha**: date — Fecha del pedido
- **total**: number — Total del pedido
- **estado**: string — Estado del pedido

## 5. Diseño de APIs
### Obtener productos
- Método: GET
- URL: /api/productos
- Request: {}
- Response: [{ id, nombre, descripcion, precio, cantidadEnStock }]

### Crear producto
- Método: POST
- URL: /api/productos
- Request: { nombre, descripcion, precio, cantidadEnStock }
- Response: { id, nombre, descripcion, precio, cantidadEnStock }

### Actualizar producto
- Método: PUT
- URL: /api/productos/:id
- Request: { nombre, descripcion, precio, cantidadEnStock }
- Response: { id, nombre, descripcion, precio, cantidadEnStock }

### Eliminar producto
- Método: DELETE
- URL: /api/productos/:id
- Request: {}
- Response: {}

## 6. Dependencias externas
- **express**: 4.17.1 — Framework para Node.js
- **mongodb**: 3.6.4 — Driver para MongoDB
- **mongoose**: 5.10.18 — ORM para MongoDB
- **jwt**: 8.5.1 — Librería para tokens de autenticación

## 7. Seguridad (si aplica)
- **Autenticación**: Se utilizará JSON Web Tokens (JWT) para autenticar a los usuarios.
- **Autorización**: Se utilizarán roles y permisos para autorizar a los usuarios a realizar acciones en el sistema.
- **Cifrado**: Se utilizará SSL/TLS para cifrar las comunicaciones entre el cliente y el servidor.