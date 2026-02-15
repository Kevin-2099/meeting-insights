# app.py - Meeting Insights
import streamlit as st
import re
import json
import pandas as pd
from io import StringIO
from collections import defaultdict

# ------------------------
# Función de análisis 
# ------------------------
def parse_meeting_minutes(text):
    lines = text.splitlines()
    tasks = []
    decisions = []
    participation = defaultdict(int)

    # Verbos de acción (ES + EN)
    task_verbs = re.compile(
        r"\b(corregir|revisar|actualizar|validar|configurar|mejorar|documentar|redactar|coordinar|update|review|fix|validate|configure|improve|document|draft|coordinate)\b",
        re.IGNORECASE
    )

    # Patrones de responsable (ES + EN)
    responsible_patterns = [
        re.compile(r"Responsable:\s*([A-Za-zÁÉÍÓÚÑáéíóúñ ]+)", re.IGNORECASE),
        re.compile(r"Asignado a\s*([A-Za-zÁÉÍÓÚÑáéíóúñ ]+)", re.IGNORECASE),
        re.compile(r"([A-Za-zÁÉÍÓÚÑáéíóúñ ]+)\s+se encarga de", re.IGNORECASE),
        re.compile(r"Responsible:\s*([A-Za-zÁÉÍÓÚÑáéíóúñ ]+)", re.IGNORECASE),
        re.compile(r"Assigned to\s*([A-Za-zÁÉÍÓÚÑáéíóúñ ]+)", re.IGNORECASE),
        re.compile(r"([A-Za-zÁÉÍÓÚÑáéíóúñ ]+)\s+is responsible for", re.IGNORECASE)
    ]

    # Fechas ISO
    date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")

    # Participantes
    participant_pattern = re.compile(r"^\*?\s*([A-Za-zÁÉÍÓÚÑáéíóúñ]+):")

    # Frases de decisión (ES + EN)
    decision_pattern = re.compile(
        r"(se acuerda|se decide|priorizar|vamos a|quedamos en|se establece|se define|se sugiere|we agree|we decide|prioritize|let's|is agreed|it is decided|is recommended|we suggest)",
        re.IGNORECASE
    )

    # Palabras a ignorar en participación (ES + EN)
    ignore_names = ["Fecha", "Hora", "Lugar", "Agenda", "Notas", "Date", "Time", "Location", "Notes", "Tasks", "Decisions"]

    for line in lines:
        line_clean = line.strip()

        # ---- PARTICIPACIÓN ----
        participant_match = participant_pattern.match(line_clean)
        if participant_match:
            name = participant_match.group(1).strip()
            # ❌ No contar Tasks ni Decisions
            if name not in ignore_names:
                participation[name] += 1

        # ---- DECISIONES ----
        if decision_pattern.search(line_clean):
            decision_clean = re.sub(r"^[A-Za-zÁÉÍÓÚÑáéíóúñ]+:\s*", "", line_clean)
            # ❌ Filtrar falsos positivos: evitar comentarios que son tareas
            if not task_verbs.search(decision_clean):
                decisions.append(decision_clean)
            continue

        # ---- TAREAS ----
        if task_verbs.search(line_clean):
            # ❌ Filtrar falsos positivos: frases que son decisiones
            if any(dp in line_clean.lower() for dp in ["propongo", "de acuerdo", "vamos a", "se sugiere", "we suggest", "we agree", "let's"]):
                continue

            task_text = line_clean
            responsible = "Sin responsable"
            for rp in responsible_patterns:
                m = rp.search(line_clean)
                if m:
                    responsible = m.group(1).strip()
                    break

            date_match = date_pattern.search(line_clean)
            due_date = date_match.group(0) if date_match else "Sin fecha"

            # ❌ Limpiar duplicación de Responsable y Fecha
            task_text = re.sub(r"(Responsable:|Responsible:).*$", "", task_text).strip()
            task_text = re.sub(r"– \d{4}-\d{2}-\d{2}", "", task_text).strip()

            tasks.append({
                "task": task_text,
                "responsible": responsible,
                "due_date": due_date
            })

    return {
        "tasks": tasks,
        "decisions": decisions,
        "participation": dict(participation)
    }

# ------------------------
# Funciones de presentación
# ------------------------
def generate_markdown(insights):
    md = "## Meeting Insights\n\n"

    md += "### Participación por persona\n"
    if insights["participation"]:
        for person, count in insights["participation"].items():
            md += f"- {person}: {count} intervenciones\n"
    else:
        md += "- No se detectaron participantes\n"

    md += "\n### Tareas detectadas\n"
    if insights["tasks"]:
        for t in insights["tasks"]:
            md += f"- {t['task']} (Responsable: {t['responsible']}, Fecha: {t['due_date']})\n"
    else:
        md += "- No se detectaron tareas\n"

    md += "\n### Decisiones clave\n"
    if insights["decisions"]:
        for d in insights["decisions"]:
            md += f"- {d}\n"
    else:
        md += "- No se detectaron decisiones\n"

    return md

def generate_html(insights):
    participation_df = pd.DataFrame(
        list(insights["participation"].items()), columns=["Persona", "Intervenciones"]
    )
    tasks_df = pd.DataFrame(insights["tasks"])
    decisions_df = pd.DataFrame({"Decisiones": insights["decisions"]})

    html = "<h2>Meeting Insights</h2>"
    html += "<h3>Participación por persona</h3>"
    html += participation_df.to_html(index=False) if not participation_df.empty else "<p>No hay datos</p>"
    html += "<h3>Tareas detectadas</h3>"
    html += tasks_df.to_html(index=False) if not tasks_df.empty else "<p>No hay tareas</p>"
    html += "<h3>Decisiones clave</h3>"
    html += decisions_df.to_html(index=False) if not decisions_df.empty else "<p>No hay decisiones</p>"

    return html

# ------------------------
# Interfaz Streamlit
# ------------------------
st.set_page_config(page_title="Meeting Insights ", layout="wide")
st.title("📊 Meeting Insights ")

uploaded_file = st.file_uploader("Sube el acta / Upload minutes", type=["txt", "md"])
text_input = st.text_area("O pega el texto del acta aquí / Or paste the text here:")

if uploaded_file:
    text = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
elif text_input:
    text = text_input
else:
    text = None

if text:
    insights = parse_meeting_minutes(text)

    st.subheader("📋 Resumen de insights / Summary")
    st.markdown(generate_markdown(insights))

    st.subheader("👥 Participación / Participation")
    st.dataframe(pd.DataFrame(list(insights["participation"].items()), columns=["Persona", "Intervenciones"]))

    st.subheader("💾 Exportar / Export insights")
    st.download_button("Exportar Markdown / Markdown", generate_markdown(insights), file_name="meeting_insights.md")
    st.download_button("Exportar HTML / HTML", generate_html(insights), file_name="meeting_insights.html")
    st.download_button("Exportar JSON / JSON", json.dumps(insights, indent=2, ensure_ascii=False), file_name="meeting_insights.json")

    st.success("✅ Análisis completado / Analysis completed")
