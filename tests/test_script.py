import unittest
import pandas as pd
import streamlit as st
import os
import datetime

class PruebasSistemaDePedidos(unittest.TestCase):
    def setUp(self):
        self.pedidos = pd.DataFrame({
            "Pedido ID": [],
            "Producto": [],
            "Cantidad": [],
            "Pago": [],
            "Estado": [],
            "Fecha de entrega": [],
            "Departamento": []
        })

    def test_crear_pedido(self):
        producto = "Producto 1"
        cantidad = 5
        pago = "Tarjeta de crédito"
        estado = "En proceso"
        fecha_entrega = datetime.date.today()
        departamento = "Departamento 1"
        agregar_pedido(len(self.pedidos) + 1, producto, cantidad, pago, estado, fecha_entrega, departamento)
        self.assertEqual(len(self.pedidos), 1)
        self.assertEqual(self.pedidos.loc[0, "Producto"], producto)
        self.assertEqual(self.pedidos.loc[0, "Cantidad"], cantidad)
        self.assertEqual(self.pedidos.loc[0, "Pago"], pago)
        self.assertEqual(self.pedidos.loc[0, "Estado"], estado)
        self.assertEqual(self.pedidos.loc[0, "Fecha de entrega"], fecha_entrega)
        self.assertEqual(self.pedidos.loc[0, "Departamento"], departamento)

    def test_realizar_pedido_con_campos_incompletos(self):
        producto = "Producto 1"
        cantidad = 0
        pago = "Tarjeta de crédito"
        estado = "En proceso"
        fecha_entrega = datetime.date.today()
        departamento = "Departamento 1"
        with self.assertRaises(ValueError):
            agregar_pedido(len(self.pedidos) + 1, producto, cantidad, pago, estado, fecha_entrega, departamento)

    def test_verificar_estado_de_pedido(self):
        producto = "Producto 1"
        cantidad = 5
        pago = "Tarjeta de crédito"
        estado = "En proceso"
        fecha_entrega = datetime.date.today()
        departamento = "Departamento 1"
        agregar_pedido(len(self.pedidos) + 1, producto, cantidad, pago, estado, fecha_entrega, departamento)
        actualizar_estado_pedido(len(self.pedidos), "Enviado", datetime.date.today(), "Departamento 2")
        self.assertEqual(self.pedidos.loc[0, "Estado"], "Enviado")
        self.assertEqual(self.pedidos.loc[0, "Fecha de entrega"], datetime.date.today())
        self.assertEqual(self.pedidos.loc[0, "Departamento"], "Departamento 2")

    def test_cancelar_pedido(self):
        producto = "Producto 1"
        cantidad = 5
        pago = "Tarjeta de crédito"
        estado = "En proceso"
        fecha_entrega = datetime.date.today()
        departamento = "Departamento 1"
        agregar_pedido(len(self.pedidos) + 1, producto, cantidad, pago, estado, fecha_entrega, departamento)
        pedidos.drop(pedidos[pedidos["Pedido ID"] == len(self.pedidos)].index, inplace=True)
        self.assertEqual(len(self.pedidos), 0)

    def test_modificar_pedido(self):
        producto = "Producto 1"
        cantidad = 5
        pago = "Tarjeta de crédito"
        estado = "En proceso"
        fecha_entrega = datetime.date.today()
        departamento = "Departamento 1"
        agregar_pedido(len(self.pedidos) + 1, producto, cantidad, pago, estado, fecha_entrega, departamento)
        pedidos.loc[pedidos["Pedido ID"] == len(self.pedidos), "Producto"] = "Producto 2"
        pedidos.loc[pedidos["Pedido ID"] == len(self.pedidos), "Cantidad"] = 10
        pedidos.loc[pedidos["Pedido ID"] == len(self.pedidos), "Pago"] = "PayPal"
        self.assertEqual(self.pedidos.loc[0, "Producto"], "Producto 2")
        self.assertEqual(self.pedidos.loc[0, "Cantidad"], 10)
        self.assertEqual(self.pedidos.loc[0, "Pago"], "PayPal")

    def test_enviar_correos_electronicos_automáticos(self):
        producto = "Producto 1"
        cantidad = 5
        pago = "Tarjeta de crédito"
        estado = "En proceso"
        fecha_entrega = datetime.date.today()
        departamento = "Departamento 1"
        agregar_pedido(len(self.pedidos) + 1, producto, cantidad, pago, estado, fecha_entrega, departamento)
        enviar_correo_electronico(len(self.pedidos))
        self.assertEqual(len(self.pedidos), 1)

if __name__ == "__main__":
    unittest.main()