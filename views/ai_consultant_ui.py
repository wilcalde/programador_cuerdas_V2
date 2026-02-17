import streamlit as st

def render_ai_consultant(db):
    st.title("\U0001f916 Consultor IA")
    st.info("Chat con el asistente de producci\u00f3n inteligente")
    
    # Simple chat interface
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for msg in st.session_state.chat_history:
        if msg['role'] == 'user':
            st.chat_message("user").write(msg['content'])
        else:
            st.chat_message("assistant").write(msg['content'])
    
    # Chat input
    user_input = st.chat_input("Escribe tu consulta...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        
        # Simulated response
        response = f"Procesando consulta: '{user_input}'. Esta funcionalidad est\u00e1 en desarrollo."
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
    
    # Generate scenario button
    if st.button("\U0001f52e Generar Escenario Autom\u00e1tico"):
        with st.spinner("Generando escenario optimizado..."):
            st.success("Escenario en desarrollo")
