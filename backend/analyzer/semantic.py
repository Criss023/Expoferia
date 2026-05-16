"""
FASE 3: ANÁLISIS SEMÁNTICO
Base de conocimiento con reglas para verificar la veracidad de enunciados.
Si no puede determinar → retorna INDETERMINADO para pasar al fallback de IA.
"""

import re
import math

# BASE DE CONOCIMIENTO — HECHOS VERDADEROS

TRUE_FACTS = [

    # ── ASTRONOMÍA ──
    r"(tierra|la tierra).*(orbita|gira alrededor|gira en torno).*(sol)",
    r"(tierra).*(gira).*(sol)",
    r"(sol).*(es una|es la|es).*(estrella)",
    r"(sol).*(estrella)",
    r"(luna).*(satélite).*(tierra|natural)",
    r"(luna).*(satélite natural)",
    r"(tierra).*(planeta)",
    r"(tierra).*(planeta azul)",
    r"(sol).*(centro).*(sistema solar)",
    r"(sistema solar).*(sol).*(centro)",
    r"(plutón).*(planeta enano)",
    r"(plutón).*(no es un planeta)",
    r"(sistema solar).*(8|ocho).*(planetas)",
    r"(hay|existen).*(8|ocho).*(planetas).*(sistema solar)",
    r"(marte).*(planeta rojo)",
    r"(júpiter).*(planeta más grande)",
    r"(júpiter).*(más grande).*(sistema solar)",
    r"(venus).*(planeta más caliente)",
    r"(mercurio).*(planeta más cercano).*(sol)",
    r"(mercurio).*(más pequeño).*(planetas)",
    r"(neptuno).*(planeta más lejano)",
    r"(saturno).*(anillos)",
    r"(saturno).*(tiene anillos)",
    r"(luna).*(orbita|gira alrededor).*(tierra)",
    r"(año luz).*(distancia)",
    r"(sol).*(93 millones|150 millones).*(kilómetros|millas)",
    r"(tierra).*(tercer planeta)",
    r"(luz del sol).*(8 minutos|ocho minutos).*(tierra)",
    r"(vía láctea).*(galaxia)",
    r"(tierra).*(pertenece).*(vía láctea)",
    r"(universo).*(expansión|se expande)",
    r"(big bang).*(origen).*(universo)",

    # ── CIENCIA Y FÍSICA ──
    r"(agua).*(h2o|h₂o)",
    r"(agua).*(hidrógeno).*(oxígeno)",
    r"(agua).*(dos átomo|2 átomo).*(hidrógeno)",
    r"(agua).*(hierve|punto de ebullición).*(100)",
    r"(agua).*(congela|punto de congelación).*(0)",
    r"(oxígeno).*(o2|o₂)",
    r"(dióxido de carbono).*(co2|co₂)",
    r"(luz).*(velocidad).*(300)",
    r"(velocidad de la luz).*(300)",
    r"(luz).*(viaja|se desplaza).*(más rápido)",
    r"(nada).*(viaja más rápido).*(luz)",
    r"(dna|adn).*(doble hélice)",
    r"(adn|dna).*(información genética)",
    r"(fotosíntesis).*(plantas|luz solar|clorofila)",
    r"(plantas).*(fotosíntesis)",
    r"(einstein).*(relatividad)",
    r"(teoría de la relatividad).*(einstein)",
    r"(e=mc|e = mc).*(einstein)",
    r"(newton).*(gravedad|gravitación)",
    r"(ley de gravedad).*(newton)",
    r"(darwin).*(evolución|selección natural)",
    r"(evolución).*(darwin)",
    r"(átomo).*(protones|neutrones|electrones)",
    r"(tabla periódica).*(elementos)",
    r"(mendeleev).*(tabla periódica)",
    r"(gravedad).*(atrae|atracción)",
    r"(sonido).*(viaja más lento).*(luz)",
    r"(luz).*(más rápida).*(sonido)",
    r"(electricidad).*(electrones)",
    r"(energía no se crea ni se destruye)",
    r"(primera ley de newton).*(inercia)",
    r"(inercia).*(primera ley)",
    r"(fuerza).*(masa).*(aceleración)",
    r"(segunda ley de newton).*(fuerza)",
    r"(tercera ley de newton).*(acción).*(reacción)",
    r"(temperatura).*(celsius|fahrenheit|kelvin)",
    r"(0 kelvin|cero absoluto|cero kelvin).*(temperatura más baja)",
    r"(hidrógeno).*(elemento más abundante).*(universo)",
    r"(oxígeno).*(necesario|respirar|respiración)",
    r"(co2|dióxido de carbono).*(plantas).*(absorb)",
    r"(presión).*(aumenta).*(profundidad)",
    r"(arquímedes).*(principio|flotación)",

    # ── BIOLOGÍA ──
    r"(humanos|seres humanos|homo sapiens).*(mamíferos)",
    r"(ballena).*(mamífero)",
    r"(delfín).*(mamífero)",
    r"(murciélago).*(mamífero)",
    r"(perro).*(mamífero)",
    r"(gato).*(mamífero)",
    r"(elefante).*(mamífero)",
    r"(corazón humano).*(cuatro|4).*(cámaras|cavidades)",
    r"(humano).*(206|doscientos seis).*(huesos)",
    r"(adulto).*(206).*(huesos)",
    r"(cerebro humano).*(más complejo)",
    r"(adn|dna).*(todos los seres vivos)",
    r"(células).*(unidad básica).*(vida)",
    r"(virus).*(más pequeño).*(bacteria)",
    r"(bacteria).*(más grande).*(virus)",
    r"(corazón).*(bombea).*(sangre)",
    r"(pulmones).*(oxígeno|respiración)",
    r"(hígado).*(órgano más grande).*(interior)",
    r"(piel).*(órgano más grande)",
    r"(sangre).*(roja|glóbulos rojos|hemoglobina)",
    r"(glóbulos rojos).*(oxígeno)",
    r"(glóbulos blancos).*(defensas|sistema inmune)",
    r"(vacuna).*(inmunidad|enfermedad)",
    r"(antibiótico).*(bacteria)",
    r"(antibiótico).*(no funciona).*(virus)",
    r"(tigre).*(felino|felidae)",
    r"(tiburón).*(pez)",
    r"(tiburón).*(no es mamífero)",
    r"(serpiente).*(reptil)",
    r"(cocodrilo).*(reptil)",
    r"(rana).*(anfibio)",
    r"(mariposa).*(insecto)",
    r"(araña).*(arácnido)",
    r"(araña).*(no es insecto)",
    r"(fotosíntesis).*(oxígeno)",
    r"(plantas).*(producen oxígeno)",
    r"(árbol).*(produce oxígeno)",
    r"(humano).*(23 pares).*(cromosomas)",
    r"(46 cromosomas).*(humano)",
    r"(gemelos idénticos).*(mismo adn)",

    # ── GEOGRAFÍA ──
    r"(everest).*(montaña más alta|pico más alto|cima más alta)",
    r"(everest).*(8[,.]848|8848).*(metros)",
    r"(amazonas).*(río más largo|río más caudaloso)",
    r"(nilo).*(África)",
    r"(pacífico).*(océano más grande|océano más extenso)",
    r"(atlántico).*(segundo océano)",
    r"(africa).*(continente)",
    r"(africa).*(continente más grande).*(calor|caliente|temperaturas)",
    r"(asia).*(continente más grande)",
    r"(asia).*(continente más poblado)",
    r"(antártida).*(continente más frío)",
    r"(antártida).*(polo sur)",
    r"(ártico).*(polo norte)",
    r"(brasil).*(país más grande).*(sudamérica|latinoamérica|america del sur)",
    r"(brasil).*(más grande).*(america del sur|sudamérica)",
    r"(rusia).*(país más grande).*(mundo)",
    r"(china|india).*(país más poblado)",
    r"(vaticano).*(país más pequeño)",
    r"(australia).*(continente|país)",
    r"(canada).*(segundo país más grande)",
    r"(sahara).*(desierto más grande).*(caliente|caluroso)",
    r"(antártida).*(desierto más grande).*(mundo)",
    r"(guatemala).*(país).*(centroamérica|centroamericano)",
    r"(centroamérica).*(siete|7).*(países)",
    r"(ciudad de guatemala|guatemala city).*(capital).*(guatemala)",
    r"(guatemala).*(capital).*(ciudad de guatemala)",
    r"(tikal).*(guatemala)",
    r"(quetzal).*(moneda).*(guatemala)",
    r"(quetzal).*(ave nacional).*(guatemala)",
    r"(quetzal).*(símbolo).*(guatemala)",
    r"(lago atitlán|atitlán).*(guatemala)",
    r"(motagua|río motagua).*(guatemala)",
    r"(usac|san carlos).*(universidad pública).*(guatemala)",
    r"(usac|universidad de san carlos).*(pública)",
    r"(umg|mariano gálvez|mariano galvez).*(privada)",
    r"(url|rafael landívar|landívar).*(privada)",
    r"(ufm|francisco marroquín).*(privada)",
    r"(parís).*(capital).*(francia)",
    r"(madrid).*(capital).*(españa)",
    r"(roma).*(capital).*(italia)",
    r"(berlín).*(capital).*(alemania)",
    r"(tokio|tokyo).*(capital).*(japón|japon)",
    r"(beijing|pekín).*(capital).*(china)",
    r"(washington|washington d\.?c).*(capital).*(estados unidos)",
    r"(brasilia).*(capital).*(brasil)",
    r"(buenos aires).*(capital).*(argentina)",
    r"(lima).*(capital).*(perú|peru)",
    r"(bogotá|bogota).*(capital).*(colombia)",
    r"(ciudad de méxico|cdmx).*(capital).*(méxico|mexico)",
    r"(london|londres).*(capital).*(reino unido|inglaterra)",
    r"(moscú|moscu).*(capital).*(rusia)",
    r"(nilo).*(África|egipto|africa)",
    r"(amazonas).*(america del sur|sudamérica|brasil)",
    r"(mediterráneo).*(mar).*(europa|africa)",
    r"(himalaya).*(asia|cordillera)",
    r"(andes).*(sudamérica|america del sur)",
    r"(cordillera más larga).*(andes)",

    # ── HISTORIA ──
    r"(colón|colon).*(llegó|descubrió|llegó a).*(america|1492)",
    r"(1492).*(colón|colon|llegada|descubrimiento)",
    r"(descubrimiento de america).*(1492)",
    r"(segunda guerra mundial).*(1939|1945)",
    r"(segunda guerra mundial).*(1939).*(1945)",
    r"(primera guerra mundial).*(1914|1918)",
    r"(primera guerra mundial).*(1914).*(1918)",
    r"(estados unidos).*(independencia).*(1776)",
    r"(independencia).*(estados unidos).*(1776)",
    r"(revolución francesa).*(1789)",
    r"(napoleón|napoleon).*(francia)",
    r"(hitler).*(segunda guerra mundial|nazi|alemania)",
    r"(segunda guerra mundial).*(hitler)",
    r"(bomba atómica).*(hiroshima|nagasaki|japón)",
    r"(hiroshima|nagasaki).*(bomba atómica)",
    r"(muro de berlín).*(1989|cayó|caída)",
    r"(guerra fría).*(estados unidos).*(unión soviética|urss)",
    r"(independencia de guatemala).*(1821)",
    r"(guatemala).*(independencia).*(1821|15 de septiembre)",
    r"(15 de septiembre).*(independencia).*(centroamérica|guatemala)",
    r"(mayas).*(civilización|cultura|guatemala|mesoamérica)",
    r"(einstein).*(nació).*(alemania|1879)",
    r"(newton).*(nació).*(inglaterra|1643)",
    r"(darwin).*(nació).*(inglaterra|1809)",
    r"(lincoln).*(presidente).*(estados unidos)",
    r"(mandela|nelson mandela).*(sudáfrica|apartheid)",
    r"(gandhi).*(india|independencia|no violencia)",
    r"(revolución industrial).*(inglaterra|siglo xviii|siglo xix)",
    r"(cristóbal colón|colon).*(1451|génova|genovés)",
    r"(luna).*(llegó|alunizó|primer hombre).*(1969)",
    r"(armstrong|neil armstrong).*(luna|1969)",
    r"(apollo 11).*(luna|1969)",

    # ── MATEMÁTICAS Y NÚMEROS ──
    r"(pi|π).*(3\.14|3,14)",
    r"(número pi).*(irracional|infinito)",
    r"(pi).*(relación|circunferencia).*(diámetro)",
    r"(suma de ángulos).*(triángulo).*(180)",
    r"(ángulos).*(triángulo).*(180 grados)",
    r"(cuadrado de la hipotenusa).*(suma).*(catetos)",
    r"(teorema de pitágoras).*(a²|a\^2|catetos|hipotenusa)",
    r"(pitágoras).*(triángulo rectángulo)",
    r"(número primo).*(solo divisible).*(1|sí mismo)",
    r"(2).*(único número primo par)",
    r"(0 no es positivo|cero no es positivo)",
    r"(infinito).*(no es un número)",
    r"(raíz cuadrada de 4).*(2|dos)",
    r"(raíz cuadrada de 9).*(3|tres)",
    r"(raíz cuadrada de 16).*(4|cuatro)",

    # ── TECNOLOGÍA ──
    r"(internet).*(arpanet|1960|1969)",
    r"(www|world wide web).*(tim berners.lee|berners)",
    r"(computadora|computador|ordenador).*(procesa|datos|información)",
    r"(inteligencia artificial|ia).*(machine learning|aprendizaje)",
    r"(python).*(lenguaje de programación)",
    r"(java).*(lenguaje de programación)",
    r"(javascript).*(lenguaje de programación)",
    r"(html).*(lenguaje de marcado|páginas web)",
    r"(css).*(estilos|páginas web)",
    r"(sql).*(base de datos)",
    r"(google).*(buscador|motor de búsqueda)",
    r"(facebook|meta).*(red social)",
    r"(apple).*(iphone|mac|steve jobs)",
    r"(microsoft).*(windows|bill gates)",
    r"(linux).*(sistema operativo|código abierto|linus torvalds)",
    r"(bitcoin).*(criptomoneda|blockchain)",
    r"(blockchain).*(descentralizado)",
    r"(robot).*(programado|automático)",
    r"(compilador).*(traduce|código fuente|lenguaje máquina)",
    r"(compilador).*(lenguaje de alto nivel).*(bajo nivel|máquina)",

    # ── ARTE Y CULTURA ──
    r"(mona lisa|la gioconda).*(leonardo da vinci|davinci)",
    r"(capilla sixtina).*(miguel ángel|michelangelo)",
    r"(beethoven).*(compositor|sordo|sinfonía)",
    r"(mozart).*(compositor|austria)",
    r"(shakespeare).*(escritor|dramaturgo|inglés|hamlet|romeo)",
    r"(cervantes).*(don quijote|quijote)",
    r"(don quijote).*(cervantes)",
    r"(picasso).*(pintor|cubismo|español)",
    r"(van gogh).*(pintor|holandés|girasoles)",

    # ── MEDICINA Y SALUD ──
    r"(corazón).*(late|latidos|bombea)",
    r"(corazón humano).*(late).*(60|70|80).*(veces|latidos)",
    r"(temperatura normal).*(cuerpo humano).*(36|37)",
    r"(fiebre).*(temperatura).*(38|37\.5)",
    r"(vitamina c).*(naranja|limón|cítrico)",
    r"(calcio).*(huesos|dientes)",
    r"(hierro).*(sangre|hemoglobina)",
    r"(insulina).*(diabetes|glucosa|páncreas)",
    r"(penicilina).*(fleming|antibiótico)",
    r"(fleming).*(penicilina|antibiótico)",
    r"(vacuna).*(jenner|viruela)",
    r"(rayos x).*(röntgen|roentgen)",
    r"(adn|dna).*(watson|crick|doble hélice)",

]

# ─────────────────────────────────────────────
# BASE DE CONOCIMIENTO — HECHOS FALSOS
# ─────────────────────────────────────────────

FALSE_FACTS = [

    # ── ASTRONOMÍA ──
    r"(sol).*(gira|orbita).*(tierra)",
    r"(tierra).*(centro).*(universo|sistema solar)",
    r"(tierra).*(plana|es plana|forma plana)",
    r"(sol).*(es un planeta|es planeta)",
    r"(luna).*(estrella)",
    r"(luna).*(produce|genera).*(luz propia)",
    r"(plutón).*(planeta|es un planeta$)",
    r"(sistema solar).*(9|nueve).*(planetas)",
    r"(sol).*(gira).*(planetas)",
    r"(tierra).*(única galaxia)",
    r"(marte).*(habitable|vida humana actual)",

    # ── CIENCIA ──
    r"(einstein).*(reprobó|jalado|reprobó|suspendió).*(matemáticas|física)",
    r"(einstein).*(malo en|mal en).*(matemáticas)",
    r"(einstein).*(inventó).*(bomba atómica)",
    r"(vidrio).*(líquido|fluye)",  # Mito del vidrio líquido
    r"(lengua).*(zonas).*(sabor|dulce|amargo|salado)",  # Mito del mapa de la lengua
    r"(humano).*(10.*(cerebro|mente|capacidad))",  # Mito del 10% del cerebro
    r"(usamos.*(10|diez) por ciento).*(cerebro)",
    r"(luz).*(más lenta).*(sonido)",
    r"(sonido).*(más rápido).*(luz)",
    r"(agua).*(hierve).*(90|80|70).*(nivel del mar)",
    r"(agua).*(tres).*(átomos|moléculas)",
    r"(oxígeno).*(o3)",  # O3 es ozono
    r"(sangre).*(azul).*(venas)",  # La sangre siempre es roja
    r"(sangre venosa).*(azul)",
    r"(nervios).*(más rápidos).*(luz)",
    r"(uñas|cabello).*(sigue creciendo).*(muerte|muertos)",

    # ── GEOGRAFÍA ──
    r"(australia).*(continente más grande)",
    r"(africa).*(continente más grande).*(mundo)",  # Asia es el más grande
    r"(río más largo).*(nilo).*(mundo)",
    r"(amazonas).*(africa|europa|asia)",
    r"(everest).*(america|europa|africa)",
    r"(estados unidos).*(país más grande).*(mundo)",
    r"(china).*(país más grande).*(mundo)",
    r"(brasil).*(capital).*(rio de janeiro|rio)",  # La capital es Brasilia
    r"(australia).*(capital).*(sídney|sydney)",   # La capital es Canberra
    r"(nueva zelanda).*(australia)",
    r"(umg|mariano gálvez|mariano galvez).*(pública|universidad pública)",
    r"(usac|san carlos).*(privada)",
    r"(guatemala).*(capital).*(quetzaltenango|xela|antigua)",
    r"(antigua guatemala).*(capital).*(guatemala)",
    r"(parís).*(capital).*(españa|italia|alemania)",
    r"(madrid).*(capital).*(portugal|francia|italia)",
    r"(tokio|tokyo).*(capital).*(china|corea)",
    r"(beijing|pekín).*(capital).*(japón|corea)",
    r"(washington).*(ciudad más grande).*(estados unidos)",
    r"(nueva york|new york).*(capital).*(estados unidos)",

    # ── BIOLOGÍA ──
    r"(ballena).*(pez|pescado)",
    r"(delfín).*(pez)",
    r"(murciélago).*(ave|pájaro)",
    r"(tiburón).*(mamífero)",
    r"(araña).*(insecto)",
    r"(serpiente).*(anfibio)",
    r"(rana).*(reptil)",
    r"(plantas).*(no producen oxígeno)",
    r"(plantas).*(consumen oxígeno).*(producen co2)",
    r"(humano).*(8|diez|10).*(sentidos básicos)",  # Son 5
    r"(humano).*(300|400).*(huesos).*(adulto)",
    r"(sangre).*(azul)",
    r"(corazón).*(lado derecho).*(cuerpo)",  # Está ligeramente a la izquierda
    r"(antibiótico).*(cura).*(virus|gripe|resfriado)",
    r"(gemelos).*(mismo.*(huella dactilar|huellas))",

    # ── HISTORIA ──
    r"(colón|colon).*(llegó|descubrió).*(1491|1493|1500)",
    r"(primera guerra mundial).*(1915|1916|1920)",
    r"(segunda guerra mundial).*(1940|1941|1950)",
    r"(independencia).*(estados unidos).*(1770|1775|1780)",
    r"(napoleon|napoleón).*(italiano|español)",
    r"(independencia de guatemala).*(1810|1820|1822)",
    r"(einstein).*(inventó|descubrió).*(gravedad)",
    r"(newton).*(inventó|descubrió).*(relatividad)",
    r"(darwin).*(descubrió).*(gravedad)",
    r"(armstrong).*(luna).*(1968|1970|1965)",
    r"(apollo 11).*(1968|1970)",
    r"(colón|colon).*(español|nació en españa)",  # Era genovés

    # ── TECNOLOGÍA ──
    r"(html).*(lenguaje de programación)",  # Es de marcado, no de programación
    r"(css).*(lenguaje de programación)",   # Es de estilos
    r"(python).*(lenguaje compilado)",      # Es interpretado
    r"(java).*(lenguaje interpretado puro)",
    r"(internet).*(inventó).*(bill gates|zuckerberg|steve jobs)",
    r"(facebook).*(primer red social)",
    r"(google).*(primer buscador)",

    # ── MITOS POPULARES ──
    r"(gran muralla china).*(visible).*(espacio|luna)",
    r"(gran muralla).*(ver desde).*(espacio|luna)",
    r"(pez de colores|pez dorado).*(memoria de).*(3|tres) segundo",
    r"(humano).*(traga).*(8|ocho).*(arañas).*(año|sueño|dormir)",
    r"(rayo).*(no cae dos veces).*(mismo lugar)",
    r"(pelo|vello|cabello).*(crece más rápido).*(afeitarse)",
    r"(vacuna).*(causa|provoca).*(autismo)",
    r"(microondas).*(radiación peligrosa|cancerígeno)",
]


def evaluate_math(sentence: str):
    """Evalúa expresiones matemáticas en múltiples formatos."""

    # Patrón amplio que cubre muchas formas de expresar operaciones
    match = re.search(
        r'(\d+(?:[.,]\d+)?)\s*'
        r'([\+\-\*\/]|más|menos|por|entre|dividido entre|dividido por|dividido|'
        r'sobre|multiplicado por|por|elevado a|al cuadrado|al cubo|'
        r'sumado a|sumado con|más que|menos que|resta|suma de|producto de)\s*'
        r'(\d+(?:[.,]\d+)?)\s*'
        r'(?:=|es igual a|es|son|igual a|equivale a|da como resultado|'
        r'resulta en|resulta|da|el resultado es|el resultado es de)\s*'
        r'(\d+(?:[.,]\d+)?)',
        sentence, re.IGNORECASE
    )

    if not match:
        return None

    try:
        a       = float(match.group(1).replace(',', '.'))
        op      = match.group(2).strip().lower()
        b       = float(match.group(3).replace(',', '.'))
        claimed = float(match.group(4).replace(',', '.'))
    except ValueError:
        return None

    op_map = {
        '+': a + b,
        'más': a + b,
        'sumado a': a + b,
        'sumado con': a + b,
        'suma de': a + b,
        'más que': a + b,
        '-': a - b,
        'menos': a - b,
        'menos que': a - b,
        'resta': a - b,
        '*': a * b,
        'por': a * b,
        'multiplicado por': a * b,
        'producto de': a * b,
        '/': (a / b) if b != 0 else None,
        'entre': (a / b) if b != 0 else None,
        'dividido': (a / b) if b != 0 else None,
        'dividido entre': (a / b) if b != 0 else None,
        'dividido por': (a / b) if b != 0 else None,
        'sobre': (a / b) if b != 0 else None,
        'elevado a': a ** b,
        'al cuadrado': a ** 2,
        'al cubo': a ** 3,
    }

    actual = op_map.get(op)
    if actual is None:
        return None

    is_true = abs(actual - claimed) < 0.0001
    return {
        "is_math": True,
        "actual_result": actual,
        "claimed_result": claimed,
        "verdict": "VERDADERO" if is_true else "FALSO",
        "confidence": 1.0,
        "explanation": (
            f"{a} {op} {b} = {actual} ✓"
            if is_true else
            f"{a} {op} {b} = {actual}, no {claimed}"
        )
    }


def semantic_analysis(sentence: str, has_negation: bool) -> dict:
    """
    Verifica la veracidad del enunciado con reglas predefinidas.
    """
    sentence_lower = sentence.lower()

    # 1. Intentar evaluación matemática
    math_result = evaluate_math(sentence)
    if math_result:
        return {
            "verdict": math_result["verdict"],
            "confidence": math_result["confidence"],
            "method": "REGLA_MATEMATICA",
            "explanation": math_result["explanation"],
            "rule_matched": "Operación aritmética",
            "needs_ai": False
        }

    # 2. Buscar en hechos verdaderos
    for pattern in TRUE_FACTS:
        if re.search(pattern, sentence_lower):
            verdict = "FALSO" if has_negation else "VERDADERO"
            return {
                "verdict": verdict,
                "confidence": 0.90,
                "method": "REGLA_BASE_CONOCIMIENTO",
                "explanation": f"El enunciado {'contradice' if has_negation else 'fue verificado mediante'} las reglas de la base de conocimiento interna.",
                "rule_matched": pattern,
                "needs_ai": False
            }

    # 3. Buscar en hechos falsos
    for pattern in FALSE_FACTS:
        if re.search(pattern, sentence_lower):
            verdict = "VERDADERO" if has_negation else "FALSO"
            return {
                "verdict": verdict,
                "confidence": 0.90,
                "method": "REGLA_BASE_CONOCIMIENTO",
                "explanation": f"El enunciado {'corrige' if has_negation else 'contradice'} un hecho registrado en la base de conocimiento interna.",
                "rule_matched": pattern,
                "needs_ai": False
            }

    # 4. No se pudo determinar → necesita IA
    return {
        "verdict": "INDETERMINADO",
        "confidence": 0.0,
        "method": "SIN_REGLA",
        "explanation": "No se encontró una regla que pueda verificar este enunciado.",
        "rule_matched": None,
        "needs_ai": True
    }