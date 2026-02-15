# 📊 Meeting Insights

Meeting Insights es una aplicación web interactiva construida con Streamlit que permite analizar actas de reuniones. La app detecta automáticamente tareas, decisiones clave y participación de los asistentes, generando reportes en Markdown, HTML y JSON.

## 🔹 Funcionalidades principales

- Analiza textos de actas en español e inglés.

- Detecta tareas con responsables y fechas.

- Identifica decisiones clave tomadas en la reunión.

- Cuenta las intervenciones por participante.

- Exporta resultados en:

  - Markdown (.md)
  
  - HTML (.html)
  
  - JSON (.json)

## 💻 Cómo usar

Clona el repositorio:

git clone https://github.com/Kevin-2099/meeting-insights.git

cd meeting-insights

Instala dependencias (recomendado usar un virtualenv):

pip install -r requirements.txt

Ejecuta la aplicación:

streamlit run app.py

Sube un archivo .txt o .md con el acta de la reunión, o pega el texto directamente en la aplicación.

Explora los insights y descarga los reportes en el formato que necesites.

## ⚙️ Requisitos

- Streamlit

- pandas

Instala dependencias con:

pip install streamlit pandas

## 📄 Licencia
Este proyecto se distribuye bajo una licencia propietaria con acceso al código (source-available).

El código fuente se pone a disposición únicamente para fines de visualización, evaluación y aprendizaje.

❌ No está permitido copiar, modificar, redistribuir, sublicenciar, ni crear obras derivadas del software o de su código fuente sin autorización escrita expresa del titular de los derechos.

❌ El uso comercial del software, incluyendo su oferta como servicio (SaaS), su integración en productos comerciales o su uso en entornos de producción, requiere un acuerdo de licencia comercial independiente.

📌 El texto legalmente vinculante de la licencia es la versión en inglés incluida en el archivo LICENSE.

Se proporciona una traducción al español en LICENSE_ES.md únicamente con fines informativos. En caso de discrepancia, prevalece la versión en inglés.

## Autor
Kevin-2099
