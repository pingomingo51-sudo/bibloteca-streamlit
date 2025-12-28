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
    df = pd.read_csv("biblioteca.csv", sep=";")
    df.columns = df.columns.str.strip().str.lower()

    for col in ["isbn", "fecha_prestamo", "email", "prestado_a"]:
        if col not in df.columns:
            df[col] = ""

    return df


def guardar_datos(df):
    df.to_csv("biblioteca.csv", index=False, sep=";")
    st.cache_data.clear()


df = cargar_datos()

# --------------------------------------------------
# PESTAÑAS
# --------------------------------------------------
tab_inicio, tab_libros, tab_peliculas, tab_prestamos = st.tabs(
    ["🏠 Inicio", "📚 Libros", "🎬 Películas", "🔄 Préstamos"]
)

# ==================================================
# 🏠 INICIO
# ==================================================
with tab_inicio:
    st.title("📖 Biblioteca Municipal Almaluez")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", len(df))
    col2.metric("Libros", len(df[df["tipo"].str.lower() == "libro"]))
    col3.metric("Películas", len(df[df["tipo"].str.lower() == "película"]))
    col4.metric("Prestados", len(df[df["disponible"].str.lower() != "sí"]))

    # -------------------------
    # DISPONIBLES
    # -------------------------
    st.subheader("Disponibles")
    disponibles = df[df["disponible"].str.lower() == "sí"]

    columnas_disponibles = [
        c for c in disponibles.columns
        if c not in ["disponible", "prestado_a", "email", "fecha_prestamo"]
    ]

    st.dataframe(
        disponibles[["id"] + [c for c in columnas_disponibles if c != "id"]],
        width=1200
    )

    # -------------------------
    # NO DISPONIBLES
    # -------------------------
    st.subheader("No disponibles")
    no_disponibles = df[df["disponible"].str.lower() != "sí"]

    columnas_no_disponibles = [
        c for c in no_disponibles.columns
        if c != "disponible"
    ]

    st.dataframe(
        no_disponibles[["id"] + [c for c in columnas_no_disponibles if c != "id"]],
        width=1200
    )

# ==================================================
# 📚 LIBROS
# ==================================================
with tab_libros:
    st.title("📚 Libros")

    libros_df = df[df["tipo"].str.lower() == "libro"]

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        titulo = st.selectbox("Título", [""] + sorted(libros_df["titulo"].dropna().unique()))
    with col2:
        autor = st.selectbox("Autor", [""] + sorted(libros_df["autor"].dropna().unique()))
    with col3:
        genero = st.selectbox("Género", [""] + sorted(libros_df["genero"].dropna().unique()))
    with col4:
        saga = st.selectbox("Saga", [""] + sorted(libros_df["saga"].dropna().unique()))
    with col5:
        isbn = st.selectbox(
            "ISBN",
            [""] + sorted(libros_df["isbn"].dropna().astype(str).unique())
        )

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

    st.dataframe(
        libros_df[["id"] + [c for c in libros_df.columns if c != "id"]],
        width=1200
    )

# ==================================================
# 🎬 PELÍCULAS
# ==================================================
with tab_peliculas:
    st.title("🎬 Películas")

    pelis_df = df[df["tipo"].str.lower() == "película"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        titulo = st.selectbox("Película", [""] + sorted(pelis_df["titulo"].dropna().unique()))
    with col2:
        director = st.selectbox("Director", [""] + sorted(pelis_df["autor"].dropna().unique()))
    with col3:
        genero = st.selectbox("Género", [""] + sorted(pelis_df["genero"].dropna().unique()))
    with col4:
        saga = st.selectbox("Saga", [""] + sorted(pelis_df["saga"].dropna().unique()))

    if titulo:
        pelis_df = pelis_df[pelis_df["titulo"] == titulo]
    if director:
        pelis_df = pelis_df[pelis_df["autor"] == director]
    if genero:
        pelis_df = pelis_df[pelis_df["genero"] == genero]
    if saga:
        pelis_df = pelis_df[pelis_df["saga"] == saga]

    st.dataframe(
        pelis_df[["id"] + [c for c in pelis_df.columns if c not in ["id", "isbn"]]],
        width=1200
    )

# ==================================================
# 🔄 PRÉSTAMOS
# ==================================================
with tab_prestamos:
    st.title("🔄 Gestión de préstamos")

    opciones = df["id"].astype(str) + " - " + df["titulo"]
    seleccion = st.selectbox("Selecciona una obra", opciones)

    obra_id = int(seleccion.split(" - ")[0])
    fila = df[df["id"] == obra_id].iloc[0]

    st.write(f"**Título:** {fila['titulo']}")
    st.write(f"**Disponible:** {fila['disponible']}")

    if str(fila["disponible"]).lower() == "sí":
        nombre = st.text_input("Nombre de la persona")
        email = st.text_input("Email")

        if st.button("📕 Prestar"):
            if not nombre or not email:
                st.error("Debes introducir nombre y email")
            else:
                df.loc[df["id"] == obra_id, "disponible"] = "No"
                df.loc[df["id"] == obra_id, "prestado_a"] = nombre
                df.loc[df["id"] == obra_id, "email"] = email
                df.loc[df["id"] == obra_id, "fecha_prestamo"] = pd.Timestamp.now().strftime(
                    "%Y-%m-%d %H:%M"
                )
                guardar_datos(df)
                st.success("Préstamo registrado correctamente")
    else:
        if st.button("📗 Devolver"):
            df.loc[df["id"] == obra_id, "disponible"] = "Sí"
            df.loc[df["id"] == obra_id, "prestado_a"] = ""
            df.loc[df["id"] == obra_id, "email"] = ""
            df.loc[df["id"] == obra_id, "fecha_prestamo"] = ""
            guardar_datos(df)
            st.success("Devolución registrada correctamente")

