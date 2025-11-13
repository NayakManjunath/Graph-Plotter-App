import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

st.set_page_config(page_title="Advanced Graph Plotter", layout="wide")

st.title("📊 Advanced Graph Plotter App")
st.write("Choose how you want to provide the data:")

# Input Method
input_method = st.radio(
    "Select Input Method",
    ["Manual Entry", "Upload CSV"]
)

df = None

# Manual Entry
if input_method == "Manual Entry":
    st.subheader("Enter Data Manually")

    x_values = st.text_input("Enter X values (comma separated)")
    y_values = st.text_input("Enter Y values (comma separated)")

    if x_values and y_values:
        try:
            x_list = [float(i.strip()) for i in x_values.split(",")]
            y_list = [float(i.strip()) for i in y_values.split(",")]

            if len(x_list) != len(y_list):
                st.error("X and Y must have the same number of values.")
            else:
                df = pd.DataFrame({"X": x_list, "Y": y_list})

        except:
            st.error("Please enter valid numeric values.")


# CSV Upload
else:
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            df = df.dropna()

            numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

            if len(numeric_cols) == 0:
                st.error("CSV must contain at least one numeric column.")
                df = None
            else:
                st.write("### Select Columns for Plotting")

                col1, col2 = st.columns(2)
                with col1:
                    x_col = st.selectbox("Select X-axis", numeric_cols)
                with col2:
                    y_col = st.selectbox("Select Y-axis", numeric_cols)

                df = df[[x_col, y_col]].dropna()
                df.columns = ["X", "Y"]

        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            df = None


# Plotting Section
if df is not None:

    st.subheader("Select Plot Type")

    plot_type = st.selectbox(
        "Choose Plot Type",
        [
            "Line Plot",
            "Bar Plot",
            "Scatter Plot",
            "Histogram",
            "Box Plot",
            "Area Plot",
            "Pie Chart",
            "KDE Plot (Density)",
            "Heatmap"
        ]
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    # Line Plot
    if plot_type == "Line Plot":
        ax.plot(df["X"], df["Y"], marker="o", linestyle="-")

    # Bar Plot
    elif plot_type == "Bar Plot":
        ax.bar(df["X"], df["Y"])

    # Scatter Plot
    elif plot_type == "Scatter Plot":
        ax.scatter(df["X"], df["Y"])

    # Histogram
    elif plot_type == "Histogram":
        ax.hist(df["Y"], bins=20, edgecolor="black")

    # Box Plot
    elif plot_type == "Box Plot":
        ax.boxplot(df["Y"])

    # Area Plot
    elif plot_type == "Area Plot":
        ax.fill_between(df["X"], df["Y"], alpha=0.4)

    # Pie Chart
    elif plot_type == "Pie Chart":
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(df["Y"], labels=df["X"], autopct="%1.1f%%")

    # KDE Plot
    elif plot_type == "KDE Plot (Density)":
        sns.kdeplot(df["Y"], ax=ax, fill=True)

    # Heatmap (works only if more than 2 numeric columns exist)
    elif plot_type == "Heatmap":
        try:
            uploaded_file.seek(0)
            full_df = pd.read_csv(uploaded_file).dropna()
            full_numeric = full_df.select_dtypes(include=["number"])

            if full_numeric.shape[1] < 2:
                st.error("Heatmap requires at least 2 numeric columns.")
            else:
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.heatmap(full_numeric.corr(), annot=True, cmap="coolwarm", ax=ax)

        except:
            st.error("Heatmap requires CSV input.")

    ax.set_title(plot_type)
    ax.grid(True)

    # Show chart
    st.pyplot(fig)


    # Download Button
    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)

    st.download_button(
        label="📥 Download Graph Image",
        data=buffer,
        file_name="graph.png",
        mime="image/png"
    )
