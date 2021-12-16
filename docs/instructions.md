# [Django - Backend - Entrevista](https://www.notion.so/Django-Backend-Entrevista-9e048362475f45eaaad990f9837e146e)

## CONTEXTO GENERAL

**Plerk** somos una plataforma para administrar los beneficios de los colaboradores remotos y locales, **mediante nuestra tarjeta virtual los colaboradores pueden disfrutar de los beneficios que las empresas les otorguen**. Esto significa que cada colaborador cuenta con una tarjeta virtual la cual tiene un presupuesto. Así como una tarjeta física de debito o crédito al realizar una compra se genera una "TRANSACCION" y al tener muchos colaboradores tenemos **MUCHAS TRANSACCIONES**.

Esta prueba se enfoca al análisis y manejo de los datos de TRANSACCIONES que se han generado durante un periodo de tiempo dentro de PLERK por lo tanto el tener cuidado con los valores, números y empresas es fundamental ya que cualquier mal calculo puede afectar el control de costos por empresa y salir una cuenta muy grande que la empresa debe absorber.

Por lo tanto en Plerk trabajamos con muchos datos e información que pasa constantemente a través de nuestros servicios, la cual necesitamos analizar, manejar y determinar en qué parte nos encontramos con respecto a los datos de operaciones y transacciones.

**En esta prueba se evaluarán los siguientes aspectos:**

- Definición de modelado de datos
- Manejo de ORM
- Optimización y limpieza de código
- Solución de la prueba

## PROBLEMA

Al tener tantos datos e información de transacciones, llega un punto donde se pierde el manejo y control de la operación, visualización y monitoreo. Para ello Plerk te ha asignado una tarea muy importante para la operación.

Ayudarnos a localizar ciertas combinaciones con los datos compartidos, para conocer mejor las operaciones y transacciones que se tienen.

**En el documento anexo en el apartado de base de datos, se encuentra un archivo en CSV que debe ser importado a una base de datos en el motor de su preferencia y considerando el siguiente modelado base, en este punto se puede proponer mejoras e información extra que se considere necesaria:**

**Modelado Base**

- Transacción:
  - ID (en el formato que se considere más seguro)
  - ID de empresa
  - Price (el price actual no viene en la cantidad real... requiere una conversión... 😉) o evaluación por ser costos reales
  - Fecha de transacción
  - Estatus de transacción
    - closed —> transaccion cobrada
    - reversed —> cobro realizado y regresado (para validar tarjeta)
    - pending —> pendiente de cobrar
  - Estatus de aprobación
    - false —> no se hizo un cobro
    - true —> el cobro si fue aplicado a la tarjeta
  - Cobro Final (Boolean)
    - Este punto es una combinación de "Estatus de transacción y estatus de aprobación"
      - Sólo se deben cobrar aquellas combinaciones que sean:
        - status_transaction = closed
        - status_approved = true
- Empresa:
  - Nombre
  - Status (activa/inactiva)
  - ID (en el formato que se considere más seguro)

Nota:

- Puedes realizar un diagrama entidad relación para apoyarte en tu modelado y si lo realizaste no olvides anexarlo en el correo del resultado.

Para este punto ya se debe tener un PROYECTO de DJANGO el cual contenga el modelado, a partir de este momento se requiere agregarle al proyecto DJANGO REST FRAMEWORK para crear unos servicios que nos ayuden a obtener la información.

**SERVICIOS BASE:**

- Servicio de resumen:
  - Este servicio no recibirá ningún parámetro, pero deberá regresar un resumen de lo que se encuentra en la base de datos previamente importada. Por ejemplo:
    - La empresa con más ventas
    - La empresa con menos ventas
    - El precio total de las transacciones que SÍ se cobraron
    - El precio total de las transacciones que NO se cobraron
    - La empresa con más rechazos de ventas (es decir, no se cobraron)
- Servicio de empresa
  - Este servicio deberá recibir el ID de la empresa y nos deberá regresar la siguiente información
    - Nombre de la empresa
    - Total de transacciones que SÍ se cobraron
    - Total de transacciones que NO se cobraron
    - El día que se registraron más transacciones
- Propuesta personal:
  - Este espacio es para proponer algún servicio con información que consideres importante para la operación o de conocimiento para la empresa.

### BASE DE DATOS

[test_database.csv](assets/test_database.csv)

### CONSIDERACIONES Y RECOMENDACIONES:

- Revisa bien los datos compartidos, planea tu modelado de datos de la forma que consideres más optima, nosotros te compartimos una base ahora es **momento de ponerle tu toque y tu experiencia.**
- Considera aspectos generales de un proyecto, el que sea de uso interno no significa que debamos pasar por alto ciertos temas importantes 🤐
- En cualquier momento que tengas alguna duda, consúltanos. Te podemos ayudar a aclarar algún punto.

### TIEMPO DE LA ENTREGA

- Sabemos que cada developer trabaja a diferente ritmo. Por lo que entendemos esta situación y consideramos que la mejor forma es la siguiente:
  - **Una vez que hayas leído y vuelto a leer la prueba, antes de comenzar a programar, contesta el correo de la prueba con tu estimación de la prueba y fecha compromiso de la entrega.**
  - Al no tener límite de tiempo, no significa que no se tenga un máximo, queremos conocer tu estimación y análisis de la prueba.
  - Es importante considerar que nos encontramos en un ciclo de evaluación por lo que el tiempo de entrega de la prueba puede afectar la elección, mientras más pronto tenemos la solución más pronto tomamos la mejor decisión para PLERK.
  - Cualquier duda que se tenga de la prueba o de la definición favor de anexarla en el correo enviado de la prueba o escribir directamente a [antonio@plerk.io](mailto:antonio@plerk.io)

### ENTREGABLES:

- Repositorio de GITHUB/GITLAB con el proyecto
- Collection de POSTMAN (u otras alternativas) para probar los endpoints
- Pluss: Despliegue de la solución en alguna plataforma gratuita o servidor como:
  - Heroku
  - Pythonanywhere
- Dependiendo la prueba entregada se agendará una llamada para presentar y explicar el proyecto, resolver dudas y platicar sobre la solución.
- Se agendará en cuanto se reciba la prueba.

MUCHO ÉXITO!!
