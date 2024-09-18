# Explicación del Diagrama de Clases

### 1. **Producer (Productor)**
   La clase *Producer* es la principal y representa al productor que gestiona varias fincas. Tiene una **relación de uno a muchos** con la clase *Farm*, lo que indica que un productor puede tener varias fincas.

### 2. **Farm (Finca)**
   La clase *Farm* representa una finca individual que está asociada a un productor (*Producer*). A su vez, una finca puede tener múltiples viveros (*Nursery*), lo que se expresa con una **relación de uno a muchos** con la clase *Nursery*.

### 3. **Nursery (Vivero)**
   *Nursery* representa un vivero ubicado dentro de una finca específica (*Farm*). Cada vivero tiene asociadas varias tareas (*Task*), por lo tanto, mantiene una **relación de uno a muchos** con la clase *Task*.

### 4. **Task (Labor)**
   *Task* representa una labor o tarea realizada en un vivero (*Nursery*). Está vinculada con varias aplicaciones de productos (*ProductApplication*), lo que se refleja en una **relación de uno a muchos**. Cada tarea está asociada con el control de plagas, hongos o fertilización a través de productos específicos.

### 5. **ProductApplication (AplicaciónProducto)**
   *ProductApplication* representa la aplicación de un producto en una tarea específica (*Task*). Está vinculada tanto a una tarea como a un producto de control (*ControlProduct*), y gestiona la interacción entre las labores realizadas y los productos aplicados.

### 6. **ControlProduct (ProductoControl)**
   *ControlProduct* es una clase abstracta que representa cualquier producto utilizado en la aplicación de control, ya sea para plagas, hongos o fertilización. Esta clase tiene tres **subclases** que heredan sus atributos:

   - **FungusControl (ControlHongo):** Maneja productos específicos para el control de hongos.
   - **PestControl (ControlPlaga):** Se especializa en el control de plagas.
   - **FertilizerControl (ControlFertilizante):** Gestiona productos de fertilización.

   Cada una de estas subclases añade atributos específicos adicionales a los heredados de *ControlProduct*, permitiendo gestionar los detalles específicos de cada tipo de producto.