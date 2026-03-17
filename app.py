import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página e CSS (Mantendo seu design original)
st.set_page_config(page_title="Gerador de Roteiros", layout="centered")

st.markdown("""
    <style>
    /* Forçando as cores e fontes do seu design original */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        text-transform: lowercase;
    }
    
    .stApp {
        background-color: #1a1a2e;
        color: #ffffff;
    }
    
    h1 {
        color: #e8612d !important;
        text-align: center;
        font-weight: 800;
    }
    
    p {
        color: #a0a0b5;
        text-align: center;
    }
    
    /* Estilizando o botão principal */
    .stButton>button {
        background-color: #e8612d;
        color: white;
        border: none;
        width: 100%;
        padding: 0.8rem;
        font-weight: 600;
        border-radius: 6px;
        transition: opacity 0.3s;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        background-color: #e8612d;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Configurando a chave da API do Gemini puxando do cofre
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Interface (Formulário)
st.markdown("<h1>gerador de roteiros</h1>", unsafe_allow_html=True)
st.markdown("<p>preencha as informações e receba um roteiro completo gerado por ia.</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    tema = st.text_input("tema / pauta *", placeholder="ex: como organizar a rotina")
    formato = st.selectbox("formato do vídeo *", ["tutorial/passo a passo", "demonstração ao vivo", "dica rápida", "bastidores", "storytelling", "lista/ranking", "antes e depois", "polêmico/opinião", "vlog"])
    tom = st.selectbox("tom de voz *", ["amiga que manja", "profissional mas leve", "energético", "calmo com autoridade", "bem-humorado", "inspirador", "personalizado"])

with col2:
    duracao = st.selectbox("duração estimada *", ["30s", "1min", "1min30s", "2min", "3min"])
    linguagem = st.selectbox("linguagem *", ["informal e direta", "informal e leve", "semi-formal", "formal", "coloquial", "educativa"])
    publico = st.text_input("como chama o público? (opcional)", placeholder="ex: divas, pessoal")

pontos = st.text_area("pontos principais do conteúdo *", placeholder="liste o que quer ensinar ou mostrar. 1 ponto por linha.")

st.markdown("---")
st.markdown("<p style='text-align: left; color: #e8612d; font-weight: 600;'>opcionais</p>", unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    gancho = st.text_input("gancho inicial (hook)", placeholder="sua ideia para os primeiros 3 seg")
    perfil = st.text_input("@ do perfil", placeholder="ex: @seunome")
with col4:
    cta = st.text_input("cta desejado", placeholder="ex: clica no link da bio")
    contexto = st.text_input("contexto extra", placeholder="detalhes extras para a ia")

# 3. Lógica de Geração
if st.button("gerar roteiro mágico"):
    if not tema or not pontos:
        st.warning("por favor, preencha o tema e os pontos principais.")
    else:
        with st.spinner("pensando... gerando roteiro mágico..."):
            
            system_prompt = f"""
            Você é um roteirista profissional de vídeos curtos. Sua missão é escrever um roteiro EXATO, pronto para ser lido no teleprompter, sem usar colchetes de placeholder.
            O texto DEVE ser gerado 100% em letras minúsculas (lowercase).
            
            Diretrizes:
            - Tema: {tema}
            - Pontos que DEVEM ser abordados em falas reais: {pontos}
            - Formato: {formato}
            - Duração: {duracao} (crie timestamps adaptados)
            - Tom: {tom}
            - Linguagem: {linguagem}
            - Chamar o público de: {publico if publico else 'pessoal'}
            - Contexto extra: {contexto if contexto else 'Nenhum'}
            - CTA: {cta if cta else 'Pedir para curtir e seguir'}
            - Perfil: {perfil if perfil else 'Nenhum'}
            - Gancho do usuário: {gancho if gancho else 'Crie 2 opções de ganchos fortes'}

            Estrutura:
            ===== INFORMAÇÕES DO VÍDEO =====
            ===== OPÇÕES DE GANCHO (ESCOLHA 1) =====
            ===== ROTEIRO DETALHADO =====
            ===== LEGENDA E DICAS =====
            """

            try:
                # Usando o modelo gratuito e rápido do Gemini
                model = genai.GenerativeModel('gemini-1.5-flash', system_instruction="Você é um assistente especialista em roteiros virais. Responda APENAS em letras minúsculas.")
                
                resposta = model.generate_content(system_prompt)
                roteiro_gerado = resposta.text.lower()
                
                st.success("roteiro gerado com sucesso!")
                st.code(roteiro_gerado, language="markdown")
                
            except Exception as e:
                st.error(f"erro ao conectar com o gemini: {e}")
