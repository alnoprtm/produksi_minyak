import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout="wide")

def load_all_data():
    dataMinyak = pd.read_csv('produksi_minyak_mentah.csv')
    country = pd.read_json('kode_negara_lengkap.json')
    mergeResult = pd.merge(left=country, right=dataMinyak, left_on='alpha-3', right_on='kode_negara')
    data = dataHasil=mergeResult[['name','tahun','produksi','alpha-3','country-code','iso_3166-2','region','sub-region','intermediate-region','region-code','sub-region-code']]
    data2 = data.rename({'name': 'Negara','produksi':'Produksi' ,'tahun': 'Tahun','alpha-3':'Kode Negara'}, axis='columns')
    return data2
def total_data(dataset):
    total_dataframe = dataset[['Negara','Tahun','Kode Negara','region','sub-region','Produksi']]
    return total_dataframe
st.header("Produksi Minyak Negara")
st.header("")
dataset=load_all_data()
dataset_bersih = dataset[dataset['Produksi'] != 0]
dataset_tidak_produksi = dataset[dataset['Produksi'] == 0]

menu = st.sidebar.radio("Lihat Berdasarkan:",("Analisa Negara","Analisa Tahun","Hasil Analisa"))
if menu=="Analisa Negara":
    data_select_negara = dataset_bersih.groupby('Negara',as_index=False).mean()
    chooseCountry = st.selectbox('Pilih negara untuk di tampilkan',data_select_negara['Negara'])
    negara_data = dataset[dataset['Negara'] == chooseCountry]
    if chooseCountry:
        state_total = total_data(negara_data)
        st.subheader("Grafik pendapatan minyak negara "+chooseCountry)
        fig = px.line(x=state_total['Tahun'], y=state_total['Produksi'], labels={"x": "Tahun", "y": "Produksi"})
        fig.update_traces(line_color='red')
        fig.update_layout(margin=dict(l=0, r=10, b=0, t=30),yaxis_title=None, xaxis_title=None)
        st.plotly_chart(fig, use_container_width=True)
    kolom1,kolom2=st.columns((3,3))
    with kolom1:
        st.subheader("Produksi tertinggi pada negara "+chooseCountry)
        smallValue = negara_data
        smallValue = smallValue.sort_values(by=['Produksi'],ascending=False).head(1)
        st.subheader("Total produksi : "+smallValue['Produksi'].to_string(index=False))
        st.markdown("Negara      : "+smallValue['Negara'].to_string(index=False))
        st.markdown("Kode Negara : "+smallValue['Kode Negara'].to_string(index=False))
        st.markdown("Tahun       : "+smallValue['Tahun'].to_string(index=False))
        st.markdown("Region      : "+smallValue['region'].to_string(index=False))
        st.markdown("Sub Region  : "+smallValue['sub-region'].to_string(index=False))
    with kolom2:
        st.subheader("Produksi terendah pada negara "+chooseCountry)
        smallValue = negara_data
        smallValue = smallValue.sort_values(by=['Produksi'],ascending=True).head(1)
        st.subheader("Total produksi : "+smallValue['Produksi'].to_string(index=False))
        st.markdown("Negara      : "+smallValue['Negara'].to_string(index=False))
        st.markdown("Kode Negara : "+smallValue['Kode Negara'].to_string(index=False))
        st.markdown("Tahun       : "+smallValue['Tahun'].to_string(index=False))
        st.markdown("Region      : "+smallValue['region'].to_string(index=False))
        st.markdown("Sub Region  : "+smallValue['sub-region'].to_string(index=False))

    


if menu=="Analisa Tahun":
    select_year = st.selectbox("Pilih tahun untuk di tampilkan",dataset['Tahun'])
    if select_year:
        
        state_year = dataset[dataset['Tahun'] == select_year]
        state_total = total_data(state_year)

        st.subheader("Pendapatan minyak pada tahun "+str(select_year))
        fig = px.bar(state_total, x='Produksi',y='Negara',color='Negara',labels={'Jumlah':'Produksi tahun %s' % (select_year)})
        st.plotly_chart(fig, use_container_width=True)

        
        st.subheader("Negara tertinggi pada tahun "+str(select_year))
        nilai = int(st.number_input("Banyak Negara Tahun", min_value=1,max_value=100))
        dataMax = state_total.sort_values(by=['Produksi'],ascending=False).head(nilai)
        dataf = dataMax[['Negara','Tahun','Produksi']]
        max_data = px.bar(dataf, x='Negara',y='Produksi',labels={'Jumlah':'Produksi tahun %s' % (select_year)})
        st.plotly_chart(max_data,use_container_width=True)

        kolom1,kolom2=st.columns((3,3))
        with kolom1:
            st.subheader("Negara Produksi tertinggi pada tahun "+str(select_year))
            data_tahun =dataset_bersih[dataset_bersih["Tahun"] == select_year]
            data_tahun=data_tahun[data_tahun['Produksi']==data_tahun['Produksi'].max()]
            st.subheader("Total produksi : "+data_tahun['Produksi'].to_string(index=False))
            st.markdown("Negara      : "+data_tahun['Negara'].to_string(index=False))
            st.markdown("Kode Negara : "+data_tahun['Kode Negara'].to_string(index=False))
            st.markdown("Tahun       : "+data_tahun['Tahun'].to_string(index=False))
            st.markdown("Region      : "+data_tahun['region'].to_string(index=False))
            st.markdown("Sub Region  : "+data_tahun['sub-region'].to_string(index=False))

        with kolom2:
            st.subheader("Negara Produksi terendah pada tahun "+str(select_year))
            data_tahun =dataset_bersih[dataset_bersih["Tahun"] == select_year]
            data_tahun=data_tahun[data_tahun['Produksi']==data_tahun['Produksi'].min()]
            data_tahun = data_tahun.head(5)
            st.subheader("Total produksi : "+data_tahun['Produksi'].to_string(index=False))
            st.markdown("Negara      : "+data_tahun['Negara'].to_string(index=False))
            st.markdown("Kode Negara : "+data_tahun['Kode Negara'].to_string(index=False))
            st.markdown("Tahun       : "+data_tahun['Tahun'].to_string(index=False))
            st.markdown("Region      : "+data_tahun['region'].to_string(index=False))
            st.markdown("Sub Region  : "+data_tahun['sub-region'].to_string(index=False))


    st.subheader("Negara 0 produksi pada tahun "+str(select_year))
    data_tahun =dataset_tidak_produksi[dataset_tidak_produksi["Tahun"] == select_year]
    st.dataframe(data_tahun[["Negara",'Kode Negara',"Tahun","Produksi",'region','sub-region']])
if menu=="Hasil Analisa":
    st.subheader("Negara dengan nilai produksi secara kumulatif")
    nilai_cum = int(st.number_input("Banyak Negara", min_value=1,max_value=100))
    Data = dataset[['Negara','Kode Negara','Tahun','Produksi','region','sub-region']]
    Data['Produksi Kumulatif'] = Data['Produksi'].cumsum()
    total = Data.sort_values(by=['Produksi Kumulatif'],ascending=False)
    urut = total.groupby('Negara',as_index=False).sum()
    dataMax = urut.sort_values(by=['Produksi'],ascending=False).head(nilai_cum)
    bar_chart = px.bar(dataMax, x='Negara',y='Produksi')
    st.plotly_chart(bar_chart,use_container_width=True)

    kolom1,kolom2=st.columns((3,3))
    with kolom1:
        st.subheader("Produksi tertinggi sepanjang tahun ")
        highValue = dataset_bersih
        highValue = highValue.sort_values(by=['Produksi'],ascending=False).head(1)
        st.subheader("Total produksi : "+highValue['Produksi'].to_string(index=False))
        st.markdown("Negara      : "+highValue['Negara'].to_string(index=False))
        st.markdown("Kode Negara : "+highValue['Kode Negara'].to_string(index=False))
        st.markdown("Tahun       : "+highValue['Tahun'].to_string(index=False))
        st.markdown("Region      : "+highValue['region'].to_string(index=False))
        st.markdown("Sub Region  : "+highValue['sub-region'].to_string(index=False))
    
    with kolom2:
        st.subheader("Produksi terendah sepanjang tahun ")
        smallValue = dataset_bersih
        smallValue = smallValue.sort_values(by=['Produksi'],ascending=True).head(1)
        st.subheader("Total produksi : "+smallValue['Produksi'].to_string(index=False))
        st.markdown("Negara      : "+smallValue['Negara'].to_string(index=False))
        st.markdown("Kode Negara : "+smallValue['Kode Negara'].to_string(index=False))
        st.markdown("Tahun       : "+smallValue['Tahun'].to_string(index=False))
        st.markdown("Region      : "+smallValue['region'].to_string(index=False))
        st.markdown("Sub Region  : "+smallValue['sub-region'].to_string(index=False))

    st.subheader("Negara dengan 0 produksi")
    st.dataframe(dataset_tidak_produksi[['Negara','Kode Negara','Tahun','Produksi','region','sub-region']])
    

st.markdown(" <style>footer {visibility: hidden;}</style> ", unsafe_allow_html=True)
