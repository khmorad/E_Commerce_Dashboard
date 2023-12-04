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

# program starts with with existing csv file from previous search
# currently holding the data for Books item
df = pd.read_csv("walmart_data.csv")
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = tk.Tk()
window.title("E-Commerence DataAnalysis Dashboard")
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


# this is the function that make the search button work
# which will run the create_matplotlib_plots function again to update the plots
# this works i just dont want to waste api calls
def print_entry_content():
    # Get the text from entry_1 input box
    content = input_box.get()

    # creates a new datafram variable which first gets the searched keyword from the api
    # based on the searched keyword
    new_df = process_walmart_data_by_keyword(
        content
    )  # Get new data based on the item name

    # update the global DataFrame 'df' with the new data
    # because the dataframe is being used in other functions
    global df
    df = new_df

    # Recreate the entire plotting
    create_matplotlib_plots()
    # also update the datarame table on located on the left side of the dashboard
    display_dataframe(window, df, 2.0, 47.0, 266.0, 552.0)
    print("Entry Content:", content)


def create_matplotlib_plots():
    # ************************************heatmap correlation matrix****************************************
    selected_columns = ["item_price", "avg_rating", "reviews"]
    subset_df = df[selected_columns]
    cor_matrix = subset_df.corr()

    # heatmap of the correlation matrix
    fig_heatmap, ax_heatmap = plt.subplots(figsize=(4, 4))
    sns.heatmap(
        cor_matrix,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5,
        ax=ax_heatmap,
        # this size correlated to the values inside the heatmap
        annot_kws={"size": 7},
    )
    plt.title("Correlation Matrix Heatmap", fontsize=9)
    # using .tick_params to make the font of x and y axist to appropriate size
    # FIXME: small window size is a problem
    ax_heatmap.tick_params(axis="x", labelsize=6)
    ax_heatmap.tick_params(axis="y", labelsize=6)

    # set the color fo plot to match the background color fo the window
    ax_heatmap.set_facecolor("#FAFAFA")

    # now converting Matplotlib plot to Tkinter-compatible canvas using FigureCanvasTkAgg
    canvas_heatmap = FigureCanvasTkAgg(fig_heatmap, master=window)
    canvas_heatmap.draw()

    # Get the dimensions of the rectangle where the heap map will get located in
    heatmap_x1 = 316.0
    heatmap_y1 = 148.0
    heatmap_x2 = 539.0
    heatmap_y2 = 332.0

    # width of the heatmap rectangle
    heatmap_width = heatmap_x2 - heatmap_x1
    # height of the heatmap rectangle
    heatmap_height = heatmap_y2 - heatmap_y1

    # place heatmap within the tkinter canvas (place it within the desired rectangle)
    heatmap_widget = canvas_heatmap.get_tk_widget()
    heatmap_widget.place(
        x=heatmap_x1,
        y=heatmap_y1,
        width=heatmap_width,
        height=heatmap_height,
    )

    # *********************************bar chart avg based on seller******************************************************
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
    ax2.set_xlabel("Seller Name", fontsize=7)
    ax2.set_ylabel("Average Price")
    ax2.set_title("Top 10 Average Prices Based on Seller", fontsize=10)
    ax2.set_facecolor("#FAFAFA")
    # using .tick_params to make the font of x and y axist to appropriate size
    ax2.tick_params(axis="x", labelsize=8)
    ax2.tick_params(axis="y", labelsize=6)

    def bar_label(sel):
        ind = sel.target.index
        if ind < len(topAvgPriceBar):
            seller_name = topAvgPriceBar.index[ind]
            sel.annotation.set_text(f"${bars[ind].get_height():.2f} - {seller_name}")
            sel.annotation.get_bbox_patch().set(fc="white", alpha=1.0)
            sel.annotation.get_bbox_patch().set(edgecolor="black", linewidth=1)

            def on_leave(event):
                sel.annotation.set_visible(False)
                canvas2.draw()

            canvas2.mpl_connect("axes_leave_event", on_leave)

    # using mplcursors library so i can make the bar plot more interactive
    # .cursor method and .add method so trigger the bar_label function onece the
    # mouse is hover over the bar
    mplcursors.cursor(bars, hover=True).connect("add", bar_label)

    canvas2 = FigureCanvasTkAgg(fig2, master=window)
    canvas2.draw()

    # writing the exact dimensions of the rectangle for bar chart placement
    bar_x1 = 553.0
    bar_y1 = 149.0
    bar_x2 = 969.0
    bar_y2 = 332.0

    # calc the bar width
    bar_width = bar_x2 - bar_x1
    # calc the bar height
    bar_height = bar_y2 - bar_y1

    bar_graph = canvas2.get_tk_widget()
    bar_graph.place(x=bar_x1, y=bar_y1, width=bar_width, height=bar_height)
    # *********************************pie chart avg based on seller******************************************************
    # create a pie chart for the top 5 average prices based on sellers
    fig_pie, ax_pie = plt.subplots(figsize=(4, 4))

    # Prepare data for the pie chart
    sizes = topAvgPriceBar.values
    labels = topAvgPriceBar.index

    # this is where design the pie chart
    # use autopct to set the percentage format to 1 decimal place
    # display percentage format with 1 decimal place
    ax_pie.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
        textprops={"fontsize": 5.2},
    )
    # equal aspect ratio ensures that pie is drawn as a circle
    ax_pie.axis("equal")
    # Set the title for the pie chart and change the font size to 10 so it would fit the
    # rectangle for the graph
    ax_pie.set_title("Avg Prices by Seller", fontsize=10)

    # Convert Matplotlib pie chart to Tkinter-compatible canvas
    canvas_pie = FigureCanvasTkAgg(fig_pie, master=window)
    canvas_pie.draw()

    # Get the dimensions of the rectangle for pie chart placement
    pie_x1 = 318.0
    pie_y1 = 350.0
    pie_x2 = 541.0
    pie_y2 = 524.0

    # calculate the of the pie chart rectangle
    pie_width = pie_x2 - pie_x1
    # calcualte height of the pie chart rectangle
    pie_height = pie_y2 - pie_y1

    # now use the calculated width and height to
    # Embed the pie chart within the tkinter canvas
    pie_widget = canvas_pie.get_tk_widget()
    pie_widget.place(x=pie_x1, y=pie_y1, width=pie_width, height=pie_height)
    # *********************************scatter plot price vs number of reviews**************************************
    fig_scatter, ax_scatter = plt.subplots(figsize=(1, 1))
    ax_scatter.scatter(df["item_price"], df["reviews"])  # Sample scatter plot
    ax_scatter.set_xlabel("X-axis")
    ax_scatter.set_ylabel("Y-axis")
    ax_scatter.set_title("Price Vs Number of Reviews", fontsize=9)
    # using setfacecolor to make the plot match the background color of the window
    # which is failing miserablely :(
    ax_scatter.set_facecolor("#FAFAFA")  # Set plot background color
    # using .tick_params to make the font of x and y axist to appropriate size
    ax_scatter.tick_params(axis="x", labelsize=7)
    ax_scatter.tick_params(axis="y", labelsize=6)

    # now converting Matplotlib plot to Tkinter-compatible canvas using FigureCanvasTkAgg
    canvas_scatter = FigureCanvasTkAgg(fig_scatter, master=window)
    canvas_scatter.draw()

    # get the dimensions of the rectangle for scatter plot placement
    scatter_x1 = 555.0
    scatter_y1 = 348.0
    scatter_x2 = 744.0
    scatter_y2 = 522.0

    # calculate the width by subtracting the x-coordinates
    scatter_width = scatter_x2 - scatter_x1

    # using scatter_y2 - scatter_y1 to get the height of the rectangle
    scatter_rect_height = scatter_y2 - scatter_y1

    # embed the scatter plot within the tkinter canvas (place it within the desired rectangle)
    scatter_plot_widget = canvas_scatter.get_tk_widget()
    scatter_plot_widget.place(
        x=scatter_x1,
        y=scatter_y1,
        width=scatter_width,
        height=scatter_rect_height,
    )

    top_sellers = df["seller_name"].value_counts().nlargest(2).index
    df_top_sellers = df[df["seller_name"].isin(top_sellers)]

    fig_boxplot, ax_boxplot = plt.subplots(figsize=(4, 4))
    sns.boxplot(x="seller_name", y="item_price", data=df_top_sellers, ax=ax_boxplot)
    plt.title("Prices for Top 2 Sellers", fontsize=10)
    ax_boxplot.set_xlabel("Seller Name")
    ax_boxplot.set_ylabel("Item Price")
    ax_boxplot.set_facecolor("#FAFAFA")
    # change the font size for both x and y axis to appropriate size
    ax_boxplot.tick_params(axis="x", labelsize=6)
    ax_boxplot.tick_params(axis="y", labelsize=8)
    # now converting Matplotlib plot to Tkinter-compatible canvas using FigureCanvasTkAgg
    canvas_boxplot = FigureCanvasTkAgg(fig_boxplot, master=window)
    canvas_boxplot.draw()

    # Get the dimensions of the rectangle for boxplot placement
    boxplot_x1 = 778.0
    boxplot_y1 = 347.0
    boxplot_x2 = 967.0
    boxplot_y2 = 521.0

    # Calculate the width  of the boxplot rectangle
    boxplot_rect_width = boxplot_x2 - boxplot_x1
    # calculate height for boxplot rectangle
    boxplot_rect_height = boxplot_y2 - boxplot_y1

    # Embed the boxplot within the tkinter canvas (place it within the desired rectangle)
    boxplot_widget = canvas_boxplot.get_tk_widget()
    boxplot_widget.place(
        x=boxplot_x1,
        y=boxplot_y1,
        width=boxplot_rect_width,
        height=boxplot_rect_height,
    )

    # Set actual seller names as x-axis tick labels
    seller_labels = df_top_sellers["seller_name"].unique()
    ax_boxplot.set_xticklabels(seller_labels)


# Sthis method displays the dataframe on the left side of the dashboard containing all the data
# from the csv file retreived from the api call
def display_dataframe(window, dataframe, x1, y1, x2, y2):
    frame = ttk.Frame(window)
    frame.place(x=x1, y=y1, width=(x2 - x1), height=(y2 - y1))
    #  create a treeview widget
    tree = ttk.Treeview(frame)
    columns = list(dataframe.columns)
    tree["columns"] = columns[1:]
    # format the columns of the treeview
    # this is where loop is used to create the columns of the table
    # based on the columns in the dataframe
    for col in columns[1:]:
        tree.heading(col, text=col)
        # setting the width of the columns to appropriate
        # size compared to the window size
        tree.column(col, width=52)
    # Set width for the first column to 0 because i didnt want to display the index values
    tree.column("#0", width=0)
    # Insert data rows into the treeview and exclude the index value in each row
    for idx, row in dataframe.iterrows():
        values = list(row)[1:]
        # Provide the index value as the first value in each row
        tree.insert("", "end", text=idx, values=values)

    tree.pack(fill="both", expand=True)


canvas.place(x=0, y=0)

# window containing the dataframe on the left side of the dashboard
canvas.create_rectangle(1.0, 47.0, 266.0, 552.0, fill="#F9F9F9", outline="")
canvas.create_rectangle(2.0, 46.0, 267.0, 551.0, fill="#C9C9C9", outline="")


canvas.create_rectangle(0.0, 3.0, 999.0, 49.0, fill="#F0F0F0", outline="")

# use the image included in the assets folder
entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(543.5, 98.5, image=entry_image_1)
input_box = Entry(bd=0, bg="#D1F1EB", fg="#000716", highlightthickness=0)
input_box.place(x=319.0, y=83.0, width=449.0, height=29.0)

canvas.create_rectangle(0.0, 0.0, 999.0, 46.0, fill="#38BBD8", outline="")

canvas.create_rectangle(9.0, 4.0, 58.0, 43.0, fill="#FFEBCD", outline="")

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(33.0, 23.0, image=image_image_1)


# the title of the dashboard
canvas.create_text(
    72.0,
    11.0,
    anchor="nw",
    text="E-Commerence DataAnalysis Dashboard\n",
    fill="#21272A",
    font=("Righteous Regular", 22 * -1),
)


# all the rectangles created to create a dashboard
# the boxed are created by creating a rectangle with a lighter color (#F9F9F9)
# shadows boxes are manually created by creating a rectangle with a darker color (#C9C9C9)


canvas.create_rectangle(320.0, 352.0, 533.0, 526.0, fill="#C9C9C9", outline="")
canvas.create_rectangle(557.0, 350.0, 746.0, 524.0, fill="#C9C9C9", outline="")
canvas.create_rectangle(780.0, 349.0, 969.0, 523.0, fill="#C9C9C9", outline="")

# top left box (heatmap)
canvas.create_rectangle(316.0, 148.0, 539.0, 332.0, fill="#F9F9F9", outline="")

canvas.create_rectangle(318.0, 150.0, 541.0, 334.0, fill="#C9C9C9", outline="")

# place bottom left box of dashboard (pie chart)
canvas.create_rectangle(318.0, 350.0, 541.0, 524.0, fill="#F9F9F9", outline="")

canvas.create_rectangle(320.0, 351.0, 543.0, 525.0, fill="#C9C9C9", outline="")

canvas.create_rectangle(555.0, 348.0, 744.0, 522.0, fill="#F9F9F9", outline="")
canvas.create_rectangle(557.0, 349.0, 746.0, 523.0, fill="#C9C9C9", outline="")

canvas.create_rectangle(780.0, 348.0, 969.0, 522.0, fill="#C9C9C9", outline="")
canvas.create_rectangle(778.0, 347.0, 967.0, 521.0, fill="#F9F9F9", outline="")


canvas.create_rectangle(555.0, 348.0, 744.0, 522.0, fill="#F9F9F9", outline="")

canvas.create_rectangle(778.0, 347.0, 967.0, 521.0, fill="#F9F9F9", outline="")


# top right graph (bar chart)
canvas.create_rectangle(553.0, 149.0, 969.0, 332.0, fill="#F9F9F9", outline="")
canvas.create_rectangle(555.0, 151.0, 971.0, 334.0, fill="#C2C2C2", outline="")

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
# button which once pressed will run the method print_entry_content which then
# will retreive the value from the input box and run the ploting method  and dataframe method
# once again to update the plots and dataframe
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


# calling the display_dataframe function to display the dataframe on the left side of the dashboard
# the values in the parameter represent the dimensions of the rectangle the table is placed in
display_dataframe(window, df, 2.0, 47.0, 266.0, 552.0)

window.mainloop()
