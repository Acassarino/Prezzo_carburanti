import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype
)

st.title("Controlla il prezzo aggiornato dei Carburanti")
st.title("Aggiornamento del 16-11-2023  8:00")

#st.title(df_aggiornamento)
#st.write(
#    """This app is based on this blog [here](https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/).
#    Can you think of ways to extend it with visuals?
#    """
#)


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns
    Args:
        df (pd.DataFrame): Original dataframe
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Aggiungi Filtri")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    #for col in df.columns:
    #    if is_object_dtype(df[col]):
    #        try:
    #            df[col] = pd.to_datetime(df[col])
    #        except Exception:
    #            pass

        #if is_datetime64_any_dtype(df[col]):
           #df[col] = df[col].dt.tz_localize(None)
           ##df[col] = df[col].dt.tz_localize(timezone='Europe/Berlin')

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filtro attivo", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 15:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input)]

    return df


df = pd.read_csv(
    "Carburanti-distributori.csv", index_col=0
)
st.dataframe(filter_dataframe(df))

st.write(
    """Applicazione basata sui dati rilevati al seguente link [here](https://www.mise.gov.it/index.php/it/open-data/elenco-dataset/carburanti-prezzi-praticati-e-anagrafica-degli-impianti?wsdl?wsdl?wsdl).
    """)
st.write( """La licenza è la [IODL 2.0] (http://www.dati.gov.it/iodl/2.0/)""")

st.write( 'Lavoro a cura di Andrea Cassarino')
st.write( 'Email:  ing.acassarino@gmail.com')


#html_string = "<img style="display:none"; position:relative; left:-9999999px; src="https://clk.tradedoubler.com/click?p=237081&amp;a=1900897&amp;url=https%3A%2F%2Fwww.ticketone.it%2F" />"
#st.markdown(html_string, unsafe_allow_html=True)

header_html = "<img src='https://clk.tradedoubler.com/click?p=237081&amp;a=1900897&amp;url=https%3A%2F%2Fwww.ticketone.it%2F' class='img-fluid' style='display:none' position:relative left:-9999999px>"

st.markdown(
    header_html, unsafe_allow_html=True,
)
