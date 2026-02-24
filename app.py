
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Provisional Natality Data Dashboard")
st.subheader("Birth Analysis by State and Gender")

STEP 3 — Load Data

try:
df = pd.read_csv("Provisional_Natality_2025_CDC.csv")
except FileNotFoundError:
st.error("Dataset file not found in repository.")
st.stop()

Normalize column names

df.columns = (
df.columns.str.strip()
.str.lower()
.str.replace(" ", "_")
)

required_fields = [
"state_of_residence",
"month",
"month_code",
"year_code",
"sex_of_infant",
"births",
]

missing_fields = [col for col in required_fields if col not in df.columns]

if missing_fields:
st.error(f"Missing required logical fields: {missing_fields}")
st.write(df.columns)
st.stop()

Convert births to numeric

df["births"] = pd.to_numeric(df["births"], errors="coerce")
df = df.dropna(subset=["births"])

STEP 4 — Sidebar Filters

months = sorted(df["month"].dropna().unique())
genders = sorted(df["sex_of_infant"].dropna().unique())
states = sorted(df["state_of_residence"].dropna().unique())

month_options = ["All"] + list(months)
gender_options = ["All"] + list(genders)
state_options = ["All"] + list(states)

selected_months = st.sidebar.multiselect(
"Select Month",
options=month_options,
default=["All"]
)

selected_genders = st.sidebar.multiselect(
"Select Gender",
options=gender_options,
default=["All"]
)

selected_states = st.sidebar.multiselect(
"Select State",
options=state_options,
default=["All"]
)

STEP 5 — Filtering Logic

filtered_df = df.copy()

if "All" not in selected_months:
filtered_df = filtered_df[filtered_df["month"].isin(selected_months)]

if "All" not in selected_genders:
filtered_df = filtered_df[filtered_df["sex_of_infant"].isin(selected_genders)]

if "All" not in selected_states:
filtered_df = filtered_df[filtered_df["state_of_residence"].isin(selected_states)]

if filtered_df.empty:
st.warning("No data available for the selected filters.")
st.stop()

STEP 6 — Aggregation

agg_df = (
filtered_df
.groupby(["state_of_residence", "sex_of_infant"], as_index=False)["births"]
.sum()
.sort_values("state_of_residence")
)

STEP 7 — Plot

fig = px.bar(
agg_df,
x="state_of_residence",
y="births",
color="sex_of_infant",
title="Total Births by State and Gender",
template="plotly_white"
)

fig.update_layout(
legend_title_text="Gender",
xaxis_title="State of Residence",
yaxis_title="Births"
)

st.plotly_chart(fig, use_container_width=True)

STEP 8 — Show Filtered Table

st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)
