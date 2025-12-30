import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Commandes",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 
st.markdown("""
<style>
    
    .stApp {
        max-height: 100vh;
        overflow-y: hidden;
    }
    
    .main-container {
        padding: 10px;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* KPI cards */
    .kpi-card {
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid;
        height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .kpi-total { border-left-color: #4361ee; }
    .kpi-livrees { border-left-color: #4CAF50; }
    .kpi-non-livrees { border-left-color: #F44336; }
    .kpi-taux { border-left-color: #FF9800; }
    .kpi-infos { border-left-color: #9C27B0; }
    
    .kpi-value {
        font-size: 26px;
        font-weight: bold;
        margin: 5px 0;
    }
    
    .kpi-label {
        font-size: 14px;
        color: #666;
        margin: 0;
    }
    
    /* Conteneurs de graphiques */
    .chart-container {
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        height: 400px;
    }
    
    .small-chart-container {
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        height: 400px;
    }
    
    /* Titres */
    .section-title {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 15px;
        color: #2c3e50;
    }
    
    .js-plotly-plot {
        height: 320px !important;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour charger les données
@st.cache_data
def charger_donnees():
    """Charge les 4 fichiers CSV et les fusionne"""
    
    try:
        temps = pd.read_csv('data/Dim_Temps.csv')
        commande = pd.read_csv('data/TF_Commande.csv')
        employe = pd.read_csv('data/Dim_Employee.csv')
        client = pd.read_csv('data/Dim_Client.csv')
        
        df = commande.merge(temps, on='id_temps', how='left')
        df = df.merge(employe[['id_seqEmployee', 'Nom', 'Prenom']], 
                     on='id_seqEmployee', how='left')
        df = df.merge(client[['id_seqClient', 'CompanyName', 'Country']], 
                     on='id_seqClient', how='left')
        
        df['Total_Commandes'] = df['nb_commandes_livrees'] + df['nb_commandes_non_livrees']
        df['Taux_Livraison'] = (df['nb_commandes_livrees'] / df['Total_Commandes'] * 100).round(2)
        
        return df
    
    except Exception as e:
        st.error(f"Erreur chargement donnees: {e}")
        return pd.DataFrame()

# Titre principal
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h1 style="text-align: center; margin-bottom: 20px;">Dashboard Analyse Commandes</h1>', unsafe_allow_html=True)

# Charger les données
df = charger_donnees()

if df.empty:
    st.error("Donnees non chargees. Verifiez les fichiers CSV dans le dossier 'data/'")
    st.stop()

# ============ SECTION KPI ============
st.markdown('<div class="section-title">Indicateurs Principaux</div>', unsafe_allow_html=True)

# Calculer les KPI
total_commandes = df['Total_Commandes'].sum()
commandes_livrees = df['nb_commandes_livrees'].sum()
commandes_non_livrees = df['nb_commandes_non_livrees'].sum()
taux_livraison = (commandes_livrees / total_commandes * 100) if total_commandes > 0 else 0
nb_clients = df['id_seqClient'].max()
nb_employes = df['id_seqEmployee'].max()

# Afficher les KPI en 5 colonnes
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f'''
    <div class="kpi-card kpi-total">
        <div class="kpi-value">{total_commandes:,}</div>
        <div class="kpi-label">Total Commandes</div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    pourcentage_livrees = (commandes_livrees / total_commandes * 100) if total_commandes > 0 else 0
    st.markdown(f'''
    <div class="kpi-card kpi-livrees">
        <div class="kpi-value">{commandes_livrees:,}</div>
        <div class="kpi-label">Commandes Livrees ({pourcentage_livrees:.1f}%)</div>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    pourcentage_non_livrees = (commandes_non_livrees / total_commandes * 100) if total_commandes > 0 else 0
    st.markdown(f'''
    <div class="kpi-card kpi-non-livrees">
        <div class="kpi-value">{commandes_non_livrees:,}</div>
        <div class="kpi-label">Commandes Non Livrees ({pourcentage_non_livrees:.1f}%)</div>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    st.markdown(f'''
    <div class="kpi-card kpi-taux">
        <div class="kpi-value">{taux_livraison:.1f}%</div>
        <div class="kpi-label">Taux de Livraison</div>
    </div>
    ''', unsafe_allow_html=True)

with col5:
    st.markdown(f'''
    <div class="kpi-card kpi-infos">
        <div class="kpi-value">{nb_clients} / {nb_employes}</div>
        <div class="kpi-label">Clients / Employes</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)

# ============ PREMIERE LIGNE: 2 GRAPHIQUES ============
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown('<div class="section-title">Commandes par Mois</div>', unsafe_allow_html=True)
    with st.container():
        # Grouper par mois
        df_mois = df.groupby('mois_annee').agg({
            'nb_commandes_livrees': 'sum',
            'nb_commandes_non_livrees': 'sum'
        }).reset_index().sort_values('mois_annee')
        
        fig_mois = go.Figure()
        fig_mois.add_trace(go.Bar(
            x=df_mois['mois_annee'],
            y=df_mois['nb_commandes_livrees'],
            name='Livrees',
            marker_color='#4CAF50'
        ))
        fig_mois.add_trace(go.Bar(
            x=df_mois['mois_annee'],
            y=df_mois['nb_commandes_non_livrees'],
            name='Non Livrees',
            marker_color='#F44336'
        ))
        
        fig_mois.update_layout(
            barmode='group',
            height=320,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        fig_mois.update_xaxes(title_text="Mois")
        fig_mois.update_yaxes(title_text="Nombre de Commandes")
        
        st.plotly_chart(fig_mois, use_container_width=True, config={'displayModeBar': False})

with col_g2:
    st.markdown('<div class="section-title">Commandes par Annee</div>', unsafe_allow_html=True)
    with st.container():
        # Grouper par annee
        df_annee = df.groupby('annee').agg({
            'nb_commandes_livrees': 'sum',
            'nb_commandes_non_livrees': 'sum'
        }).reset_index()
        
        fig_annee = go.Figure()
        fig_annee.add_trace(go.Bar(
            x=df_annee['annee'],
            y=df_annee['nb_commandes_livrees'],
            name='Livrees',
            marker_color='#4CAF50'
        ))
        fig_annee.add_trace(go.Bar(
            x=df_annee['annee'],
            y=df_annee['nb_commandes_non_livrees'],
            name='Non Livrees',
            marker_color='#F44336'
        ))
        
        fig_annee.update_layout(
            barmode='stack',
            height=320,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        fig_annee.update_xaxes(title_text="Annee")
        fig_annee.update_yaxes(title_text="Nombre de Commandes")
        
        st.plotly_chart(fig_annee, use_container_width=True, config={'displayModeBar': False})

st.markdown('<div style="margin: 15px 0;"></div>', unsafe_allow_html=True)

# ============ DEUXIEME LIGNE: 3 GRAPHIQUES ============
col_g3, col_g4, col_g5 = st.columns(3)

with col_g3:
    st.markdown('<div class="section-title">Top 10 Clients</div>', unsafe_allow_html=True)
    with st.container():
        # Top 10 clients
        df_client = df.groupby(['CompanyName', 'Country']).agg({
            'nb_commandes_livrees': 'sum',
            'nb_commandes_non_livrees': 'sum',
            'Total_Commandes': 'sum'
        }).reset_index().nlargest(10, 'Total_Commandes')
        
        df_client['Nom_Affiche'] = df_client.apply(
            lambda x: f"{x['CompanyName'][:15]}..." if len(x['CompanyName']) > 15 else x['CompanyName'], 
            axis=1
        )
        
        fig_client = go.Figure()
        fig_client.add_trace(go.Bar(
            y=df_client['Nom_Affiche'],
            x=df_client['Total_Commandes'],
            name='Total',
            orientation='h',
            marker_color='#4361ee',
            hovertemplate='<b>%{y}</b><br>Total: %{x}<br>Pays: %{customdata}',
            customdata=df_client['Country']
        ))
        
        fig_client.update_layout(
            height=320,
            showlegend=False,
            margin=dict(l=40, r=40, t=40, b=40),
            yaxis={'categoryorder': 'total ascending'}
        )
        
        fig_client.update_xaxes(title_text="Commandes")
        
        st.plotly_chart(fig_client, use_container_width=True, config={'displayModeBar': False})

with col_g4:
    st.markdown('<div class="section-title">Top 10 Employes</div>', unsafe_allow_html=True)
    with st.container():
        # Top 10 employes
        df_employe = df.groupby(['Nom', 'Prenom']).agg({
            'nb_commandes_livrees': 'sum',
            'nb_commandes_non_livrees': 'sum',
            'Total_Commandes': 'sum'
        }).reset_index().nlargest(10, 'Total_Commandes')
        
        df_employe['Nom_Complet'] = df_employe['Prenom'] + ' ' + df_employe['Nom']
        df_employe['Nom_Complet'] = df_employe['Nom_Complet'].apply(
            lambda x: x[:15] + '...' if len(x) > 15 else x
        )
        
        # Calculer le taux pour chaque employe
        df_employe['Taux_Livraison'] = (df_employe['nb_commandes_livrees'] / df_employe['Total_Commandes'] * 100).round(1)
        
        fig_employe = go.Figure()
        fig_employe.add_trace(go.Bar(
            y=df_employe['Nom_Complet'],
            x=df_employe['Total_Commandes'],
            name='Total',
            orientation='h',
            marker_color='#9C27B0',
            hovertemplate='<b>%{y}</b><br>Total: %{x}<br>Taux: %{customdata}%',
            customdata=df_employe['Taux_Livraison']
        ))
        
        fig_employe.update_layout(
            height=320,
            showlegend=False,
            margin=dict(l=40, r=40, t=40, b=40),
            yaxis={'categoryorder': 'total ascending'}
        )
        
        fig_employe.update_xaxes(title_text="Commandes")
        
        st.plotly_chart(fig_employe, use_container_width=True, config={'displayModeBar': False})

with col_g5:
    st.markdown('<div class="section-title">Taux par Pays</div>', unsafe_allow_html=True)
    with st.container():
        # Taux par pays - CAMEMBERT
        df_pays = df.groupby('Country').agg({
            'nb_commandes_livrees': 'sum',
            'Total_Commandes': 'sum'
        }).reset_index()
        
        df_pays = df_pays[df_pays['Total_Commandes'] > 0]  # Enlever les pays sans commandes
        df_pays['Taux_Livraison'] = (df_pays['nb_commandes_livrees'] / df_pays['Total_Commandes'] * 100).round(1)
        
        # Créer le camembert
        fig_pays = px.pie(
            df_pays,
            values='Taux_Livraison',
            names='Country',
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig_pays.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Taux: %{value:.1f}%<br>Commandes: %{customdata}',
            customdata=df_pays['Total_Commandes'],
            pull=[0.05 if i < 3 else 0 for i in range(len(df_pays))]  # Mettre en avant les 3 premiers
        )
        
        fig_pays.update_layout(
            height=320,
            showlegend=False,
            margin=dict(l=40, r=40, t=40, b=40),
            title={
                'text': 'Taux de Livraison (%)',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 14}
            }
        )
        
        st.plotly_chart(fig_pays, use_container_width=True, config={'displayModeBar': False})

st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)

# ============ TABLEAU RESUMÉ ============
st.markdown('<div class="section-title">Resume par Annee</div>', unsafe_allow_html=True)

with st.container():
    # Calculer les statistiques par annee
    stats_annee = df.groupby('annee').agg({
        'nb_commandes_livrees': 'sum',
        'nb_commandes_non_livrees': 'sum',
        'Total_Commandes': 'sum',
        'id_seqClient': 'nunique',
        'id_seqEmployee': 'nunique'
    }).reset_index()
    
    stats_annee['Taux_Livraison'] = (stats_annee['nb_commandes_livrees'] / stats_annee['Total_Commandes'] * 100).round(1)
    
    # Renommer les colonnes
    stats_annee.columns = ['Annee', 'Livrees', 'Non Livrees', 'Total', 'Clients', 'Employes', 'Taux %']
    
    # Afficher le tableau
    st.dataframe(
        stats_annee.style
            .format({
                'Livrees': '{:,}',
                'Non Livrees': '{:,}',
                'Total': '{:,}',
                'Taux %': '{:.1f}%'
            })
            .background_gradient(subset=['Taux %'], cmap='RdYlGn', vmin=0, vmax=100)
            .set_properties(**{
                'text-align': 'center',
                'font-size': '12px'
            }),
        use_container_width=True,
        height=200
    )

st.markdown('</div>', unsafe_allow_html=True)

# ============ FOOTER ============
st.markdown(f"""
<div style='text-align: center; color: #666; font-size: 12px; margin-top: 20px; padding-top: 10px; border-top: 1px solid #eee;'>
    <p>Dashboard Commandes • Periode: {df['annee'].min()} a {df['annee'].max()} • 
    {len(df):,} commandes analysees</p>
</div>
""", unsafe_allow_html=True) 