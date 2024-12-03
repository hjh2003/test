import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import requests

# Streamlit 應用標題
st.title("天津市人口數據地圖與表格")

# 讀取 GeoJSON 數據
geojson_url = "https://github.com/hjh2003/test/raw/refs/heads/main/%E5%A4%A9%E6%B4%A5%E5%B8%82%E5%90%84%E5%8D%80%E4%BA%BA%E5%8F%A3.json"
geojson_data = requests.get(geojson_url).json()

# 提取各區的人口數據
population_data = []
for feature in geojson_data["features"]:
    name = feature["properties"].get("name", "未知區域")
    population = feature["properties"].get("population", 0)
    population_data.append({"區域": name, "人口": population})

# 將數據轉換為 Pandas 數據框
df = pd.DataFrame(population_data)

# 使用 Leafmap 創建地圖
m = leafmap.Map(center=[39.12, 117.2], zoom=10)

# 添加 GeoJSON 圖層，並設置 3D 效果
m.add_geojson(
    geojson_data,
    layer_name="Landslide",
    style={
        "fill-extrusion-color": {
            "property": "population",
            "stops": [
                [300000, "#FFEDA0"],
                [1100000, "#FEB24C"],
                [1700000, "#FF5000"]
            ]
        },
        "fill-extrusion-height": ["*", ["get", "population"], 0.02],
        "fill-extrusion-opacity": 1,
    },
)

# 在 Streamlit 中顯示地圖
st.subheader("人口數據地圖")
m.to_streamlit(height=700)

# 在 Streamlit 中顯示人口數據表格
st.subheader("各區人口數據")
st.dataframe(df.sort_values(by="人口", ascending=False))  # 按人口數排序
