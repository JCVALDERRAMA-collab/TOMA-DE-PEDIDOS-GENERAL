import streamlit as st
import pandas as pd
from datetime import datetime
import os
import re
from st_copy_to_clipboard import st_copy_to_clipboard

# --- Configuration for the consecutive number ---
CONSECUTIVE_FILE = 'ultimo_consecutivo.txt'
INITIAL_CONSECUTIVE = 1000

def get_next_consecutive():
    """Reads the last consecutive number from a file, increments it, and saves it back.
    This function should only be called when a *new* order is being finalized."""
    current_consecutive = INITIAL_CONSECUTIVE
    if os.path.exists(CONSECUTIVE_FILE):
        try:
            with open(CONSECUTIVE_FILE, 'r') as f:
                content = f.read().strip()
                if content:
                    current_consecutive = int(content)
                else:
                    st.warning(f"Advertencia: El archivo '{CONSECUTIVE_FILE}' está vacío. Reiniciando consecutivo a {INITIAL_CONSECUTIVE}.")
                    current_consecutive = INITIAL_CONSECUTIVE
        except ValueError:
            st.warning(f"Advertencia: El archivo '{CONSECUTIVE_FILE}' contiene un valor inválido. Reiniciando consecutivo a {INITIAL_CONSECUTIVE}.")
            current_consecutive = INITIAL_CONSECUTIVE

    next_consecutive = current_consecutive + 1
    with open(CONSECUTIVE_FILE, 'w') as f:
        f.write(str(next_consecutive))

    return next_consecutive

# Initialize the file if it doesn't exist on first run
if not os.path.exists(CONSECUTIVE_FILE):
    with open(CONSECUTIVE_FILE, 'w') as f:
        f.write(str(INITIAL_CONSECUTIVE))

# --- 1. Datos de los productos ---
productos_data = [
    {"COD_PRODUCTO": "DDPHCO0010", "DESCRIPCION": "DERMADIVA CON COLAGENO X 10 UNIDAD / CAJA X 48", "UNIDAD_X_PAQUETE": 10, "UNIDAD_X_CAJA": 48},
    {"COD_PRODUCTO": "DDPHPE0001", "DESCRIPCION": "DERMADIVA CON PEPINO X 10UNIDAD / CAJA X 48", "UNIDAD_X_PAQUETE": 10, "UNIDAD_X_CAJA": 48},
    {"COD_PRODUCTO": "DDPHSR0010", "DESCRIPCION": "DERMADIVA CON ROSAS Y ALOE VERA X 10 UNIDAD / CAJA X 48", "UNIDAD_X_PAQUETE": 10, "UNIDAD_X_CAJA": 48},
    {"COD_PRODUCTO": "DDPHBA0010", "DESCRIPCION": "TOALLA DESMAQUILLANTE DERMADIVA X 10-48 SURTIDA", "UNIDAD_X_PAQUETE": 10, "UNIDAD_X_CAJA": 48},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "AMARRE TO. DESMAQUILLANTES FACE CLEAN COLAGENO X 30 / CAJA X 24", "UNIDAD_X_PAQUETE": 30, "UNIDAD_X_CAJA": 24},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "AMARRE TO. DESMAQUILLANTES FACE CLEAN MIXTA X 30 / CAJA X 24 UN", "UNIDAD_X_PAQUETE": 30, "UNIDAD_X_CAJA": 24},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "AMARRE TO. DESMAQUILLANTES FACE CLEAN PEPINO X 30 / CAJA X 24 U", "UNIDAD_X_PAQUETE": 30, "UNIDAD_X_CAJA": 24},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "AMARRE TO. DESMAQUILLANTES FACE CLEAN ROSAS Y ALOE VERA X 30 /", "UNIDAD_X_PAQUETE": 30, "UNIDAD_X_CAJA": 24},
    {"COD_PRODUCTO": "SWPHSA0050", "DESCRIPCION": "TOALLAS HUMEDAS SENIORS WIPES X 50 / CAJA X 12 UND", "UNIDAD_X_PAQUETE": 50, "UNIDAD_X_CAJA": 12},
    {"COD_PRODUCTO": "FKPHSA0010", "DESCRIPCION": "PAÑITOS HÚMEDOS FRESKITOS X 10 / CAJA X 48", "UNIDAD_X_PAQUETE": 10, "UNIDAD_X_CAJA": 48},
    {"COD_PRODUCTO": "FKPHSA0025", "DESCRIPCION": "PAÑITOS HÚMEDOS FRESKITOS X 25 / CAJA X 48 UND", "UNIDAD_X_PAQUETE": 25, "UNIDAD_X_CAJA": 48},
    {"COD_PRODUCTO": "FTPHSA0040", "DESCRIPCION": "PAÑITOS HÚMEDOS FRESKITOS X 40 / CAJA X 36 UND", "UNIDAD_X_PAQUETE": 40, "UNIDAD_X_CAJA": 36},
    {"COD_PRODUCTO": "FTPHSA0102", "DESCRIPCION": "PAÑITOS HÚMEDOS FRESKITOS X 102 / CAJA X 12 UND", "UNIDAD_X_PAQUETE": 102, "UNIDAD_X_CAJA": 12},
    {"COD_PRODUCTO": "FTPHSA0105", "DESCRIPCION": "PAÑITOS HÚMEDOS FRESKITOS X 105 / CAJA X 24 UND", "UNIDAD_X_PAQUETE": 105, "UNIDAD_X_CAJA": 24},
    {"COD_PRODUCTO": "FGPHSA001", "DESCRIPCION": "PAÑITOS HÚMEDOS ED ESPECIAL NEGRO X1", "UNIDAD_X_PAQUETE": 1, "UNIDAD_X_CAJA": 480},
    {"COD_PRODUCTO": "FGPHSA0010", "DESCRIPCION": "PAÑITOS HÚMEDOS ED ESPECIAL NEGRO X10", "UNIDAD_X_PAQUETE": 10, "UNIDAD_X_CAJA": 48},
    {"COD_PRODUCTO": "FGPHSA0015", "DESCRIPCION": "PAÑITOS HÚMEDOS ED ESPECIAL NEGRO X15", "UNIDAD_X_PAQUETE": 15, "UNIDAD_X_CAJA": 30},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "DETERGENTE MAXI WASH PLUS X 5 KG / BULTO X 4", "UNIDAD_X_PAQUETE": 5, "UNIDAD_X_CAJA": 4},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "DETERGENTE MAXI WASH PLUS X 2 KG / BULTO X 10", "UNIDAD_X_PAQUETE": 2, "UNIDAD_X_CAJA": 10},
    {"COD_PRODUCTO": "MWHTAO1000", "DESCRIPCION": "DETERGENTE MAXI WASH PLUS X 1 KG / BULTO X 20 UND", "UNIDAD_X_PAQUETE": 1, "UNIDAD_X_CAJA": 20},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "DETERGENTE MAXI WASH MULTIUSOS X 1 KG / BULTO X 20 UND", "UNIDAD_X_PAQUETE": 1, "UNIDAD_X_CAJA": 20},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "DETERGENTE MAXI WASH MULTIUSOS X 2 KG / BULTO X 10 UND", "UNIDAD_X_PAQUETE": 2, "UNIDAD_X_CAJA": 10},
    {"COD_PRODUCTO": "ANEBMF0300", "DESCRIPCION": "ENJUAGUE BUCAL ACTIVMINT MENTA FRESCA X 300ML / CAJA X 15 UN", "UNIDAD_X_PAQUETE": 300, "UNIDAD_X_CAJA": 15},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "ENJUAGUE BUCAL ACTIVMINT MENTA FRESCA X 500ML / CAJA X 15 UN", "UNIDAD_X_PAQUETE": 500, "UNIDAD_X_CAJA": 15},
    {"COD_PRODUCTO": "ANEBYB0300", "DESCRIPCION": "ENJUAGUE BUCAL ACTIVMINT YERBABUENA 300ML / CAJA X 15 UND", "UNIDAD_X_PAQUETE": 300, "UNIDAD_X_CAJA": 15},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "ENJUAGUE BUCAL ACTIVMINT YERBABUENA 500ML / CAJA X 15 UND", "UNIDAD_X_PAQUETE": 500, "UNIDAD_X_CAJA": 15},
    {"COD_PRODUCTO": "FKCRLB0012", "DESCRIPCION": "CREMA HUMECTANTE FRESKITOS MANOS Y CUERPO X 800ML / CAJA X 12", "UNIDAD_X_PAQUETE": 800, "UNIDAD_X_CAJA": 12},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "JABON LIQUIDO AVENA X 1000 ML / CAJA X 16", "UNIDAD_X_PAQUETE": 1000, "UNIDAD_X_CAJA": 16},
    {"COD_PRODUCTO": "FKJLFR1000", "DESCRIPCION": "JABON LIQUIDO FRESKITOS FRUTOS ROJOS X 1L / CAJA X 16 UND", "UNIDAD_X_PAQUETE": 1000, "UNIDAD_X_CAJA": 16},
    {"COD_PRODUCTO": "FKJLMV1000", "DESCRIPCION": "JABON LIQUIDO FRESKITOS MANZANA VERDE X 1L / CAJA X 16 UND", "UNIDAD_X_PAQUETE": 1000, "UNIDAD_X_CAJA": 16},
    {"COD_PRODUCTO": "FPPNMC050", "DESCRIPCION": "PAÑITOS HUMEDOS FRESKISPETS X 50 / CAJA X 48 UND", "UNIDAD_X_PAQUETE": 50, "UNIDAD_X_CAJA": 48},
    {"COD_PRODUCTO": "FKSHAL0800", "DESCRIPCION": "SHAMPOO FRESKITOS ALOE Y MANZANILLA X 500 ML / CAJA X 24 UND", "UNIDAD_X_PAQUETE": 500, "UNIDAD_X_CAJA": 24},
    {"COD_PRODUCTO": "FKSHMA0800", "DESCRIPCION": "SHAMPOO FRESKITOS MANZANILLA X 800 ML / CAJA X 24 UND", "UNIDAD_X_PAQUETE": 800, "UNIDAD_X_CAJA": 24},
    {"COD_PRODUCTO": "FKSHMA0800", "DESCRIPCION": "SHAMPOO FRESKITOS MANZANILLA X 800 ML / CAJA X 12 UND", "UNIDAD_X_PAQUETE": 800, "UNIDAD_X_CAJA": 12},
    {"COD_PRODUCTO": "FKSHRM0500", "DESCRIPCION": "SHAMPOO FRESKITOS ROMERO Y FRUTOS DEL BOSQUE X 500 ML / CAJ", "UNIDAD_X_PAQUETE": 500, "UNIDAD_X_CAJA": 24},
    {"COD_PRODUCTO": "FKSHRM0800", "DESCRIPCION": "SHAMPOO FRESKITOS ROMERO Y FRUTOS DEL BOSQUE X 800 ML / CAJ", "UNIDAD_X_PAQUETE": 800, "UNIDAD_X_CAJA": 12},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "JABON FACE CLEAN CARBÓN ACTIVADO 75 GR", "UNIDAD_X_PAQUETE": 1, "UNIDAD_X_CAJA": 18},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "JABON BAÑO BARRA CAJA SURTIDA X 75 GR / CAJA X 75 -", "UNIDAD_X_PAQUETE": 75, "UNIDAD_X_CAJA": 75},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "PAÑALES 0 X 18 X 12", "UNIDAD_X_PAQUETE": 18, "UNIDAD_X_CAJA": 12},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "PAÑALES 1 X 18 X 12", "UNIDAD_X_PAQUETE": 18, "UNIDAD_X_CAJA": 12},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "PAÑALES ET 2 X 18 X 12", "UNIDAD_X_PAQUETE": 18, "UNIDAD_X_CAJA": 12},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "PAÑALES ET 3 X 18 X 12", "UNIDAD_X_PAQUETE": 18, "UNIDAD_X_CAJA": 12},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "PAÑALES ET 4 X 18 X 12", "UNIDAD_X_PAQUETE": 18, "UNIDAD_X_CAJA": 12},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "TOALLAS DE COCINA 80 UNID X 15", "UNIDAD_X_PAQUETE": 80, "UNIDAD_X_CAJA": 15},
    {"COD_PRODUCTO": "HCTHFL0020", "DESCRIPCION": "TOALLAS MULTIUSOS BBQ HYPER CLEAN X 20 / CAJA X 12 UND", "UNIDAD_X_PAQUETE": 20, "UNIDAD_X_CAJA": 12},
    {"COD_PRODUCTO": "POBOLD7W12", "DESCRIPCION": "BOMBILLO LED POLAR X 7W / CAJA X 12 UND", "UNIDAD_X_PAQUETE": 1, "UNIDAD_X_CAJA": 12},
    {"COD_PRODUCTO": "#N/D", "DESCRIPCION": "BOMBILLO LED POLAR X 9W / CAJA X 12 UND", "UNIDAD_X_PAQUETE": 9, "UNIDAD_X_CAJA": 12},
]

df_productos = pd.DataFrame(productos_data)
# Prepend an empty string to the product descriptions for the "empty" selectbox option
all_product_options = [""] + df_productos['DESCRIPCION'].tolist()

# --- Initialize session state ---
if 'pedido_actual' not in st.session_state:
    st.session_state.pedido_actual = []
if 'global_summary_core_text' not in st.session_state:
    st.session_state.global_summary_core_text = ""
if 'show_generated_summary' not in st.session_state:
    st.session_state.show_generated_summary = False
if 'cliente_email_input' not in st.session_state:
    st.session_state.cliente_email_input = ''
if 'cliente_telefono_input' not in st.session_state:
    st.session_state.cliente_telefono_input = ''
if 'product_select_index' not in st.session_state:
    st.session_state.product_select_index = 0
if 'cantidad_cajas_input' not in st.session_state:
    st.session_state.cantidad_cajas_input = 0
if 'cantidad_unidades_input' not in st.session_state:
    st.session_state.cantidad_unidades_input = 0
if 'current_consecutive_number' not in st.session_state:
    st.session_state.current_consecutive_number = None
if 'reset_inputs_flag' not in st.session_state:
    st.session_state.reset_inputs_flag = False
if 'nit_input_value' not in st.session_state: # New: To store NIT input
    st.session_state.nit_input_value = ''
if 'nombre_cliente_display' not in st.session_state: # New: To store client name to display
    st.session_state.nombre_cliente_display = 'CONSUMIDOR FINAL'

# --- NEW: Load Client Data ---
# Changed to .xlsx
CLIENTES_FILE = 'clientes.xlsx' 
df_clientes = pd.DataFrame() # Initialize an empty DataFrame
if os.path.exists(CLIENTES_FILE):
    try:
        # Use pd.read_excel() for Excel files
        df_clientes = pd.read_excel(CLIENTES_CSV)
        # Ensure NIT column is treated as string to avoid type issues (e.g., leading zeros)
        df_clientes['NIT'] = df_clientes['NIT'].astype(str)
    except Exception as e:
        st.error(f"Error al cargar la base de datos de clientes: {e}. Asegúrate de que '{CLIENTES_FILE}' sea un archivo Excel válido.")
else:
    st.warning(f"Advertencia: No se encontró el archivo de clientes '{CLIENTES_FILE}'. El autocompletado de clientes no funcionará.")


# --- NEW: Function to lookup client name ---
def lookup_client_name(nit_value):
    if df_clientes.empty or not nit_value:
        return 'CONSUMIDOR FINAL' # Default if no data or no NIT entered

    # Search for the NIT in the client DataFrame
    # Ensure the input NIT is also a string for consistent comparison
    found_client = df_clientes[df_clientes['NIT'] == str(nit_value)]
    if not found_client.empty:
        return found_client.iloc[0]['NOMBRE_CLIENTE']
    else:
        return 'CONSUMIDOR FINAL' # Default if NIT not found


# --- NEW: Callback for NIT input change ---
def on_nit_change():
    # Update the stored NIT value and re-lookup client name
    st.session_state.nombre_cliente_display = lookup_client_name(st.session_state.nit_input_widget)
    # Important: Reset summary if NIT changes to ensure it's regenerated with correct client name
    st.session_state.global_summary_core_text = ""
    st.session_state.show_generated_summary = False


# --- Check reset flag at the start of the script ---
if st.session_state.reset_inputs_flag:
    st.session_state.product_select_index = 0
    st.session_state.cantidad_cajas_input = 0
    st.session_state.cantidad_unidades_input = 0
    st.session_state.reset_inputs_flag = False # Reset the flag immediately

# --- Validation functions for email and phone ---
def is_valid_email(email):
    """Basic email validation."""
    if not email: # Allow empty email
        return True
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)

def is_valid_phone(phone):
    """Basic phone validation (allows for optional leading + and spaces/hyphens)."""
    if not phone: # Allow empty phone
        return True
    # Ensures at least 7 digits, allows + at start, and spaces/hyphens in between
    return re.match(r"^\+?[\d\s\-]{7,15}$", phone)

# --- Callback function to handle adding product and setting reset flag ---
def add_product_callback(producto_encontrado, selected_index, cantidad_cajas, cantidad_unidades):
    if not selected_index or (cantidad_cajas == 0 and cantidad_unidades == 0):
        st.error("❌ Error: Selecciona un producto e ingresa al menos una cantidad (caja o unidad).")
    else:
        st.session_state.pedido_actual.append({
            "COD_PRODUCTO": producto_encontrado['COD_PRODUCTO'],
            "DESCRIPCION": selected_index,
            "CANT_CAJAS": cantidad_cajas,
            "CANT_UNIDADES_IND": cantidad_unidades,
            "UNIDAD_X_CAJA": producto_encontrado['UNIDAD_X_CAJA'],
            "UNIDAD_X_PAQUETE": producto_encontrado['UNIDAD_X_PAQUETE']
        })
        st.success(f"Producto '{selected_index}' añadido al pedido.")
        st.session_state.global_summary_core_text = ""
        st.session_state.show_generated_summary = False
        st.session_state.reset_inputs_flag = True # Set the flag here to trigger reset on next run
        # No need for st.rerun() here, as setting the flag will cause it naturally

# --- Callback function for 'Volver y Añadir Más Productos' button ---
def go_back_and_add_more():
    st.session_state.show_generated_summary = False
    st.session_state.global_summary_core_text = ""
    st.session_state.reset_inputs_flag = True # Reset inputs when going back
    # No st.rerun() needed

# --- Callback function for 'Limpiar Pedido Completo' button ---
def clear_all_products():
    st.session_state.pedido_actual = []
    st.session_state.global_summary_core_text = ""
    st.session_state.show_generated_summary = False
    st.session_state.current_consecutive_number = None
    st.session_state.reset_inputs_flag = True # Reset inputs when clearing order
    st.success("✔️ ¡Pedido limpiado!")
    # No st.rerun() needed


# --- Streamlit UI ---
st.set_page_config(layout="centered", page_title="Generador de Pedidos Consumidor Final")

# --- Sección para el logo ---
try:
    st.image("LOGO 2.png", width=200)
except FileNotFoundError:
    st.warning("⚠️ No se encontró el logo. Asegúrate de que 'LOGO 2.png' esté en la misma carpeta o la ruta sea correcta.")

st.title("📝 Generador de Pedidos General")
st.markdown("Completa los detalles para generar un resumen de tu solicitud.")

st.write("---")

st.subheader("Datos del Cliente")

# Modified NIT input
nit_input_value = st.text_input(
    "NIT:",
    value=st.session_state.nit_input_value, # Use session state for value
    key='nit_input_widget', # Unique key
    on_change=on_nit_change # Call on_nit_change when NIT input changes
)

# After the text_input, update the session state for the NIT value
st.session_state.nit_input_value = nit_input_value

# Display the client name based on lookup
# Use st.session_state.nombre_cliente_display for the client name
nombre_cliente = st.text_input(
    "Cliente:",
    value=st.session_state.nombre_cliente_display, # Use the dynamic client name
    disabled=True, # Keep this disabled as it's auto-populated
    key='cliente_display_input' # A new key for the display field
)


st.write("---")

st.subheader("Selección de Productos")

if not st.session_state.show_generated_summary:
    selected_index = st.selectbox(
        'Selecciona un producto:',
        options=all_product_options,
        index=st.session_state.product_select_index,
        key='product_select_widget',
        help="Empieza a escribir o selecciona un producto de la lista."
    )
    # The selectbox's value changes, so we need to update its index in state
    # This line should remain as it updates the index based on user selection in the current run
    st.session_state.product_select_index = all_product_options.index(selected_index) if selected_index in all_product_options else 0


    producto_encontrado = None
    if selected_index and selected_index != "":
        df_filtered = df_productos[df_productos['DESCRIPCION'] == selected_index]
        if not df_filtered.empty:
            producto_encontrado = df_filtered.iloc[0]
        else:
            st.error("Producto no válido o no encontrado. Por favor, selecciona de la lista.")

    col1, col2 = st.columns(2)

    with col1:
        cantidad_cajas = st.number_input(
            "Cantidad de Cajas:",
            min_value=0,
            value=st.session_state.cantidad_cajas_input,
            step=1,
            disabled=(producto_encontrado is None),
            key='cantidad_cajas_input'
        )

    with col2:
        cantidad_unidades = st.number_input(
            "Cantidad de Unidades Individuales:",
            min_value=0,
            value=st.session_state.cantidad_unidades_input,
            step=1,
            disabled=(producto_encontrado is None),
            key='cantidad_unidades_input'
        )

    st.button(
        'Añadir Producto al Pedido',
        type="primary",
        key='add_product_button',
        disabled=(producto_encontrado is None or (cantidad_cajas == 0 and cantidad_unidades == 0)),
        on_click=add_product_callback,
        args=(producto_encontrado, selected_index, cantidad_cajas, cantidad_unidades)
    )

st.write("---")

st.subheader("Productos en el Pedido")
if st.session_state.pedido_actual:
    if not st.session_state.show_generated_summary:
        st.button("Limpiar Pedido Completo", key='clear_all_products_button', type="secondary", on_click=clear_all_products)

    for i, item in enumerate(st.session_state.pedido_actual):
        total_unidades_item = (item['CANT_CAJAS'] * item['UNIDAD_X_CAJA']) + item['CANT_UNIDADES_IND']
        st.markdown(f"**{i+1}.** {item['DESCRIPCION']} - Cajas: {item['CANT_CAJAS']}, Unidades: {item['CANT_UNIDADES_IND']} (Total: {total_unidades_item} uds)")
else:
    st.info("No hay productos añadidos al pedido aún.")

st.write("---")

st.subheader("Información de Contacto Adicional")

cliente_email_input = st.text_input("Email Cliente:", value=st.session_state.cliente_email_input, placeholder='ejemplo@dominio.com', key='cliente_email_input')
cliente_telefono_input = st.text_input("Teléfono Cliente:", value=st.session_state.cliente_telefono_input, placeholder='Ej: 3001234567', key='cliente_telefono_input')

# Check if contact info has changed. If so, reset summary state
if (cliente_email_input != st.session_state.get('last_email_input_value', '')) or \
   (cliente_telefono_input != st.session_state.get('last_phone_input_value', '')):
    st.session_state.global_summary_core_text = ""
    st.session_state.show_generated_summary = False
    st.session_state.last_email_input_value = cliente_email_input
    st.session_state.last_phone_input_value = cliente_telefono_input


st.write("---")

if not st.session_state.show_generated_summary:
    if st.button('Generar Resumen Final', type="secondary", key='generate_summary_button'):
        if not st.session_state.pedido_actual:
            st.warning("No hay productos en el pedido para generar un resumen.")
        else:
            email_valid = is_valid_email(cliente_email_input)
            phone_valid = is_valid_phone(cliente_telefono_input)

            if not email_valid:
                st.error("❌ Error: Formato de email inválido. Por favor, corrígelo antes de generar el resumen.")
            elif not phone_valid:
                st.error("❌ Error: Formato de teléfono inválido. Por favor, corrígelo antes de generar el resumen.")
            else:
                if st.session_state.current_consecutive_number is None:
                    st.session_state.current_consecutive_number = get_next_consecutive()

                summary_core = ""
                summary_core += "--- Resumen General de la Solicitud ---\n"
                summary_core += f"Número de Pedido: {st.session_state.current_consecutive_number}\n"
                summary_core += f"Fecha y Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                summary_core += f"NIT: {st.session_state.nit_input_value}\n" # Use stored NIT value
                summary_core += f"Cliente: {st.session_state.nombre_cliente_display}\n" # Use stored client name

                if cliente_email_input:
                    summary_core += f"Email Cliente: {cliente_email_input}\n"
                if cliente_telefono_input:
                    summary_core += f"Teléfono Cliente: {cliente_telefono_input}\n"

                summary_core += "\n--- Detalles de los Productos Pedidos ---\n"

                for i, item in enumerate(st.session_state.pedido_actual):
                    total_unidades_item = (item['CANT_CAJAS'] * item['UNIDAD_X_CAJA']) + item['CANT_UNIDADES_IND']
                    summary_core += f"\nProducto {i+1}:\n"
                    summary_core += f"  Código: {item['COD_PRODUCTO']}\n"
                    summary_core += f"  Descripción: {item['DESCRIPCION']}\n"
                    summary_core += f"  Cant. Cajas: {item['CANT_CAJAS']}\n"
                    summary_core += f"  Cant. Unidades Individuales: {item['CANT_UNIDADES_IND']}\n"
                    summary_core += f"  Unidades por Caja (del producto): {item['UNIDAD_X_CAJA']}\n"
                    summary_core += f"  Total Unidades Calculadas: {total_unidades_item}\n"

                summary_core += "\n-------------------------------------\n"
                summary_core += "Resumen de la solicitud finalizado."

                st.session_state.global_summary_core_text = summary_core
                st.session_state.show_generated_summary = True
                st.rerun()


if st.session_state.show_generated_summary:
    st.write("---")
    st.subheader("Resumen Generado")
    st.code(st.session_state.global_summary_core_text)

    col_sum1, col_sum2 = st.columns(2)
    with col_sum1:
        if st.button("Copiar Información", key='copy_summary_button', type="primary"):
            st_copy_to_clipboard(st.session_state.global_summary_core_text)
            st.success("¡Mensaje copiado al portapapeles! Ya puedes pegarlo donde necesites.")
    with col_sum2:
        st.button(
            "Volver y Añadir Más Productos",
            key='add_more_products_button',
            type="secondary",
            on_click=go_back_and_add_more
        )
        
st.markdown("---")
st.caption("Hecho por Cartera ATW Internacional.")
