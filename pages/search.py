import streamlit as st
from classes.cv import cv
import base64
import pandas as pd
from pathlib import Path
def app():
    #st.set_page_config(layout="wide")
    st.markdown("# Search profil ❄️")
    #st.sidebar.markdown("# Search profil ❄️")

    CV=cv()

    text=st.title("Fit Job For:")
    jobdesc=st.text_area("")
    submit=st.button("Find")

    if not jobdesc=="":

        df=CV.load_cv_dir(jobdesc)
                #df['score']=df['score']*100
        data=df[['score','name','contact_number','email',"PDF_CV_PATH"]]
        data.sort_values('score',ascending=False)
        column_configuration={        
                "PDF_CV_PATH":st.column_config.TextColumn(
                "PDF_CV_PATH",width=None,      
                    ) ,      
                "score": st.column_config.ProgressColumn(
                            "Score", help="Score rate",
                                min_value=0,
                                max_value=1,
                                
                                #step=1,
                                #format="%.2f %%",
                        ),
                    }
            


        st.header("All found profiles")
        df = data[data['score']>0]
        event = st.dataframe(
                        df[df['score']>0][['score','name','contact_number','email']],
                        column_config=column_configuration,
                        use_container_width=True,
                        hide_index=True,
                        on_select="rerun",
                        selection_mode="single-row",
                    )
        people = event.selection.rows
        if people:
            st.header("Selected profile")
            people = event.selection.rows
            filtered_df = df.iloc[people]
            st.dataframe(
                            filtered_df,
                            column_config=column_configuration,
                            use_container_width=True,
                        )
            file=filtered_df["PDF_CV_PATH"].iloc[0]
            file=Path("resources")/ str(file)
            with open(file, "rb") as f:
                            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                            pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="900" height="1500" type="application/pdf"></iframe>'
                            st.markdown(pdf_display, unsafe_allow_html=True)



if __name__ == "__main__":
    app() 
