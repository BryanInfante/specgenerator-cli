# DESIGN.md

## 1. Arquitectura general
El sistema de notificaciones por email para SaaS se diseñará utilizando una arquitectura de microservicios, con componentes separados para el registro de usuarios, configuración de preferencias de notificación, envío de notificaciones y registro de eventos. Esto permitirá una mayor escalabilidad y flexibilidad en el sistema.

## 2. Decisiones de arquitectura (ADRs)
### ADR-01: Elección de tecnología para el envío de correos electrónicos
**Decisión:** Utilizar un servicio de correo electrónico dedicado como SendGrid o Mailgun para el envío de notificaciones.
**Razón:** Estos servicios ofrecen una alta confiabilidad y escalabilidad en el envío de correos electrónicos, además de características adicionales como seguimiento y análisis de entregas.
**Consecuencia:** El sistema dependerá de un servicio externo para el envío de correos electrónicos, lo que puede implicar costos adicionales y dependencia de un proveedor externo.

### ADR-02: Diseño de la base de datos
**Decisión:** Utilizar una base de datos relacional como PostgreSQL para almacenar información de usuarios y notificaciones.
**Razón:** Las bases de datos relacionales ofrecen una gran flexibilidad y capacidad de consulta, lo que es ideal para almacenar y recuperar información de usuarios y notificaciones.
**Consecuencia:** El sistema requerirá una configuración y mantenimiento adecuados de la base de datos para garantizar el rendimiento y la integridad de los datos.

## 3. Estructura de carpetas/proyecto
```
notificaciones-saas/
├── api/
│   ├── usuarios/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   └── serializers.py
│   ├── notificaciones/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   └── serializers.py
│   └── eventos/
│       ├── __init__.py
│       ├── models.py
│       ├── views.py
│       └── serializers.py
├── core/
│   ├── __init__.py
│   ├── utils.py
│   └── tasks.py
├── requirements.txt
├── settings.py
└── manage.py
```

## 4. Modelo de datos detallado
### Usuario
- `id`: `integer` — Identificador único del usuario
- `nombre`: `string` — Nombre del usuario
- `correo_electronico`: `string` — Correo electrónico del usuario
- `preferencias_notificacion`: `json` — Preferencias de notificación del usuario

### Notificación
- `id`: `integer` — Identificador único de la notificación
- `tipo`: `string` — Tipo de notificación (por ejemplo, "registro", "evento", etc.)
- `contenido`: `string` — Contenido de la notificación
- `fecha_envio`: `datetime` — Fecha y hora de envío de la notificación
- `usuario_destino`: `integer` — Identificador del usuario destino de la notificación

### Evento
- `id`: `integer` — Identificador único del evento
- `tipo`: `string` — Tipo de evento (por ejemplo, "registro", "actualización", etc.)
- `fecha_ocurrencia`: `datetime` — Fecha y hora de ocurrencia del evento
- `descripcion`: `string` — Descripción del evento

## 5. Diseño de APIs
### /api/usuarios/registro
- Método: `POST`
- URL: `/api/usuarios/registro`
- Request: `{"nombre": "string", "correo_electronico": "string"}`
- Response: `{"id": integer, "nombre": "string", "correo_electronico": "string"}`

### /api/notificaciones/enviar
- Método: `POST`
- URL: `/api/notificaciones/enviar`
- Request: `{"tipo": "string", "contenido": "string", "usuario_destino": integer}`
- Response: `{"id": integer, "tipo": "string", "contenido": "string", "fecha_envio": "datetime"}`

### /api/eventos/registro
- Método: `POST`
- URL: `/api/eventos/registro`
- Request: `{"tipo": "string", "fecha_ocurrencia": "datetime", "descripcion": "string"}`
- Response: `{"id": integer, "tipo": "string", "fecha_ocurrencia": "datetime", "descripcion": "string"}`

### /api/usuarios/preferencias
- Método: `GET`
- URL: `/api/usuarios/preferencias`
- Request: `{"usuario": integer}`
- Response: `{"preferencias_notificacion": json}`

## 6. Dependencias externas
- `sendgrid`: `6.9.5` — Servicio de correo electrónico dedicado
- `mailgun`: `0.6.0` — Servicio de correo electrónico dedicado
- `postgresql`: `12.9` — Base de datos relacional
- `django`: `3.2.9` — Framework web de Python
- `djangorestframework`: `3.12.2` — Framework de API REST para Django

## 7. Seguridad
- Utilizar autenticación y autorización adecuadas para proteger los endpoints de la API
- Utilizar HTTPS para cifrar la comunicación entre el cliente y el servidor
- Utilizar una política de seguridad adecuada para la base de datos y los servicios externos utilizados
- Realizar pruebas de seguridad y penetración para identificar vulnerabilidades y mejorar la seguridad del sistema