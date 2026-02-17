import streamlit as st
import pandas as pd
from datetime import datetime

def render_backlog_page(db):
    st.title("\U0001f4cb Backlog de Pedidos")
    
    orders = db.get_orders()
    deniers = db.get_deniers()
    
    # Summary metrics
    total_kg = sum(o.get('total_kg', 0) for o in orders)
    total_orders = len(orders)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pedidos", total_orders)
    col2.metric("Total Kg Pendientes", f"{total_kg:,.0f}")
    col3.metric("Deniers Activos", len(deniers))
    
    # Orders table
    if orders:
        st.subheader("Pedidos Pendientes")
        df = pd.DataFrame(orders)
        
        # Add priority column formatting
        if 'priority' in df.columns:
            df['priority'] = df['priority'].map({1: '\U0001f534 Alta', 2: '\U0001f7e1 Media', 3: '\U0001f7e2 Baja'})
        
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay pedidos pendientes")
    
    # Add new order form
    st.subheader("\u2795 Agregar Pedido")
    with st.form("add_order"):
        col1, col2 = st.columns(2)
        with col1:
            denier_options = {d['name']: d['id'] for d in deniers}
            selected_denier = st.selectbox("Denier", list(denier_options.keys()))
        with col2:
            kg = st.number_input("Kg", min_value=0.0, step=100.0)
        
        req_date = st.date_input("Fecha Requerida", value=datetime.now())
        
        if st.form_submit_button("Agregar Pedido"):
            if selected_denier and kg > 0:
                db.create_order(
                    denier_options[selected_denier], 
                    kg, 
                    str(req_date)
                )
                st.success(f"Pedido de {kg}kg ({selected_denier}) agregado")
                st.rerun()
            else:
                st.warning("Complete todos los campos")
    
    # Edit/Delete section
    if orders:
        st.subheader("\u270f\ufe0f Editar / Eliminar")
        for order in orders:
            with st.expander(f"Pedido {order['id'][:8]}..."):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.json(order)
                with col2:
                    if st.button("\U0001f5d1\ufe0f Eliminar", key=f"del_{order['id']}"):
                        db.delete_order(order['id'])
                        st.success("Pedido eliminado")
                        st.rerun()
