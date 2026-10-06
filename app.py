import streamlit as st
import pandas as pd
import plotly.express as px

#  Configuration de la page (Critère : Compatible mobile / layout wide)
st.set_page_config(page_title="Dashboard Afrique - Sprint S2", layout="wide", page_icon="🌍")

#  Chargement des données optimisé (Critère : Chargement < 5 secondes)
@st.cache_data
def load_data():
    df = pd.read_csv('dataset_afrique.csv')
    return df

df = load_data()


# SIDEBAR : Filtres interactifs

st.sidebar.header("Filtres")

# Filtre Année
annee_min = int(df['Annee'].min())
annee_max = int(df['Annee'].max())
annee_selection = st.sidebar.slider("Sélectionnez l'année :", min_value=annee_min, max_value=annee_max, value=annee_max)

# Filtre Région
regions = df['Region'].dropna().unique().tolist()
region_selection = st.sidebar.multiselect("Filtrer par Région :", options=regions, default=regions)

# Application des filtres sur le dataset
df_filtre = df[(df['Annee'] == annee_selection) & (df['Region'].isin(region_selection))]
df_historique = df[df['Region'].isin(region_selection)] # Pour les graphiques temporels

st.sidebar.markdown("---")
st.sidebar.caption("Source des données : Banque Mondiale / ONU")


# SECTION 1 : Vue d'ensemble (KPIs)

st.title("🌍 Analyse des Indicateurs Socio-Économiques en Afrique")
st.markdown("Ce dashboard interactif explore les relations entre la démographie, la consommation et l'énergie à travers le continent africain.")

st.header("Vue d'ensemble")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label=f"Population Totale ({annee_selection})", value=f"{int(df_filtre['Population'].sum()):,}".replace(',', ' '))
with col2:
    st.metric(label="Moyenne Consommation/Hab", value=f"{df_filtre['Consommation_Par_Habitant'].mean():.2f}")
with col3:
    st.metric(label="Croissance Démographique Moyenne", value=f"{df_filtre['Croissance_Pop_pct'].mean():.2f} %")

st.markdown("---")


# SECTION 2 : Visualisations


col_gauche, col_droite = st.columns(2)

with col_gauche:
    # VISUALISATION 1 : Analyse temporelle (Plotly Line)
    st.header("Analyse Temporelle")
    st.write("Évolution de la population au fil du temps par région.")
    df_region_pop = df_historique.groupby(['Annee', 'Region'])['Population'].sum().reset_index()
    fig1 = px.line(df_region_pop, x='Annee', y='Population', color='Region', markers=True, 
                   title="Croissance de la population par région")
    st.plotly_chart(fig1, use_container_width=True)

    # VISUALISATION 3 : Corrélations (Scatter Plot)
    st.header("Corrélations")
    st.write("Lien entre Consommation et Énergie par habitant.")
    fig3 = px.scatter(df_filtre, x='Consommation_Par_Habitant', y='Energie_Par_Habitant', 
                      color='Region', hover_name='Code_Pays', size='Population',
                      title=f"Consommation vs Énergie ({annee_selection})")
    st.plotly_chart(fig3, use_container_width=True)

with col_droite:
    # VISUALISATION 2 : Comparaison géographique (Carte Choroplèthe)
    st.header("Comparaison Géographique")
    st.write("Répartition de la consommation par habitant sur la carte.")
    # Les codes ISO-3 de la Banque Mondiale fonctionnent nativement avec Plotly !
    fig2 = px.choropleth(df_filtre, locations='Code_Pays', color='Consommation_Par_Habitant',
                         hover_name='Code_Pays', scope='africa', color_continuous_scale='Viridis',
                         title=f"Carte de la Consommation par Habitant ({annee_selection})")
    st.plotly_chart(fig2, use_container_width=True)

    # VISUALISATION 4 : Distribution (Box Plot)
    st.header("Distribution")
    st.write("Dispersion de la consommation par habitant selon les régions.")
    fig4 = px.box(df_filtre, x='Region', y='Consommation_Par_Habitant', color='Region',
                  title=f"Distribution de la consommation par région ({annee_selection})")
    st.plotly_chart(fig4, use_container_width=True)

# VISUALISATION 5 : Top 10 (Bar Chart) exigé en complément
st.markdown("---")
st.header("Top 10 des pays")
st.write("Les 10 pays avec la plus forte consommation par habitant pour l'année sélectionnée.")
top_10 = df_filtre.nlargest(10, 'Consommation_Par_Habitant')
fig5 = px.bar(top_10, x='Code_Pays', y='Consommation_Par_Habitant', color='Region', text_auto='.2s',
              title=f"Top 10 Consommation par Habitant ({annee_selection})")
st.plotly_chart(fig5, use_container_width=True)
