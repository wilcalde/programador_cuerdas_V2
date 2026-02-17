import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render_programming_page(db, run_scheduler_fn):
    st.title("\u2699\ufe0f Programaci\u00f3n de Producci\u00f3n")
    
    # Get data
    orders = db.get_orders()
    machines = db.get_machines_torsion()
    deniers = db.get_deniers()
    
    if not orders:
        st.warning("No hay pedidos pendientes en el backlog.")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        strategy = st.selectbox("Estrategia", ["Por Kg/Hora", "Por Prioridad", "Mixta"])
    with col2:
        horizon = st.slider("D\u00edas a programar", 1, 14, 7)
    
    if st.button("\u25b6\ufe0f Ejecutar Programaci\u00f3n", type="primary"):
        with st.spinner("Generando plan de producci\u00f3n..."):
            result = run_scheduler_fn(orders, machines, deniers, strategy, horizon)
            
            if result:
                st.success("\u2705 Plan generado exitosamente")
                
                # Display summary metrics
                col1, col2, col3, col4 = st.columns(4)
                summary = result.get('resumen_programa', {})
                col1.metric("Total Kg", f"{summary.get('total_kg', 0):,.0f}")
                col2.metric("D\u00edas", summary.get('dias_totales', 0))
                col3.metric("Rewinders", summary.get('total_rewinders', 0))
                col4.metric("Operarios/Turno", summary.get('operarios_turno', 0))
                
                # Display schedule table
                if 'tabla_turnos' in result:
                    st.subheader("Cronograma por Turnos")
                    for turno in result['tabla_turnos']:
                        st.markdown(f"**{turno['fecha']}**")
                        if turno.get('detalles'):
                            df = pd.DataFrame(turno['detalles'])
                            st.dataframe(df, use_container_width=True)

def render_config_page(db):
    st.title("\u2699\ufe0f Configuraci\u00f3n")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Torsi\u00f3n", "Rewinder", "Cat\u00e1logo", "Turnos"])
    
    with tab1:
        st.subheader("M\u00e1quinas de Torsi\u00f3n")
        machines = db.get_machines_torsion()
        for m in machines:
            with st.expander(f"M\u00e1quina {m['id']}"):
                rpm = st.number_input("RPM", value=m.get('rpm', 0), key=f"rpm_{m['id']}")
                torsions = st.number_input("Torsiones/m", value=m.get('torsions_meter', 0), key=f"tor_{m['id']}")
                husos = st.number_input("Husos Activos", value=m.get('husos_activos', 0), key=f"hus_{m['id']}")
                if st.button("Guardar", key=f"save_{m['id']}"):
                    db.update_machine_torsion(m['id'], rpm, torsions, husos)
                    st.success(f"M\u00e1quina {m['id']} actualizada")
    
    with tab2:
        st.subheader("Configuraci\u00f3n Rewinder por Denier")
        configs = db.get_rewinder_denier_configs()
        for c in configs:
            col1, col2, col3 = st.columns(3)
            col1.text(f"Denier: {c['denier']}")
            col2.text(f"MP: {c['mp_segundos']}s")
            col3.text(f"TM: {c['tm_minutos']}min")
    
    with tab3:
        st.subheader("Cat\u00e1logo de Deniers")
        deniers = db.get_deniers()
        df = pd.DataFrame(deniers)
        st.dataframe(df, use_container_width=True)
    
    with tab4:
        st.subheader("Calendario de Turnos")
        today = datetime.now().date()
        for i in range(7):
            day = today + timedelta(days=i)
            hours = st.number_input(
                f"{day.strftime('%A %d/%m')}", 
                min_value=0, max_value=24, value=24,
                key=f"shift_{day}"
            )
