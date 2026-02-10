# AWS-Data-Lake

# 🕵️‍♂️ AWS Data Lake: Detección de Fraude Bancario

## 📌 Descripción del Proyecto
Este proyecto simula un entorno de **Ingeniería de Datos en la Nube** para detectar transacciones fraudulentas. Se construyó un pipeline ETL (Extract, Transform, Load) completo utilizando servicios nativos de AWS bajo una arquitectura Serverless.

El objetivo fue ingerir datos transaccionales sin estructurar, catalogarlos automáticamente y permitir consultas analíticas mediante SQL para identificar patrones de robo en tiempo real.

## 🏗️ Arquitectura
**Flujo de Datos:**
`Python Script (Generador)` ➔ `AWS S3 (Data Lake)` ➔ `AWS Glue Crawler (Catalogación)` ➔ `AWS Athena (Análisis SQL)`

* **Lenguajes:** Python 3.9, SQL (Presto/Trino).
* **Servicios AWS:**
    * **S3:** Almacenamiento de objetos (Raw Data).
    * **IAM:** Gestión de permisos y roles de servicio.
    * **Glue Data Catalog:** Metadatos y esquematización automática.
    * **Athena:** Consultas interactivas Serverless.

## ⚙️ Retos Técnicos y Soluciones (Troubleshooting)
Durante la implementación, se resolvieron problemas críticos de configuración de infraestructura que son comunes en entornos empresariales:

### 1. Error de Entidad de Confianza (IAM)
* **Problema:** El Crawler fallaba con `Internal Service Exception`.
* **Diagnóstico:** El Rol de IAM se creó con la entidad de confianza `ec2.amazonaws.com` en lugar de `glue.amazonaws.com`.
* **Solución:** Se recreó el rol asignando explícitamente la relación de confianza al servicio de Glue, permitiéndole asumir los permisos necesarios.

### 2. Bloqueo de Lake Formation
* **Problema:** A pesar de tener permisos de Administrador, el Crawler no podía escribir la tabla en la base de datos.
* **Causa:** AWS Lake Formation estaba protegiendo la base de datos por defecto.
* **Solución:** Se revirtió el modelo de permisos a IAM estándar (desactivando las reglas granulares de Lake Formation para este laboratorio).

### 3. Definición de Rutas en S3 (The "Empty Table" Bug)
* **Problema:** Athena mostraba la tabla pero con 0 registros.
* **Causa:** El Crawler apuntaba al archivo específico (`.../archivo.csv`) en lugar del directorio contenedor. Hive/Athena interpretan las rutas como carpetas.
* **Solución:** Se redefinió la tabla utilizando DDL (SQL) para apuntar al bucket raíz (`s3://bucket-name/`), permitiendo la lectura correcta de los objetos.

## 📊 Resultados del Análisis
Mediante SQL, se identificaron las transacciones de mayor impacto financiero marcadas como fraude.

**Insight Principal:**
Se detectó un patrón de fraude recurrente en la ciudad de **Culiacán**, con montos cercanos a los **$80,000 MXN** por transacción en comercios minoristas.

**Consulta SQL utilizada:**
```sql
SELECT id_transaccion, fecha, ciudad, monto, comercio
FROM "transacciones_bancarias_csv"
WHERE es_fraude = 1
ORDER BY monto DESC
LIMIT 10;
