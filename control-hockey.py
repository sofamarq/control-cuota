import streamlit as st
import pandas as pd
from io import BytesIO

st.title('Control de Cuotas de Hockey')
st.write('Sube un archivo Excel con las columnas "Cobrar" y "Efectivas".')

# Entrada para seleccionar el mes
mes = st.text_input("Ingrese el mes del análisis (ejemplo: Marzo 2024)")

uploaded_file = st.file_uploader("Subir archivo Excel", type=["xls", "xlsx", "xlsm"])

if uploaded_file is not None and mes:
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

            st.write(f"Total cobrado más de una vez: {len(repetidos)}")
            if repetidos:
                st.write("Número de socia cobrado más de una vez:")
                st.write(pd.Series(repetidos, index=range(1, len(repetidos) + 1)))

            # Crear archivo Excel con historial de análisis
            output = BytesIO()
            no_cobrados_df = pd.DataFrame({'Número de socia no cobrados': no_pagaron_ids})
            historial_df = pd.DataFrame({
                'Concepto': ["Total a cobrar", "Total efectivas", "Total no cobrado", "Total cobrado más de una vez"],
                'Valor': [total_cobrar, total_efectivas, len(no_pagaron_ids), len(repetidos)]
            })
            
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                no_cobrados_df.to_excel(writer, index=False, sheet_name='No Cobrados')
                historial_df.to_excel(writer, index=False, sheet_name='Historial')
            output.seek(0)

            filename = f"analisis_cuotas_{mes.replace(' ', '_')}.xlsx"

            st.download_button(
                label="Descargar reporte completo en Excel",
                data=output,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error('El archivo debe tener las columnas "Cobrar" y "Efectivas".')
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
else:
    st.info('Ingrese el mes del análisis y suba un archivo.')
