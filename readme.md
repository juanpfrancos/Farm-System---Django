# Explicación del Diagrama de Clases

### 1. Producer
`Producer` es la entidad que representa a un productor, con los siguientes campos:
- **identity_document**: Documento de identidad único.
- **first_name**: Nombre del productor.
- **last_name**: Apellido del productor.
- **phone**: Número de teléfono.
- **email**: Correo electrónico.

Este modelo también contiene los métodos:
- **clean()**: Valida el campo `email`.
- **save()**: Llama al método `full_clean()` antes de guardar.

Un `Producer` puede tener varias **Farm**s asociadas (relación uno a muchos).

### 2. Farm
`Farm` representa una finca, que tiene las siguientes propiedades:
- **producer**: Llave foránea que asocia la finca a un productor.
- **cadastral_number**: Número catastral único.
- **municipality**: Municipio donde está ubicada la finca.

Una finca puede tener varios **Nursery**s (viveros) asociados (relación uno a muchos).

### 3. Nursery
`Nursery` es un vivero dentro de una finca, y tiene los siguientes campos:
- **farm**: Llave foránea que asocia el vivero a una finca.
- **code**: Código del vivero.
- **crop_type**: Tipo de cultivo en el vivero.

Un vivero puede tener varias **Task**s (relación uno a muchos).

### 4. Task
`Task` representa una tarea realizada en un vivero, con los siguientes campos:
- **nursery**: Llave foránea que asocia la tarea a un vivero.
- **date**: Fecha de la tarea.
- **description**: Descripción de la tarea.

Una tarea puede tener varias **ProductApplication**s (relación uno a muchos).

### 5. ControlProduct (Clase Abstracta)
`ControlProduct` es una clase abstracta que define productos de control, con los siguientes campos comunes:
- **ica_registration**: Registro ICA único.
- **name**: Nombre del producto.
- **application_frequency**: Frecuencia de aplicación (en días).
- **price**: Precio del producto.

Tres tipos de productos heredan de esta clase:

#### FungusControl
Controla hongos, con campos adicionales:
- **withdrawal_period**: Período de retiro (en días).
- **fungus_name**: Nombre del hongo que controla.

#### PestControl
Controla plagas, con el campo adicional:
- **withdrawal_period**: Período de retiro (en días).

#### FertilizerControl
Controla fertilizantes, con el campo adicional:
- **last_application_date**: Fecha de la última aplicación.

### 6. ProductApplication
`ProductApplication` representa la aplicación de un producto en una tarea, con los siguientes campos:
- **task**: Llave foránea que asocia la aplicación de un producto a una tarea.
- **content_type**: Llave foránea genérica que permite referenciar diferentes tipos de productos (`FungusControl`, `PestControl`, `FertilizerControl`).
- **object_id**: Referencia al producto específico.
- **product**: Llave genérica (combina `content_type` y `object_id`).
- **application_date**: Fecha de la aplicación.

`ProductApplication` utiliza un campo de clave genérica (`GenericForeignKey`) para referenciar a un tipo de producto específico.

---

## Relaciones Principales
- **Producer** tiene muchas **Farm**s.
- **Farm** tiene muchos **Nursery**s.
- **Nursery** tiene muchas **Task**s.
- **Task** tiene muchas **ProductApplication**s.
- **ProductApplication** puede referenciar varios tipos de productos heredados de **ControlProduct** mediante una clave genérica.
