from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Banco de preguntas extraído de tu PDF [cite: 3, 6, 12]
preguntas_db = [
    {
        "id": 1,
        "pregunta": "¿Cuáles de los siguientes enunciados son ciertos en relación con la cuantización?",
        "opciones": [
            "Permite manejar el error de cuantización mediante el número de bits.",
            "Ninguna de las opciones",
            "Reproduce fielmente la amplitud de la señal continua original",
            "Introduce errores debido a la pérdida de precisión numérica",
            "El número de niveles no está relacionado con el número de bits",
            "Lalongitud de la señal muestreada depende del numero de bits del cuantizador"
        ],
        "correctas": [0, 3], # [cite: 35]
    },
    {
        "id": 2,
        "pregunta": "Teniendo en cuenta la norma-p, para p=1 indique cuáles de los siguientes enunciados son correctos:",
        "opciones": [
            "Está directamente relacionada con la energía",
            "Proporciona información acerca del 'tamaño' de una señal x",
            "También se conoce como acción",
            "Ninguna de las opciones",
            "Corresponde a la amplitud de la señal"
        ],
        "correctas": [1, 2], # [cite: 45]
    },
    {
        "id": 3,
        "pregunta": "Al aplicar la Transformada Discreta de Fourier, la señal y su transformada son:",
        "opciones": [
            "Discreta en el dominio temporal y continua en el dominio frecuencial",
            "Discreta en el dominio temporal y discreta en el dominio frecuencial",
            "Continua en el dominio temporal y discreta en el dominio frecuencial",
            "Ninguna de las opciones"
        ],
        "correctas": [1], # [cite: 53]
    },
    {
        "id": 4,
        "pregunta": "Clasifique el sistema y[n]=x[n]+2x[n-1]-0.5x[n-5]",
        "opciones": ["ARMA", "MA", "FIR", "IIR"],
        "correctas": [1, 2], # [cite: 67]
    },
    {
        "id": 5,
        "pregunta": "Seleccione los enunciados correctos:",
        "opciones": [
            "Se puede representar la señal de entrada de un sistema LTI en terminos de un conjunto de señales basicas y utilizar el principio de superposicion para determinar la salida de un sistema en terminos de sus respuestas a estas señales basicas",
            "La superposicion es una de las propiedades mas importantes de los sistemas lineales e invariantes en el tiempo (LTI)",
            "Ninguna de las opciones es correcta."
        ],
        "correctas": [0, 1], # [cite: 76]
    },
    {
        "id": 6,
        "pregunta": "Señales las opciones correctas",
        "opciones": [
            "La transformada de fourier de una secuencia discreta es la transformada Z de la secuencia evaluda sobre el eje imaginario",
            "Ninguna de las opciones es correcta.",
            "La transformada de fourier de una secuencia discreta es la transformada Z de la secuencia evaluada fuera delcirculo unitario",
            "La transformada de fourier de una secuencia discreta es la transformada Z de la secuencia evaluada sobre delcirculo unitario"
        ],
        "correctas": [3], # [cite: 85]
    },
    {
        "id": 7,
        "pregunta": "Teniendo en cuenta la definicion de producto interno indique cuales de los siguientes enunciados son correctos",
        "opciones": [
            "Es posible interpretar la Transformada de Fourier como un producto interno entre señales exponenciales complejas",
            "Induce una norma sobre el espacio en el que está definido",
            "Ninguna de las opciones",
            "Es una función de dos señales o vectores que devuelve un valor real positivo",
            "Proporciona información acerca de la similitud entre una señal x y otra señal y",
            "Si su valor es igual a cero significa que las señales son ortonormalles"
        ],
        "correctas": [1, 4], # [cite: 147]
    },
    {
        "id": 8,
        "pregunta": "Al aplicar la Transformada Discreta de Fourier a una señal, la misma resulta ser.",
        "opciones": [
            " Discreta y aperiódica",
            "Continua y periódica",
            "Continua y aperiódica.",
            "Discreta y periódica"
        ],
        "correctas": [3],
    },
    {
        "id": 9,
        "pregunta": "Clasifique el sistema y[n] = x[n] + 2",
        "opciones": [
            "Causal",
            "Ninguna de las opciones.",
            "Linea",
            "Invariante en el tiempo",
            "Con memoria"
        ],
        "correctas": [0, 3],
    },
    {
        "id": 10,
        "pregunta": "Elija las afirmaciones verdaderas para la convolución lineal y la convolución circular",
        "opciones": [
            "La convolución lineal puede calcularse a partir de la convolución circular",
            "La convolución circular puede calcularse mediante la propiedad de convolución circular de la Transformada Discreta de Fourier",
            "La convolución lineal se puede obtener agregando unos a una de las señales a convolucionar y haciendo una convolución circular",
            "La convolución circular y la convolución lineal de dos señales producen resultados de igual longitud",
            "La convolución circular puede obtenerse truncando la convolución lineal",
            "La convolución circular es la convolución para señales periódicas"
        ],
        "correctas": [0, 1, 5],
    },
    {
        "id": 11,
        "pregunta": "¿Cuál de las siguientes afirmaciones se corresponde con la clasificación fenomenológica de las señales?",
        "opciones": [
            "En términos estrictos, las computadoras pueden manejar únicamente señales digitales, ya que las señales discretas pueden ser discretas en el tiempo pero pueden no serlo en amplitud.",
            "Una señal se puede definir como deterministica si sus valores son conocidos de antemano o pueden ser predichos exactamente.",
            "Las señales digitales son señales de tiempo discreto cuyos valores en amplitud son cuantizados.",
            "En el caso en que la amplitud y la variable independiente sean continuas, entonces la señal es analógica."
        ],
        "correctas": [1],
    },
    {
        "id": 12,
        "pregunta": "¿Cuáles son los principales efectos de convertir una señal analógica en digital?",
        "opciones": [
            "Se pierden los cambios más rápidos que la duración de la señal",
            "Ninguna de las opciones",
            "La precisión de la cuantización de la señal depende sólo del número de bits disponible.",
            "La variable dependiente posee un número finito de valores posibles",
            "La variable independiente es distinta de 0 sólo para algunos valores particulares",
            "La máxima frecuencia disponible para estas señales es dos veces la frecuencia de muestreo x"
        ],
        "correctas": [3, 4],
    },
    {
        "id": 13,
        "pregunta": "Teniendo en cuenta las denominadas Distancias de Minkowski indique cuales de los siguientes enunciados son correctos:",
        "opciones": [
            "Ninguna de las opciones",
            "La distancia Euclidea y la de Manhattan devuelven el mismo resultado entre dos señales",
            "Si sumo las distancias entre tres señales tomadas de a pares el resultado es igual a la distancia entre cualquiera de ellas x",
            "Constituyen una familia de métricas definidas a partir de la norma p",
            "La sumatoria de las diferencias de las señales al cuadrado es la distancia Euclidea"
        ],
        "correctas": [3],
    },
    {
        "id": 14,
        "pregunta": "Seleccione cuales son propiedades de la transformada de Fourier Discreta:",
        "opciones": [
            "La transformada del producto de dos señales es la convolución circular de las transformadas de las señales ",
            "La transformada de una señal retardada en un instante es el conjugado de la transformada de la señal sin retardar",
            "La transformada de una convolución circular de dos señales es el producto de las transformadas de las señales",
            "La transformada de una suma de señales es la suma de las transformadas de las señales.",
            "La transformada del producto de dos señales temporales es el producto de la transformada de la primer señal, por el conjugado de la segunda señal",
            "La transformada del producto de dos señales es la convolución de las transformadas de las señales",
            "La transformada de una convolución de dos señales es el producto de las transformadas de las señales"
        ],
        "correctas": [0,2,3],
    },
    {
        "id": 15,
        "pregunta": "Clasifique el sistema y[n] = exp(x[n])",
        "opciones": [
            "Ninguna de las opciones",
            "Invariante en el tiempo",
            "Con memoria",
            "Causal",
            "Lineal"
        ],
        "correctas": [1,3],
    },
    {
        "id": 16,
        "pregunta": "Seleccione los enunciados correctos:",
        "opciones": [
            "Una multiplicación en el dominio del tiempo implica una convolución en la frecuencia o a la inversa, una multiplicación en el dominio de la frecuencia implica una convolución en el tiempo.",
            "Ninguna de las opciones",
            "La convolución es uno de los procesos más importantes y eficaces en el análisis de sistemas LT, ya que permite establecer una relación entre la entrada y la salida en el dominio del tiempo y el de la frecuencia."
        ],
        "correctas": [0, 2],
    },
    {
        "id": 17,
        "pregunta": "La Transformada Z de una secuencia discreta y real es",
        "opciones": [
            "Una función simétrica continua de variable real",
            "Una función continua de variable compleja y que toma valores complejos",
            "Una secuencia discreta con valores reales",
            "Otra secuencia discreta pero que puede tomar valores complejos"
        ],
        "correctas": [1],
    },
    {
        "id": 18,
        "pregunta": "Cuáles de las siguientes son suposiciones que se hacen al aplicar predicción lineal?:",
        "opciones": [
            "Se debe poder asegurar que el comportamiento del sistema que se quiere identificar es lineal",
            "Se deben conocer los valores actuales y pasados de la entrada del sistema",
            "La señal generada por el sistema es estacionaria o estacionaria por tramos",
            "El comportamiento del sistema se puede aproximar suficientemente bien mediante un modelo lineal",
            "Se deben conocer los valores actuales y pasados de la salida del sistema",
            "Ninguna de las opciones"
        ],
        "correctas": [2,3,4],
    },
    {
        "id": 19,
        "pregunta": "Seleccione la opcion Verdadera según corresponda",
        "opciones": [
            "La norma-p mide la energía de una señal.",
            "Un espacio vectorial es un conjunto de señales que cumplen ciertas propiedades algebraicas.",
            "Una base ortogonal es un conjunto de señales linealmente independientes.",
            "Un espacio de señales puede ser finito o infinito dimensional.",
            "Si dos señales son ortogonales, entonces su producto interno es cero."
        ],
        "correctas": [1,2,3,4],
    },
    {
        "id": 20,
        "pregunta": "Seleccione la opcion Verdadera según corresponda",
        "opciones": [
            "La TDF se puede utilizar para calcular la convolución circular de dos señales.",
            "La TDF puede utilizarse para analizar señales en tiempo discreto, pero no en tiempo continuo.",
            "Si la señal original es real y de duración finita, el espectro de la TDF es simétrico.",
            "La TDF de una señal de duración finita siempre produce un espectro discreto.",
            "La TDF de una señal siempre da una señal con valores complejos"
        ],
        "correctas": [0,1,2,3],
    },
    {
        "id": 21,
        "pregunta": "Seleccione la opcion Verdadera según corresponda",
        "opciones": [
            "En los métodos estáticos para resolver el sistema de ecuaciones simultáneas de Wiener-Hopf, la función objetivo es una estimación del Error Cuadritico Total (ECT).",
            "En los métodos adaptativos, se optimiza instante a instante según el Error Cuadratico Total",
            "El método de Levinson-Durbin para resolver el sistema de ecuaciones es método predilecto para los métodos adaptativos.",
            "En el método adaptativo de Widrow se utiliza el error cuadrático instantaneo como una aproximación válida para el error cuadrático esperado.",
            "Para identificar un sistema solo se necesitan conocer los coeficientes del mismo.",
            "El criterio de Akaike sirve para determinar la ganancia del sistema.",
            "El error de predicción final se utiliza para la determinación del orden del sistema"
        ],
        "correctas": [0,2,3,6],
    },
    {
        "id": 22,
        "pregunta": "Una señal de voz registrada a una persona mientras habla se puede clasificar como",
        "opciones": [
            "Deterministica",
            "Aleatoria",
            "Estacionaria",
            "Periódicas",
            "Estacionaria por tramos",
            "Armónicas",
            "Pseudo Aleatorias",
            "Transitorias",
            "Cuasi Periodica",
            "No Ergodicas",
            "Periódicas",
            "Ninguna es correcta."
        ],
        "correctas": [4],
    },
    {
        "id": 23,
        "pregunta": " Una baja relación señal ruido indica que la señal:",
        "opciones": [
            "es fácil de entender",
            "es dificil de entender",
            "es compleja",
            "no tiene ruido",
            "tiene mucho ruido",
            "tiene poco ruido",
            "es dificil de analizar",
            "Ninguna es correcta"
        ],
        "correctas": [4],
    },
    {
        "id": 24,
        "pregunta": "Seleccione la opcion Verdadera según corresponda",
        "opciones": [
            "La norma infinito mide la amplitud de la señal",
            "Un espacio vectorial es un conjunto vectores en R^60 que cumplen ciertas propiedades algebraicas.",
            "La norma depende de un elemento del espacio mientras que la distancia depende de dos elementos.",
            "La norma nos proporciona información acerca de la estructura de la señal.",
            "La norma siempre es un numero reall no negativo.",
            "La norma 0 indica la cantidad de elementos de la señal iguales a cero."
        ],
        "correctas": [0,1,2,4],
    },
    {
        "id": 25,
        "pregunta": "Si una señal compuesta por la suma de dos senoidales de 10, 30 y 60 Hz se muestrea a una frecuencia de muestreo de 100Hz:",
        "opciones": [
            "Posee 2 picos en su espectro (10 y 30 Hz)",
            "Posee 3 picos en su espectro(10, 30 y 60Hz)",
            "Posee 3 picos en su espectro(0, 10 y 30Hz)",
            "Posee 3 picos en su espectro(10, 30 y 50 Hz)",
            "Posee 3 picos en su espectro(10, 30 y 40 Hz)",
            "Ninguna es correcta."
        ],
        "correctas": [4],
    },
    {
        "id": 26,
        "pregunta": "El teorema del desplazamiento",
        "opciones": [
            "Asegura que las transformaciones conformes siempre conserven la estabilidad del sistema",
            "Permite convertir una ecuación en diferencias en una razón de polinomios en z",
            "Permite calcular la Transformada Z inversa x",
            "Se aplica al pasar del plano s al plano z"
        ],
        "correctas": [1],
    },
    {
        "id": 27,
        "pregunta": "¿Cuáles de las siguientes aseveraciones respecto del ruido son ciertas?",
        "opciones": [
            "Cualquier serial que interfiere con la percepción o registro de otra",
            "Ninguna de las opciones",
            "Lo que es considerado como ruido o señal de interés es relativo",
            "Cualquier señal aleatoria puede ser considerada ruido",
            "Una señal deterministica nunca puede considerarse como ruido"
        ],
        "correctas": [0,2],
    },
    {
        "id": 28,
        "pregunta": "Teniendo en cuenta la definición de métrica indique cuáles de los siguientes enunciados son correctos:",
        "opciones": [
            "Ninguna de las opciones",
            "Cumple con la desigualdad del triángulo",
            "Se puede definir a partir de una norma",
            "Satisface la propiedad de que d(x, y) = d(y, x)",
            "Es una función d(x, y) que devuelve un valor real",
            "Satisface la propiedad de que d(x, y)=0 si y sólo si x=y",
            "Proporciona información acerca del distancia entre una señal x y otra señal y"
        ],
        "correctas": [1,2,3,5,6],
    },
    {
        "id": 29,
        "pregunta": "Si se tiene una señal continua z(t)=sin(2x5t)+sin(2x10r) +6, la cual es muestreada a una frecuencia de 18 Hz durante un segundo, obteniendo una secuencia z[n] de 18 muestras, ¿cuáles de las siguientes afirmaciones son correctas?",
        "opciones": [
            "El espectro de magnitud de z presenta energia en las frecuencias: 5 Hz, 10 Hz y 0 Hz",
            "El espectro de magnitud de z presenta energia en las frecuencias: 5 Hz, 9 Hz y 0 Hz",
            "El espectro de magnitud de z presenta energía en las frecuencias: 5 Hz, 8 Hz y 0 Hz",
            "l espectro de magnitud de z presenta energía en las frecuencias: 5 Hz y 10 Hz",
            "La resolución frecuencial es de 0.5 Hz",
            "La resolución frecuencial es de 2 Hz",
            "La resolución frecuencial es de 1 Hz"
        ],
        "correctas": [2, 6],
    },
    {
        "id": 30,
        "pregunta": "¿Cuántos elementos tiene convolución lineal de dos señales de N y M muestras?",
        "opciones": [
            "(N+M-1) muestras",
            " N+M muestras",
            "M muestras",
            "Ninguna de las opciones",
            "N muestras"
        ],
        "correctas": [0],
    },
    {
        "id": 31,
        "pregunta": "La transformación conforme Bilineal",
        "opciones": [
            "No requiere ninguna consideración especial en relación a la frecuencia de muestreo más x allá de que se cumpla con el teorema de Nyquist",
            "Alcanza su máxima precisión para las componentes de alta frecuencia",
            "Mapea la infinito del sistem continuo en -pi del plano z",
            "El sistema obtenido puede implementarse con menos costo computacional que el que x se obtendría aplicando la transformación de Euler"
        ],
        "correctas": [2],
    },
    {
        "id": 32,
        "pregunta": "¿Por qué los polos deben estar dentro del círculo unitario?",
        "opciones": [
            "Porque así el círculo unitario en Z se mapea correctamente el semiplano izquierdo de s.",
            "Porque de esa forma sabemos que la respuesta al impulso del sistema se agota en un tiempo finito.",
            "Porque se asegura la estabilidad del sistema.",
            "Porque es un sistema lineal e invariante en el tiempo."
        ],
        "correctas": [2],
    },
    {
        "id": 33,
        "pregunta": "¿Cuáles son las características típicas de una señal aleatoria o estocástica?",
        "opciones": [
            "Ninguna de las opciones",
            "La media",
            "El periodo",
            "El desvío estánda",
            "La varianza"
        ],
        "correctas": [1,3,4],
    },
    {
        "id": 34,
        "pregunta": "Seleccione las propiedades de la convolución discreta:",
        "opciones": [
            "Asociativa: x*(y*w) = (x*y)*w",
            "Conmutativa: y*x = x*y",
            "Ninguna de las opciones"
        ],
        "correctas": [0,1],
    },
    {
        "id": 35,
        "pregunta": "¿Cuál es la clasificación fenomenológica de una señal senoidal?",
        "opciones": [
            "Determinística",
            "Pseudoaleatorias",
            "Sinusoidal",
            "Periódica",
            "Ninguna de las opciones",
            "Armónicas"
        ],
        "correctas": [0,2,3],
    },
    {
        "id": 36,
        "pregunta": "Seleccione la opcion Verdadera según corresponda en cuanto a las ecuaciones en diferencias",
        "opciones": [
            "Son la representación matemática de los sistemas discretos no lineales.",
            "Permiten calcular la salida de un sistema ante cualquier entrada.",
            "Son el equivalente discreto a transformada de Laplace.",
            "Permiten clasificar los sistemas en AR,MA O ARMA.",
            "Permiten estudiar las propiedades del sistema."
        ],
        "correctas": [1,3,4],
    },
    {
        "id": 37,
        "pregunta": "Dada dos señales x = [101] y h = [27], la convolución lineal x*h es:",
        "opciones": [
            "x*h = [27]",
            "Ninguna de las opciones",
            "x*h = [2277]",
            "x*h = [2727]",
            "x*h = [2227]"
        ],
        "correctas": [3],
    },
    {
        "id": 38,
        "pregunta": "¿Cuántos elementos tiene convolución circular de dos señales de N muestras?",
        "opciones": [
            "2*N muestras",
            "(2*N-1) muestras",
            "N muestras",
            "Ninguna de las opciones"
        ],
        "correctas": [2],
    },
    {
        "id": 39,
        "pregunta": "Clasifique el sistema y[n] = a[n]+2x[n-1]",
        "opciones": [
            "Ninguna de las opciones.",
            "Con memoria",
            "Lineal",
            "Causal",
            "Invariante en el tiempo"
        ],
        "correctas": [1,2,3,4],
    },
    {
        "id": 40,
        "pregunta": "Seleccione la opcion Verdadera según corresponda",
        "opciones": [
            "Todos los sistemas de tipo MA son FIR",
            "Un sistema de tipo MA puede ser IIR.",
            "Todos los sistemas de tipo AR son IIR.",
            "Los sistemas IIR pueden ser de tipo AR O ARMA",
            "Todos los sistemas de tipo ARMA son FIR."
        ],
        "correctas": [0,2,3],
    },
    {
        "id": 41,
        "pregunta": "¿Cuáles de estas funciones pueden utilizarse para interpolación?",
        "opciones": [
            "Función sinc",
            "Función escalón",
            "Ninguna de las opciones",
            "Función lineal",
            "Función delta de Dirac"
        ],
        "correctas": [0,1,3],
    },
    {
        "id": 42,
        "pregunta": "Señale los efectos de utilizar ventanas rectangulares en el espectro de las señales resultantes:",
        "opciones": [
            "Rizado en alta frecuencia",
            "Rizado en las bajas frecuencia",
            "Aliasing",
            "Ninguna de las opciones."
        ],
        "correctas": [0],
    },
    {
        "id": 43,
        "pregunta": "¿Cuáles de los siguientes son pasos necesarios para la conversión de una señal analógica en digital?",
        "opciones": [
            "Muestreo",
            "Cuantización",
            "Ventaneo",
            "Normalización",
            "Codificación",
            "Retención",
            "Ninguna de las opciones",
            "Eliminación de la media"
        ],
        "correctas": [0,1,2,4,5],
    },
    {
        "id": 44,
        "pregunta": "Seleccione cuáles son las fórmulas para el cálculo de la resolución frecuencial",
        "opciones": [
            "f=T0/1",
            "f=1/NT",
            "f=1/T0",
            "f=fm/N"
        ],
        "correctas": [1,2,3],
    },
    {
        "id": 45,
        "pregunta": "Selecciones las afirmaciones verdaderas:",
        "opciones": [
            "En un sistema invariante en el tiempo un desplazamiento en la entrada produce el mismo desplazamiento en la salida",
            "En un sistema invariante en el tiempo los coeficientes que definen la dinámica del sistema pueden no ser constantes.",
            "Un sistema es inestable si su salida diverge para una entrada acotada.",
            "Todo sistema que cumple con la propiedad de superposición es LTI",
            "Los sistemas incrementalmente lineales responden en forma lineal a cambios en la entrada."
        ],
        "correctas": [0,2,4],
    },
    {
        "id": 46,
        "pregunta": "Seleccione los enunciados correctos:",
        "opciones": [
            "Una multiplicación en el dominio del tiempo implica una convolución en la frecuencia o a la inversa, una multiplicación en el dominio de la frecuencia implica una convolución en el tiempo.",
            "Ninguna de las opciones",
            "La convolución es uno de los procesos más importantes y eficaces en el análisis de sistemas LTI, ya que permite establecer una relación entre la entrada y la salida en el dominio del tiempo y el de la frecuencia."
        ],
        "correctas": [0,2],
    },
    {
        "id": 47,
        "pregunta": "¿Cuáles de los siguientes enunciados son ciertos para un proceso aleatorio?",
        "opciones": [
            "Estacionariedad no implica ergodicidad",
            "Ninguna de las opciones",
            "Una realización difiere de otra sólo por su valor medio",
            "Técnicamente es un sinónimo de señal aleatoria",
            "Las señales ergódicas pueden considerarse deterministicas",
            "Es no estacionario cuando sus parámetros estadisticos no se mantienen constantes"
        ],
        "correctas": [0,5],
    },
    {
        "id": 48,
        "pregunta": "Teniendo en cuenta la definición de norma indique cuáles de los siguientes enunciados son correctos:",
        "opciones": [
            "Satisface la desigualdad triangular",
            "Ninguna de las opciones",
            "Es una función de dos elementos del espacio que devuelve un valor real positivo",
            "Proporciona información acerca del tamaño de una señal x",
            "Proporciona información acerca de la distancia de una señal x a la señal con todos sus elementos iguales a 0 (origen de coordenadas)",
            "Es homogénea con respecto a la escala"
        ],
        "correctas": [3,4,5],
    },




]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar_parcial')
def generar_parcial():
    # Selecciona 5 preguntas aleatorias [cite: 12]
    seleccion = random.sample(preguntas_db, 5)
    return jsonify(seleccion)

@app.route('/calificar', methods=['POST'])
def calificar():
    respuestas_usuario = request.json # Diccionario {id_pregunta: [indices_seleccionados]}
    resultados = []
    puntaje_total = 0

    for p_id_str, elecciones in respuestas_usuario.items():
        p_id = int(p_id_str)
        pregunta = next(p for p in preguntas_db if p['id'] == p_id)
        
        correctas = set(pregunta['correctas'])
        usuario = set(elecciones)
        
        # Lógica de puntaje parcial (0 a 20 puntos)
        aciertos = len(correctas.intersection(usuario))
        errores = len(usuario.difference(correctas))
        
        # Cálculo simplificado: (Aciertos / Total_Correctas) * 20 - Penalidad por errores
        score_pregunta = max(0, (aciertos / len(correctas)) * 20 - (errores * 5))
        
        puntaje_total += score_pregunta
        resultados.append({
            "id": p_id,
            "pregunta": pregunta['pregunta'],
            "score": round(score_pregunta, 2),
            "correctas_texto": [pregunta['opciones'][i] for i in pregunta['correctas']],
        })

    return jsonify({
        "puntaje_final": round(puntaje_total, 2),
        "detalle": resultados
    })

if __name__ == '__main__':
    app.run(debug=True)