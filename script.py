import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import datetime

# Configuración inicial
st.title("Sistema de Gestión de Pedidos en Línea")
st.markdown("Bienvenido a nuestra tienda en línea")

# Barra de navegación
nav = st.sidebar.selectbox("Navegación", ["Realizar Pedido", "Ver Estado de Pedido", "Cancelar/Modificar Pedido"])

# Base de datos de pedidos
pedidos = pd.DataFrame({
    "Pedido ID": [],
    "Producto": [],
    "Cantidad": [],
    "Pago": [],
    "Estado": [],
    "Fecha de entrega": [],
    "Departamento": []
})

# Función para agregar nuevo pedido
def agregar_pedido(pedido_id, producto, cantidad, pago, estado, fecha_entrega, departamento):
    if not pedidos.loc[pedidos["Pedido ID"] == pedido_id].empty:
        st.error("El pedido ya existe en la base de datos")
        return
    pedidos.loc[len(pedidos.index)] = {
        "Pedido ID": pedido_id,
        "Producto": producto,
        "Cantidad": cantidad,
        "Pago": pago,
        "Estado": estado,
        "Fecha de entrega": fecha_entrega,
        "Departamento": departamento
    }

# Función para actualizar estado de pedido
def actualizar_estado_pedido(pedido_id, estado, fecha_entrega, departamento):
    if not pedidos.loc[pedidos["Pedido ID"] == pedido_id].empty:
        pedidos.loc[pedidos["Pedido ID"] == pedido_id, "Estado"] = estado
        pedidos.loc[pedidos["Pedido ID"] == pedido_id, "Fecha de entrega"] = fecha_entrega
        pedidos.loc[pedidos["Pedido ID"] == pedido_id, "Departamento"] = departamento
    else:
        st.error("El pedido no existe en la base de datos")

# Función para enviar correo electrónico
def enviar_correo_electronico(pedido_id):
    try:
        mensaje = MIMEMultipart()
        mensaje["From"] = os.environ["CORREO_ELECTRONICO"]
        mensaje["To"] = os.environ["CORREO_CLIENTE"]
        mensaje["Subject"] = "Estado de Pedido"
        cuerpo = f"El estado de su pedido {pedido_id} es {pedidos.loc[pedidos['Pedido ID'] == pedido_id, 'Estado'].values[0]}. La fecha de entrega es {pedidos.loc[pedidos['Pedido ID'] == pedido_id, 'Fecha de entrega'].values[0]}."
        mensaje.attach(MIMEText(cuerpo, "plain"))
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(mensaje["From"], os.environ["CONTRASEÑA"])
        servidor.sendmail(mensaje["From"], mensaje["To"], mensaje.as_string())
        servidor.quit()
        st.success("Correo electrónico enviado con éxito")
    except Exception as e:
        st.error(f"Error al enviar correo electrónico: {e}")

# Formulario de pedido
if nav == "Realizar Pedido":
    st.header("Formulario de Pedido")
    producto = st.selectbox("Seleccione un producto", ["Producto 1", "Producto 2", "Producto 3"])
    cantidad = st.number_input("Ingrese la cantidad", min_value=1, max_value=10)
    pago = st.selectbox("Seleccione un método de pago", ["Tarjeta de crédito", "PayPal"])
    if st.button("Realizar Pedido"):
        pedido_id = len(pedidos) + 1
        agregar_pedido(pedido_id, producto, cantidad, pago, "En proceso", datetime.date.today(), "Departamento 1")
        st.success("Pedido realizado con éxito")

# Tablero de estado de pedido
if nav == "Ver Estado de Pedido":
    st.header("Tablero de Estado de Pedido")
    pedido_id = st.selectbox("Seleccione el pedido", pedidos["Pedido ID"])
    estado_pedido = st.selectbox("Seleccione el estado del pedido", ["En proceso", "Enviado", "Entregado"])
    fecha_entrega = st.date_input("Fecha de entrega")
    departamento = st.selectbox("Seleccione el departamento responsable", ["Departamento 1", "Departamento 2"])
    if st.button("Actualizar Estado de Pedido"):
        actualizar_estado_pedido(pedido_id, estado_pedido, fecha_entrega, departamento)
        st.success("Estado de pedido actualizado con éxito")

# Botón de cancelación/modificación de pedido
if nav == "Cancelar/Modificar Pedido":
    st.header("Cancelar/Modificar Pedido")
    pedido_id = st.selectbox("Seleccione el pedido", pedidos["Pedido ID"])
    if st.button("Cancelar Pedido"):
        pedidos.drop(pedidos[pedidos["Pedido ID"] == pedido_id].index, inplace=True)
        st.success("Pedido cancelado con éxito")
    if st.button("Modificar Pedido"):
        producto = st.selectbox("Seleccione un producto", ["Producto 1", "Producto 2", "Producto 3"])
        cantidad = st.number_input("Ingrese la cantidad", min_value=1, max_value=10)
        pago = st.selectbox("Seleccione un método de pago", ["Tarjeta de crédito", "PayPal"])
        if st.button("Modificar Pedido"):
            pedidos.loc[pedidos["Pedido ID"] == pedido_id, "Producto"] = producto
            pedidos.loc[pedidos["Pedido ID"] == pedido_id, "Cantidad"] = cantidad
            pedidos.loc[pedidos["Pedido ID"] == pedido_id, "Pago"] = pago
            st.success("Pedido modificado con éxito")

# Gráfico de informes
if st.button("Generar Informe"):
    st.header("Informe de Pedidos")
    informe = pedidos
    st.write(informe)

# Enviar correos electrónicos automáticos
if st.button("Enviar Correos Electrónicos"):
    for index, row in pedidos.iterrows():
        enviar_correo_electronico(row["Pedido ID"])
        st.success("Correo electrónico enviado con éxito")