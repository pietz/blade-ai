import streamlit as st
from PIL import Image
import requests
import io, json

models = {
    "P1 - Blade Segmentation": "https://dwtoc-ai.azurewebsites.net/api/p1?code=b4JeF3Sy0OVq13aBga1CPPpxaHYGNim99pHipZigaLi23EEkY3WW9A%3D%3D",
    "P3 - Damage Classification": "https://dwtoc-ai.azurewebsites.net/api/p3?code=kGdcP4HM4CPnCiA2DWUcc%2F4xvabbz5ORSwzXhh4u1hBldrqwtvtw5Q%3D%3D",
}

s = 3
headers = {"Content-Type": "application/octet-stream"}

st.sidebar.image(Image.open("lhind_blue.png"), use_column_width=True)
#st.sidebar.title("DWTOC AI")
m = st.sidebar.selectbox("Select a model", list(models.keys()))
url = models[m]
files = st.sidebar.file_uploader("Select Image File(s)", accept_multiple_files=True)

for f in files:
    # img = Image.open(f)
    # f.seek(0)
    response = requests.post(url=url, data=f.read(), headers=headers)
    if response.status_code == 200:
        if "Segmentation" in m:
            img = Image.open(io.BytesIO(response.content))
            st.image(img, use_column_width=True)
        else:  # Classification
            prob_dict = json.loads(response.content)
            st.write(prob_dict)
    else:
        st.write(response.status_code, response.reason)
