import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mca
from adjustText import adjust_text
##
st.title("CrossTable Analysis APP")

## Data
st.subheader("Data Selection")
uploaded_file = st.file_uploader(
    label="Upload an excel file"
)
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file) #load first sheet
    #
    # fpath = "data/BrandValue.xlsx"
    # df = pd.read_excel(fpath)

    st.subheader("Uploaded Data")
    st.write(df)

    # correspondence analysis
    df = df.set_index(df.columns[0])
    ncols = df.shape[1]
    mdl = mca.MCA(df, ncols=ncols, benzecri=False)
    a1 = pd.DataFrame(mdl.fs_r(N=2), columns=["x", "y"]).assign(vartype="row", label= df.index)
    a2 = pd.DataFrame(mdl.fs_c(N=2), columns=["x", "y"]).assign(vartype="col", label=df.columns)
    dfp = pd.concat([a1, a2], ignore_index=True)

    # scatter plot
    st.subheader('Correspondence Mapping')
    fig = sns.scatterplot(data=dfp, x="x", y="y", hue="vartype")
    texts = [plt.text(dfp.x[i], dfp.y[i], dfp.label[i], ha='center', va='center') for i in range(len(dfp))]
    adjust_text(texts)
    # plt.show()
    st.pyplot(plt)

    # xy coordinate table
    st.subheader("XY coordinates of Mapping")
    st.write(dfp)

    # Download
    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('shift-JIS')

    csv = convert_df(dfp)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='MappingCoordinates.csv',
        mime='text/csv',
    )




