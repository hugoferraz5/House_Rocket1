import pandas as pd
import streamlit as st
import numpy as np
import folium
import geopandas

from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

import plotly.express as px

from datetime import datetime

st.set_page_config(layout='wide')


@st.cache(allow_output_mutation=True)
def get_data( path ):
    data = pd.read_csv( path )

    return data

@st.cache(allow_output_mutation=True)
def get_geofile( url ):
    geofile = geopandas.read_file( url )

    return geofile

def set_feature( data ):
    # add new features
    data['price_m2'] = data['price'] / data['sqft_lot']

    return data

def overview_data( data ):
    f_attributes = st.sidebar.multiselect('Enter columns', data.columns)
    f_zipcode = st.sidebar.multiselect(
        'Enter zipcode',
        data['zipcode'].unique())

    st.title('Data Overview')

    if (f_zipcode != []) & (f_attributes != []):
        data = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]

    elif (f_zipcode != []) & (f_attributes == []):
        data = data.loc[data['zipcode'].isin(f_zipcode), :]

    elif (f_zipcode == []) & (f_attributes != []):
        data = data.loc[:, f_attributes]

    else:
        data = data.copy()

    st.dataframe(data)
    c1, c2 = st.beta_columns((1, 1))

    # average metrics
    df1 = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
    df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df3 = data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
    df4 = data[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

    # merge
    m1 = pd.merge(df1, df2, on='zipcode', how='inner')
    m2 = pd.merge(m1, df3, on='zipcode', how='inner')
    df = pd.merge(m2, df4, on='zipcode', how='inner')

    df.columns = ['ZIPCODE', 'TOTAL HOUSES', 'PRICE', 'SQFT LIVING',
                  'PRICE/M2']
    c1.header('Average Values')
    c1.dataframe(df, height=600)

    # Statistic Descriptive
    num_attributes = data.select_dtypes(include=['int64', 'float64'])
    media = pd.DataFrame(num_attributes.apply(np.mean))
    mediana = pd.DataFrame(num_attributes.apply(np.median))
    std = pd.DataFrame(num_attributes.apply(np.std))

    max_ = pd.DataFrame(num_attributes.apply(np.max))
    min_ = pd.DataFrame(num_attributes.apply(np.min))

    df1 = pd.concat([max_, min_, media, mediana, std], axis=1).reset_index()

    df1.columns = ['attributes', 'max', 'min', 'media', 'median', 'std']

    c2.header('Descriptive Analysis')
    c2.dataframe(df1, height=600)

    return None

def portfolio_density( data, geofile ):
    st.title('Region Overview')

    c1, c2 = st.beta_columns((1, 1))
    c1.header('Portfolio Density')

    df = data.sample(1000)

    # Base Map - Folium
    density_map = folium.Map(location=[data['lat'].mean(),
                                       data['long'].mean()],
                             default_zoom_start=15)

    marker_cluster = MarkerCluster().add_to(density_map)
    for name, row in df.iterrows():
        folium.Marker([row['lat'], row['long']],
                      popup='Sold R${0} on: {1}. Features: {2} sqft, {3} bedrooms, {4} bathrooms, year built: {5}'.format(
                          row['price'],
                          row['date'],
                          row['sqft_living'],
                          row['bedrooms'],
                          row['bathrooms'],
                          row['yr_built'])).add_to(marker_cluster)

    with c1:
        folium_static(density_map)

    # Region Price Map
    c2.header('Price Density')

    df = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df.columns = ['ZIP', 'PRICE']

    # df = df.sample( 10 )

    geofile = geofile[geofile['ZIP'].isin(df['ZIP'].tolist())]

    region_price_map = folium.Map(location=[data['lat'].mean(),
                                            data['long'].mean()],
                                  default_zoom_start=15)

    region_price_map.choropleth(data=df,
                                geo_data=geofile,
                                columns=['ZIP', 'PRICE'],
                                key_on='feature.properties.ZIP',
                                fill_color='YlOrRd',
                                fill_opacity=0.7,
                                line_opacity=0.2,
                                legend_name='AVG PRICE')

    with c2:
        folium_static(region_price_map)

    return None

def commercial_distribution( data ):
    st.sidebar.title('Commercial Options')
    st.title('Commercial Attributes')

    # --------- Average price per year

    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

    # filters
    min_year_built = int(data['yr_built'].min())
    max_year_built = int(data['yr_built'].max())
    st.sidebar.subheader('Select Max Year Built')
    f_year_built = st.sidebar.slider('Year Built', min_year_built,
                                     max_year_built,
                                     min_year_built)

    st.header('Average Price per Year built')

    # data selection
    df = data.loc[data['yr_built'] < f_year_built]
    df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

    # plot
    fig = px.line(df, x='yr_built', y='price')
    st.plotly_chart(fig, use_container_width=True)

    # --------- Average price per Day
    st.header('Average Price per day')
    st.sidebar.subheader('Select Max Date')

    # filters
    min_date = datetime.strptime(data['date'].min(), '%Y-%m-%d')
    max_date = datetime.strptime(data['date'].max(), '%Y-%m-%d')

    f_date = st.sidebar.slider('Date', min_date, max_date, min_date)

    # data filtering
    data['date'] = pd.to_datetime(data['date'])
    df = data.loc[data['date'] < f_date]
    df = df[['date', 'price']].groupby('date').mean().reset_index()

    # plot
    fig = px.line(df, x='date', y='price')
    st.plotly_chart(fig, use_container_width=True)

    # -------------- Histograma
    st.header('Price Distribution')
    st.sidebar.subheader('Select Max Price')

    # filter
    min_price = int(data['price'].min())
    max_price = int(data['price'].max())
    avg_price = int(data['price'].mean())

    # data filtering
    f_price = st.sidebar.slider('Price', min_price, max_price, avg_price)
    df = data.loc[data['price'] < f_price]

    # data plot
    fig = px.histogram(df, x='price', nbins=50)
    st.plotly_chart(fig, use_container_width=True)

    return None

def attributes_distribution( data ):
    st.sidebar.title('Attributes Options')
    st.title('House Attributes')

    # filters
    f_bedrooms = st.sidebar.selectbox('Max number of bedrooms',
                                      data['bedrooms'].unique())

    f_bathrooms = st.sidebar.selectbox('Max number of bathrooms',
                                       data['bathrooms'].unique())

    c1, c2 = st.beta_columns(2)

    # House per bedrooms
    c1.header('Houses per bedrooms')
    df = data[data['bedrooms'] < f_bedrooms]
    fig = px.histogram(df, x='bedrooms', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    # House per bathrooms
    c2.header('Houses per bathrooms')
    df = data[data['bathrooms'] < f_bedrooms]
    fig = px.histogram(df, x='bathrooms', nbins=19)
    c2.plotly_chart(fig, use_container_width=True)

    # filters
    f_floors = st.sidebar.selectbox('Max number of floor',
                                    sorted(set(data['floors'].unique())))

    f_waterview = st.sidebar.checkbox('Only Houses with Water View')

    c1, c2 = st.beta_columns(2)

    # House per floors
    c1.header('Houses per floor')
    df = data[data['floors'] < f_floors]

    # plot
    fig = px.histogram(df, x='floors', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    # House per water view
    if f_waterview:
        df = data[data['waterfront'] == 1]

    else:
        df = data.copy()

    fig = px.histogram(df, x='waterfront', nbins=10)
    c2.plotly_chart(fig, use_container_width=True)

    return None



def hipoteses( data ):
    st.markdown("<h1 style='text-align: center; color: black;'>Hipóteses de Negócio</h1>", unsafe_allow_html=True)

    c1,c2 = st.beta_columns(2)

    c1.subheader('Hipótese 1:  Imóveis com vista para a água são em média 30% mais caros')
    h1 = data[['price', 'waterfront',  'sqft_lot']].groupby('waterfront').mean().reset_index()
    h1['waterfront'] = h1['waterfront'].astype(str)
    fig = px.bar(h1, x='waterfront', y = 'price', color = 'waterfront',  labels={"waterfront": "Visão para água",
                                                                                 "price": "Preço"},
                                                                                  template= 'simple_white')

    fig.update_layout(showlegend = False)
    c1.plotly_chart(fig, use_container_width= True)

        #=========================================
        # ========== H2 ==========
        #==========================================.
    c2.subheader('Hipótese 2: Imóveis com data de construção menor que 1955 são em média 50% mais baratos')
    data['construcao'] = data['yr_built'].apply(lambda x: '> 1955' if x > 1955
                                                                   else '< 1955')

    h2 = data[['construcao', 'price',  'sqft_lot']].groupby('construcao').mean().reset_index()

    fig2 = px.bar(h2, x='construcao', y = 'price', color = 'construcao', labels = {"contrucao":"Ano da Construção",
                                                                                   'price': 'Preço'},
                                                                                    template='simple_white')




    fig2.update_layout(showlegend = False)
    c2.plotly_chart(fig2, use_container_width= True)

        #=========================================
        # ========== H3 ==========
        #==========================================.
    c3,c4 = st.beta_columns(2)

    c3.subheader('Hipótese 3: Imóveis sem porão com maior área total são 40% mais caros do que imóveis com porão')
    data['porao'] = data['sqft_basement'].apply(lambda x: 'nao' if x == 0
                                                      else 'sim')

    h3 = data[['porao', 'sqft_lot', 'price']].groupby('porao').sum().reset_index()
    fig3 = px.bar(h3, x='porao', y = 'price', color = 'porao', labels = {'price': 'Preço',
                                                                             'sqft_lot': 'Área Total'},
                                                                            template= 'simple_white')
    fig3.update_layout(showlegend = False)
    c3.plotly_chart(fig3, use_container_width= True)



        #=========================================
        # ========== H4 ==========
        #==========================================.

    c4.subheader('Hipótse 4: Imóveis antigos e não renovados são 40% mais baratos')
    data['renovacao'] =  data['yr_renovated'].apply(lambda  x: 'sim' if x > 0 else
                                                            'nao')

    data['contrucao'] = data['yr_built'].apply(lambda x: 'antigo' if (x < 1951) else
                                                   'atual')
    h8 = data[data['renovacao'] == 1]
    h8 = data[['contrucao', 'price', 'sqft_lot']].groupby('contrucao').sum().reset_index()
    fig6 = px.bar(h8, x ='contrucao', y = 'price', color = 'contrucao', labels = {'price':'Preço','contrucao': 'Tempo de Imóveis não renovados'} ,
                                                                                    template= 'simple_white')

    fig6.update_layout(showlegend = False)
    c4.plotly_chart(fig6, use_container_width= True)


        #=========================================
        # ========== H5 ==========
        #==========================================.
    c7, c8 = st.beta_columns(2)

    c7.subheader('Hipótese 5: Imóveis com mais banheiros são em média 5% mais caros')
    data['banheiro'] =  data['bathrooms'].apply(lambda x: '0-3' if (x > 0 ) & (x < 3) else
                                                       '3-5' if (x > 3) & (x < 5) else
                                                       '5-8')

    h9 = data[['banheiro', 'price', 'sqft_lot']].groupby('banheiro').mean().reset_index()
    fig7 = px.bar(h9, x = 'banheiro', y = 'price', color = 'banheiro', labels = {'price':'Preço','banheiro':
                                                                                'Quantidade de banheiros'},
                                                                                template= 'simple_white')


    fig7.update_layout(showlegend = False)
    c7.plotly_chart(fig7, use_container_width= True)


        #=========================================
        # ========== H6 ==========
        #==========================================.
    c8.subheader('Hipótese 6: O crescimento do preço dos imóveis mês após mês no ano de 2014 é de 10% ')
    data['date'] = pd.to_datetime(data['date'])

    data['mes'] = data['date'].dt.month
    data['ano'] = data['date'].dt.year

    year_df = data[data['ano'] == 2014]


    h41 = year_df[['mes', 'price', 'sqft_lot']].groupby('mes').sum().reset_index()
    fig41 = px.line(h41, x='mes', y = 'price', color_discrete_sequence= ['teal'], template = 'simple_white',
                labels={'mes':'Mês', 'price': 'Preço'})

    c8.plotly_chart(fig41, use_container_width= True)
        #=========================================
        # ========== H7 ==========
        #==========================================
    st.subheader('Hipótese 7: Imóveis com 3 banheiros tem um crescimento mês após mês de 15 %')
    h5 = data[(data['bathrooms'] == 3)]

    h5 = h5[['mes', 'price', 'sqft_lot']].groupby('mes').sum().reset_index()


    fig5 = px.line(h5, x = 'mes', y = 'price', color_discrete_sequence= ['teal'], template = 'simple_white',
               labels= {'mes':'Mês', 'price': 'Preço'})

    st.plotly_chart(fig5, x='mes', y='price', use_container_width= True)



def questoes_negocio( data ):
    st.markdown("<h1 style='text-align: center; color: black;'> Questões de Negócio</h1>", unsafe_allow_html=True)
    st.subheader('1. Quais são os imóveis que a House Rocket deveria comprar e por qual preço?')
        #Respondendo
    a = data[['zipcode', 'price']].groupby('zipcode').median().reset_index()
    df2 = pd.merge(a, data, on='zipcode', how = 'inner')
    df2 = df2.rename(columns = {'price_y' : 'price', 'price_x' : 'price_median'} ) #alterando nome das colunas
        #criando coluna
    for i, row in df2.iterrows():
        if (row['price_median'] >= row['price']) & (row['condition'] < 3):
            df2.loc[i,'pay'] =  'sim'
        else:
            df2.loc[i, 'pay'] = 'nao'

        #criar coluna com cor
    for i, row in df2.iterrows():
        if (row['pay'] == 'sim'):
         df2.loc[i,'marker_color'] = 'green'
        else:
            df2.loc[i, 'marker_color'] = 'red'
        ############################################
    st.markdown('Mapa - Quais imóveis devem ser comprados?')
    st.markdown("""
    <style>
    .big-font {
        font-size:14px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font"> Em verde os imóveis indicados '
                'para compra  <br> Em vermelho os imóveis não indicados para compra </p>', unsafe_allow_html=True)

    mapa = folium.Map(width = 600, height = 300,
                      location = [data['lat'].mean(),data[ 'long'].mean()],
                      default_zoom_start=30)
    features = {}
    for row in pd.unique(df2['marker_color']):
        features[row] = folium.FeatureGroup(name=row)

    for index, row in df2.head(10000).iterrows():
        circ = folium.Circle([row['lat'], row['long']],
            radius=150, color=row['marker_color'], fill_color=row['marker_color'],
            fill_opacity = 1, popup= 'Compra: {0}, Preço: {1}'.format(row['pay'],
                              row['price']))
        circ.add_to(features[row['marker_color']])

    for row in pd.unique(df2["marker_color"]):
        features[row].add_to(mapa)

    folium.LayerControl().add_to(mapa)
    folium_static(mapa)

        ############
        # QUESTÃO 2 #
        ############

    st.subheader('2. Uma vez comprado, qual é o melhor momento para vendê-lo e por qual preço?')
    df3 = df2.copy()

    df3['season'] = df3['mes'].apply(lambda x: 'summer' if (x > 5) & (x < 8) else
                                               'spring' if (x >= 2) & (x <= 5) else
                                               'fall' if (x >= 8) & (x < 12) else
                                               'winter')

    df3 = df3[df3['pay'] == 'sim']
    df4 = df3[['season', 'zipcode', 'price']].groupby(['zipcode', 'season']).median().reset_index()

    df4 = df4.rename(columns = {'price' : 'price_medi_season', 'season': 'season_median'} )

    df5 = pd.merge(df3, df4, on='zipcode', how = 'inner')

    for i, row in df5.iterrows():
        if (row['price_medi_season'] > row['price']):
            df5.loc[i, 'sale'] =  row['price'] * 1.3
        else:
            df5.loc[i, 'sale'] = row['price'] * 1.1


    df5= df5[['price_medi_season', 'price', 'sale', 'price_median', 'season', 'zipcode']]


    fig11 = px.bar(df5, x = 'season', y = 'sale', color = 'season', labels={'season':'Estação do Ano', 'sale': 'Preço de Venda'},
                                                                        template = 'simple_white')
    fig11.update_layout(showlegend = False)
    st.plotly_chart(fig11, x='season', y='sale', use_container_width= True)
    return None
    

if __name__ == '__main__':
    # ETL
    # data extration
    path = 'kc_house_data.csv'
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'

    data = get_data( path )
    geofile = get_geofile( url )

    # transformation
    data = set_feature( data )

    overview_data( data )

    portfolio_density( data, geofile )

    commercial_distribution( data )

    attributes_distribution( data )

    hipoteses( data )

    questoes_negocio( data )