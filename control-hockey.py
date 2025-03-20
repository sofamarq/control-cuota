import streamlit as st
import pandas as pd

st.title('Control de Cuotas de Hockey')
st.write('Sube un archivo Excel con las columnas "Cobrar" y "Efectivas".')

uploaded_file = st.file_uploader("Subir archivo Excel", type=["xls", "xlsx", "xlsm"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        if 'Cobrar' in df.columns and 'Efectivas' in df.columns:
            cobrar_ids = pd.to_numeric(df['Cobrar'], errors='coerce').dropna().astype(int).tolist()
            efectivas_ids = pd.to_numeric(df['Efectivas'], errors='coerce').dropna().astype(int).tolist()

            total_cobrar = len(cobrar_ids)
            total_efectivas = len(efectivas_ids)
            no_pagaron_ids = list(set(cobrar_ids) - set(efectivas_ids))
            repetidos = [id for id in set(efectivas_ids) if efectivas_ids.count(id) > 1]

            st.write(f"Total a cobrar: {total_cobrar}")
            st.write(f"Total efectivas: {total_efectivas}")
            st.write(f"Total no cobrado: {len(no_pagaron_ids)}")
            st.write("Número de socia no cobrados:")
            st.write(pd.Series(no_pagaron_ids, index=range(1, len(no_pagaron_ids) + 1)))

            st.write(f"Total cobrados más de una vez: {len(repetidos)}")
            if repetidos:
                st.write("Número de socia cobrado más de una vez:")
                st.write(pd.Series(repetidos, index=range(1, len(repetidos) + 1)))
        else:
            st.error('El archivo debe tener las columnas "Cobrar" y "Efectivas".')
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
else:
    st.info('Espera a que subas el archivo.')
