### 7.1 Entity Roles and Groups for Complex Named Entity

En flujos conversacionales de complejidad media y avanzada, no basta con identificar que una palabra pertenece a un tipo de entidad genérico. A veces necesitamos capturar el contexto gramatical o el agrupamiento en el que se encuentra. En nuestro cotizador, esto aparece cuando el usuario compara dos instalaciones o menciona múltiples obras en el mismo mensaje.

#### Objetivos de aprendizaje
- Comprender qué son los roles y grupos de entidades.
- Identificar casos de uso en el dominio de instalaciones eléctricas.
- Entrenar el NLU para reconocer roles y grupos.

#### Roles de entidad

Los roles permiten etiquetar una misma entidad con diferentes funciones dentro de un mensaje.

Ejemplo del cotizador:
> *"Quiero reemplazar la instalación de mi casa en **Rosario** por una nueva en **Córdoba**."*

Aquí, tanto *"Rosario"* como *"Córdoba"* son entidades tipo `ubicacion`, pero desempeñan funciones diferentes:
- `ubicacion` con rol `origen`: Rosario.
- `ubicacion` con rol `destino`: Córdoba.

En `data/nlu.yml`:
```yaml
nlu:
  - intent: cambiar_ubicacion
    examples: |
      - Quiero reemplazar la instalación de mi casa en [Rosario](ubicacion:origen) por una nueva en [Córdoba](ubicacion:destino)
      - Necesito pasar el servicio eléctrico de [Buenos Aires](ubicacion:origen) a [Mendoza](ubicacion:destino)
```

En `domain.yml`:
```yaml
entities:
  - ubicacion:
      roles:
        - origen
        - destino
```

#### Grupos de entidades

Los grupos permiten asociar entidades relacionadas que pertenecen al mismo concepto dentro de una frase.

Ejemplo del cotizador:
> *"Necesito cotizar dos obras: una **residencial** de **60 m²** y otra **comercial** de **150 m²**."*

Aquí necesitamos asociar:
- Grupo 1: `tipo_instalacion=residencial` + `metraje=60`.
- Grupo 2: `tipo_instalacion=comercial` + `metraje=150`.

En `data/nlu.yml`:
```yaml
nlu:
  - intent: solicitar_multiples_cotizaciones
    examples: |
      - Necesito cotizar dos obras: una [residencial](tipo_instalacion){"group": "obra_1"} de [60](metraje){"group": "obra_1"} m² y otra [comercial](tipo_instalacion){"group": "obra_2"} de [150](metraje){"group": "obra_2"} m²
```

#### Ejercicio práctico

1. Define en `domain.yml` la entidad `ubicacion` con los roles `origen` y `destino`.
2. Añade al menos cuatro ejemplos en `data/nlu.yml` que usen roles.
3. Define un intent `solicitar_multiples_cotizaciones` con al menos dos ejemplos que usen grupos.
4. Entrena el modelo:
   ```bash
   rasa train
   ```
5. Prueba con mensajes como:
   - *"Quiero cambiar la instalación de La Plata a Mar del Plata."*
   - *"Cotizame una residencial de 70 m2 y una comercial de 120 m2."*
6. Verifica en la salida de `rasa shell nlu` que Rasa asigna correctamente los roles y grupos.

#### Resumen
Los roles y grupos permiten capturar estructuras más complejas en el lenguaje natural. En el cotizador eléctrico, nos sirven para comparar ubicaciones o cotizar múltiples obras en una sola conversación. En el próximo capítulo veremos cómo extender Rasa con componentes personalizados cuando los componentes nativos no sean suficientes.
