import pandas as pd
import random
from datetime import datetime, timedelta
import uuid

# --- CONFIGURACIÓN ---
NUM_REGISTROS = 10000
PORCENTAJE_FRAUDE = 0.05  # 5% de las transacciones serán fraudulentas

# Listas de datos simulados
CIUDADES_SEGURAS = ['CDMX', 'Monterrey', 'Guadalajara', 'Queretaro', 'Merida']
CIUDADES_RIESGO = ['Tijuana', 'Culiacan', 'Reynosa', 'Lagos', 'Moscu'] # Ciudades para simular anomalías
CATEGORIAS = ['Supermercado', 'Gasolinera', 'Restaurante', 'Farmacia', 'Streaming']
CATEGORIAS_LUJO = ['Joyeria', 'Electronica', 'Casino', 'Viajes']

def generar_tarjeta_falsa():
    # Genera un número fake que parece real pero enmascarado
    bin_card = random.choice(['4152', '5500', '3782']) 
    return f"{bin_card}-xxxx-xxxx-{random.randint(1000,9999)}"

def generar_datos():
    data = []
    print(f"🔄 Generando {NUM_REGISTROS} transacciones (Simulando {PORCENTAJE_FRAUDE*100}% de fraude)...")

    for _ in range(NUM_REGISTROS):
        es_fraude = random.random() < PORCENTAJE_FRAUDE
        
        # Datos base
        tx_id = str(uuid.uuid4())
        cliente_id = random.randint(10000, 99999)
        tarjeta = generar_tarjeta_falsa()
        fecha = datetime(2026, 2, 1) + timedelta(minutes=random.randint(0, 40000))

        if es_fraude:
            # --- LÓGICA DE FRAUDE ---
            # Montos altos, ciudades extrañas o categorías de alto riesgo
            monto = round(random.uniform(15000.00, 80000.00), 2)
            ciudad = random.choice(CIUDADES_RIESGO)
            categoria = random.choice(CATEGORIAS_LUJO)
            comercio = f"Comercio_Sospechoso_{random.randint(1,50)}"
        else:
            # --- LÓGICA NORMAL ---
            # Montos comunes, ciudades habituales
            monto = round(random.uniform(20.00, 2500.00), 2)
            ciudad = random.choice(CIUDADES_SEGURAS)
            categoria = random.choice(CATEGORIAS)
            comercio = f"Comercio_Local_{random.randint(1,100)}"

        data.append([tx_id, fecha, cliente_id, tarjeta, comercio, categoria, ciudad, monto, int(es_fraude)])

    # Crear DataFrame
    columns = ['id_transaccion', 'fecha', 'cliente_id', 'numero_tarjeta', 'comercio', 'categoria', 'ciudad', 'monto', 'es_fraude']
    df = pd.DataFrame(data, columns=columns)
    
    # Guardar a CSV
    archivo = 'transacciones_bancarias.csv'
    df.to_csv(archivo, index=False)
    print(f"✅ Archivo generado exitosamente: {archivo}")

if __name__ == "__main__":
    generar_datos()
