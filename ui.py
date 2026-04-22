import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos de pedidos
pedidos = pd.DataFrame({
    'Fecha de entrega': ['2023-03-15', '2023-03-20', '2023-03-25'],
    'Estado del pedido': ['Pendiente', 'En proceso', 'Entregado'],
    'Detalles del pedido': ['Pedido 1', 'Pedido 2', 'Pedido 3']
})

# Crear barra de navegación
st.sidebar.title('Menú')
menu = st.sidebar.selectbox('Seleccione una opción', ['Crear pedido', 'Ver pedidos', 'Asignar pedido', 'Notificaciones'])

# Crear formulario de creación de pedido
if menu == 'Crear pedido':
    st.title('Crear pedido')
    fecha_entrega = st.date_input('Fecha de entrega')
    estado_pedido = st.selectbox('Estado del pedido', ['Pendiente', 'En proceso', 'Entregado'])
    detalles_pedido = st.text_input('Detalles del pedido')
    if st.button('Crear pedido'):
        # Crear nuevo pedido
        nuevo_pedido = pd.DataFrame({
            'Fecha de entrega': [fecha_entrega],
            'Estado del pedido': [estado_pedido],
            'Detalles del pedido': [detalles_pedido]
        })
        pedidos = pd.concat([pedidos, nuevo_pedido])

# Crear tabla de pedidos
if menu == 'Ver pedidos':
    st.title('Pedidos')
    st.write(pedidos)

# Crear gráfico de estado de pedidos
if menu == 'Ver pedidos':
    st.title('Estado de pedidos')
    plt.bar(pedidos['Estado del pedido'].value_counts().index, pedidos['Estado del pedido'].value_counts().values)
    st.pyplot(plt)

# Crear botón de asignación de pedido
if menu == 'Asignar pedido':
    st.title('Asignar pedido')
    cliente = st.selectbox('Seleccione un cliente', ['Cliente 1', 'Cliente 2', 'Cliente 3'])
    if st.button('Asignar pedido'):
        # Asignar pedido al cliente
        pedidos.loc[pedidos['Fecha de entrega'] == '2023-03-15', 'Estado del pedido'] = 'Asignado'

# Crear campo de búsqueda
st.title('Buscar pedidos')
busqueda = st.text_input('Ingrese la fecha de entrega, estado del pedido o detalles del pedido')
if st.button('Buscar'):
    # Buscar pedidos
    resultados = pedidos[pedidos['Fecha de entrega'].str.contains(busqueda) | pedidos['Estado del pedido'].str.contains(busqueda) | pedidos['Detalles del pedido'].str.contains(busqueda)]
    st.write(resultados)
Nota: Este código es solo un ejemplo y debe ser adaptado y personalizado según las necesidades específicas del proyecto.