import streamlit as st
import numpy as np
import pandas as pd
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
# st.sidebar.title("DWTOC AI")
m = st.sidebar.selectbox("Select a model", list(models.keys()))
url = models[m]
files = st.sidebar.file_uploader("Select Image File(s)", accept_multiple_files=True)

for f in files:
    img = Image.open(f).convert("RGB")
    size = img.size
    w = 480
    h = int(img.size[1] / img.size[0] * w)
    img = img.resize((w, h))
    body = io.BytesIO()
    img.save(body, format="JPEG")
    response = requests.post(url=url, data=body.getvalue(), headers=headers)
    if response.status_code == 200:
        left, right = st.beta_columns(2)
        left.image(img, use_column_width=True)
        if "Segmentation" in m:
            msk = Image.open(io.BytesIO(response.content))
            img_arr = np.array(img)
            msk_arr = np.array(msk)[..., None] / 255.0
            # msk_arr = (msk_arr > 0.5).astype(np.float64)
            res_arr = img_arr * msk_arr
            res_arr = res_arr.astype(np.uint8)
            res = Image.fromarray(res_arr)
            right.image(res, use_column_width=True)
        else:  # Classification
            prob_dict = json.loads(response.content)
            right.bar_chart(pd.DataFrame.from_dict(prob_dict, orient="index"))
            # right.write(prob_dict)
    else:
        st.write(response.status_code, response.reason)
