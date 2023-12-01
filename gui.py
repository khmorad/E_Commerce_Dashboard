import matplotlib.pyplot as plt
import mplcursors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import pandas as pd
from data import process_walmart_data_by_keyword
import seaborn as sns

df = pd.read_csv("walmart_data.csv")
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = tk.Tk()

window.geometry("999x551")
window.configure(bg="#FFFFFF")


canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=551,
    width=999,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)
canvas.pack()


def print_entry_content():
    content = entry_1.get()  # Get the text from entry_1
    print("Entry Content:", content)


def create_matplotlib_plots():
    selected_columns = ["item_price", "avg_rating", "reviews"]
    subset_df = df[selected_columns]
    cor_matrix = subset_df.corr()

    # Create a heatmap of the correlation matrix
    fig_heatmap, ax_heatmap = plt.subplots(figsize=(4, 4))
    sns.heatmap(
        cor_matrix,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5,
        ax=ax_heatmap,
        annot_kws={"size": 7},
    )
    plt.title("Correlation Matrix Heatmap", fontsize=10)
    ax_heatmap.xaxis.label.set_size(7)
    ax_heatmap.yaxis.label.set_size(7)

    # Adjust layout to give more space for labels

    ax_heatmap.set_facecolor("#FAFAFA")

    # Convert the heatmap to a Tkinter-compatible canvas
    canvas_heatmap = FigureCanvasTkAgg(fig_heatmap, master=window)
    canvas_heatmap.draw()

    # Get the dimensions of the rectangle for heatmap placement
    heatmap_rect_x1, heatmap_rect_y1, heatmap_rect_x2, heatmap_rect_y2 = (
        316.0,
        148.0,
        529.0,
        332.0,
    )

    # Calculate the width and height of the heatmap rectangle
    heatmap_rect_width = heatmap_rect_x2 - heatmap_rect_x1
    heatmap_rect_height = heatmap_rect_y2 - heatmap_rect_y1

    # Embed the heatmap within the tkinter canvas (place it within the desired rectangle)
    heatmap_widget = canvas_heatmap.get_tk_widget()
    heatmap_widget.place(
        x=heatmap_rect_x1,
        y=heatmap_rect_y1,
        width=heatmap_rect_width,
        height=heatmap_rect_height,
    )
    avgPriceBar = df.groupby("seller_name")["item_price"].mean()
    topAvgPriceBar = avgPriceBar.sort_values(ascending=False).head(10)

    company_mapping = {}
    for i, company in enumerate(topAvgPriceBar.index):
        new_label = f"c{i + 1}"
        company_mapping[company] = new_label

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    bars = ax2.bar(
        [company_mapping[company] for company in topAvgPriceBar.index],
        topAvgPriceBar.values,
        color="lightblue",
    )
    ax2.set_xlabel("Seller Name")
    ax2.set_ylabel("Average Price")
    ax2.set_title("Top 10 Average Prices Based on Seller")
    ax2.set_facecolor("#FAFAFA")

    def bar_label(sel):
        ind = sel.target.index
        if ind < len(topAvgPriceBar):
            seller_name = topAvgPriceBar.index[ind]
            sel.annotation.set_text(f"{bars[ind].get_height()} - {seller_name}")
            sel.annotation.get_bbox_patch().set(fc="white", alpha=1.0)
            sel.annotation.get_bbox_patch().set(edgecolor="black", linewidth=1)

            def on_leave(event):
                sel.annotation.set_visible(False)
                canvas2.draw()

            canvas2.mpl_connect("axes_leave_event", on_leave)

    mplcursors.cursor(bars, hover=True).connect("add", bar_label)

    canvas2 = FigureCanvasTkAgg(fig2, master=window)
    canvas2.draw()

    bar_rect_x1, bar_rect_y1, bar_rect_x2, bar_rect_y2 = 553.0, 149.0, 969.0, 332.0
    bar_rect_width = bar_rect_x2 - bar_rect_x1
    bar_rect_height = bar_rect_y2 - bar_rect_y1

    bar_plot_widget = canvas2.get_tk_widget()
    bar_plot_widget.place(
        x=bar_rect_x1, y=bar_rect_y1, width=bar_rect_width, height=bar_rect_height
    )
    avgPriceBar = df.groupby("seller_name")["item_price"].mean()
    topAvgPriceBar = avgPriceBar.sort_values(ascending=False).head(10)  # Select top 5

    # Create a pie chart for the top 5 average prices based on sellers
    fig_pie, ax_pie = plt.subplots(figsize=(4, 4))

    # Prepare data for the pie chart
    sizes = topAvgPriceBar.values
    labels = topAvgPriceBar.index

    ax_pie.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",  # Display percentage format with 1 decimal place
        startangle=140,
        textprops={"fontsize": 5.2},
    )
    ax_pie.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle
    ax_pie.set_title("Avg Prices by Seller")  # Set the title for the pie chart

    # Convert Matplotlib pie chart to Tkinter-compatible canvas
    canvas_pie = FigureCanvasTkAgg(fig_pie, master=window)
    canvas_pie.draw()

    # Get the dimensions of the rectangle for pie chart placement
    pie_rect_x1, pie_rect_y1, pie_rect_x2, pie_rect_y2 = 318.0, 350.0, 531.0, 524.0

    # Calculate the width and height of the pie chart rectangle
    pie_rect_width = pie_rect_x2 - pie_rect_x1
    pie_rect_height = pie_rect_y2 - pie_rect_y1

    # Embed the pie chart within the tkinter canvas (place it within the desired rectangle)
    pie_chart_widget = canvas_pie.get_tk_widget()
    pie_chart_widget.place(
        x=pie_rect_x1, y=pie_rect_y1, width=pie_rect_width, height=pie_rect_height
    )
    # Create a sample scatter plot
    fig_scatter, ax_scatter = plt.subplots(figsize=(4, 4))
    ax_scatter.scatter(df["item_price"], df["reviews"])  # Sample scatter plot
    ax_scatter.set_xlabel("X-axis")
    ax_scatter.set_ylabel("Y-axis")
    ax_scatter.set_title("Sample Scatter Plot")
    ax_scatter.set_facecolor("#FAFAFA")  # Set plot background color

    # Convert Matplotlib scatter plot to Tkinter-compatible canvas
    canvas_scatter = FigureCanvasTkAgg(fig_scatter, master=window)
    canvas_scatter.draw()

    # Get the dimensions of the rectangle for scatter plot placement
    scatter_rect_x1, scatter_rect_y1, scatter_rect_x2, scatter_rect_y2 = (
        555.0,
        348.0,
        744.0,
        522.0,
    )

    # Calculate the width and height of the scatter plot rectangle
    scatter_rect_width = scatter_rect_x2 - scatter_rect_x1
    scatter_rect_height = scatter_rect_y2 - scatter_rect_y1

    # Embed the scatter plot within the tkinter canvas (place it within the desired rectangle)
    scatter_plot_widget = canvas_scatter.get_tk_widget()
    scatter_plot_widget.place(
        x=scatter_rect_x1,
        y=scatter_rect_y1,
        width=scatter_rect_width,
        height=scatter_rect_height,
    )

    top_sellers = df["seller_name"].value_counts().nlargest(3).index
    df_top_sellers = df[df["seller_name"].isin(top_sellers)]

    fig_boxplot, ax_boxplot = plt.subplots(figsize=(4, 4))
    sns.boxplot(x="seller_name", y="item_price", data=df_top_sellers, ax=ax_boxplot)
    plt.title("Prices for Top 3 Sellers")
    ax_boxplot.set_xlabel("Seller Name")
    ax_boxplot.set_ylabel("Item Price")
    ax_boxplot.set_facecolor("#FAFAFA")  # Set plot background color

    # Mapping company names to c1, c2, c3
    company_mapping = {company: f"c{i + 1}" for i, company in enumerate(top_sellers)}

    # Update x-axis labels to show c1, c2, c3 instead of actual seller names
    seller_labels = [
        company_mapping[seller] for seller in df_top_sellers["seller_name"].unique()
    ]
    ax_boxplot.set_xticklabels(seller_labels)

    # Convert Matplotlib boxplot to Tkinter-compatible canvas
    canvas_boxplot = FigureCanvasTkAgg(fig_boxplot, master=window)
    canvas_boxplot.draw()

    # Get the dimensions of the rectangle for boxplot placement
    boxplot_rect_x1, boxplot_rect_y1, boxplot_rect_x2, boxplot_rect_y2 = (
        778.0,
        347.0,
        967.0,
        521.0,
    )

    # Calculate the width and height of the boxplot rectangle
    boxplot_rect_width = boxplot_rect_x2 - boxplot_rect_x1
    boxplot_rect_height = boxplot_rect_y2 - boxplot_rect_y1

    # Embed the boxplot within the tkinter canvas (place it within the desired rectangle)
    boxplot_widget = canvas_boxplot.get_tk_widget()
    boxplot_widget.place(
        x=boxplot_rect_x1,
        y=boxplot_rect_y1,
        width=boxplot_rect_width,
        height=boxplot_rect_height,
    )

    # Mapping company names to c1, c2, c3
    company_mapping = {company: f"c{i + 1}" for i, company in enumerate(top_sellers)}

    def bar_label(sel):
        ind = sel.target.index
        if ind < len(top_sellers):
            seller_name = top_sellers[ind]
            c_name = company_mapping[seller_name]
            sel.annotation.set_text(
                f"{bars[ind].get_height()} - {c_name} ({seller_name})"
            )
            sel.annotation.get_bbox_patch().set(fc="white", alpha=1.0)
            sel.annotation.get_bbox_patch().set(edgecolor="black", linewidth=1)

            def on_leave(event):
                sel.annotation.set_visible(False)
                canvas_boxplot.draw()

            canvas_boxplot.mpl_connect("axes_leave_event", on_leave)

    bars = ax_boxplot.get_children()[1:]  # Get the bars in the boxplot

    mplcursors.cursor(bars, hover=True).connect("add", bar_label)


def display_dataframe(window, dataframe, x1, y1, x2, y2):
    frame = ttk.Frame(window)
    frame.place(x=x1, y=y1, width=(x2 - x1), height=(y2 - y1))

    tree = ttk.Treeview(frame)

    # Get column names including the index
    columns = list(dataframe.columns)

    # Rename the index column
    tree["columns"] = columns[1:]

    # Set headings for columns and adjust column widths
    for col in columns[1:]:
        tree.heading(col, text=col)
        tree.column(col, width=52)  # Set the width as desired, e.g., 100 pixels
    # Set width for the first column (index column)
    tree.column("#0", width=0)  # Set the width as desired
    # Insert data rows into the treeview
    for idx, row in dataframe.iterrows():
        values = list(row)[1:]  # Exclude the index value in each row
        tree.insert("", "end", text=idx, values=values)  # Provide the index value here

    tree.pack(fill="both", expand=True)


canvas.place(x=0, y=0)
canvas.create_rectangle(2.0, 46.0, 267.0, 551.0, fill="#C9C9C9", outline="")

canvas.create_rectangle(1.0, 47.0, 266.0, 552.0, fill="#F9F9F9", outline="")

canvas.create_rectangle(0.0, 3.0, 999.0, 49.0, fill="#F0F0F0", outline="")

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(543.5, 98.5, image=entry_image_1)
entry_1 = Entry(bd=0, bg="#D1F1EB", fg="#000716", highlightthickness=0)
entry_1.place(x=319.0, y=83.0, width=449.0, height=29.0)

canvas.create_rectangle(0.0, 0.0, 999.0, 46.0, fill="#38BBD8", outline="")

canvas.create_rectangle(9.0, 4.0, 58.0, 43.0, fill="#FFEBCD", outline="")

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(33.0, 23.0, image=image_image_1)

canvas.create_text(
    72.0,
    11.0,
    anchor="nw",
    text="E-Commerence DataAnalysis Dashboard\n",
    fill="#21272A",
    font=("Righteous Regular", 22 * -1),
)

canvas.create_rectangle(318.0, 150.0, 531.0, 334.0, fill="#C9C9C9", outline="")

canvas.create_rectangle(320.0, 352.0, 533.0, 526.0, fill="#C9C9C9", outline="")

canvas.create_rectangle(557.0, 350.0, 746.0, 524.0, fill="#C9C9C9", outline="")

canvas.create_rectangle(780.0, 349.0, 969.0, 523.0, fill="#C9C9C9", outline="")

canvas.create_rectangle(316.0, 148.0, 529.0, 332.0, fill="#F9F9F9", outline="")

canvas.create_rectangle(320.0, 351.0, 533.0, 525.0, fill="#C9C9C9", outline="")

canvas.create_rectangle(557.0, 349.0, 746.0, 523.0, fill="#C9C9C9", outline="")

canvas.create_rectangle(780.0, 348.0, 969.0, 522.0, fill="#C9C9C9", outline="")

canvas.create_rectangle(318.0, 350.0, 531.0, 524.0, fill="#F9F9F9", outline="")

canvas.create_rectangle(555.0, 348.0, 744.0, 522.0, fill="#F9F9F9", outline="")

canvas.create_rectangle(778.0, 347.0, 967.0, 521.0, fill="#F9F9F9", outline="")

canvas.create_rectangle(318.0, 350.0, 531.0, 524.0, fill="#F9F9F9", outline="")

canvas.create_rectangle(555.0, 348.0, 744.0, 522.0, fill="#F9F9F9", outline="")

canvas.create_rectangle(778.0, 347.0, 967.0, 521.0, fill="#F9F9F9", outline="")

canvas.create_rectangle(555.0, 151.0, 971.0, 334.0, fill="#C2C2C2", outline="")

canvas.create_rectangle(553.0, 149.0, 969.0, 332.0, fill="#F9F9F9", outline="")

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=print_entry_content,
    relief="flat",
)
button_1.place(x=777.0, y=83.0, width=56.0, height=31.0)
window.resizable(False, False)
create_matplotlib_plots()


# Adjust the rectangle dimensions to fit your desired location
display_dataframe(window, df, 2.0, 47.0, 266.0, 552.0)

window.mainloop()
