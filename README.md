![](RackMultipart20230503-1-6umn3t_html_b846257e0f7fe86e.png)

ITESM- Campus Puebla

## Trasformación digital de organizaciones de la sociedad civil

##


#
# **GUI Procesamiento distribuido**

Integrantes:

Víctor Alfonso Mancera Osorio A01733749

Uziel Humberto López Meneses A01733922

Fernando de la Torre Rodríguez A01174460

Fecha: 03/05/23

**Introducción**

En este trabajo, se exploró la creación de una aplicación de escritorio que utiliza Qt Designer para diseñar la interfaz gráfica de usuario, y se conecta con un código C para realizar un efecto de "blurring" (desenfoque) en imágenes. Para crear la interfaz gráfica de usuario, se empleará PyQt5, una biblioteca de Python que permite el desarrollo de aplicaciones de escritorio con una GUI fácil de usar y personalizable. Se han creado diversas clases y herramientas en Python, como BlurringWorker, MainApp, ImageLabel, entre otras, que facilitan la interacción entre el usuario y el algoritmo de desenfoque de imágene con el objetivo de presentar una aplicación cuyo uso proporcioer una forma fácil y accesible de aplicar el efecto de "blurring" a las imágenes, sin necesidad de tener conocimientos avanzados de ejecución de scripts.

En la primera parte del trabajo se describe el proceso de diseño de la interfaz de usuario utilizando Qt Designer, que incluye la creación de botones y widgets para cargar y mostrar imágenes, así como para aplicar el efecto de "blurring". Además, se detalla la conexión de los elementos de la interfaz con el código C utilizando las señales y ranuras de Qt.

En la segunda parte del trabajo se describe el código C utilizado para aplicar el efecto de "blurring" a las imágenes. Este código se basa en un algoritmo de procesamiento de imágenes que utiliza una técnica de suavizado para reducir el ruido y las irregularidades en la imagen.

Finalmente, se presentan los resultados de la aplicación, incluyendo ejemplos de imágenes antes y después de aplicar el efecto de "blurring". Además, se discuten las posibilidades de mejora y las aplicaciones potenciales de esta herramienta en diferentes campos, como la fotografía, el diseño gráfico y la visión por computadora.

**Metodología**

_ **Enlace al repositorio del proyecto:** _[**https://github.com/UzielLopez/image-blurer**](https://github.com/UzielLopez/image-blurer)

En el proyecto desarrollado, las entradas principales son la imagen a desenfocar, la máscara inicial, el número de máscaras a utilizar en el proceso y la dirección del directorio en donde se almacenarán las imágenes desenfocadas. La imagen se carga a través de la interfaz gráfica de usuario, donde se arrastra y suelta el archivo correspondiente en el área designada. La máscara inicial y el número de máscaras se ingresan como valores enteros en los campos correspondientes de la GUI, al igual que la dirección del directorio resultante.. Es importante tener en cuenta que la máscara inicial debe ser un número entero entre 3 y 17, mientras que el número de máscaras debe estar en el rango de 1 a 50. Estos rangos establecen las condiciones de operación del experimento y garantizan un correcto funcionamiento del algoritmo de desenfoque.

Las salidas del proyecto incluyen el resultado de la aplicación de desenfoque en la imagen proporcionada. Estos resultados se almacenan en el directorio de salida especificado por el usuario en la GUI. La imagen desenfocada se guarda con un nombre que incluye la máscara utilizada y la información del nodo del clúster que procesó la imagen.

El experimento se realiza bajo la premisa de distribuir la carga de trabajo entre los nodos disponibles del clúster de cómputo, lo cual es posible gracias a las herramientas y tecnologías mencionadas anteriormente, como MPICH, OpenMP, NFS y OpenSSH. Estas condiciones de operación permiten una ejecución eficiente y confiable del algoritmo de desenfoque de imágenes y facilitan la interacción del usuario con el proceso a través de la interfaz gráfica desarrollada en PyQt5.


_ **Comprobación del estado de los hosts de la red** _

Antes de ejecutar el comando mpirun para correr nuestro ejecutable en el clúster de MPI, desde el hilo de ejecución principal del programa de Python se comprueba el estado actual de cada uno de los nodos registrados en el archivo /etc/hosts. Esta función (check\_cluster\_status(masks: int) -\> int) se encuentra en el archivo /ui/Utils/c\_integration.py.

En esta función, se utiliza el módulo de re para identificar mediante expresiones regulares los nombres de los hosts y sus respectivas direcciones IP. Cuando estos son identificados, se utiliza el comando fping para realizar un ping rápido a cada una de las direcciones registradas y comprobar su estatus a través de un ping ICMP. Una vez se corrió el comando, se rescata del output de este y se toman las IPs disponibles para después escribir en un nuevo archivo de machinefile los nombres de los hosts disponibles, distribuyendo la carga equitativamente entre máquinas conforme al número de máscaras especificado a través del parámetro masks.

La función regresa el número de hosts disponibles en un entero que es utilizado por la clase que representa nuestra ventana principal para actualizar la GUI con la cantidad de hosts entre la que se va a distribuir la carga de trabajo.

_ **Comunicación entre el programa de Python y el programa en C** _

Cuando el usuario ha ingresado los valores correspondientes para la máscara inicial, el número de máscaras, el directorio de salida y se haya arrastrado ya la imagen que quiere procesar al espacio correspondiente, el botón de "Ejecutar" llama a la función que validator, que a su vez llama a la función execute\_blurring en caso de que todos los campos requeridos sean válidos. execute\_blurring llama invoca al método blur del objeto miembro blurringThread.

blurringThread es una instancia de una clase que extiende de la clase QThread. Esta clase nos permite crear nuevos hilos de ejecución desde el hilo principal, proceso que es necesario para evitar que la interfaz deje de responder mientras se termina de ejecutar la tarea asignada a través de MPI al nodo maestro. En cuanto se da click a Ejecutar, blurring thread utiliza su método run para ejecutar la tarea especificada y en cuanto llama con un callback a una función de la ventana principal, indicándonos que el comando terminó de correr y que por ende, se han generando todas las imágenes.

 En el código que se corre desde el hilo representado por blurringThread, se utiliza la librería subprocess para correr el comando de Linux correspondiente para ejecutar el programa de MP (en este caso mpirun), componiendo este a través de cadenas especiales para pasarle al programa algunos argumentos de ejecución como el nombre del archivo de entrada.

_ **QT Designer** _

Para el desarrollo de la GUI, se utilizó el programa de QT Designer para el diseño de la interfaz gráfica que emplea nuestro programa de C para hacer el desenfoque de imágenes; se utilizó una main windows, junto con labels, para indicar nombres, así como textEdits para poder indicar el número de máscaras y las máscaras iniciales; así como la dirección de la carpeta donde las imágenes serán generadas; finalmente un botón que abre otra ventana que permite ver la previsualización de las imágenes generadas con el código de desenfoque.

_ **Gui Drag & Drop** _

El desarrollo del drag & drop, en el código de python, fue creando un vertical layout en el Qt Designer; mediante el cual recibe el filepath; de la imagen, utilizando el QPixmap el cual es una librería que se usa para trabajar con mapas bits; que permite cargar y manipular imágenes en una aplicación Qt. Posteriormente con el filepath, lo tomamos para poder relacionarlo al código de C, en el cual tomamos el self.filepath para indicar la imagen a tomar para empezar a hacer el efecto del desenfoque.

![](RackMultipart20230503-1-6umn3t_html_dd7830ea5196a94d.jpg)

Imágen 1.2. Interfaz gráfica para ejecutar el programa en C.

**Características principales de la clase `MainPage`:**

En el código de MainPage, en la primera línea, se importan varias clases de PyQt5 necesarias para crear la GUI, como loadUi para cargar la interfaz de usuario desde un archivo .ui, y las clases para crear etiquetas, botones, ventanas y widgets.

La clase MainApp es la clase principal de la aplicación y hereda de la clase QMainWindow de PyQt5. Dentro de su método \_\_init\_\_, se carga la interfaz de usuario desde un archivo .ui utilizando la función loadUi. Luego, se crea un objeto ImageLabel personalizado que se utiliza para mostrar la imagen en la GUI, y se agrega a la GUI con el método addWidget del objeto verticalLayout. También se configura el objeto photoViewer para que se ajuste al centro y se escalen las imágenes para adaptarse al tamaño de la etiqueta.

Los métodos dragEnterEvent, dragMoveEvent y dropEvent se utilizan para permitir al usuario arrastrar y soltar una imagen en la GUI. Si el archivo arrastrado es una imagen, se llama al método set\_image para mostrar la imagen en la etiqueta photoViewer. El método set\_image utiliza la clase QPixmap de PyQt5 para cargar la imagen desde el archivo y configurarla como el pixmap de la etiqueta photoViewer.

El método validator se utiliza para validar dos entradas de texto en la GUI. Si el usuario ingresa un número entero válido en el rango especificado, se muestra un mensaje de "Óptimo". De lo contrario, se muestra un mensaje de error correspondiente.

El método getImage se utiliza para crear un widget de imagen personalizado con un borde punteado y de tamaño fijo.

En general, este código se utiliza para crear una aplicación de PyQt5 que muestra una imagen en una GUI y permite al usuario arrastrar y soltar una imagen en la GUI. Además, la aplicación tiene botones para obtener resultados y validar entradas de texto.



_ **Visualización del resultado de desenfoque** _

En el código, se posee una clase `ResultPage`, que hereda de `QMainWindow` y representa una ventana de resultados en una aplicación de escritorio PyQt5. La ventana muestra una imagen base y permite a los usuarios navegar entre las imágenes procesadas (desenfocadas) mediante botones para ir a la imagen anterior o siguiente.

**Secciones principales del código:**

1. Importación de bibliotecas y módulos necesarios.

2. Definición de la clase `ResultPage`, que hereda de `QMainWindow`. Esta clase define la interfaz de usuario y maneja eventos como cambiar la imagen mostrada.

3. Funciones auxiliares para crear y configurar elementos de la interfaz de usuario, como botones y etiquetas de imagen.

**Características principales de la clase `ResultPage`:**

- Al inicializar la instancia de `ResultPage`, carga la interfaz de usuario desde el archivo 'results.ui' y configura los elementos básicos de la ventana, como la etiqueta de la imagen principal, la etiqueta del título de la imagen y los botones para navegar entre las imágenes.

- La función `evaluateButtonsEnable()` habilita o deshabilita los botones "Anterior" y "Siguiente" según la posición de la imagen actual en la lista de imágenes.

- La función `clickChangeImage()` se conecta a los botones "Anterior" y "Siguiente" y actualiza la imagen mostrada cuando se hace clic en uno de estos botones.

- La función `changePixelmapMainImage()` actualiza el mapa de píxeles de la imagen principal en función de la ruta de la imagen proporcionada.

- Las funciones `createButtonGroup()` y `createLabelForImages()` son funciones auxiliares para crear y configurar grupos de botones y etiquetas de imagen, respectivamente.

Cuando el usuario hace clic en los botones "Anterior" y "Siguiente", la aplicación actualiza la imagen mostrada y el título de la imagen de acuerdo con la lista de imágenes procesadas. Los botones se habilitan o deshabilitan de acuerdo con la posición actual en la lista de imágenes.

![](RackMultipart20230503-1-6umn3t_html_5847228aa6792294.jpg)

Imágen 1.4. Pantalla 'MainResult', generada a partir del código de python.

**Documentación de la clase:**

Clase `ResultPage` (más detalles):

- Constructor ` __init__ (self, baseImage)`:

- Acepta como argumento `baseImage`, que es la imagen base que se muestra al inicio.

- Carga la interfaz de usuario desde el archivo 'results.ui'.

- Inicializa el atributo `currentImageIndex` a 0, que representa el índice de la imagen actual en la lista de imágenes.

- Inicializa el atributo `images` como una lista que contiene la imagen base.

- Crea la etiqueta de la imagen principal (`mainImageLabel`) utilizando la función `createLabelForImages()`.

- Crea la etiqueta del título de la imagen (`imageTitleLabel`) y la agrega a `verticalLayout`.

- Crea los botones "Anterior" y "Siguiente" (`prevButton` y `nextButton`) utilizando la clase `CustomButton`, y les asigna la función `clickChangeImage()` como controlador de eventos de clic. Inicialmente, ambos botones están deshabilitados.

- Crea un grupo de botones utilizando la función `createButtonGroup()` y lo agrega a `verticalLayout`.

- Función `evaluateButtonsEnable(self)`:

- Habilita el botón "Siguiente" si `currentImageIndex` es menor que `len(self.images) - 1`, de lo contrario, lo deshabilita.

- Habilita el botón "Anterior" si `currentImageIndex` es mayor que 0, de lo contrario, lo deshabilita.

- Función `clickChangeImage(self, button: CustomButton)`:

- Acepta como argumento `button`, que es una instancia de `CustomButton`.

- Modifica `currentImageIndex` en función del tipo de botón (`"NEXT"` o `"PREV"`).

- Llama a `evaluateButtonsEnable()` para actualizar el estado habilitado/deshabilitado de los botones "Anterior" y "Siguiente".

- Si el `currentImageIndex` está dentro del rango de la lista `images`, actualiza el mapa de píxeles de la imagen principal y el texto de `imageTitleLabel` utilizando la función `changePixelmapMainImage()`.

- Función `changePixelmapMainImage(self, imagePath: str)`:

- Acepta como argumento `imagePath`, que es la ruta de la imagen a mostrar.

- Carga la imagen en un objeto `QPixmap`.

- Escala la imagen a un tamaño de 320x240 píxeles.

- Establece el mapa de píxeles de `mainImageLabel` como la imagen escalada.

- Función `createButtonGroup(self) -\> QWidget`:

- Crea un objeto `QWidget` llamado `buttonsWidget` para contener los botones "Anterior" y "Siguiente".

- Crea un objeto `QHBoxLayout` y lo asigna a `buttonsWidget`.

- Agrega `prevButton` y `nextButton` al layout horizontal.

- Retorna `buttonsWidget`.

- Función `createLabelForImages(self) -\> QLabel`:

- Crea un objeto `ImageLabel` llamado `mainImageLabel`.

- Carga la imagen inicial (en el índice `currentImageIndex` de la lista `images`) en un objeto `QPixmap`.

- Escala la imagen a un tamaño de 320x240 píxeles.

_ **Implementación de evaluación de resultados** _

Se posee una función llamada 'getAllImages` que busca y carga imágenes desde un directorio especificado, y luego actualiza la ventana de resultados de la aplicación con las imágenes encontradas.

1. Importaciones:

- `os`: Módulo que provee funciones para interactuar con el sistema operativo.

- `re`: Módulo de expresiones regulares.

- `Image`: Clase `Image` de la biblioteca PIL (Python Imaging Library) para manejo de imágenes.

2. Definición de la función `getAllImages(imagesPath: str, app)`:

- `imagesPath`: Ruta del directorio donde buscar imágenes.

- `app`: Instancia de la ventana de resultados de la aplicación (clase `ResultPage`).

3. Verificación del límite de imágenes:

- Si el número de imágenes en `app.images` es mayor o igual a 40, la función imprime un mensaje y retorna sin hacer nada.

4. Creación de una lista para almacenar las nuevas imágenes encontradas:

- `images = []`: Lista vacía para almacenar las rutas de las nuevas imágenes reconocidas.

5. Búsqueda de imágenes en el directorio:

- `for file in os.listdir(imagesPath):`: Itera sobre todos los archivos en el directorio especificado por `imagesPath`.

- Si el archivo tiene la extensión ".bmp", continúa con el siguiente paso. De lo contrario, pasa al siguiente archivo.

- `imagePath = imagesPath + "/" + file`: Construye la ruta completa del archivo de imagen.

- Intenta abrir la imagen con `Image.open(imagePath)`. Si la imagen no se puede abrir, imprime un mensaje indicando que la imagen aún se encuentra en construcción y omite este archivo.

- Si la imagen se puede abrir y aún no está en `app.images`, la añade a la lista `images` e imprime un mensaje. De lo contrario, imprime un mensaje indicando que la imagen ya ha sido añadida a la aplicación.

6. Ordena la lista de imágenes encontradas:

- `images.sort(key=lambda f: int(re.sub('\D', '', f)))`: Ordena la lista `images` en base a los números contenidos en los nombres de archivo, utilizando una expresión regular para eliminar todos los caracteres no numéricos.

7. Extiende la lista de imágenes de la aplicación con las nuevas imágenes encontradas:

- `app.images.extend(images)`: Añade las imágenes de la lista `images` a la lista `app.images`.

8. Evalúa si los botones de navegación de la ventana de resultados deben habilitarse o deshabilitarse:

- `app.evaluateButtonsEnable()`: Llama al método `evaluateButtonsEnable` de la instancia `app` de la ventana de resultados.

9. Imprime un separador:

- `print("--------------------")`: Imprime una línea de guiones para separar la salida de diferentes llamadas a la función `getAllImages`.

_ **Descripción del método principal** _

Este código es el punto de entrada principal de la aplicación. Aquí se crean e inicializan las ventanas principales de la aplicación y se inicia el ciclo de eventos de la aplicación.

1. Importaciones:

- `sys`: Módulo de utilidades de sistema.

- `QApplication`: Clase principal que administra la aplicación y su ciclo de vida.

- `QTimer`: Clase de temporizador para realizar tareas periódicas.

- `MainApp`: Clase que representa la ventana principal de la aplicación (importada desde `Pages.MainPage`).

- `ResultPage`: Clase que representa la ventana de resultados (importada desde `Pages.ResultPage`).

- `getAllImages`: Función auxiliar que obtiene todas las imágenes en un directorio (importada desde `Utils.index`).

2. Verificación de la función principal:

- `if __name__ == " __main__":` verifica si este script se está ejecutando como el punto de entrada principal de la aplicación.

3. Creación de la aplicación:

- `app = QApplication(sys.argv)`: crea una instancia de la aplicación PyQt.

4. Inicialización de variables y objetos:

- `results = False`: variable booleana que indica si se deben mostrar los resultados.

- `imagePath = ["/"]`: lista con un solo elemento, que es una cadena que representa la ruta de la imagen.

- `resultsPage = ResultPage("/")`: crea una instancia de `ResultPage`.

- `configPage = MainApp(resultsPage, imagePath)`: crea una instancia de `MainApp` y le pasa la instancia de `ResultPage` y la ruta de la imagen.

5. Mostrar la ventana principal:

- `configPage.show()`: muestra la ventana principal de la aplicación (`MainApp`).

6. Temporizador:

- `timer = QTimer()`: crea un objeto `QTimer`.

- `timer.timeout.connect(lambda: getAllImages(imagePath[0], resultsPage))`: conecta la señal de tiempo agotado del temporizador a una función anónima (lambda) que llama a `getAllImages` con la ruta de la imagen y la instancia de `ResultPage`. La función `getAllImages` se ejecutará cada vez que se agote el tiempo del temporizador.

- `timer.start(5000)`: inicia el temporizador con un intervalo de 5000 milisegundos (5 segundos). La función `getAllImages` se llamará cada 5 segundos.

7. Ejecución y salida de la aplicación:

- `sys.exit(app.exec_())`: inicia el ciclo de eventos de la aplicación y espera a que se cierre la aplicación. Cuando la aplicación se cierra, el programa termina con el código de salida devuelto por `app.exec_()`.

En resumen, este código crea e inicia una aplicación PyQt que muestra una ventana principal (`MainApp`) y utiliza un temporizador para actualizar la ventana de resultados (`ResultPage`) cada 5 segundos con nuevas imágenes obtenidas de la ruta especificada en `imagePath`.

**Resultados**

**Conclusiones**

_ **Victor Mancera:** _

La práctica presentada en este informe demuestra cómo es posible implementar y utilizar un clúster de cómputo distribuido basado en MPICH para ejecutar aplicaciones paralelas de alto rendimiento, en este caso, un algoritmo de desenfoque de imágenes. Se han considerado elementos esenciales como la comunicación eficiente entre los nodos del clúster mediante MPICH, la utilización de tecnologías como NFS y OpenSSH para facilitar el acceso a los archivos y la seguridad en las conexiones, y la aplicación de OpenMP para aprovechar el paralelismo a nivel de hilos en cada máquina.

La interfaz gráfica desarrollada en PyQt5 permite al usuario interactuar fácilmente con el proceso de

desenfoque, proporcionando entradas como la imagen a desenfocar, la máscara inicial y el número de máscaras a utilizar. Estos parámetros determinan la respuesta del experimento y pueden ajustarse según las necesidades específicas del usuario. Asimismo, la selección del directorio de salida para almacenar los resultados permite un fácil acceso y análisis de los datos generados.

Para modificar la respuesta de acuerdo a los datos del experimento, se pueden ajustar los parámetros de entrada, como la máscara inicial y el número de máscaras, en función de las características de la imagen y el nivel de desenfoque deseado. Además, se puede explorar la posibilidad de incorporar nuevas técnicas de paralelismo o mejorar las existentes para optimizar aún más la ejecución del algoritmo.

Esta práctica destaca la importancia de las herramientas y tecnologías utilizadas en la creación de un clúster de cómputo distribuido y la implementación de aplicaciones paralelas, así como la flexibilidad y capacidad de adaptación de la solución propuesta para ajustarse a diferentes escenarios y requerimientos. El trabajo realizado sienta las bases para futuras mejoras y aplicaciones en el ámbito del cómputo distribuido y paralelo.

**Uziel**

A lo largo de este módulo, fuimos construyendo de manera incremental el código en C necesario para realizar el procesamiento de las imágenes de forma distribuida, reduciendo el tiempo total tomado para generar las imágenes necesarias con cada entrega. Todo este proceso fue sumamente técnico y requirió muchas horas de trabajo principalmente por dificultades en la configuración de las máquinas virtuales y problemas específicos a la distribución de Linux que utilizamos.

Sin embargo, para que el programa y toda su capacidad pueda ser utilizada por la mayor cantidad de usuarios se requiere que este sea accesible y fácil de utilizar. Si bien los comandos requeridos para hacerlo funcional son sencillos, la realidad es que la mayor parte de la gente que utilizaría un programa de este tipo no se sentiría cómoda escribiendo comandos en terminal. Por ello, es importante que como ingenieros entendamos el funcionamiento de cada una de las partes de nuestro código para así tener la capacidad de adaptarlo para distintos casos de uso y distintos usuarios meta.

 Esto implicó, entre otras cosas, saber identificar la necesidad de distribuir las funciones del programa entre más de un hilo de ejecución para permitir que el usuario aún pudiera interactuar con la interfaz gráfica mientras en el fondo se siguen generando las imágenes desenfocadas. Es indispensable que como ingenieros de software tengamos la capacidad de identificar estas necesidades para saber cómo tenemos que implementar nuestro código de tal forma que se garantice la usabilidad del programa por parte de los usuarios meta.

**Fer**

Juntando lo aprendido a lo largo del módulo, el código de blurring, junto con la implementación de la paralelización por parte de las máquinas virtuales; el proyecto que conectó tres máquinas virtuales para dividir el proceso de ejecución de un programa en C, y que además implementó una interfaz gráfica diseñada en QT Designer y programada en pyQT5, resultó en una solución eficiente y escalable para la ejecución de procesos pesados.

La división del proceso de ejecución en tres máquinas virtuales permitió aprovechar la capacidad de procesamiento de cada una de ellas, lo que mejoró significativamente el rendimiento del programa en comparación con la ejecución en una sola máquina.

Además, la implementación de una interfaz gráfica intuitiva y fácil de usar diseñada en QT Designer y programada en pyQT5, brindó al usuario una experiencia más amigable y cómoda al interactuar con el programa.

En general, este proyecto es una solución altamente recomendable para procesos que requieren alta capacidad de procesamiento y que además necesitan de una interfaz gráfica para interactuar con el usuario. Lo cual también ayudó a una implementación más intuitiva además de eficiente gracias a la interfaz gráfica, que permite al usuario controlar la ejecución del programa.
