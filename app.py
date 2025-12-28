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

    # Asegurar columnas necesarias
    for col in ["isbn", "fecha_prestamo", "email"]:
        if col not in df.columns:
            df[col] = ""

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
# 🏠 INICIO
# ==================================================
with tab_inicio:
    st.title("📖 Biblioteca Municipal")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", len(df))
    col2.metric("Libros", len(df[df["tipo"].str.lower() == "libro"]))
    col3.metric("Películas", len(df[df["tipo"].str.lower() == "película"]))
    col4.metric(
        "Prestados",
        len(df[df["disponible"].str.lower() != "sí"])
    )

    st.subheader("📗 Disponibles")
    disponibles_df = df[df["disponible"].str.lower() == "sí"]
    st.dataframe(
        disponibles_df[["id"] + [c for c in disponibles_df.columns if c != "id"]],
        use_container_width=True
    )

    st.subheader("📕 No disponibles")
    no_disponibles_df = df[df["disponible"].str.lower() != "sí"]
    st.dataframe(
        no_disponibles_df[["id"] + [c for c in no_disponibles_df.columns if c != "id"]],
        use_container_width=True
    )

    # ---- Retrasos ----
    st.subheader("⏰ Préstamos con más de 30 días")

    prestados = df[df["fecha_prestamo"] != ""].copy()
    if not prestados.empty:
        prestados["fecha_prestamo"] = pd.to_datetime(prestados["fecha_prestamo"])
        prestados["dias"] = (pd.Timestamp.now() - prestados["fecha_prestamo"]).dt.days
        retrasos = prestados[prestados["dias"] >= 30]

        st.dataframe(
            retrasos[["id", "titulo", "prestado_a", "email", "fecha_prestamo", "dias"]],
            use_container_width=True
        )
    else:
        st.info("No hay préstamos registrados.")

# ==================================================
# 📚 LIBROS
# ==================================================
with tab_libros:
    st.title("📚 Libros")
    libros_df = df[df["tipo"].str.lower() == "libro"]

    col1, col2, col3, col4, col5 = st.columns(5)

    titulo = st.selectbox(
        "Título",
        [""] + sorted(libros_df["titulo"].dropna().unique().tolist())
    )

    autor = st.selectbox(
        "Autor",
        [""] + sorted(libros_df["autor"].dropna().unique().tolist())
    )

    genero = st.selectbox(
        "Género",
        [""] + sorted(libros_df["genero"].dropna().unique().tolist())
    )

    saga = st.selectbox(
        "Saga",
        [""] + sorted(libros_df["saga"].dropna().unique().tolist())
    )

    isbn = st.selectbox(
        "ISBN",
        [""] + sorted(libros_df["isbn"].dropna().astype(str).unique().tolist())
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
        use_container_width=True
    )

# ==================================================
# 🎬 PELÍCULAS
# ==================================================
with tab_peliculas:
    st.title("🎬 Películas")
    pelis_df = df[df["tipo"].str.lower() == "película"]

    titulo_peli = st.selectbox(
        "Película",
        [""] + sorted(pelis_df["titulo"].dropna().unique().tolist())
    )

    director = st.selectbox(
        "Director",
        [""] + sorted(pelis_df["autor"].dropna().unique().tolist())
    )

    genero_peli = st.selectbox(
        "Género",
        [""] + sorted(pelis_df["genero"].dropna().unique().tolist())
    )

    saga_peli = st.selectbox(
        "Saga",
        [""] + sorted(pelis_df["saga"].dropna().unique().tolist())
    )

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
# 🔄 PRÉSTAMOS
# ==================================================
with tab_prestamos:
    st.title("🔄 Gestión de préstamos")

    opciones = df["id"].astype(str) + " - " + df["titulo"]
    seleccion = st.selectbox("Selecciona una obra", opciones)

    obra_id = int(seleccion.split(" - ")[0])
    fila = df[df["id"] == obra_id].iloc[0]

    st.write(f"**Título:** {fila['titulo']}")
    st.write(f"**Tipo:** {fila['tipo']}")
    st.write(f"**ISBN:** {fila['isbn'] if fila['tipo'].lower() == 'libro' else '—'}")
    st.write(f"**Disponible:** {fila['disponible']}")
    st.write(f"**Prestado a:** {fila['prestado_a'] if fila['prestado_a'] else '—'}")
    st.write(f"**Email:** {fila['email'] if fila['email'] else '—'}")
    st.write(f"**Fecha de préstamo:** {fila['fecha_prestamo'] if fila['fecha_prestamo'] else '—'}")

    if fila["disponible"].str.lower() == "sí":
        persona = st.text_input("Nombre de la persona")
        email = st.text_input("Email de contacto")

        if st.button("📕 Prestar"):
            if not persona or not email:
                st.error("Debes introducir nombre y email")
            elif "@" not in email:
                st.error("El email no es válido")
            else:
                df.loc[df["id"] == obra_id, "disponible"] = "No"
                df.loc[df["id"] == obra_id, "prestado_a"] = persona
                df.loc[df["id"] == obra_id, "email"] = email
                df.loc[df["id"] == obra_id, "fecha_prestamo"] = (
                    pd.Timestamp.now().strftime("%Y-%m-%d")
                )
                guardar_datos(df)
                st.success("Préstamo registrado correctamente, tiene 1 mes para devolverlo")
    else:
        if st.button("📗 Devolver"):
            df.loc[df["id"] == obra_id, "disponible"] = "Sí"
            df.loc[df["id"] == obra_id, "prestado_a"] = ""
            df.loc[df["id"] == obra_id, "email"] = ""
            df.loc[df["id"] == obra_id, "fecha_prestamo"] = ""
            guardar_datos(df)
            st.success("Devolución registrada correctamente")

