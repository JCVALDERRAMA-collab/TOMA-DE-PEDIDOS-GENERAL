# --- NEW: Load Client Data ---
CLIENTES_FILE = 'clientes.xlsx' # Cambiado a .xlsx
df_clientes = pd.DataFrame() # Initialize an empty DataFrame
if os.path.exists(CLIENTES_FILE):
    try:
        df_clientes = pd.read_excel(CLIENTES_FILE) # Cambiado a pd.read_excel
        # Ensure NIT column is treated as string to avoid type issues (e.g., leading zeros)
        df_clientes['NIT'] = df_clientes['NIT'].astype(str)
    except Exception as e:
        st.error(f"Error al cargar la base de datos de clientes: {e}. Asegúrate de que '{CLIENTES_FILE}' sea un archivo Excel válido con una hoja de trabajo predeterminada.")
else:
    st.warning(f"Advertencia: No se encontró el archivo de clientes '{CLIENTES_FILE}'. El autocompletado de clientes no funcionará.")
        
st.markdown("---")
st.caption("Hecho por Cartera ATW Internacional.")
