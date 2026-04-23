# ============================================================
#  🌸 MI EMBARAZO — Versión Web (Beta)
#  Construida con Streamlit
#  ─────────────────────────────────────────────────────────
#  Para ejecutar localmente:
#    pip install streamlit matplotlib plotly
#    streamlit run app.py
#
#  Para desplegar gratis en Streamlit Cloud:
#    https://share.streamlit.io
# ============================================================

import streamlit as st
from datetime import date, datetime, timedelta

# ── Configuración de la página ─────────────────────────────
# Debe ser la PRIMERA llamada a streamlit en el script
st.set_page_config(
    page_title="Mi Embarazo 🌸",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS personalizado ──────────────────────────────────────
# Streamlit permite inyectar CSS para personalizar colores y estilos
st.markdown("""
<style>
    /* Fondo principal */
    .stApp { background-color: #FFF0F5; }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #F8BBD0; }

    /* Títulos principales */
    h1 { color: #880E4F !important; }
    h2 { color: #880E4F !important; }
    h3 { color: #D63384 !important; }

    /* Botones primarios */
    .stButton > button {
        background-color: #D63384;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        padding: 0.4rem 1.2rem;
    }
    .stButton > button:hover {
        background-color: #880E4F;
        color: white;
    }

    /* Métricas (contadores grandes) */
    [data-testid="stMetric"] {
        background-color: #F8BBD0;
        border-radius: 10px;
        padding: 12px;
        border-left: 4px solid #D63384;
    }

    /* Cajas de info */
    .info-box {
        background-color: #FCE4EC;
        border-left: 4px solid #D63384;
        border-radius: 6px;
        padding: 14px 18px;
        margin: 8px 0;
        color: #3D0026;
    }

    /* Cajas de alerta médica */
    .alerta-box {
        background-color: #FFEBEE;
        border-left: 4px solid #C62828;
        border-radius: 6px;
        padding: 14px 18px;
        margin: 8px 0;
        color: #B71C1C;
    }

    /* Tags de nombres */
    .nombre-tag-nina {
        display: inline-block;
        background-color: #F48FB1;
        color: #880E4F;
        border-radius: 20px;
        padding: 4px 14px;
        margin: 4px;
        font-weight: bold;
        font-size: 0.95em;
    }
    .nombre-tag-nino {
        display: inline-block;
        background-color: #90CAF9;
        color: #0D47A1;
        border-radius: 20px;
        padding: 4px 14px;
        margin: 4px;
        font-weight: bold;
        font-size: 0.95em;
    }

    /* Aviso médico en el pie */
    .aviso-medico {
        background-color: #FFF9C4;
        border: 1px solid #F9A825;
        border-radius: 6px;
        padding: 10px 16px;
        color: #5D4037;
        font-size: 0.85em;
        margin-top: 20px;
    }

    /* Ocultar el menú de Streamlit y el footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  DATOS — Copiados directamente de la app de escritorio
# ══════════════════════════════════════════════════════════════

INFO_SEMANAS = {
    1:  "Tu bebé es apenas un grupo de células. ¡El viaje acaba de comenzar!",
    2:  "Se está produciendo la fecundación. Tu cuerpo empieza a prepararse.",
    3:  "El óvulo fecundado viaja hacia el útero para implantarse.",
    4:  "El embrión se implanta en el útero. Puedes notar ligero malestar.",
    5:  "El corazón del bebé empieza a formarse. ¡Un gran momento!",
    6:  "El embrión mide unos 4 mm. Los órganos principales comienzan su desarrollo.",
    7:  "El cerebro crece rápidamente. Se forman los primeros rasgos faciales.",
    8:  "El bebé mide alrededor de 1,6 cm. ¡Ya tiene dedos en formación!",
    9:  "Los músculos comienzan a desarrollarse. El bebé puede hacer pequeños movimientos.",
    10: "¡Oficialmente ya es un feto! Mide unos 3 cm y tiene todos los órganos básicos.",
    11: "Los huesos comienzan a endurecerse. El bebé ya puede abrir y cerrar el puño.",
    12: "Fin del primer trimestre. El riesgo de aborto disminuye significativamente.",
    13: "Comienzo del segundo trimestre. Puedes sentirte con más energía.",
    14: "El bebé puede hacer muecas y fruncir el ceño. Mide unos 8,7 cm.",
    15: "Puede que empieces a notar los primeros movimientos, como burbujas.",
    16: "El bebé oye sonidos del exterior. ¡Háblale y ponle música!",
    17: "Se forma una capa de grasa bajo la piel para mantener el calor.",
    18: "El bebé duerme y se despierta con ciclos regulares.",
    19: "Los sentidos se desarrollan: gusto, olfato, vista, oído y tacto.",
    20: "¡Mitad del embarazo! El bebé mide unos 25 cm de cabeza a talón.",
    21: "El bebé traga líquido amniótico y practica su sistema digestivo.",
    22: "El bebé tiene cejas y párpados bien definidos.",
    23: "Empiezan a formarse las huellas dactilares. ¡Única como tú!",
    24: "El bebé responde a sonidos fuertes moviéndose o dando una patada.",
    25: "Los pulmones producen surfactante, clave para respirar al nacer.",
    26: "Los ojos del bebé pueden abrirse. Comienzo del tercer trimestre.",
    27: "El cerebro crece muy rápido. El bebé ya tiene ritmos de sueño y vigilia.",
    28: "El bebé puede soñar. Su cerebro muestra actividad en fase REM.",
    29: "El bebé se prepara para el parto adoptando la posición cabeza abajo.",
    30: "El bebé mide unos 40 cm y pesa alrededor de 1,3 kg.",
    31: "Todos los sentidos están activos. El bebé reconoce tu voz.",
    32: "El bebé practica respirar moviendo el diafragma.",
    33: "Sus huesos se endurecen, excepto el cráneo (para facilitar el parto).",
    34: "El bebé gana unos 200 g por semana. ¡Creciendo fuerte!",
    35: "Los pulmones están casi maduros. El bebé ya podría nacer con poca asistencia.",
    36: "El bebé ocupa casi todo el útero. Las patadas son más notorias.",
    37: "¡Embarazo a término temprano! El bebé está listo para el mundo.",
    38: "El bebé sigue ganando grasa y perfeccionando sus funciones.",
    39: "El bebé se está preparando para nacer. Descansa y confía en tu cuerpo.",
    40: "¡Fecha probable de parto! Tu bebé puede llegar en cualquier momento.",
    41: "Algunos bebés se toman su tiempo. Habla con tu médico si llegas aquí.",
    42: "Tu médico evaluará la situación. ¡El encuentro está muy cerca!",
}

DETALLE_BEBE = {
    4:  {"tam": "Semilla de amapola (~2 mm)", "peso": "< 1 g",
         "emoji": "🌱",
         "desc": "El embrión acaba de implantarse. Se forman las capas de células que darán "
                 "lugar a todos los órganos. Puedes notar ligero sangrado de implantación."},
    5:  {"tam": "Semilla de sésamo (~4 mm)", "peso": "< 1 g", "emoji": "🫘",
         "desc": "Empieza a formarse el tubo neural. El corazón primitivo ya late."},
    6:  {"tam": "Lenteja (~6 mm)", "peso": "< 1 g", "emoji": "🫛",
         "desc": "Se forman los pliegues faciales. El corazón late 100-160 veces por minuto."},
    7:  {"tam": "Arándano (~13 mm)", "peso": "< 1 g", "emoji": "🫐",
         "desc": "El cerebro crece: 100 neuronas por minuto. Las manos tienen forma de paleta."},
    8:  {"tam": "Frambuesa (~16 mm)", "peso": "~1 g", "emoji": "🍇",
         "desc": "Se forman los dedos. El bebé puede mover los brazos."},
    9:  {"tam": "Cereza (~23 mm)", "peso": "~2 g", "emoji": "🍒",
         "desc": "Los músculos se desarrollan. Se forman los dientes de leche."},
    10: {"tam": "Fresa (~31 mm)", "peso": "~4 g", "emoji": "🍓",
         "desc": "Ya es oficialmente un feto. Todos los órganos vitales están formados."},
    11: {"tam": "Lima (~41 mm)", "peso": "~7 g", "emoji": "🍋",
         "desc": "Los huesos empiezan a endurecerse. El bebé puede abrir y cerrar el puño."},
    12: {"tam": "Ciruela (~54 mm)", "peso": "~14 g", "emoji": "🍑",
         "desc": "Fin del primer trimestre. El riesgo de aborto disminuye notablemente."},
    13: {"tam": "Kiwi (~74 mm)", "peso": "~23 g", "emoji": "🥝",
         "desc": "Las huellas dactilares ya están formadas. El bebé puede chuparse el dedo."},
    16: {"tam": "Aguacate (~12 cm)", "peso": "~100 g", "emoji": "🥑",
         "desc": "El bebé puede hacer muecas. El sistema nervioso controla los músculos."},
    20: {"tam": "Plátano (~25 cm)", "peso": "~300 g", "emoji": "🍌",
         "desc": "¡Mitad del embarazo! El bebé oye sonidos del exterior."},
    24: {"tam": "Mazorca de maíz (~30 cm)", "peso": "~600 g", "emoji": "🌽",
         "desc": "El bebé responde a sonidos fuertes con patadas."},
    28: {"tam": "Berenjena (~37 cm)", "peso": "~1 kg", "emoji": "🍆",
         "desc": "Tercer trimestre. El bebé abre los ojos. Puede soñar."},
    32: {"tam": "Col (~42 cm)", "peso": "~1,7 kg", "emoji": "🥬",
         "desc": "Todos los sentidos funcionan. Reconoce tu voz."},
    36: {"tam": "Col romanesca (~47 cm)", "peso": "~2,6 kg", "emoji": "🥦",
         "desc": "Los pulmones están casi maduros. Suele estar cabeza abajo."},
    40: {"tam": "Sandía (~51 cm)", "peso": "~3,4 kg", "emoji": "🍉",
         "desc": "El bebé está listo para nacer. ¡Puede llegar en cualquier momento!"},
}

CHECKLIST_TRIMESTRES = {
    1: [
        "Confirmar embarazo con prueba de farmacia",
        "Primera visita al médico o matrona",
        "Análisis de sangre completo (1er trimestre)",
        "Control de tensión arterial",
        "Ecografía semanas 11-13 (translucencia nucal)",
        "Tomar ácido fólico diariamente",
        "Informar al ginecólogo de medicamentos que tomes",
        "Evitar alcohol, tabaco y fármacos no prescritos",
    ],
    2: [
        "Ecografía morfológica (semanas 18-22)",
        "Análisis de sangre 2.º trimestre",
        "Control de glucosa (test de O'Sullivan)",
        "Vacuna de la tos ferina (semana ~28)",
        "Preparar clases de preparto",
        "Elegir hospital o centro de parto",
        "Revisar posición del bebé",
        "Informarte sobre lactancia materna",
    ],
    3: [
        "Visitas médicas cada 2 semanas (luego semanales)",
        "Ecografía del 3er trimestre",
        "Análisis de estreptococo grupo B (semana 35-37)",
        "Plan de parto: hablar con tu médico",
        "Preparar la bolsa para el hospital",
        "Instalar la silla de bebé en el coche",
        "Conocer los signos del inicio del parto",
        "Asistir a clases de preparto",
    ],
}

CONSEJOS = {
    "🥗 Alimentación": [
        "Come frutas y verduras variadas a diario.",
        "Asegura un aporte adecuado de hierro: legumbres, carnes magras.",
        "El calcio es fundamental: leche, yogur, queso.",
        "Toma ácido fólico según te indique tu médico.",
        "Evita pescado azul grande (atún rojo, pez espada) por el mercurio.",
        "Come carnes y huevos siempre bien cocinados.",
        "Lava bien frutas y verduras antes de consumirlas.",
        "Bebe al menos 8 vasos de agua al día.",
    ],
    "🚶 Ejercicio suave": [
        "Caminar 30 minutos diarios es ideal durante todo el embarazo.",
        "La natación es muy recomendable: alivia el peso y es de bajo impacto.",
        "El yoga prenatal ayuda con la respiración y la flexibilidad.",
        "Evita deportes de contacto o con riesgo de caídas.",
        "Consulta siempre a tu médico antes de iniciar una nueva actividad.",
        "Escucha a tu cuerpo: si notas dolor o mareo, para y descansa.",
    ],
    "⚠️ Qué evitar": [
        "Alcohol: no existe ninguna cantidad segura durante el embarazo.",
        "Tabaco: aumenta el riesgo de parto prematuro y bajo peso al nacer.",
        "Medicamentos sin prescripción médica.",
        "Quesos blandos no pasteurizados (riesgo de listeria).",
        "Sashimi, sushi o carnes crudas (riesgo de toxoplasmosis).",
        "Infusiones en grandes cantidades (algunas pueden ser perjudiciales).",
        "Esfuerzos físicos intensos o levantar objetos muy pesados.",
        "Rayos X sin protección abdominal.",
    ],
}

SINTOMAS_CATEGORIAS = {
    "🤢 Físicos frecuentes": [
        "Náuseas o vómitos", "Cansancio y fatiga", "Mareos",
        "Dolor de cabeza", "Dolor de espalda lumbar", "Dolor pélvico",
        "Hinchazón de pies y tobillos", "Calambres nocturnos",
        "Ardor de estómago / reflujo", "Estreñimiento",
        "Frecuencia urinaria aumentada", "Congestión nasal",
        "Dificultad para respirar", "Insomnio",
    ],
    "🔄 Cambios en el cuerpo": [
        "Sensibilidad en los pechos", "Línea nigra",
        "Máscara del embarazo", "Hiperosmia (olfato muy sensible)",
        "Antojos", "Repulsión por alimentos u olores",
        "Varices", "Estrías",
    ],
    "💭 Emocionales y mentales": [
        "Cambios de humor frecuentes", "Ansiedad o preocupación",
        "Tristeza o llanto sin razón", "Miedo al parto",
        "Miedo a no ser buena madre", "Irritabilidad",
        "Dificultad de concentración ('baby brain')",
        "Ilusión y expectación positiva",
    ],
    "👶 Movimientos del bebé": [
        "Primeros movimientos (burbujas)", "Patadas fuertes",
        "Hipo del bebé", "Bebé muy activo después de comer",
        "Movimientos reducidos (consultar si persiste)",
    ],
    "🚨 Señales de alerta (consultar al médico)": [
        "Sangrado vaginal", "Dolor abdominal intenso", "Fiebre alta",
        "Edema severo en cara o manos", "Visión con destellos",
        "Dolor de cabeza muy intenso", "Contracciones antes de semana 37",
    ],
}

NOMBRES_POR_PAIS = {
    "España":         {"nina": ["Sofía","Lucía","María","Martina","Paula","Valeria","Emma","Alba","Carmen","Daniela","Noa","Claudia","Sara","Laura","Andrea","Mía","Elena","Ana","Isabel","Laia"],
                       "nino": ["Hugo","Mateo","Lucas","Leo","Martín","Alejandro","Daniel","Pablo","Adrián","David","Marcos","Javier","Iván","Carlos","Miguel","Sergio","Álvaro","Diego","Mario","Samuel"]},
    "México":         {"nina": ["Valentina","Sofía","Isabella","Camila","Valeria","María","Lucía","Daniela","Fernanda","Natalia","Regina","Ximena","Renata","Mariana","Ana","Karla","Paola","Alicia","Paulina","Michelle"],
                       "nino": ["Santiago","Mateo","Sebastián","Emiliano","Nicolás","Diego","Carlos","Daniel","Alejandro","Miguel","Jesús","Fernando","Ángel","Iván","Ricardo","Eduardo","Luis","Andrés","Jorge","Roberto"]},
    "Argentina":      {"nina": ["Valentina","Sofía","Camila","Martina","Lucía","Emma","Isabella","Agustina","Florencia","Micaela","Julieta","Victoria","Mora","Abril","Zoe","Lola","Mía","Emilia","Catalina","Pilar"],
                       "nino": ["Thiago","Benjamín","Santiago","Mateo","Nicolás","Bautista","Franco","Tomás","Juan","Agustín","Lautaro","Facundo","Gonzalo","Ignacio","Ezequiel","Martín","Joaquín","Rodrigo","Máximo","Ian"]},
    "Colombia":       {"nina": ["Sofía","Valentina","Isabella","Camila","Sara","Mariana","Daniela","Valeria","María","Paula","Natalia","Salomé","Juliana","Ángela","Carolina","Alejandra","Diana","Melissa","Vanessa","Laura"],
                       "nino": ["Santiago","Samuel","Juan","Sebastián","Nicolás","Simón","Mateo","Alejandro","Felipe","Daniel","David","Miguel","Andrés","Jorge","Esteban","Camilo","Ricardo","Luis","Héctor","Iván"]},
    "Chile":          {"nina": ["Sofía","Valentina","Isabella","Camila","Martina","Isidora","Florencia","Catalina","Fernanda","Javiera","Antonia","Emilia","Constanza","Nicole","Gabriela","Natalia","Francisca","Ignacia","Paz","Luna"],
                       "nino": ["Benjamín","Mateo","Santiago","Nicolás","Diego","Agustín","Martín","Sebastián","Felipe","Ignacio","Maximiliano","Francisco","Cristóbal","Vicente","Joaquín","Tomás","Rodrigo","Andrés","Eduardo","Bastián"]},
    "Francia":        {"nina": ["Emma","Jade","Louise","Alice","Chloé","Léa","Manon","Inès","Camille","Zoé","Charlotte","Amélie","Clara","Lucie","Juliette","Mathilde","Sarah","Océane","Pauline","Elisa"],
                       "nino": ["Gabriel","Léo","Raphaël","Louis","Hugo","Théo","Tom","Lucas","Arthur","Ethan","Nathan","Maxime","Antoine","Baptiste","Jules","Nicolas","Quentin","Alexis","Robin","Victor"]},
    "Italia":         {"nina": ["Sofia","Aurora","Giulia","Emma","Ginevra","Alice","Matilde","Beatrice","Martina","Gaia","Sara","Chiara","Giorgia","Alessia","Valentina","Francesca","Elena","Viola","Anna","Elisa"],
                       "nino": ["Leonardo","Francesco","Lorenzo","Alessandro","Matteo","Andrea","Luca","Davide","Riccardo","Marco","Gabriele","Edoardo","Tommaso","Filippo","Simone","Pietro","Federico","Antonio","Alberto","Nicolò"]},
    "Portugal":       {"nina": ["Maria","Beatriz","Matilde","Leonor","Sofia","Mariana","Ana","Carolina","Inês","Francisca","Sara","Catarina","Joana","Rita","Marta","Filipa","Lúcia","Teresa","Raquel","Andreia"],
                       "nino": ["João","Tomás","Francisco","Rodrigo","Afonso","Miguel","Pedro","Rafael","Santiago","Diogo","Guilherme","André","Henrique","Vasco","Carlos","Luís","Gabriel","Eduardo","Nuno","Rúben"]},
    "Alemania":       {"nina": ["Emma","Mia","Hannah","Sofia","Anna","Emilia","Marie","Lena","Lea","Laura","Julia","Lara","Ella","Nina","Katharina","Lisa","Klara","Maja","Paula","Charlotte"],
                       "nino": ["Noah","Leon","Paul","Finn","Jonas","Luis","Elias","Felix","Max","Moritz","Julian","Tim","Jan","Erik","Lukas","David","Tom","Simon","Alexander","Philipp"]},
    "Reino Unido":    {"nina": ["Olivia","Amelia","Isla","Ava","Mia","Freya","Lily","Florence","Rosie","Sophia","Grace","Evie","Poppy","Sienna","Ella","Jessica","Charlotte","Isabella","Emily","Harper"],
                       "nino": ["Oliver","George","Noah","Arthur","Muhammad","Harry","Leo","Oscar","Archie","Henry","Freddie","Alfie","Charlie","Theodore","Jack","Thomas","William","Ethan","James","Luca"]},
    "Estados Unidos": {"nina": ["Olivia","Emma","Charlotte","Amelia","Sophia","Isabella","Ava","Mia","Evelyn","Luna","Harper","Camila","Gianna","Elizabeth","Eleanor","Ella","Abigail","Sofia","Avery","Scarlett"],
                       "nino": ["Liam","Noah","Oliver","Elijah","James","Aiden","Lucas","Mateo","Sebastian","Ethan","Henry","Alexander","Mason","Michael","Benjamin","Daniel","Jackson","Logan","Owen","Samuel"]},
    "Brasil":         {"nina": ["Alice","Sofia","Helena","Laura","Isabella","Manuela","Julia","Valentina","Lívia","Giovanna","Maria","Luísa","Beatriz","Ana","Cecília","Rafaela","Isabela","Lara","Mariana","Camila"],
                       "nino": ["Miguel","Arthur","Heitor","Davi","Gabriel","Pedro","Bernardo","Lucas","Mateus","Rafael","Thiago","Gustavo","Leonardo","Nicolas","João","Felipe","Vinícius","Igor","Bruno","Caio"]},
    "Japón":          {"nina": ["Himari","Hina","Yua","Sakura","Ichika","Akari","Sara","Yui","Aoi","Rin","Haruka","Nana","Riko","Mei","Yuna","Miku","Saki","Koharu","Misaki","Hana"],
                       "nino": ["Haruto","Yuto","Sota","Yuki","Hayato","Ren","Hinata","Riku","Kaito","Ryusei","Sora","Tatsuki","Kei","Shota","Naoki","Takumi","Yusei","Daiki","Kota","Issei"]},
}


# ══════════════════════════════════════════════════════════════
#  FUNCIONES DE LÓGICA (idénticas a la app de escritorio)
# ══════════════════════════════════════════════════════════════

def calcular_semana_y_parto(fecha_fur: date):
    """Calcula semana actual de embarazo y fecha estimada de parto."""
    dias   = (date.today() - fecha_fur).days
    semana = (dias // 7) + 1
    parto  = fecha_fur + timedelta(days=280)
    return semana, parto

def obtener_info_semana(semana: int) -> str:
    if semana in INFO_SEMANAS:
        return INFO_SEMANAS[semana]
    if semana < 1:
        return "La fecha parece ser anterior al embarazo."
    return "Semana fuera del rango típico. Consulta siempre a tu médico."

def obtener_trimestre(semana: int) -> int:
    if semana <= 12: return 1
    if semana <= 27: return 2
    return 3

def get_detalle_bebe(semana: int) -> dict:
    """Devuelve el detalle más cercano sin lanzar excepciones."""
    try:
        semanas_disp = sorted(DETALLE_BEBE.keys())
        clave = semanas_disp[0]
        for s in semanas_disp:
            if s <= semana:
                clave = s
        return DETALLE_BEBE[clave]
    except Exception:
        return {"tam": "—", "peso": "—", "emoji": "👶",
                "desc": "Información no disponible para esta semana."}

def validar_fur(fur: date):
    """
    Devuelve (ok: bool, mensaje: str).
    ok=True significa que la fecha es válida.
    """
    hoy = date.today()
    if fur > hoy:
        return False, "La fecha no puede ser posterior a hoy."
    dias = (hoy - fur).days
    if dias > 43 * 7:
        semanas = dias // 7
        return False, (f"La fecha tiene {semanas} semanas de antigüedad. "
                       "El embarazo dura un máximo de 43 semanas.")
    return True, ""


# ══════════════════════════════════════════════════════════════
#  COMPONENTES REUTILIZABLES
# ══════════════════════════════════════════════════════════════

def aviso_medico():
    """Muestra el aviso médico estándar en el pie de cada página."""
    st.markdown("""
    <div class="aviso-medico">
        ⚕️ <strong>Aviso importante:</strong> Esta app es solo informativa
        y no sustituye en ningún caso la consulta con tu médico, matrona o ginecólogo.
        Ante cualquier duda, consulta siempre a un profesional de la salud.
    </div>
    """, unsafe_allow_html=True)

def caja_info(texto: str):
    st.markdown(f'<div class="info-box">{texto}</div>', unsafe_allow_html=True)

def caja_alerta(texto: str):
    st.markdown(f'<div class="alerta-box">🚨 {texto}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  SIDEBAR — Navegación principal
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🌸 Mi Embarazo")
    st.markdown("*Tu compañera durante estos 9 meses*")
    st.divider()

    pagina = st.radio(
        "Navegar a:",
        options=[
            "🏠 Inicio",
            "👶 Desarrollo del bebé",
            "✅ Checklist trimestre",
            "💡 Consejos",
            "🔤 Nombres",
            "🩺 Síntomas",
            "📈 Seguimiento de peso",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    # Entrada de fecha en el sidebar para que esté siempre disponible
    st.markdown("**📅 Tu fecha de última menstruación**")
    fur_input = st.date_input(
        "FUR",
        value=None,
        min_value=date(2020, 1, 1),
        max_value=date.today(),
        format="DD/MM/YYYY",
        label_visibility="collapsed",
        help="Introduce la fecha de tu última menstruación. "
             "Se usa para calcular la semana de embarazo.",
        key="fur_global",
    )

    # Calculamos y guardamos en session_state para compartir entre páginas
    if fur_input:
        ok, msg = validar_fur(fur_input)
        if ok:
            semana, parto = calcular_semana_y_parto(fur_input)
            st.session_state["semana"]    = semana
            st.session_state["parto"]     = parto
            st.session_state["fur"]       = fur_input
            st.session_state["trimestre"] = obtener_trimestre(semana)
            # Mini resumen en el sidebar
            st.success(f"**Semana {semana}** de embarazo")
            dias_rest = (parto - date.today()).days
            if dias_rest > 0:
                st.info(f"⏳ Faltan **{dias_rest} días** para el parto estimado")
            else:
                st.warning("¡La fecha estimada de parto ya ha pasado!")
        else:
            st.error(msg)

    st.divider()
    st.markdown("<small>Versión Web Beta · Gratuita</small>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  HELPER: obtener semana del session_state
# ══════════════════════════════════════════════════════════════

def get_semana():
    """Devuelve la semana del estado, o None si no hay FUR introducida."""
    return st.session_state.get("semana", None)

def requiere_fur():
    """Muestra aviso y detiene el render si no hay FUR."""
    if get_semana() is None:
        st.info("👈 Introduce la fecha de tu última menstruación en el panel izquierdo para ver esta sección.")
        st.stop()


# ══════════════════════════════════════════════════════════════
#  PÁGINAS
# ══════════════════════════════════════════════════════════════

# ── INICIO ────────────────────────────────────────────────────
if pagina == "🏠 Inicio":
    st.title("🌸 Mi Embarazo")
    st.markdown("*Tu compañera durante estos 9 meses*")
    st.divider()

    if get_semana() is None:
        # Estado vacío: bienvenida
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### ¡Bienvenida! 👋

            Esta app te ayuda a llevar el seguimiento de tu embarazo de forma
            sencilla, privada y desde cualquier dispositivo.

            **Para empezar**, introduce la fecha de tu última menstruación
            en el panel de la izquierda.

            ---
            **Qué puedes hacer aquí:**
            - 📊 Ver tu semana actual y fecha estimada de parto
            - 👶 Información del bebé semana a semana
            - ✅ Checklist de pruebas por trimestre
            - 💡 Consejos de alimentación y ejercicio
            - 🔤 Explorar nombres por país
            - 🩺 Registrar síntomas y emociones
            - 📈 Seguir la evolución de tu peso
            """)
        with col2:
            st.markdown("""
            <div style='text-align:center; font-size:5em; padding:20px;'>
            🌸
            </div>
            """, unsafe_allow_html=True)
    else:
        semana  = st.session_state["semana"]
        parto   = st.session_state["parto"]
        fur     = st.session_state["fur"]
        trim    = st.session_state["trimestre"]
        nombres_trim = {1: "Primer", 2: "Segundo", 3: "Tercer"}
        dias_rest = (parto - date.today()).days

        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Semana actual", f"Semana {semana}", delta=f"de 40")
        with col2:
            st.metric("Trimestre", f"{nombres_trim[trim]} trimestre")
        with col3:
            st.metric("Fecha de parto", parto.strftime("%d/%m/%Y"))
        with col4:
            if dias_rest > 0:
                st.metric("Días restantes", f"{dias_rest} días")
            else:
                st.metric("Días restantes", "¡Ya pasó!")

        # Barra de progreso
        st.markdown("#### Progreso del embarazo")
        pct = min(100, round((semana / 40) * 100, 1))
        st.progress(pct / 100, text=f"{pct}% completado (semana {semana} de 40)")

        st.divider()

        # Info de la semana
        st.markdown("#### 🌱 Esta semana")
        caja_info(obtener_info_semana(semana))

        # Detalle del bebé
        detalle = get_detalle_bebe(semana)
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**{detalle['emoji']} Tamaño del bebé:** {detalle['tam']}")
        with col_b:
            st.markdown(f"**⚖️ Peso aproximado:** {detalle['peso']}")
        st.markdown(f"*{detalle['desc']}*")

    st.divider()
    aviso_medico()


# ── DESARROLLO DEL BEBÉ ────────────────────────────────────────
elif pagina == "👶 Desarrollo del bebé":
    st.title("👶 Desarrollo del bebé")
    st.divider()

    semana_sel = st.slider(
        "Selecciona una semana",
        min_value=1, max_value=42, value=get_semana() or 20,
        help="Desliza para ver información de cualquier semana"
    )

    # Botón rápido a la semana actual
    if get_semana():
        if st.button(f"📍 Ir a mi semana actual ({get_semana()})"):
            semana_sel = get_semana()

    st.divider()

    col1, col2 = st.columns([1, 2])
    detalle = get_detalle_bebe(semana_sel)

    with col1:
        st.markdown(f"""
        <div style='text-align:center; background:#FCE4EC; border-radius:12px;
                    padding:24px; font-size:4em;'>
            {detalle['emoji']}
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Tamaño:** {detalle['tam']}")
        st.markdown(f"**Peso:** {detalle['peso']}")
        trimestre = obtener_trimestre(semana_sel)
        nombres_t = {1: "🌱 Primer trimestre", 2: "🌸 Segundo trimestre", 3: "🌺 Tercer trimestre"}
        st.markdown(f"**Etapa:** {nombres_t[trimestre]}")

    with col2:
        st.markdown(f"### Semana {semana_sel}")
        info = obtener_info_semana(semana_sel)
        caja_info(f"<strong>{info}</strong>")
        st.markdown("")
        st.markdown(detalle["desc"])

    # Timeline visual de progreso
    st.divider()
    st.markdown("#### 📊 Timeline del embarazo")

    import plotly.graph_objects as go

    fig = go.Figure()
    colores = ["#F8BBD0"] * 42
    if semana_sel <= 42:
        for i in range(semana_sel):
            colores[i] = "#D63384"

    fig.add_trace(go.Bar(
        x=list(range(1, 43)),
        y=[1] * 42,
        marker_color=colores,
        text=[str(i) if i % 4 == 0 else "" for i in range(1, 43)],
        textposition="inside",
        hovertemplate="Semana %{x}<extra></extra>",
    ))
    fig.update_layout(
        height=120,
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(title="Semana", tickmode="linear", dtick=4),
        yaxis=dict(visible=False),
        plot_bgcolor="#FFF0F5",
        paper_bgcolor="#FFF0F5",
    )
    # Línea vertical en la semana seleccionada
    fig.add_vline(x=semana_sel, line_dash="dash", line_color="#880E4F", line_width=2)
    st.plotly_chart(fig, use_container_width=True)

    aviso_medico()


# ── CHECKLIST ─────────────────────────────────────────────────
elif pagina == "✅ Checklist trimestre":
    st.title("✅ Checklist por trimestre")

    if get_semana():
        trim_actual = st.session_state["trimestre"]
        st.info(f"Estás en el **{['primer','segundo','tercer'][trim_actual-1]} trimestre** "
                f"(semana {get_semana()}). Se muestra tu checklist actual.")
        trimestres_mostrar = [trim_actual]
    else:
        st.info("Introduce tu fecha de última menstruación para ver solo tu trimestre actual. "
                "Por ahora se muestran todos.")
        trimestres_mostrar = [1, 2, 3]

    # Mostrar también los otros trimestres si la usuaria quiere
    if get_semana():
        if st.checkbox("Ver también los otros trimestres"):
            trimestres_mostrar = [1, 2, 3]

    nombres_trim = {
        1: "🌱 Primer Trimestre (semanas 1-12)",
        2: "🌸 Segundo Trimestre (semanas 13-27)",
        3: "🌺 Tercer Trimestre (semanas 28-42)",
    }

    for t in trimestres_mostrar:
        st.markdown(f"### {nombres_trim[t]}")
        for tarea in CHECKLIST_TRIMESTRES[t]:
            # Cada checkbox tiene una key única para que Streamlit los diferencie
            st.checkbox(tarea, key=f"check_{t}_{tarea[:20]}")
        st.divider()

    aviso_medico()


# ── CONSEJOS ──────────────────────────────────────────────────
elif pagina == "💡 Consejos":
    st.title("💡 Consejos generales")
    st.markdown("*Información orientativa para un embarazo saludable.*")
    st.divider()

    tab_alim, tab_ejer, tab_evit = st.tabs([
        "🥗 Alimentación", "🚶 Ejercicio suave", "⚠️ Qué evitar"
    ])

    for tab, (clave, items) in zip(
        [tab_alim, tab_ejer, tab_evit], CONSEJOS.items()
    ):
        with tab:
            for item in items:
                st.markdown(f"🌸 {item}")

    aviso_medico()


# ── NOMBRES ────────────────────────────────────────────────────
elif pagina == "🔤 Nombres":
    st.title("🔤 Nombres populares")
    st.divider()

    col_pais, col_gen, col_busq = st.columns([2, 1, 2])
    with col_pais:
        pais = st.selectbox("País", sorted(NOMBRES_POR_PAIS.keys()))
    with col_gen:
        genero = st.radio("Género", ["Niña 👧", "Niño 👦"],
                          horizontal=True)
    with col_busq:
        busqueda = st.text_input("🔍 Buscar nombre", placeholder="Escribe aquí...")

    clave_gen = "nina" if "Niña" in genero else "nino"
    nombres = NOMBRES_POR_PAIS.get(pais, {}).get(clave_gen, [])

    if busqueda:
        nombres = [n for n in nombres if busqueda.lower() in n.lower()]

    st.divider()

    # Mostrar como tags visuales
    clase_css = "nombre-tag-nina" if clave_gen == "nina" else "nombre-tag-nino"
    tags_html = "".join(
        f'<span class="{clase_css}">{nombre}</span>'
        for nombre in sorted(nombres)
    )

    if tags_html:
        st.markdown(
            f"<div style='line-height:2.4em;'>{tags_html}</div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("No se encontraron nombres con ese filtro.")

    st.divider()
    st.markdown(f"*{len(nombres)} nombres encontrados para {pais}*")


# ── SÍNTOMAS ──────────────────────────────────────────────────
elif pagina == "🩺 Síntomas":
    st.title("🩺 Síntomas y emociones")
    st.markdown("*Marca lo que estás experimentando hoy. "
                "Nota: los datos solo se guardan en tu sesión actual.*")
    st.divider()

    # Usamos session_state para guardar los marcados durante la sesión
    if "sintomas_marcados" not in st.session_state:
        st.session_state["sintomas_marcados"] = []

    total_marcados = 0

    for categoria, sintomas in SINTOMAS_CATEGORIAS.items():
        with st.expander(categoria, expanded=(categoria == "🤢 Físicos frecuentes")):
            cols = st.columns(2)
            for i, sintoma in enumerate(sintomas):
                col = cols[i % 2]
                key = f"sint_{categoria[:10]}_{sintoma[:15]}"
                if "alerta" in categoria.lower():
                    # Los síntomas de alerta se destacan en rojo
                    marcado = col.checkbox(f"🔴 {sintoma}", key=key)
                else:
                    marcado = col.checkbox(sintoma, key=key)
                if marcado:
                    total_marcados += 1

    st.divider()

    if total_marcados > 0:
        caja_info(f"Has marcado <strong>{total_marcados} síntoma(s)</strong> hoy. "
                  "Recuerda comentárselos a tu médico o matrona en tu próxima visita.")

    # Nota adicional libre
    nota = st.text_area(
        "📝 Notas adicionales (cómo te sientes hoy)",
        placeholder="Escribe aquí cualquier detalle que quieras recordar...",
        height=120
    )

    aviso_medico()


# ── SEGUIMIENTO DE PESO ────────────────────────────────────────
elif pagina == "📈 Seguimiento de peso":
    st.title("📈 Seguimiento de peso")
    st.divider()

    # ── Nota sobre almacenamiento ──────────────────────────────
    st.info(
        "ℹ️ **Nota de la versión Beta:** En la versión web los datos de peso "
        "se guardan solo durante tu sesión actual. Si cierras la pestaña, "
        "se borran. Para persistencia permanente, usa la app de escritorio."
    )

    # Inicializar lista de pesos en session_state
    if "pesos" not in st.session_state:
        st.session_state["pesos"] = []

    # Formulario para añadir peso
    with st.form("form_peso", clear_on_submit=True):
        col_f, col_p, col_b = st.columns([2, 2, 1])
        with col_f:
            fecha_peso = st.date_input("Fecha", value=date.today(),
                                       format="DD/MM/YYYY")
        with col_p:
            kg = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0,
                                 step=0.1, format="%.1f")
        with col_b:
            st.markdown("<br>", unsafe_allow_html=True)  # espaciado
            enviar = st.form_submit_button("➕ Añadir")

        if enviar:
            st.session_state["pesos"].append({
                "fecha": fecha_peso,
                "peso": kg
            })
            st.success(f"✓ Añadido: {kg} kg el {fecha_peso.strftime('%d/%m/%Y')}")

    pesos = st.session_state["pesos"]

    if pesos:
        # Ordenar por fecha
        pesos_ord = sorted(pesos, key=lambda x: x["fecha"])

        # Gráfica con plotly
        import plotly.graph_objects as go

        fechas_str = [p["fecha"].strftime("%d/%m") for p in pesos_ord]
        valores    = [p["peso"] for p in pesos_ord]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=fechas_str, y=valores,
            mode="lines+markers+text",
            line=dict(color="#D63384", width=3),
            marker=dict(color="#880E4F", size=10,
                        line=dict(color="white", width=2)),
            text=[f"{v:.1f}" for v in valores],
            textposition="top center",
            textfont=dict(color="#880E4F", size=11),
            name="Peso",
        ))
        fig.update_layout(
            height=380,
            plot_bgcolor="#FFF8FA",
            paper_bgcolor="#FFF0F5",
            xaxis=dict(title="Fecha", gridcolor="#F8BBD0"),
            yaxis=dict(title="Peso (kg)", gridcolor="#F8BBD0"),
            margin=dict(l=10, r=10, t=20, b=10),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Estadísticas rápidas
        col1, col2, col3 = st.columns(3)
        col1.metric("Peso inicial", f"{valores[0]:.1f} kg")
        col2.metric("Peso actual",  f"{valores[-1]:.1f} kg")
        variacion = valores[-1] - valores[0]
        col3.metric("Variación total",
                    f"{variacion:+.1f} kg",
                    delta=f"{variacion:+.1f} kg")

        # Tabla de registros
        st.divider()
        st.markdown("#### Todos los registros")
        for i, p in enumerate(reversed(pesos_ord)):
            col_d, col_v, col_x = st.columns([3, 2, 1])
            col_d.write(p["fecha"].strftime("%d/%m/%Y"))
            col_v.write(f"**{p['peso']:.1f} kg**")
            if col_x.button("🗑", key=f"del_{i}",
                            help="Eliminar este registro"):
                st.session_state["pesos"].remove(p)
                st.rerun()
    else:
        st.markdown("""
        <div style='text-align:center; color:#AAAAAA; padding:40px; font-size:1.1em;'>
            Sin registros todavía.<br>Añade tu primer peso con el formulario de arriba.
        </div>
        """, unsafe_allow_html=True)

    aviso_medico()
