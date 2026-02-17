import streamlit as st
import plotly.graph_objects as go

def render_dashboard(db):
    st.title("\U0001f4ca Dashboard")
    
    # KPIs
    orders = db.get_orders()
    machines = db.get_machines_torsion()
    
    total_pending = sum(o.get('total_kg', 0) - (o.get('produced_kg') or 0) for o in orders)
    active_machines = len([m for m in machines if m.get('husos_activos', 0) > 0])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Kg Pendientes", f"{total_pending:,.0f}")
    col2.metric("Pedidos Activos", len(orders))
    col3.metric("M\u00e1quinas Activas", active_machines)
    col4.metric("Eficiencia", "80%")
    
    # Workload Chart
    st.subheader("Carga de Trabajo")
    if orders:
        denier_kg = {}
        for o in orders:
            d = o.get('deniers', {}).get('name', 'Sin Denier') if o.get('deniers') else 'Sin Denier'
            denier_kg[d] = denier_kg.get(d, 0) + o.get('total_kg', 0)
        
        fig = go.Figure([go.Bar(x=list(denier_kg.keys()), y=list(denier_kg.values()))])
        fig.update_layout(
            title="Kg por Denier",
            xaxis_title="Denier",
            yaxis_title="Kilogramos",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Sync button
    if st.button("\U0001f504 Sincronizar con Google Sheets"):
        from integrations.google_sheets import sync_production_from_sheets
        result = sync_production_from_sheets()
        if 'error' in result:
            st.error(result['error'])
        else:
            st.success("Sincronizaci\u00f3n completada")
    
    # Machine Status
    st.subheader("Estado de M\u00e1quinas Torsi\u00f3n")
    for m in machines:
        status = "\U0001f7e2 Activa" if m.get('husos_activos', 0) > 0 else "\U0001f534 Inactiva"
        st.text(f"{m['id']}: {status} - {m.get('husos_activos', 0)} husos")
