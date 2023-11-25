# SwaggerForge3scale 🐍
PyBridge3scale es una potente herramienta de automatización en Python diseñada para simplificar la creación de backends en la plataforma 3scale. Facilita considerablemente el proceso de creacion y configuracion.


## Configuracíom ⚙️
El archivo de configuración principal es config.yaml, que contiene la información clave la creacion de los artefactos

### configuracion de Backend para 3scale 🖥️
El archivo config.yaml tiene la siguiente estructura:

```yaml
backend:
  swaggerUrl: http://tu-url.com/api-docs
  privateBaseURL: http://la-ruta-privada-que-usara-el-back.com
  backendName: "nombre de tu backend"
  name: "nombre de la app"
  path: /ruta/donde/guardar/el/backend
```
Donde:
- swaggerUrl: Dirección URL del Swagger asociado al backend.
- privateBaseURL: URL base privada para el backend.
- backendName: Identificación del backend en 3scale.
- name: Nombre específico de la aplicación (requisito según la estructura del Swagger).
- path: Ruta local donde se generan los artefactos del backend en tu computadora.

## Consideraciones Importantes ℹ️
Es crucial tener en cuenta el método de creación de nombres para cada backend y métrica. Estos se generan mediante la fórmula `método + endpoint + autoIncremental`. Esta estrategia asegura identificadores únicos para cada regla de mapeo, evitando posibles repeticiones. Sin embargo puede no ser del todo intuitivo al momento de hacer una busqueda especifica en un backend muy extenso.

## Uso 🚀
El proyecto consta de un solo archivo, app.py, que contiene la lógica principal del código. Para ejecutarlo, utiliza el siguiente comando:

```bash
python3 app.py
```

## Dependencias 🧩 
- yaml
- json
- subprocess
- requests

## Contribución 🤝
¡Tu contribución es bienvenida! Si tienes mejoras, informes de errores o ideas para nuevas características, no dudes en colaborar.
