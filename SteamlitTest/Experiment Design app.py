# import streamlit as st
# import pandas as pd
# import random
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import numpy as np
#
# st.set_page_config(page_title="On-Farm Experiment Design Assistant", layout="wide")
#
# st.title("🧪 On-Farm Experiment Design Assistant")
#
# # =========================
# # A. Experiment definition
# # =========================
# st.header("A. Experiment definition")
#
# exp_name = st.text_input("Experiment name")
# crop = st.text_input("Crop")
# season = st.text_input("Season / Year", "2025")
#
# research_question = st.text_area(
#     "Research question",
#     placeholder="e.g. Does product X increase yield enough to pay for itself?"
# )
#
# primary_metric = st.selectbox(
#     "Primary evaluation metric",
#     ["Yield", "Profitability", "Soil health", "Other"]
# )
#
# # =========================
# # B. Treatments & control
# # =========================
# st.header("B. Treatments")
#
# n_treatments = st.number_input(
#     "Number of treatments (including control)",
#     min_value=2,
#     max_value=5,
#     value=2
# )
#
# treatments = []
# for i in range(n_treatments):
#     col1, col2 = st.columns([3, 1])
#     with col1:
#         name = st.text_input(f"Treatment {i+1} name", f"T{i+1}")
#     with col2:
#         is_control = st.checkbox("Control", value=(i == 0), key=f"ctrl_{i}")
#     desc = st.text_input(f"{name} description", key=f"desc_{i}")
#     treatments.append(
#         {
#             "name": name,
#             "is_control": is_control,
#             "description": desc
#         }
#     )
#
# if not any(t["is_control"] for t in treatments):
#     st.error("⚠ At least one treatment must be a control.")
#
# # =========================
# # C. Replication advisor
# # =========================
# st.header("C. Replication strategy")
#
# change_type = st.radio(
#     "How big is the management change?",
#     ["Major management change", "Minor management change"]
# )
#
# expected_effect = st.selectbox(
#     "Expected effect size",
#     ["Large", "Moderate", "Small (≤5%)"]
# )
#
# if change_type == "Major management change":
#     recommended_rep = 2
# else:
#     recommended_rep = 4 if expected_effect == "Small (≤5%)" else 3
#
# replicates = st.number_input(
#     "Number of replicates (blocks)",
#     min_value=1,
#     value=recommended_rep
# )
#
# st.info(f"Recommended replicates: {recommended_rep}")
#
# if replicates == 1:
#     st.warning(
#         "⚠ Unreplicated trials are exploratory only. "
#         "Never adopt whole-farm practices based on them."
#     )
# def draw_experiment_layout(treatments, replicates, samples_per_plot=3):
#     control = [t["name"] for t in treatments if t["is_control"]][0]
#     others = [t["name"] for t in treatments if not t["is_control"]]
#     treatment_order = [control] + others
#
#     fig, ax = plt.subplots(figsize=(6, 8))
#
#     # Crop field
#     ax.add_patch(
#         patches.Rectangle((0, 0), 10, 20, color="#0E5A73")
#     )
#
#     # Experiment area
#     ax.add_patch(
#         patches.Rectangle((3, 5), 4, 10, color="#A6DCEF")
#     )
#
#     plot_width = 4 / len(treatment_order)
#     block_height = 10 / replicates
#
#     for b in range(replicates):
#         block_y = 5 + b * block_height
#         block_treatments = treatment_order.copy()
#         np.random.shuffle(block_treatments)
#
#         for i, tr in enumerate(block_treatments):
#             x = 3 + i * plot_width
#             y = block_y
#
#             # Plot
#             ax.add_patch(
#                 patches.Rectangle(
#                     (x, y),
#                     plot_width * 0.9,
#                     block_height * 0.9,
#                     edgecolor="black",
#                     facecolor="#B6E3A8"
#                 )
#             )
#
#             ax.text(
#                 x + plot_width / 2,
#                 y + block_height * 0.75,
#                 tr,
#                 ha="center",
#                 va="center",
#                 fontsize=9,
#                 weight="bold"
#             )
#
#             # Samples
#             for s in range(samples_per_plot):
#                 ax.plot(
#                     x + plot_width / 2,
#                     y + block_height * (0.2 + s * 0.2),
#                     marker="o",
#                     color="#0A7F2E"
#                 )
#
#     ax.set_xlim(0, 10)
#     ax.set_ylim(0, 20)
#     ax.axis("off")
#
#     return fig
#
# # =========================
# # D. Plot geometry
# # =========================
# st.header("D. Plot geometry")
# fig = draw_experiment_layout(treatments, replicates)
# st.pyplot(fig)
# plot_length = st.number_input("Plot length (meters)", value=300)
# application_width = st.number_input("Application equipment width (meters)", value=24)
# harvest_width = st.number_input("Harvest equipment width (meters)", value=8)
# buffer_width = st.number_input("Buffer width (meters)", value=2)
#
# # =========================
# # E. Generate design
# # =========================
# st.header("E. Generate experiment design")
#
# if st.button("Generate randomized design"):
#     plots = []
#     plot_counter = 1
#
#     for block in range(1, replicates + 1):
#         block_treatments = [t["name"] for t in treatments]
#         random.shuffle(block_treatments)
#
#         for pos, tr in enumerate(block_treatments, start=1):
#             plots.append(
#                 {
#                     "plot_id": f"P{plot_counter}",
#                     "block": block,
#                     "treatment": tr,
#                     "position_in_block": pos,
#                     "plot_length_m": plot_length,
#                     "application_width_m": application_width,
#                     "harvest_width_m": harvest_width,
#                     "buffer_width_m": buffer_width
#                 }
#             )
#             plot_counter += 1
#
#     layout_df = pd.DataFrame(plots)
#
#     st.subheader("Plot layout (RCBD)")
#     st.dataframe(layout_df, use_container_width=True)
#
#     # =========================
#     # F. Templates
#     # =========================
#     st.header("F. Export templates")
#
#     fieldbook_df = layout_df[["plot_id", "block", "treatment"]].copy()
#     fieldbook_df["date"] = ""
#     fieldbook_df["observation"] = ""
#     fieldbook_df["value"] = ""
#     fieldbook_df["unit"] = ""
#     fieldbook_df["notes"] = ""
#
#     management_df = layout_df[["plot_id", "treatment"]].copy()
#     management_df["date"] = ""
#     management_df["event_type"] = ""
#     management_df["product"] = ""
#     management_df["rate"] = ""
#     management_df["unit"] = ""
#
#     yield_df = layout_df[["plot_id", "treatment"]].copy()
#     yield_df["harvested_width_m"] = ""
#     yield_df["harvested_length_m"] = ""
#     yield_df["weight_kg"] = ""
#     yield_df["moisture_pct"] = ""
#     yield_df["yield_kg_ha"] = ""
#
#     st.download_button(
#         "⬇ Download plot layout",
#         layout_df.to_csv(index=False),
#         file_name="plot_layout.csv"
#     )
#
#     st.download_button(
#         "⬇ Download fieldbook",
#         fieldbook_df.to_csv(index=False),
#         file_name="fieldbook.csv"
#     )
#
#     st.download_button(
#         "⬇ Download management log",
#         management_df.to_csv(index=False),
#         file_name="management_log.csv"
#     )
#
#     st.download_button(
#         "⬇ Download yield template",
#         yield_df.to_csv(index=False),
#         file_name="yield_template.csv"
#     )
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Experiment & Sampling ID Generator", layout="wide")

st.title("🧪 Experiment & Sampling Design Generator")

# =========================
# A. Project-level inputs
# =========================
st.header("A. Project information")

col1, col2, col3 = st.columns(3)

with col1:
    country = st.selectbox(
        "Country code",
        ["NL", "IR", "FR", "SP"]
    )

with col2:
    round_id = st.selectbox(
        "Round",
        ["RR1", "RR2", "RR3"]
    )

with col3:
    app_order = st.number_input(
        "Application order",
        min_value=1,
        max_value=99,
        value=1
    )

project_id = f"{country}-{round_id}-APP{app_order:02d}"
st.success(f"Project ID: {project_id}")

# =========================
# B. Experimental design
# =========================
st.header("B. Experimental design")

col4, col5 = st.columns(2)

with col4:
    n_blocks = st.number_input(
        "Number of blocks (replicates)",
        min_value=1,
        max_value=10,
        value=3
    )

with col5:
    n_treatments = st.number_input(
        "Number of treatments per block (excluding control)",
        min_value=1,
        max_value=5,
        value=2
    )

# =========================
# C. Sampling design
# =========================
st.header("C. Sampling design")

col6, col7, col8 = st.columns(3)

with col6:
    samples_per_plot = st.number_input(
        "Samples per plot",
        min_value=1,
        max_value=10,
        value=1
    )

with col7:
    depth_from = st.number_input(
        "Layer depth from (cm)",
        value=0
    )

with col8:
    depth_to = st.number_input(
        "Layer depth to (cm)",
        value=20
    )

# =========================
# D. Generate design
# =========================
st.header("D. Generate")

if st.button("🚀 Generate experiment & sampling plan"):
    records = []

    for block in range(1, n_blocks + 1):
        # Control plot
        control_plot_id = f"{project_id}-C{block}"

        for s in range(1, samples_per_plot + 1):
            sample_id = f"{control_plot_id}-S{s}"
            layer_id = f"{sample_id}-L{depth_from}-{depth_to}"

            records.append({
                "project_id": project_id,
                "block": block,
                "plot_id": control_plot_id,
                "plot_role": "control",
                "treatment_code": "C",
                "sample_id": sample_id,
                "layer_id": layer_id,
                "depth_from_cm": depth_from,
                "depth_to_cm": depth_to,
                "purpose_id": "",
                "practice": "",
                "treatment_description": "",
                "sample_date": "",
                "sample_handling": "",
                "sample_location": ""
            })

        # Treatment plots
        for t in range(1, n_treatments + 1):
            treatment_plot_id = f"{project_id}-T{block}-{t}"

            for s in range(1, samples_per_plot + 1):
                sample_id = f"{treatment_plot_id}-S{s}"
                layer_id = f"{sample_id}-L{depth_from}-{depth_to}"

                records.append({
                    "project_id": project_id,
                    "block": block,
                    "plot_id": treatment_plot_id,
                    "plot_role": "treatment",
                    "treatment_code": f"T{t}",
                    "sample_id": sample_id,
                    "layer_id": layer_id,
                    "depth_from_cm": depth_from,
                    "depth_to_cm": depth_to,
                    "purpose_id": "",
                    "practice": "",
                    "treatment_description": "",
                    "sample_date": "",
                    "sample_handling": "",
                    "sample_location": ""
                })

    df = pd.DataFrame(records)

    st.subheader("Generated experiment & sampling table")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download CSV template",
        df.to_csv(index=False),
        file_name=f"{project_id}_sampling_plan.csv"
    )
