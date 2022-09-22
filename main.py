import pandas as pd
from flask import Flask,request
from flask import jsonify

def obtener_recomendaciones(id):
  ordenes = pd.read_csv('ordenes.csv')
  ordenes_por_producto = ordenes[ordenes.id_producto == id].id_orden.unique()

  ordenes_relevantes = ordenes[ordenes.id_orden.isin(ordenes_por_producto)]
  productos_acompannates_por_orden = ordenes_relevantes[ordenes_relevantes.id_producto != id]

  num_instancia_por_producto_acompannate = productos_acompannates_por_orden.groupby('id_producto')['id_producto'].count().reset_index(name='instancias')

  num_ordenes_por_producto = ordenes_por_producto.size
  instancias_producto = pd.DataFrame(num_instancia_por_producto_acompannate)
  instancias_producto["frequency"] = instancias_producto["instancias"]/num_ordenes_por_producto

  productos_recomendados = pd.DataFrame(instancias_producto.sort_values("frequency", ascending=False).head(3))

  productos = pd.read_csv('productos.csv')
  productos_recomendados = pd.merge(productos_recomendados, productos, on="id_producto")

  return productos_recomendados.to_json(orient="table")

# API Server
app = Flask(__name__)
@app.route("/recomendar/<int:id>", methods=["GET"])
def recomendar(id):
    print("id_producto: " + str(id))
    return obtener_recomendaciones(id)
 
if __name__ == '__main__':
   app.run()

