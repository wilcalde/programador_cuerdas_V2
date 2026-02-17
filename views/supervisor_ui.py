import streamlit as st
from datetime import datetime

def render_supervisor_reports(db):
    st.title("\U0001f4dd Reportes de Novedades")
    
    machines = db.get_machines_torsion()
    machine_ids = [m['id'] for m in machines]
    
    with st.form("report_form"):
        machine = st.selectbox("M\u00e1quina", machine_ids)
        report_type = st.selectbox("Tipo", ["Mec\u00e1nica", "El\u00e9ctrica", "Calidad", "Material"])
        description = st.text_area("Descripci\u00f3n")
        hours = st.number_input("Horas de Impacto", min_value=0.0, step=0.5)
        
        if st.form_submit_button("Registrar Novedad"):
            if machine and description:
                db.create_report(machine, report_type, description, hours)
                st.success("Novedad registrada exitosamente")
            else:
                st.warning("Complete todos los campos")
    
    # Recent reports (placeholder)
    st.subheader("Historial Reciente")
    st.info("Funcionalidad de historial en desarrollo")
