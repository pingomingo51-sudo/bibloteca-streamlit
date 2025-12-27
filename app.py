import streamlit as st
import pandas as pd

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------
st.set_page_config(
    page_title="Biblioteca Municipal Almaluez",
    layout="wide"
)

# --------------------------------------------------
# CARGA Y GUARDADO DE DATOS
# --------------------------------------------------
@st.cache_data
def cargar_datos():
    df = pd.read_csv("biblioteca.csv", sep=';')
    df.columns = df.columns.str.strip().str.lower()
    if 'isbn' not in df.columns:
        df['isbn'] = ''
    if 'fecha_prestamo' not in df.columns:
        df['fecha_prestamo'] = ''
    return df

def guardar_datos(df):
    df.to_csv("biblioteca.csv", index=False, sep=';')
    st.cache_data.clear()

df = cargar_datos()

# --------------------------------------------------
# PESTAÑAS
# --------------------------------------------------
tab_inicio, tab_libros, tab_peliculas, tab_prestamos = st.tabs(
    ["🏠 Inicio", "📚 Libros", "🎬 Películas", "🔄 Préstamos"]
)

# ==================================================
# 🏠 INICIO (vista general)
# ==================================================
with tab_inicio:
    st.title("📖 Biblioteca Municipal")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", len(df))
    col2.metric("Libros", len(df[df["tipo"].str.lower() == "libro"]))
    col3.metric("Películas", len(df[df["tipo"].str.lower() == "película"]))
    col4.metric(
        "Prestados",
        len(df[df["prestado_a"].notna() & (df["prestado_a"] != "")])
    )

    st.subheader("Disponibles")
    disponibles_df = df[df["disponible"].str.lower() == "sí"]
    st.dataframe(disponibles_df[["id"] + [c for c in disponibles_df.columns if c != "id"]],
                 use_container_width=True)

    st.subheader("No disponibles")
    no_disponibles_df = df[df["disponible"].str.lower() != "sí"]
    st.dataframe(no_disponibles_df[["id"] + [c for c in no_disponibles_df.columns if c != "id"]],
                 use_container_width=True)

# ==================================================
# 📚 LIBROS (ISBN visible) - compatible móvil
# ==================================================
with tab_libros:
    st.title("📚 Libros")
    libros_df = df[df["tipo"].str.lower() == "libro"]
    col1, col2, col3, col4, col5 = st.columns(5)

    # --- Título ---
    with col1:
        texto_titulo = st.text_input("Escribe el título")
        if texto_titulo:
            opciones_titulo = libros_df[libros_df["titulo"].str.contains(texto_titulo, case=False, na=False)]["titulo"].unique().tolist()
        else:
            opciones_titulo = libros_df["titulo"].dropna().unique().tolist()
        titulo = st.selectbox("Título", options=[""] + sorted(opciones_titulo))

    # --- Autor ---
    with col2:
        texto_autor = st.text_input("Escribe el autor")
        if texto_autor:
            opciones_autor = libros_df[libros_df["autor"].str.contains(texto_autor, case=False, na=False)].dropna()["autor"].unique().tolist()
        else:
            opciones_autor = libros_df["autor"].dropna().unique().tolist()
        autor = st.selectbox("Autor", options=[""] + sorted(opciones_autor))

    # --- Género ---
    with col3:
        texto_genero = st.text_input("Escribe el género")
        if texto_genero:
            opciones_genero = libros_df[libros_df["genero"].str.contains(texto_genero, case=False, na=False)].dropna()["genero"].unique().tolist()
        else:
            opciones_genero = libros_df["genero"].dropna().unique().tolist()
        genero = st.selectbox("Género", options=[""] + sorted(opciones_genero))

    # --- Saga ---
    with col4:
        texto_saga = st.text_input("Escribe la saga")
        if texto_saga:
            opciones_saga = libros_df[libros_df["saga"].str.contains(texto_saga, case=False, na=False)].dropna()["saga"].unique().tolist()
        else:
            opciones_saga = libros_df["saga"].dropna().unique().tolist()
        saga = st.selectbox("Saga", options=[""] + sorted(opciones_saga))

    # --- ISBN ---
    with col5:
        isbn = st.selectbox(
            "ISBN",
            options=[""] + sorted(libros_df["isbn"].dropna().astype(str).unique().tolist())
        )

    # Aplicar filtros
    if titulo:
        libros_df = libros_df[libros_df["titulo"] == titulo]
    if autor:
        libros_df = libros_df[libros_df["autor"] == autor]
    if genero:
        libros_df = libros_df[libros_df["genero"] == genero]
    if saga:
        libros_df = libros_df[libros_df["saga"] == saga]
    if isbn:
        libros_df = libros_df[libros_df["isbn"].astype(str) == isbn]

    st.dataframe(libros_df[["id"] + [c for c in libros_df.columns if c != "id"]],
                 use_container_width=True)

# ==================================================
# 🎬 PELÍCULAS (ISBN oculto) - compatible móvil
# ==================================================
with tab_peliculas:
    st.title("🎬 Películas")
    pelis_df = df[df["tipo"].str.lower() == "película"]
    col1, col2, col3, col4 = st.columns(4)

    # --- Título ---
    with col1:
        texto_titulo = st.text_input("Escribe el título de la película")
        if texto_titulo:
            opciones_titulo = pelis_df[pelis_df["titulo"].str.contains(texto_titulo, case=False, na=False)]["titulo"].unique().tolist()
        else:
            opciones_titulo = pelis_df["titulo"].dropna().unique().tolist()
        titulo_peli = st.selectbox("Película", options=[""] + sorted(opciones_titulo))

    # --- Director ---
    with col2:
        texto_director = st.text_input("Escribe el director")
        if texto_director:
            opciones_director = pelis_df[pelis_df["autor"].str.contains(texto_director, case=False, na=False)].dropna()["autor"].unique().tolist()
        else:
            opciones_director = pelis_df["autor"].dropna().unique().tolist()
        director = st.selectbox("Director", options=[""] + sorted(opciones_director))

    # --- Género ---
    with col3:
        texto_genero = st.text_input("Escribe el género")
        if texto_genero:
            opciones_genero = pelis_df[pelis_df["genero"].str.contains(texto_genero, case=False, na=False)].dropna()["genero"].unique().tolist()
        else:
            opciones_genero = pelis_df["genero"].dropna().unique().tolist()
        genero_peli = st.selectbox("Género", options=[""] + sorted(opciones_genero))

    # --- Saga ---
    with col4:
        texto_saga = st.text_input("Escribe la saga")
        if texto_saga:
            opciones_saga = pelis_df[pelis_df["saga"].str.contains(texto_saga, case=False, na=False)].dropna()["saga"].unique().tolist()
        else:
            opciones_saga = pelis_df["saga"].dropna().unique().tolist()
        saga_peli = st.selectbox("Saga", options=[""] + sorted(opciones_saga))

    # Aplicar filtros
    if titulo_peli:
        pelis_df = pelis_df[pelis_df["titulo"] == titulo_peli]
    if director:
        pelis_df = pelis_df[pelis_df["autor"] == director]
    if genero_peli:
        pelis_df = pelis_df[pelis_df["genero"] == genero_peli]
    if saga_peli:
        pelis_df = pelis_df[pelis_df["saga"] == saga_peli]

    st.dataframe(
        pelis_df[["id"] + [c for c in pelis_df.columns if c not in ["id", "isbn"]]],
        use_container_width=True
    )

# ==================================================
# 🔄 PRÉSTAMOS - con búsqueda
# ==================================================
with tab_prestamos:
    st.title("🔄 Gestión de préstamos")

    opciones = df["id"].astype(str) + " - " + df["titulo"]
    seleccion = st.selectbox(
        "Selecciona una obra",
        options=opciones,
        index=0,
    )

    obra_id = int(seleccion.split(" - ")[0])
    fila = df[df["id"] == obra_id].iloc[0]

    st.write(f"**Título:** {fila['titulo']}")
    st.write(f"**Tipo:** {fila['tipo']}")
    st.write(f"**ISBN:** {fila['isbn'] if fila['tipo'].lower() == 'libro' else '—'}")
    st.write(f"**Disponible:** {fila['disponible']}")
    st.write(f"**Prestado a:** {fila['prestado_a'] if fila['prestado_a'] else '—'}")
    st.write(f"**Fecha de préstamo:** {fila['fecha_prestamo'] if fila['fecha_prestamo'] else '—'}")

    if fila["disponible"].lower() == "sí":
        persona = st.text_input("Nombre de la persona")
        if st.button("📕 Prestar"):
            df.loc[df["id"] == obra_id, "disponible"] = "No"
            df.loc[df["id"] == obra_id, "prestado_a"] = persona
            df.loc[df["id"] == obra_id, "fecha_prestamo"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
            guardar_datos(df)
            st.success("Préstamo registrado correctamente")
    else:
        if st.button("📗 Devolver"):
            df.loc[df["id"] == obra_id, "disponible"] = "Sí"
            df.loc[df["id"] == obra_id, "prestado_a"] = ""
            df.loc[df["id"] == obra_id, "fecha_prestamo"] = ""
            guardar_datos(df)
            st.success("Devolución registrada correctamente")
