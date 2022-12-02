# DAS

## Twitter Reloaded and Event Dashboard

## El siguiente proyecto es una aplicacion, la cual permite al usuario crearse una cuenta y tanto crear como responder Tweets. Ademas, tenemos otra aplicacion la cual es un event dashboard, la cual registra algunos movimientos que se executan en la pagina en tiempo real

### Principios de solid:

Single Responsibility Principle (SRP): Este principio de solid lo implementamos en la clase usario, ya que teniamos dentro de esta calse una mini funcion para encriptar la contraseño, entonces sacamos esa funcion y la pusimos en una clase aparte 

Open/Closed Principle (OP/CP): Este principio de cumple con las rutas que asignamos, ya que los metodos estan separdos, entonces si se le quiere agregar un nuevo metodo, no hay necesidad de modificar el codigo anterior 

Liskov Substitution Principle (LSP): Aplicamos este principio sobre las clases de tweets, ya que estaba junto a el response tweet. En este caso dividimos las clases para cumplir con este principio

Interface Segregation Principle (ISP): Este principio se cumple justamente con unos de los requerimientos del proyecto, y es que lo que pasa en el dashboard de tweeter reloaded, se refleja en el event dashboard, sin presentar ninguna anomalia.

Dependency Inversion Principle (DIP): Se usa l single tone para hacer una conexion global, y esa conexion se pasa a una variable, entonces se puede modificar la base de datos sin que el sistema sufra cambios severos 


### Patrones de diseño:

Decoradores:

Single tone:
