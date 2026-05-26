import csv
import os
from datetime import datetime

import streamlit as st

# -----------------------------------
# CONFIGURACIÓN
# -----------------------------------

st.set_page_config(
    page_title="Cerrador Pro",
    page_icon="💼",
    layout="wide"
)

# -----------------------------------
# ESTILOS
# -----------------------------------

st.markdown("""
<style>

.main {
    background-color: #f4f6f8;
}

.box {
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 16px;
    background: #ffffff;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
}

.aprobado {
    border-left: 5px solid #2d8f50;
    background: #eff8f1;
    color: #1b4e2a;
}

.denegado {
    border-left: 5px solid #c0392b;
    background: #f9ecec;
    color: #782026;
}

.comision {
    padding: 20px;
    border-radius: 14px;
    background: #fff8e1;
    color: #5c4b1c;
    font-size: 18px;
    font-weight: 600;
}

.destino {
    padding: 14px;
    border-radius: 12px;
    background: #e7f5f8;
    color: #084b56;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# BASE DE DATOS
# -----------------------------------

zonas = {
    "Alabama": "Costa Este",
    "Alaska": "Costa Oeste",
    "Arizona": "Costa Oeste",
    "Arkansas": "Zona Central",
    "California": "Costa Oeste",
    "Colorado": "Costa Oeste",
    "Connecticut": "Costa Este",
    "Delaware": "Costa Este",
    "Florida": "Costa Este",
    "Georgia": "Costa Este",
    "Hawaii": "Costa Oeste",
    "Idaho": "Costa Oeste",
    "Illinois": "Costa Este",
    "Indiana": "Costa Este",
    "Iowa": "Zona Central",
    "Kansas": "Zona Central",
    "Kentucky": "Costa Este",
    "Louisiana": "Zona Central",
    "Maine": "Costa Este",
    "Maryland": "Costa Este",
    "Massachusetts": "Costa Este",
    "Michigan": "Costa Este",
    "Minnesota": "Zona Central",
    "Mississippi": "Costa Este",
    "Missouri": "Zona Central",
    "Montana": "Costa Oeste",
    "Nebraska": "Zona Central",
    "Nevada": "Costa Oeste",
    "New Hampshire": "Costa Este",
    "New Jersey": "Costa Este",
    "New Mexico": "Costa Oeste",
    "New York": "Costa Este",
    "North Carolina": "Costa Este",
    "North Dakota": "Zona Central",
    "Ohio": "Costa Este",
    "Oklahoma": "Zona Central",
    "Oregon": "Costa Oeste",
    "Pennsylvania": "Costa Este",
    "Rhode Island": "Costa Este",
    "South Carolina": "Costa Este",
    "South Dakota": "Zona Central",
    "Tennessee": "Costa Este",
    "Texas": "Zona Central",
    "Utah": "Costa Oeste",
    "Vermont": "Costa Este",
    "Virginia": "Costa Este",
    "Washington": "Costa Oeste",
    "West Virginia": "Costa Este",
    "Wisconsin": "Costa Este",
    "Wyoming": "Costa Oeste",
    "Puerto Rico": "Puerto Rico"
}

hoteles = {
    "Orlando": ["Avanti", "Buena Vista Suites"],
    "Vegas": ["Tuscany Suites"],
    "Cancún": ["Oasis Palm Lite", "Villa del Palmar"],
    "Punta Cana": ["Ancora"]
}

horarios = {
    "Costa Oeste": "6 AM - 2 PM",
    "Zona Central": "7 AM - 4 PM",
    "Costa Este": "9 AM - 5 PM",
    "Puerto Rico": "10 AM - 5 PM"
}

SALES_FILE = "sales_records.csv"
FIELDNAMES = [
    "timestamp",
    "cliente",
    "estado",
    "estado_civil",
    "edad",
    "residencia",
    "zona",
    "destino",
    "hotel",
    "paquete",
    "vigencia",
    "deducible",
    "comision",
    "ventas",
    "ganancia_unitaria",
    "total"
]


def ensure_sales_file():
    if not os.path.exists(SALES_FILE):
        with open(SALES_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def load_sales():
    ensure_sales_file()
    with open(SALES_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def save_sale(record):
    ensure_sales_file()
    with open(SALES_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(record)


def compute_package(estado_civil, edad, residencia):
    califica = False
    paquete = "MIX & MATCH"
    vigencia = "24 meses"
    motivo = "No cumple los requisitos"

    if residencia == "Sí":
        if estado_civil == "Casado / Convive":
            if 25 <= edad <= 79:
                califica = True
                paquete = "VDL"
                vigencia = "18 meses"
        elif estado_civil == "Mujer Soltera":
            if 25 <= edad <= 72:
                califica = True
                paquete = "HÍBRIDO"
                vigencia = "18 meses"
        elif estado_civil == "Hombre Soltero":
            if 35 <= edad <= 59:
                califica = True
                paquete = "VDL"
                vigencia = "18 meses"
        elif estado_civil == "Divorciado":
            if 25 <= edad <= 72:
                califica = True
                paquete = "HÍBRIDO"
                vigencia = "18 meses"

    return califica, paquete, vigencia, motivo


def reset_form():
    st.session_state["cliente"] = ""
    st.session_state["estado"] = "Alabama"
    st.session_state["estado_civil"] = "Casado / Convive"
    st.session_state["edad"] = 35
    st.session_state["residencia"] = "Sí"
    st.session_state["destino"] = "Orlando"
    st.session_state["hotel"] = hoteles["Orlando"][0]
    st.session_state["porcentaje"] = 6
    st.session_state["ventas"] = 1
    st.session_state["deducible"] = 399
    st.session_state["message"] = ""
    st.session_state["sale_registered"] = False


if "cliente" not in st.session_state:
    reset_form()

if "message" not in st.session_state:
    st.session_state["message"] = ""

if "sale_registered" not in st.session_state:
    st.session_state["sale_registered"] = False

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.header("Datos del cliente")

cliente = st.sidebar.text_input("Nombre del cliente", key="cliente")

estado = st.sidebar.selectbox(
    "Estado",
    sorted(list(zonas.keys())),
    key="estado"
)

estado_civil = st.sidebar.selectbox(
    "Estado civil",
    [
        "Casado / Convive",
        "Mujer Soltera",
        "Hombre Soltero",
        "Divorciado"
    ],
    key="estado_civil"
)

edad = st.sidebar.number_input(
    "Edad",
    18,
    100,
    key="edad"
)

residencia = st.sidebar.selectbox(
    "Residente USA/Canadá?",
    ["Sí", "No"],
    key="residencia"
)

st.sidebar.markdown("---")

st.sidebar.markdown("Vista principal con todos los hoteles disponibles por ciudad.")

porcentaje = st.sidebar.radio(
    "Comisión (%)",
    [6, 8],
    index=0,
    key="porcentaje"
) / 100

ventas = 1
st.sidebar.markdown("Solo se puede vender 1 paquete por registro.")

st.sidebar.markdown("---")

st.sidebar.button("Limpiar formulario", on_click=reset_form)

register_click = st.sidebar.button("Registrar venta")

# -----------------------------------
# LÓGICA
# -----------------------------------

zona = zonas[estado]
califica, paquete, vigencia, motivo = compute_package(estado_civil, edad, residencia)

deducible = st.number_input(
    "Monto deducible",
    150,
    500,
    399,
    key="deducible"
)

ganancia = deducible * porcentaje

total = ganancia * ventas

if register_click:
    record = {
        "timestamp": datetime.now().isoformat(sep=" ", timespec="seconds"),
        "cliente": cliente,
        "estado": estado,
        "estado_civil": estado_civil,
        "edad": edad,
        "residencia": residencia,
        "zona": zona,
        "destino": "No aplica",
        "hotel": "No aplica",
        "paquete": paquete,
        "vigencia": vigencia,
        "deducible": deducible,
        "comision": porcentaje,
        "ventas": ventas,
        "ganancia_unitaria": ganancia,
        "total": total
    }
    save_sale(record)
    st.session_state["message"] = "Venta registrada correctamente. Puede iniciar una nueva operación con Limpiar formulario."
    st.session_state["sale_registered"] = True

# -----------------------------------
# INTERFAZ
# -----------------------------------

st.title("Cerrador Pro")
st.write("Sistema de calificación y registro de ventas para paquetes vacacionales.")

if st.button("Ver registros de ventas"):
    st.session_state["show_records"] = True

if "show_records" not in st.session_state:
    st.session_state["show_records"] = False

if st.session_state["show_records"]:
    ventas_guardadas = load_sales()
    if ventas_guardadas:
        st.subheader("Registros de ventas")
        st.dataframe(ventas_guardadas, use_container_width=True)
        if st.button("Ocultar registros"):
            st.session_state["show_records"] = False
    else:
        st.info("No hay ventas registradas aún.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Resultado")

    if califica:
        st.markdown(f"""
        <div class="box aprobado">
        Cliente: {cliente or 'No ingresado'}
        <br>
        Califica para: <strong>{paquete}</strong>
        <br>
        Vigencia: {vigencia}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="box denegado">
        Cliente: {cliente or 'No ingresado'}
        <br>
        Enviar a MIX & MATCH
        <br>
        {motivo}
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Hoteles por ciudad")
    for ciudad, lista_hoteles in hoteles.items():
        st.markdown(f"""
        <div class="box destino">
        {ciudad}
        </div>
        """, unsafe_allow_html=True)
        for hotel_item in lista_hoteles:
            st.write(hotel_item)

with col2:
    st.subheader("Zona y horario")
    st.info(f"Zona detectada: {zona}\nHorario: {horarios[zona]}")

    st.subheader("Comisión")
    st.markdown(f"""
    <div class="comision">
    Total: ${total:,.2f} USD
    <br><br>
    Ganancia por unidad: ${ganancia:,.2f}
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Speech")
    if califica:
        st.success(
            """
            El cliente califica para un paquete especial. Puede comunicarle que el viaje ya está aprobado y que solo necesita cubrir el deducible para comenzar a reservar.
            Recuérdale que este paquete ofrece una vigencia amplia y un plan diseñado para maximizar su experiencia de vacaciones con el menor esfuerzo posible.
            """
        )
    else:
        st.warning(
            """
            El cliente no cumple los requisitos para los paquetes preferenciales en este momento.
            Ofrece la alternativa MIX & MATCH, destacando los beneficios del plan y la posibilidad de mantener el interés mientras se busca una opción adecuada.
            """
        )

    if st.session_state["message"]:
        st.success(st.session_state["message"])
        st.session_state["message"] = ""

st.markdown("""
### Acerca de la aplicación
Esta herramienta ayuda a los asesores a evaluar clientes y registrar cada venta con la información clave: nombre, estado, edad, residencia, destino, hotel, paquete y comisiones.
""")
