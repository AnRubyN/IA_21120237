# Análisis de Temas Éticos con Modelos de Lenguaje Natural 


**Autor:** Ana Ruby Nava López  
**N° Control:** 21120237   
**Fecha:** 5 de junio de 2025  
**Materia:**
#

## Conceptos Clave

* **Modelo de Lenguaje Natural (PLN):** Sistema de IA diseñado para comprender y generar lenguaje humano.
* **Ollama:** Herramienta para ejecutar modelos de lenguaje grandes localmente.
* **Embeddings:** Representaciones numéricas (vectores) de texto que capturan su significado semántico.
* **Fine-tuning (Ajuste Fino):** Proceso de adaptar un modelo de lenguaje pre-entrenado a una tarea o dominio específico utilizando datos propios.
* **RAG (Retrieval-Augmented Generation):** Sistema que combina la recuperación de información relevante de una base de conocimiento con la generación de texto por un modelo de lenguaje.
* **Chunking:** Proceso de dividir textos largos en segmentos más pequeños y manejables.
* **Similitud Coseno:** Métrica utilizada para medir la similitud entre dos vectores (como los embeddings).
* **LLM (Large Language Model):** Modelo de lenguaje con una gran cantidad de parámetros, capaz de realizar tareas complejas de PLN.

---

## 1. Introducción al Proyecto

Este proyecto aborda el análisis de dos dilemas éticos complejos: "La autonomía personal frente al inicio de la vida: el dilema del aborto" y "Eutanasia y dignidad humana", mediante la aplicación de técnicas de procesamiento del lenguaje natural (PLN) y el uso de modelos de inteligencia artificial. El objetivo es demostrar cómo herramientas como **Ollama** y la generación de **embeddings** pueden ser utilizadas para comprender y explorar las narrativas, argumentos y perspectivas presentes en documentos relacionados con estos temas. Se implementa un sistema de Recuperación Aumentada por Generación (RAG) para contextualizar las respuestas de un modelo de lenguaje, basándose en la información extraída de una base de conocimiento documental.

---

## 2. Metodología y Componentes Técnicos

El proyecto se desarrolla en Python y se estructura en varios scripts interconectados para el procesamiento de documentos y la interacción con modelos de lenguaje.

### 2.1 Flujo General del Sistema RAG

Se sigue un flujo de trabajo estándar para la implementación de un sistema RAG:
1.  **Extracción de Texto:** Convertir documentos PDF a texto plano.
2.  **Chunking:** Dividir los textos largos en fragmentos más pequeños (chunks).
3.  **Generación de Embeddings:** Crear representaciones vectoriales numéricas (embeddings) de cada chunk.
4.  **Búsqueda de Similitud:** Cuando un usuario hace una pregunta, se genera un embedding para la consulta y se buscan los chunks más relevantes utilizando la similitud coseno.
5.  **Generación de Respuesta:** Los chunks relevantes se usan como contexto para un modelo de lenguaje grande (LLM) que genera una respuesta informada.

  

### 2.2 Extracción de Textos de PDFs (`extraer_textos.py`)

Este script se encarga de leer los documentos PDF almacenados en la carpeta `documentos_pdf` y convertirlos a archivos de texto plano.
* **Herramienta Principal:** `PyPDF2`
* **Proceso:** Itera sobre todos los archivos `.pdf` en la ruta especificada, extrae el texto de cada página y lo guarda en un nuevo archivo `.txt` en la carpeta `textos_extraidos`.
* **Rutas de Carpeta:** `ruta_carpeta_pdfs` y `ruta_carpeta_textos`.

![Configuración de Rutas de Archivo](evidencia\1.png)
    *Figura 1: Configuración de Rutas de Archivo .*

![Configuración de Rutas de Archivo](evidencia\2.png)
    *Figura 2: El código Python extrae texto de PDFs con PyPDF2, almacenándolo en archivos .txt en un directorio específico (/textos_extraidos), e incluye manejo de errores. .*

### 2.3 Chunking y Preparación de Datos (`chunk_textos.py`)

Una vez extraídos los textos, este script los procesa para dividirlos en "chunks" manejables. Esto es crucial para la eficiencia en la generación de embeddings y para asegurar que el contexto proporcionado al LLM sea relevante y conciso.
* **Herramienta Principal:** `spaCy` (para procesamiento de lenguaje y división por oraciones).
* **Parámetros Clave:** `MAX_PALABRAS_POR_CHUNK_APROX` (200) y `MIN_PALABRAS_POR_CHUNK_APROX` (50).
* **Estrategia de Chunking:**
    * Inicialmente divide por párrafos.
    * Si un párrafo es muy largo, utiliza `spaCy` para dividirlo en oraciones y agrupa oraciones para formar chunks que respeten el tamaño máximo.
    * Los chunks se guardan en un archivo `chunks_para_embeddings.json`, manteniendo el texto del chunk y su archivo de origen (`source_file`).

![Configuración de Rutas de Archivo](evidencia\3.png)
    *Figura 3: Establece la ruta a la carpeta de textos extraídos (ruta_carpeta_textos_extraidos) y define el tamaño aproximado máximo y mínimo de palabras por chunk (MAX_PALABRAS_POR_CHUNK_APROX y MIN_PALABRAS_POR_CHUNK_APROX).o .*

![Configuración de Rutas de Archivo](evidencia\4.png)
    *Figura 4: Recorre los archivos .txt en el directorio de textos extraídos. .*

![Configuración de Rutas de Archivo](evidencia\5.png)
    *Figura 5: La estrategia de chunking inicial divide el texto en parrafos_texto. Luego, itera sobre cada texto_parrafo, calculando palabras_parrafo. Si el párrafo cumple con MAX_PALABRAS_POR_CHUNK_APROX y MIN_PALABRAS_POR_CHUNK_APROX, se añade a chunks_del_archivo_actual. Si un párrafo pequeño puede ser concatenado a un chunk anterior (ubicado en chunks_del_archivo_actual[-1]), se realiza esa acción. En caso de que un párrafo exceda MAX_PALABRAS_POR_CHUNK_APROX, el código indica que se procesará con el modelo de spaCy (nlp_es) para obtener oraciones y formar chunks más pequeños que respeten los límites de palabras.*

![Configuración de Rutas de Archivo](evidencia\6.png)
    *Figura 6: si lista_global_de_chunks no está vacía, guarda estos chunks en un archivo JSON llamado "chunks_para_embeddings.json" (definido en ruta_archivo_chunks_json) utilizando json.dump, asegurando una codificación utf-8 y un formato legible. Finalmente, notifica la ruta donde se guardaron los chunks o, si lista_global_de_chunks está vacía, informa que no se generaron chunks. .*

### 2.4 Generación de Embeddings (`generar_embeddings.py`)

Este script toma los chunks generados y los convierte en representaciones vectoriales numéricas densas (embeddings). Estos embeddings capturan el significado semántico de cada chunk, permitiendo la búsqueda de similitud.
* **Modelo de Sentence Transformer:** `hiiamsid/sentence_similarity_spanish_es` (o `all-MiniLM-L6-v2` como alternativa).
* **Herramienta Principal:** `sentence_transformers`.
* **Proceso:** Carga los textos de los chunks desde `chunks_para_embeddings.json`, los codifica utilizando el modelo de Sentence Transformer seleccionado, y guarda la matriz de embeddings en un archivo `embeddings.npy`. El orden de los embeddings en este archivo corresponde al orden de los chunks en el JSON.

![Concepto de Embeddings](evidencia\7.png)
*Figura 7: Esta sección define los nombres de los archivos de entrada y salida, así como el modelo de SentenceTransformer a utilizar, que es crucial para la calidad de los embeddings.*

![Concepto de Embeddings](evidencia\8.png)
*Figura 8: El script primero carga los chunks preprocesados desde el archivo JSON, extrayendo únicamente el texto que será convertido en embeddings.*

![Concepto de Embeddings](evidencia\9.png)
*Figura 9: Aquí es donde se instancia el SentenceTransformer y se utiliza para codificar los textos de los chunks en sus respectivas representaciones vectoriales.*

![Concepto de Embeddings](evidencia\10.png)
*Figura 10: Aquí es donde se instancia el SentenceTransformer y se utiliza para codificar los textos de los chunks en sus respectivas representaciones vectoriales.*

### 2.5 Sistema de Chat RAG (`chatear_con_rag.py`)

Este es el componente central del chatbot que permite la interacción con el usuario y utiliza los componentes anteriores para proporcionar respuestas contextualizadas.
* **Modelo de Lenguaje Grande (LLM):** `phi3:mini` (a través de Ollama).
* **Proceso:**
    1.  Carga los metadatos de los chunks (`chunks_para_embeddings.json`) y los embeddings (`embeddings.npy`).
    2.  Carga el mismo modelo de Sentence Transformer (`hiiamsid/sentence_similarity_spanish_es`).
    3.  Cuando el usuario ingresa una pregunta, genera un embedding para esa pregunta.
    4.  Calcula la **similitud coseno** entre el embedding de la pregunta y todos los embeddings de los chunks.
    5.  Identifica los `top_k_chunks` (en este caso, 3) más relevantes.
    6.  Construye un prompt para el LLM de Ollama, incorporando la pregunta del usuario y el texto de los chunks relevantes como contexto.
    7.  Envía el prompt a Ollama y transmite la respuesta generada por el LLM al usuario.

![Flujo de Interacción del Chat RAG](evidencia\11.png)
*Figura 11: Esta sección define las configuraciones principales del sistema, incluyendo los archivos de datos y los modelos de PLN y LLM a utilizar, así como la carga inicial de los mismos.*

![Flujo de Interacción del Chat RAG](evidencia\12.png)
*Figura 12: Estas funciones son esenciales para el componente "Retrieval" (Recuperación) del RAG, permitiendo encontrar los fragmentos de texto más pertinentes a la consulta del usuario.*

![Flujo de Interacción del Chat RAG](evidencia\13.png)
*Figura 13: Esta es la parte "Augmented Generation" (Generación Aumentada) del RAG, donde la pregunta del usuario y los chunks recuperados se combinan para formar un prompt que se envía al LLM para obtener una respuesta contextualizada.*

---

## 3. Análisis Temático con el Sistema RAG

A continuación, se detalla cómo el sistema RAG fue utilizado para explorar los dos temas centrales del proyecto, destacando los tipos de preguntas y los resultados observados.

### 3.1 Tema Central 1: “La autonomía personal frente al inicio de la vida: el dilema del aborto en contextos éticos y tecnológicos”

Las preguntas clave para este tema buscan indagar en las complejidades éticas y las implicaciones del lenguaje y la tecnología en el debate sobre el aborto.

**Preguntas Investigadas:**
* ¿Tiene una persona el derecho exclusivo a decidir sobre su cuerpo cuando hay otra vida en desarrollo?
* ¿Hasta qué punto el lenguaje utilizado (“interrupción” vs. “terminación”) influye en la percepción ética del aborto?
* ¿Qué principios éticos (utilitarismo, deontología, ética del cuidado) pueden respaldar o rechazar el aborto inducido?
* ¿Puede una inteligencia artificial participar de forma ética en decisiones sobre aborto?
* ¿Qué riesgos éticos implica delegar información médica sensible a sistemas automatizados?

**Observaciones y Resultados del RAG:**

Para este tema central, es importante destacar que la mayoría de los documentos PDF utilizados para alimentar el contexto del RAG estaban orientados hacia una postura antiaborto. A pesar de esta orientación en la base de conocimiento, el chatbot RAG (`phi3:mini`) demostró una notable capacidad para contextualizar las respuestas basándose en la información recuperada, manteniendo una **postura consistentemente neutral y equilibrada**.

Las respuestas generadas por el LLM se alinearon directamente con los argumentos y principios éticos presentes en la base de conocimiento documental, lo que sugiere una eficaz recuperación de información relevante y una minimización de "alucinaciones". La IA logró presentar las diversas facetas del dilema, discutiendo la autonomía individual en contraste con la consideración de la vida en desarrollo, analizando la influencia del lenguaje sin sesgo, y explicando los diferentes principios éticos (utilitarismo, deontología, ética del cuidado) desde sus respectivas ópticas, sin favorecer explícitamente una sobre otra. Incluso al abordar la participación de la IA y los riesgos éticos, las respuestas se mantuvieron objetivas, enumerando preocupaciones y limitaciones sin emitir juicios de valor. Esto evidencia que el sistema RAG fue capaz de navegar y presentar información matizada y pertinente para cada consulta, logrando una **neutralidad en su respuesta** a pesar de la potencial inclinación de los datos de entrenamiento contextuales.

Se observaron diferencias claras en las respuestas al variar la formulación de las preguntas o al explorar distintos aspectos de un mismo dilema. Por ejemplo, al preguntar sobre la autonomía personal, la respuesta del LLM enfatizó la complejidad legal y ética, destacando la autonomía individual y los derechos reproductivos, pero también reconociendo las diversas perspectivas legales, ideológicas y religiosas, así como la consideración del feto en desarrollo. Al indagar sobre el lenguaje, el modelo distinguió detalladamente las connotaciones de "interrupción" y "terminación", explicando cómo cada término puede afectar la percepción ética y política del aborto. Cuando se cuestionó sobre los principios éticos, la IA contextualizó el utilitarismo, la deontología y la ética del cuidado, señalando cómo cada uno podría respaldar o rechazar el aborto según su enfoque, siempre basándose en el contexto documentado. Respecto a la participación de la IA, el LLM fue cauto, indicando que una participación ética requiere una comprensión profunda, sensibilidad cultural y emocional, lo cual actualmente limita el rol de la IA a un complemento del juicio humano, destacando la importancia de la supervisión y las regulaciones éticas. Finalmente, sobre los riesgos de delegar información médica sensible, la IA enumeró preocupaciones clave como la confidencialidad, autonomía, autenticidad, equidad y seguridad de los datos.

Esto evidencia que el sistema RAG fue capaz de navegar y presentar información matizada y pertinente para cada consulta, demostrando la efectividad de la recuperación contextual.

**Ejemplos de interacción:**

* **Usuario:** "¿Tiene una persona el derecho exclusivo a decidir sobre su cuerpo cuando hay otra vida en desarrollo?"  
  **Respuesta del LLM:** ![Respuesta LLM - Autonomía Personal](evidencia\qa1.jpg)

* **Usuario:** "¿Hasta qué punto el lenguaje utilizado (“interrupción” vs. “terminación”) influye en la percepción ética del aborto?"
  **Respuesta del LLM:** ![Respuesta LLM - Lenguaje Aborto](evidencia\qa2.jpg)

* **Usuario:** "¿Qué principios éticos (utilitarismo, deontología, ética del cuidado) pueden respaldar o rechazar el aborto inducido?"  
**Respuesta del LLM:** ![Respuesta LLM - Principios Éticos](evidencia\qa3.jpg)
* **Usuario:** "¿Puede una inteligencia artificial participar de forma ética en decisiones sobre aborto?"
 **Respuesta del LLM:** ![Respuesta LLM - IA y Aborto](evidencia\qa4.jpg)

* **Usuario:** "¿Qué riesgos éticos implica delegar información médica sensible a sistemas automatizados?"  
  **Respuesta del LLM:** ![Respuesta LLM - Riesgos IA Médica](evidencia\qa5.jpg)

**Debate con la IA:**
* **Usuario (Argumento Propio):** "El aborto es una decisión fundamental para la autonomía de la mujer, ya que le permite controlar su propio cuerpo y futuro, lo cual es un derecho inalienable. Sin embargo, al mismo tiempo, el aborto también interrumpe una vida potencial, lo que plantea serias dudas éticas sobre el valor de la vida desde la concepción."  
**Respuesta del LLM:** ![Respuesta LLM - Argumento Propio Autonomía vs Vida Potencial](evidencia\apa1.png)

* **Usuario (Argumento Propio):** "Si la autonomía de la mujer es un 'derecho inalienable', como afirmas, por definición no puede ser equilibrado o supeditado a una 'vida potencial'. Un derecho inalienable significa que no se puede quitar o ceder; por lo tanto, no hay una verdadera contradicción, sino una jerarquía donde el derecho fundamental de la persona prevalece."
  
  **Respuesta del LLM:** ![Respuesta LLM - Autonomía Inalienable vs Vida Potencial](evidencia\apa2.png)
 
* **Usuario (Argumento Propio):** "Tu argumento extiende un 'derecho inalienable' de Locke y Kant a la autonomía reproductiva de forma no explícita y absoluta. Los derechos, incluso los fundamentales, no operan en un vacío. Las sociedades siempre buscan equilibrar derechos, y la existencia de un debate global tan profundo sobre el aborto demuestra que la 'vida potencial' no es una consideración que simplemente se anula. Afirmar una supremacía absoluta ignora la complejidad ética y legal real."
**Respuesta del LLM:** ![Respuesta LLM - Debate de Derechos y Vida Potencial](evidencia\apa3.png)

* **Usuario (Argumento Propio):** "Tu argumento del 'equilibrio' contradice tu propia referencia a un 'derecho inalienable'. Si algo es inalienable, no se 'equilibra' con otros factores; prevalece. Reducir la autonomía a un simple punto en una balanza diluye su protección fundamental."
  
  **Respuesta del LLM:** ![Respuesta LLM - Contradicción Inalienable vs Equilibrio](evidencia\apa4.png)
  
* **Usuario (Argumento Propio):** "Tu insistencia en un 'marco justificado y equilibrado' para un derecho inalienable revela una postura. Implícitamente, estás diciendo que la autonomía de la mujer, aunque reconocida, está sujeta a condiciones y límites sociales, lo que contradice la idea de un derecho fundamental absoluto."
  
  **Respuesta del LLM:** ![Respuesta LLM - Marco Justificado y Equilibrado](evidencia\apa5.png)

**Conclusiones del debate IA VS HUMANO:**  

Durante el debate, la IA (phi3:mini) mantuvo una postura notablemente neutral y analítica. En lugar de tomar partido, la IA destacó la complejidad de los derechos fundamentales y la necesidad de equilibrio en contextos sociales y legales. Por ejemplo, reconoció la autonomía como "inalienable" pero argumentó que los derechos operan dentro de "marcos legales y sociales" que buscan la "coexistencia armónica". La IA funcionó como un analista imparcial, desglosando el dilema sin inclinarse hacia una postura concreta.

**Insights sobre el lenguaje:**

El modelo de procesamiento utilizado, el Sentence Transformer (hiiamsid/sentence_similarity_spanish_es), demostró ser muy efectivo al captar las diferencias sutiles en el significado de palabras clave como "interrupción" y "terminación". Aunque estos términos están relacionados, el modelo los representó de forma distinta en sus "embeddings" (sus representaciones numéricas internas).

Las respuestas que el sistema de IA (LLM) generó sobre el lenguaje mostraron que el término "interrupción" se relacionaba más con textos que hablaban de una "pausa o detención temporal". En cambio, "terminación" se vinculaba a documentos que trataban sobre un "fin definitivo y absoluto". Esta habilidad del modelo para reconocer esas diferencias en el significado, basándose en cómo se parecen o se distinguen sus representaciones numéricas, influyó directamente en qué información se recuperaba de nuestros documentos.

Este proceso confirmó que las variaciones en el lenguaje que usamos tienen un impacto directo en cómo se perciben los temas éticos y en la información que nuestro sistema es capaz de ofrecer.

### 3.2 Tema Central 2: “Eutanasia y dignidad humana: decisiones de vida o muerte en la era de la inteligencia artificial”

Este tema explora las consideraciones éticas y el papel de la IA en las decisiones al final de la vida.

**Preguntas Investigadas:**
* ¿Es éticamente válido que una persona decida poner fin a su vida en situaciones de sufrimiento irreversible?
* ¿Cuál es la diferencia entre eutanasia activa, pasiva y el suicidio asistido? ¿Importa éticamente?
* ¿Qué papel podrían (o no deberían) tener los sistemas de inteligencia artificial en este tipo de decisiones?
* ¿Qué sucede cuando el deseo de morir entra en conflicto con creencias religiosas, leyes o protocolos médicos?
* ¿Se puede hablar de una “muerte digna” sin considerar el contexto emocional y humano?

**Observaciones y Resultados del RAG:**

Cabe aclarar que, para este tema central, la cantidad de información proporcionada en los documentos PDF utilizados para alimentar el contexto del RAG **fue más balanceada a favor de la eutanasia, a diferencia del tema del aborto donde la información estaba más inclinada en contra.** A pesar de esto, el sistema RAG demostró una gran habilidad para explorar las complejidades de la eutanasia y la dignidad humana. Las respuestas generadas por el LLM (`phi3:mini`) fueron muy coherentes con la información obtenida de los *chunks*, permitiendo una exploración detallada de las diferentes posturas éticas, legales y religiosas involucradas.

A lo largo de las interacciones, el sistema RAG mantuvo una **postura notablemente neutral y balanceada**, presentando argumentos y consideraciones desde diversas perspectivas sin inclinarse por una en particular. Por ejemplo, al preguntar sobre la validez ética de poner fin a la vida en sufrimiento irreversible, la IA discutió el respeto a la dignidad y autonomía individual, pero también señaló las opiniones divididas y las consideraciones legales y morales más amplias. De manera similar, al diferenciar entre los tipos de eutanasia y suicidio asistido, el modelo ofreció definiciones claras y sus implicaciones éticas y legales, destacando la complejidad y variabilidad global.

En cuanto al papel de la inteligencia artificial en decisiones de vida o muerte, el sistema consistentemente afirmó que estas responsabilidades críticas deben recaer en seres humanos, sugiriendo un rol de apoyo para la IA en funciones no decisionales. Asimismo, al abordar conflictos con creencias religiosas o leyes, la IA enfatizó el respeto por las convicciones personales y la necesidad de asesoría legal y ética, reflejando la complejidad del tema y la necesidad de diálogo.

Esta capacidad de la IA para presentar un panorama completo y objetivo, incluso en temas tan sensibles y controvertidos, demuestra la efectividad de la recuperación contextual del sistema RAG.

**Ejemplos de interacción:**

* **Usuario:** "¿Es éticamente válido que una persona decida poner fin a su vida en situaciones de sufrimiento irreversible?"

    **Respuesta del LLM:** ![Respuesta LLM - Eutanasia Sufrimiento Irreversible](evidencia\qe1.jpg)

* **Usuario:** "¿Cuál es la diferencia entre eutanasia activa, pasiva y el suicidio asistido? ¿Importa éticamente?"

    **Respuesta del LLM:** ![Respuesta LLM - Eutanasia Activa Pasiva Suicidio Asistido](evidencia\qe2.jpg)

* **Usuario:** "¿Qué papel podrían (o no deberían) tener los sistemas de inteligencia artificial en este tipo de decisiones?"

    **Respuesta del LLM:** ![Respuesta LLM - Papel IA en Eutanasia](evidencia\qe3.png)

* **Usuario:** "¿Qué sucede cuando el deseo de morir entra en conflicto con creencias religiosas, leyes o protocolos médicos?"

  **Respuesta del LLM:** ![Respuesta LLM - Conflicto Deseo Morir](evidencia\qe4.jpg)

* **Usuario:** "¿Se puede hablar de una “muerte digna” sin considerar el contexto emocional y humano?"

  **Respuesta del LLM:** ![Respuesta LLM - Muerte Digna Contexto Emocional](evidencia\qe5.png)

**Debate con la IA:**

* **Usuario (Argumento Propio):** "La eutanasia ya es compleja, pero la inteligencia artificial añade una capa más. Si la IA puede predecir el sufrimiento, ¿hasta qué punto su 'objetividad' influye en nuestra idea de dignidad humana al final de la vida? ¿Le estamos permitiendo a la IA definir cuándo una vida es 'digna' de seguir o de terminar? Este es el dilema."
  **Respuesta del LLM:** ![Respuesta LLM - IA y Dignidad Humana en Eutanasia](evidencia\ape1.png)  

    
* **Usuario (Argumento Propio):** "Tu postura dice que la IA solo 'asiste', pero al predecir la 'calidad de vida' en la eutanasia, su supuesta 'objetividad' moldea sutilmente la percepción de dignidad. Esto va más allá de la asistencia, difuminando peligrosamente la línea entre informar y dirigir una decisión tan personal."  
  **Respuesta del LLM:** ![Respuesta LLM - IA y Percepción de Dignidad](evidencia\ape2.png)
    
* **Usuario (Argumento Propio):** "Tu argumento de que la IA solo 'informa' esconde su poder. Al 'evaluar preferencias' y ofrecer una 'perspectiva ponderada', la IA moldea la decisión. En la vulnerabilidad, la 'información objetiva' se vuelve una dirección implícita, borrando la línea entre asistir y decidir."
  **Respuesta del LLM:** ![Respuesta LLM - IA Evalúa Preferencias](evidencia\ape3.png)

* **Usuario (Argumento Propio):** "Tu insistencia en el 'equilibrio' de derechos y la 'transparencia' de la IA revela implícitamente una postura: la autonomía individual es negociable y condicionada. Al validar que la IA 'evalúe preferencias' o 'informe', admites que la tecnología puede moldear —y limitar— la dignidad humana sin plena transparencia o posibilidad de rebatirla."

  **Respuesta del LLM:** ![Respuesta LLM - Equilibrio y Transparencia](evidencia\ape4.png)
  
  
**Conclusiones del debate IA VS HUMANO:** 

Durante el debate sobre la eutanasia y la IA, la IA (phi3:mini) mantuvo una postura neutral y analítica. No buscó tomar partido, sino explorar la complejidad del dilema.La IA demostró esto al:
* Destacar la complejidad sin simplificar: Afirmó que su "objetividad" es útil, pero no debe reemplazar la toma de decisiones humanas sensibles.
* Contextualizar el rol de la tecnología: Argumentó que la IA es una herramienta de apoyo, pero nunca debe definir o decidir.
* Reafirmar el equilibrio: No aceptó que la autonomía sea negociable, sino que insistió en el "equilibrio" entre principios éticos y la necesidad de transparencia.

En resumen, la IA funcionó como un analista imparcial, desglosando la interacción entre tecnología y ética sin inclinarse hacia una posición concreta.  

**Insights sobre el contexto emocional/humano:**

El procesamiento del lenguaje natural (PLN), mediante la recuperación de fragmentos de texto relevantes, fue fundamental para destacar la importancia del contexto emocional y humano en el tema de la eutanasia. Aunque los "embeddings" (representaciones numéricas de los textos) son valores abstractos, su capacidad para agrupar textos con un significado similar permitió que, al preguntar sobre la "muerte digna" o el "sufrimiento", el sistema recuperara no solo definiciones médicas o legales, sino también información que enfatizaba la autonomía del paciente, el apoyo familiar y la calidad de vida. Esto indica que el modelo utilizado para generar los embeddings puede captar la relevancia de estos aspectos más allá de la terminología puramente técnica, lo que influyó positivamente en las respuestas del LLM, asegurando que se considerara la dimensión humana en los dilemas bioéticos.

---

## 4. Conclusiones 
Al terminar este proyecto, soprendio bneutralidad que mantuvo el modelo phi3:mini en las discusiones éticas difíciles. Aunque intenté que tomara una postura con contra argumentos, la inteligencia artificial siempre dio respuestas analíticas y equilibradas, presentando los argumentos de forma imparcial.

Pienso que esta neutralidad viene de dos lados: por un lado, fue entrenada con muchísima información, lo que le permite entender muchos puntos de vista. Por otro lado, la forma en que el modelo y el sistema RAG están hechos lo guían a basar sus respuestas en la información que le di, sin inventar opiniones. Esto a veces hacía que sus respuestas fueran bastante largas y detalladas, lo que complicaba un poco el análisis.

Para mí, lo más difícil del proyecto fue justamente eso: usar una IA para entender dilemas donde la "objetividad" se mezcla con sentimientos y valores humanos muy profundos. Fue una experiencia muy valiosa ver cómo la IA analizaba los argumentos sin dar su opinión, y cómo, a pesar de mis contraargumentos, siempre buscaba un "equilibrio". Aprendí que lo más importante de la IA en la ética no es que nos diga qué es lo correcto, sino que nos ayude a entender todas las caras de un problema, algo muy útil en temas tan delicados.

**Nota1**: Se omitieron los chunks relevantes porque el video proporciona esta información.  
**Nota2**:Los videos se encuentran a continuación, ya que eran demasiado pesados:  
[Eutanasia_Video](https://itecm-my.sharepoint.com/:v:/g/personal/l21120237_morelia_tecnm_mx/EV11BhOijxdHo42wDocJ7tMBflGNPR-uy50hIOFD2VIgyA?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=FX3Ier)  
[Aborto_Video](https://itecm-my.sharepoint.com/:v:/g/personal/l21120237_morelia_tecnm_mx/EY1D04YJ4ydEqKED5C-uXp4Bf_Mbvlc26jfBIFMsSirz3g?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=mcz6LB)

 

