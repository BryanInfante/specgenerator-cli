# DESIGN.md

## 1. Arquitectura general
La arquitectura general del sistema de gestión de inspecciones NDT se basa en un enfoque de microservicios, donde cada componente del sistema se ejecuta como un servicio independiente. Esto permite una mayor escalabilidad, flexibilidad y mantenimiento. El sistema se divide en tres capas principales: presentación, lógica de negocio y datos. La capa de presentación se encarga de la interacción con el usuario, la capa de lógica de negocio maneja la lógica de la aplicación y la capa de datos se encarga del almacenamiento y recuperación de los datos.

## 2. Decisiones de arquitectura (ADRs)
### ADR-01: Uso de Node.js como tecnología de backend
**Decisión:** Se ha decidido utilizar Node.js como tecnología de backend para el desarrollo de la API REST.
**Razón:** Node.js es una plataforma ligera y eficiente que permite el desarrollo de aplicaciones escalables y de alta velocidad. Además, su gran comunidad y ecosistema de paquetes hacen que sea una excelente opción para el desarrollo de aplicaciones web.
**Consecuencia:** La elección de Node.js como tecnología de backend implica que debemos utilizar un framework de Node.js, como Express.js, para el desarrollo de la API REST.

### ADR-02: Uso de MongoDB como base de datos
**Decisión:** Se ha decidido utilizar MongoDB como base de datos para el almacenamiento de los datos de inspecciones.
**Razón:** MongoDB es una base de datos NoSQL que permite el almacenamiento de datos en formato JSON, lo que facilita la integración con la API REST. Además, su capacidad para manejar grandes cantidades de datos y su escalabilidad horizontal hacen que sea una excelente opción para el almacenamiento de los datos de inspecciones.
**Consecuencia:** La elección de MongoDB como base de datos implica que debemos utilizar un driver de MongoDB para Node.js para interactuar con la base de datos.

## 3. Estructura de carpetas/proyecto
```
inspecciones-ndt/
├── app/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   └── services/
├── config/
├── db/
├── node_modules/
├── package.json
├── README.md
└── server.js
```

## 4. Modelo de datos detallado
### Inspección
- **id**: String — Identificador único de la inspección
- **fecha**: Date — Fecha de la inspección
- **tipo**: String — Tipo de inspección (por ejemplo, radiografía, ultrasonido, etc.)
- **componente**: String — Componente inspeccionado
- **resultado**: String — Resultado de la inspección (por ejemplo, aprobado, rechazado, etc.)
- **evidencia**: Array<String> — Evidencia o documentación de la inspección

### Componente
- **id**: String — Identificador único del componente
- **nombre**: String — Nombre del componente
- **descripcion**: String — Descripción del componente
- **ubicacion**: String — Ubicación del componente

### Usuario
- **id**: String — Identificador único del usuario
- **nombre**: String — Nombre del usuario
- **correo**: String — Correo electrónico del usuario
- **rol**: String — Rol del usuario (por ejemplo, inspector, técnico, gerente, etc.)

## 5. Diseño de APIs
### /inspecciones
- Método: POST
- URL: /inspecciones
- Request: { tipo: String, componente: String, resultado: String, evidencia: Array<String> }
- Response: { id: String, fecha: Date, tipo: String, componente: String, resultado: String, evidencia: Array<String> }

### /inspecciones/{id}
- Método: GET
- URL: /inspecciones/{id}
- Request: None
- Response: { id: String, fecha: Date, tipo: String, componente: String, resultado: String, evidencia: Array<String> }

### /inspecciones/tipo/{tipo}
- Método: GET
- URL: /inspecciones/tipo/{tipo}
- Request: None
- Response: Array<{ id: String, fecha: Date, tipo: String, componente: String, resultado: String, evidencia: Array<String> }>

### /informes
- Método: POST
- URL: /informes
- Request: { tipo: String, fechaInicio: Date, fechaFin: Date }
- Response: { informe: String }

## 6. Dependencias externas
- **express**: 4.17.1 — Framework de Node.js para el desarrollo de la API REST
- **mongodb**: 3.6.4 — Driver de MongoDB para Node.js
- **jsonwebtoken**: 8.5.1 — Librería para la generación y verificación de tokens JSON Web

## 7. Seguridad
- La API REST utiliza tokens JSON Web para la autenticación y autorización de los usuarios.
- Los datos de inspecciones se almacenan en una base de datos MongoDB segura, con acceso restringido a los usuarios autorizados.
- La API REST utiliza HTTPS para cifrar las comunicaciones entre el cliente y el servidor.