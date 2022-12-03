# DAS

## Twitter Reloaded and Event Dashboard

## El siguiente proyecto es una aplicacion, la cual permite al usuario crearse una cuenta y tanto crear como responder Tweets. Ademas, tenemos otra aplicacion la cual es un event dashboard, la cual registra algunos movimientos que se executan en la pagina en tiempo real

### Principios de solid:

Single Responsibility Principle (SRP):
Un ejemplo de este principio es la creación de la clase Hash, la cual contiene funciones para encriptar y desencriptar contraseñas. Gracias a esto, las funciones de crear usuario y verificar login tienen una sola responsabilidad

Open/Closed Principle (OP/CP): 
Cada uno de los verbos HTTP para las rutas tiene un decorador y una función propia. De esta manera, si se quiere agregar otro verbo, por ejemplo, un 'PATCH' a la ruta /users, se puede hacer agregando una función nueva, sin necesidad de modificar funciones existentes.

Liskov Substitution Principle (LSP): Se tiene la clase 'ResponseTweet', que hereda de la clase 'Tweet'. La única diferencia entre esta clase y su clase padre es que se modifica el método 'insert'. Ambos cuentan con los mismos atributos, y si la clase heredada se sustituyera por la clase padre, aún funcionaría correctamente

Interface Segregation Principle (ISP): El dashboard de eventos es una interfaz totalmente independiente de la aplicación Twitter Reloaded. Aunque el dashboard se vea afectado por la apliación, los usuarios de esta no hacen uso de las funciones del dashboard, por lo tanto, no es necesario de estén conectadas.

Dependency Inversion Principle (DIP): Se tiene la función get_data, utilizada para obtener los datos de MongoDB. Esta depende de una abstracción, que es la conexión a la base de datos. Podríamos migrar MongoDB a SQL y el único pedazo de código que deberá cambiar es la conexión a la base de datos


### Patrones de diseño:

Decoradores: Todas las rutas utilizan un decorador que agrega nueva funcionalidad a la variable app, el cual es un objeto de tipo Flask

Eager Singleton: La clase st.experimental_singleton solo es accesible a través de init_connection, es la única de su tipo, y se crea en cuanto se carga la aplicación.
