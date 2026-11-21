import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="English Hub | Aulas & Dicas",
    page_icon="🇬🇧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS CUSTOMIZADO ---
st.markdown("""
<style>
    /* Esconde elementos padrão desnecessários do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background-color: transparent !important;}

    /* Banner de cabeçalho (Hero) */
    .hero-banner {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-left: 5px solid #3B82F6;
        border-radius: 12px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .hero-title {
        font-size: 1.9rem;
        font-weight: 700;
        color: #F8FAFC;
        margin: 0 0 6px 0;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #94A3B8;
        margin: 0;
    }

    /* Card de Aula */
    .lesson-card {
        background-color: #131C31;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 12px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .lesson-card:hover {
        border-color: #3B82F6;
        transform: translateY(-2px);
    }
    .lesson-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #F8FAFC;
        margin-bottom: 10px;
    }
    .lesson-desc {
        color: #CBD5E1;
        font-size: 0.98rem;
        line-height: 1.55;
        margin-top: 12px;
    }

    /* Badges (Etiquetas) */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 8px;
        letter-spacing: 0.3px;
    }
    .badge-cat {
        background-color: rgba(59, 130, 246, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    .badge-lvl {
        background-color: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-priv {
        background-color: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    /* Estilização dos botões de link */
    .stLinkButton > a {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.55rem 1rem !important;
        transition: background-color 0.2s ease !important;
    }
    .stLinkButton > a:hover {
        background-color: #1D4ED8 !important;
    }
</style>
""", unsafe_allow_html=True)

CSV_PATH = "data_aulas.csv"


@st.cache_data
def carregar_aulas():
    try:
        return pd.read_csv(CSV_PATH, sep=None, engine="python", encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(CSV_PATH, sep=None, engine="python", encoding="latin1")


def salvar_aulas(df):
    df.to_csv(CSV_PATH, index=False, encoding="utf-8")
    st.cache_data.clear()


# Inicializa estados de sessão
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_atual" not in st.session_state:
    st.session_state.usuario_atual = ""
if "eh_admin" not in st.session_state:
    st.session_state.eh_admin = False

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("## 🇬🇧 English Hub")
    st.caption("Comunicação clara, vocabulário real e fluência aplicada.")
    st.divider()

    opcoes_menu = ["🌍 Vitrine Pública", "🔒 Área do Aluno"]
    if st.session_state.eh_admin:
        opcoes_menu.append("⚙️ Painel do Professor")

    menu = st.radio("NAVEGAÇÃO", opcoes_menu)

    st.divider()

    if not st.session_state.autenticado:
        st.markdown("**Acesso Restrito**")
        senha_digitada = st.text_input("Senha:", type="password", placeholder="Digite sua senha...")
        if st.button("Entrar", use_container_width=True, type="primary"):
            senha_admin = st.secrets.get("admin", {}).get("senha_mestre", "")
            senhas_alunos = st.secrets.get("senhas_alunos", {})

            if senha_digitada == senha_admin and senha_admin != "":
                st.session_state.autenticado = True
                st.session_state.eh_admin = True
                st.session_state.usuario_atual = "Professor (Admin)"
                st.rerun()
            elif senha_digitada in senhas_alunos.values():
                st.session_state.autenticado = True
                st.session_state.eh_admin = False
                for user, pwd in senhas_alunos.items():
                    if pwd == senha_digitada:
                        st.session_state.usuario_atual = user.capitalize()
                st.rerun()
            else:
                st.error("Senha incorreta.")
    else:
        st.success(f"Conectado: **{st.session_state.usuario_atual}**")
        if st.button("Sair da conta", use_container_width=True):
            st.session_state.autenticado = False
            st.session_state.usuario_atual = ""
            st.session_state.eh_admin = False
            st.rerun()

try:
    df_aulas = carregar_aulas()
except Exception as e:
    st.error(f"Erro ao carregar o arquivo CSV: {e}")
    st.stop()


def exibir_aula(row):
    badge_acesso = '<span class="badge badge-priv">🔒 Exclusivo Aluno</span>' if row["acesso"] == "privado" else ""

    html_card = (
        f'<div class="lesson-card">'
        f'<div class="lesson-title">{row["titulo"]}</div>'
        f'<div>'
        f'<span class="badge badge-cat">📁 {row["categoria"]}</span>'
        f'<span class="badge badge-lvl">🎯 {row["nivel"]}</span>'
        f'{badge_acesso}'
        f'</div>'
        f'<div class="lesson-desc">{row["descricao"]}</div>'
        f'</div>'
    )
    st.markdown(html_card, unsafe_allow_html=True)

    tem_drive = pd.notna(row["link_drive"]) and str(row["link_drive"]).strip() != ""
    tem_video = pd.notna(row["link_video"]) and str(row["link_video"]).strip() != ""

    if tem_drive or tem_video:
        col_btn, col_vid = st.columns([1, 3])
        with col_btn:
            if tem_drive:
                st.link_button("📄 Material no Drive", str(row["link_drive"]).strip(), use_container_width=True)
        with col_vid:
            if tem_video:
                with st.expander("▶️ Assistir Vídeo da Aula"):
                    st.video(str(row["link_video"]).strip())

    st.write("")


# --- PÁGINA 1: VITRINE PÚBLICA ---
if menu == "🌍 Vitrine Pública":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🌍 Dicas Rápidas & Aulas Abertas</div>
        <div class="hero-subtitle">Explore conteúdos gratuitos sobre vocabulário profissional, estrutura de fala e pronúncia.</div>
    </div>
    """, unsafe_allow_html=True)

    aulas_publicas = df_aulas[df_aulas["acesso"] == "publico"]

    col_filtro, col_metrica = st.columns([3, 1])
    with col_filtro:
        categorias = ["Todas"] + list(aulas_publicas["categoria"].dropna().unique())
        cat_selecionada = st.selectbox("Filtrar por tema:", categorias)
    with col_metrica:
        st.metric("Aulas Disponíveis", len(aulas_publicas))

    if cat_selecionada != "Todas":
        aulas_publicas = aulas_publicas[aulas_publicas["categoria"] == cat_selecionada]

    st.divider()

    if aulas_publicas.empty:
        st.info("Nenhuma aula pública encontrada para este filtro.")
    else:
        for _, row in aulas_publicas.iterrows():
            exibir_aula(row)

# --- PÁGINA 2: ÁREA DO ALUNO ---
elif menu == "🔒 Área do Aluno":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🔒 Portal Exclusivo do Aluno</div>
        <div class="hero-subtitle">Repositório completo de roteiros, diálogos comentados, exercícios e materiais personalizados.</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.autenticado:
        st.warning(
            "Esta área é restrita a alunos matriculados. Insira sua senha no menu lateral para liberar o acesso.")
    else:
        aulas_privadas = df_aulas[df_aulas["acesso"] == "privado"]

        col_busca, col_metrica = st.columns([3, 1])
        with col_busca:
            busca = st.text_input("🔍 Buscar aula por palavra-chave:", placeholder="Ex: Suits, Negociação, Bancos...")
        with col_metrica:
            st.metric("Módulos Liberados", len(aulas_privadas))

        if busca:
            aulas_privadas = aulas_privadas[
                aulas_privadas["titulo"].str.contains(busca, case=False, na=False) |
                aulas_privadas["descricao"].str.contains(busca, case=False, na=False)
                ]

        st.divider()

        if aulas_privadas.empty:
            st.info("Nenhuma aula encontrada com esse termo.")
        else:
            for _, row in aulas_privadas.iterrows():
                exibir_aula(row)

# --- PÁGINA 3: PAINEL DO PROFESSOR (ADMIN) ---
elif menu == "⚙️ Painel do Professor" and st.session_state.eh_admin:
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">⚙️ Painel do Professor</div>
        <div class="hero-subtitle">Publique novas aulas, organize categorias e gerencie os materiais disponíveis na plataforma.</div>
    </div>
    """, unsafe_allow_html=True)

    tab_cadastrar, tab_gerenciar = st.tabs(["➕ Cadastrar Nova Aula", "📋 Gerenciar / Excluir Aulas"])

    with tab_cadastrar:
        with st.form("form_nova_aula", clear_on_submit=True):
            titulo = st.text_input("Título da Aula *", placeholder="Ex: Phrasal Verbs para Reuniões")

            col1, col2, col3 = st.columns(3)
            with col1:
                categorias_existentes = list(df_aulas["categoria"].dropna().unique())
                categoria = st.selectbox(
                    "Categoria / Tema *",
                    options=categorias_existentes + ["Nova Categoria..."]
                )
            with col2:
                nivel = st.selectbox("Nível *", ["Todos", "Iniciante", "Intermediário", "Avançado"])
            with col3:
                acesso = st.selectbox("Visibilidade *", ["publico", "privado"])

            nova_categoria = st.text_input("Se escolheu 'Nova Categoria...', digite o nome aqui:")
            descricao = st.text_area("Descrição / Resumo da Aula *",
                                     placeholder="Explique o que o aluno vai aprender nesta aula...")

            col_links1, col_links2 = st.columns(2)
            with col_links1:
                link_video = st.text_input("Link do Vídeo (YouTube - opcional)",
                                           placeholder="https://www.youtube.com/watch?v=...")
            with col_links2:
                link_drive = st.text_input("Link do Material no Google Drive (opcional)",
                                           placeholder="https://drive.google.com/file/d/...")

            submitted = st.form_submit_button("💾 Publicar Aula", use_container_width=True, type="primary")

            if submitted:
                cat_final = nova_categoria.strip() if categoria == "Nova Categoria..." and nova_categoria.strip() else categoria

                if not titulo.strip() or not descricao.strip() or cat_final == "Nova Categoria...":
                    st.error("Preencha os campos obrigatórios (*): Título, Categoria e Descrição.")
                else:
                    novo_id = int(df_aulas["id"].max()) + 1 if not df_aulas.empty else 1
                    nova_linha = pd.DataFrame([{
                        "id": novo_id,
                        "titulo": titulo.strip(),
                        "categoria": cat_final,
                        "nivel": nivel,
                        "acesso": acesso,
                        "descricao": descricao.strip(),
                        "link_video": link_video.strip(),
                        "link_drive": link_drive.strip()
                    }])
                    df_atualizado = pd.concat([df_aulas, nova_linha], ignore_index=True)
                    salvar_aulas(df_atualizado)
                    st.success(f"Aula '{titulo}' publicada com sucesso!")
                    st.rerun()

    with tab_gerenciar:
        st.subheader("Editar ou Excluir Aulas")
        st.caption(
            "Dê um duplo clique em qualquer célula (incluindo links do YouTube e Drive) para editar. Marque a caixa 'Excluir' para remover uma aula.")

        # Prepara uma cópia limpa para edição sem exibir 'None' ou 'NaN' nos campos vazios
        df_para_editar = df_aulas.fillna("").copy()
        df_para_editar.insert(0, "Excluir", False)

        df_editado = st.data_editor(
            df_para_editar,
            use_container_width=True,
            hide_index=True,
            disabled=["id"],  # Bloqueia edição do ID para manter a integridade
            column_config={
                "Excluir": st.column_config.CheckboxColumn("🗑️ Excluir", default=False),
                "id": st.column_config.NumberColumn("ID", width="small"),
                "titulo": st.column_config.TextColumn("Título", required=True),
                "categoria": st.column_config.TextColumn("Categoria", required=True),
                "nivel": st.column_config.SelectboxColumn(
                    "Nível",
                    options=["Todos", "Iniciante", "Intermediário", "Avançado"],
                    required=True
                ),
                "acesso": st.column_config.SelectboxColumn(
                    "Acesso",
                    options=["publico", "privado"],
                    required=True
                ),
                "descricao": st.column_config.TextColumn("Descrição", width="large"),
                "link_video": st.column_config.LinkColumn("Link do Vídeo (YouTube)"),
                "link_drive": st.column_config.LinkColumn("Link do Material (Drive)")
            },
            key="editor_aulas"
        )

        if st.button("💾 Salvar Alterações na Tabela", type="primary", use_container_width=True):
            # Remove as linhas marcadas com Excluir = True e descarta a coluna auxiliar
            df_final = df_editado[df_editado["Excluir"] == False].drop(columns=["Excluir"])
            salvar_aulas(df_final)
            st.success("Alterações salvas com sucesso no arquivo CSV!")
            st.rerun()