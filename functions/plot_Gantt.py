#  vim: set foldmethod=indent foldcolumn=4 :
#!/usr/bin/env python3

"""
Write a pyhton fucntion called "get_Gantt" thats draws a gantt diagram where:
- 1st main event is called "M1: Definición del TFM" and takes times from  28 Feb 2024 to 12 Mar 2024) 
- 2nd main event is called "M2: Estado del arte o análisis de mercado del proyecto" and takes times from  13 Mar 2024 to 26 Mar 2024
- 3rd main event is called "M3: Diseño e implementación del trabajo" and takes times from  27 Mar 2024 to 21 May 2024
- 4th main event is called "M4: Redacción de la documentación del TFM" and takes times from  22 May 2024 to 18 Jun 2024
- 5th main event is called "M5: Defensa del proyecto" and takes times from  19 Jun 2024 to 7 Jul 2024

- 1st main event has next subevents:
"Justificación y motivación del proyecto" which takes around 80% of its main event time
"Metodología y planificación" which takes around 20% of its main event time

- 2nd main event has next subevents:
"Búsqueda del conjunto de datos" which takes around 80% of its main event time
"Estudio del estado del arte y la literatura" which takes around 80% of its main event time in parallel with previous subevent
"Elección del conjunto de datos y técnicas" which takes around 20% of its main event time

- 3rd main event has next subevents:
"Análisis del conjunto de datos" which takes around 18% of its main event time
"Preparación del conjunto de datos" which takes around 7% of its main event time
"Implementación de los modelos" which takes around 50% of its main event time
"Evaluación del mejor modelo" which takes around 7% of its main event time
"Conclusiones y resultados" which takes around 18% of its main event time

- 4th main event has next subevents:
"Redacción de la memoria" which takes around 65% of its main event time
"Correcciones en la memoria" which takes around 35% of its main event time

- 5th main event has next subevents:
"Preparación de la defensa" which takes around 50% of its main event time
"Defensa" which takes around 50% of its main event time
"""
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


import pandas as pd
import plotly.express as px


def create_gantt_chart(data):
    # Expand rows to individual pairs of start-end dates
    rows = []
    for _, row in data.iterrows():
        if not isinstance(row["Inicio"], list):
            row["Inicio"] = [row["Inicio"]]
        if not isinstance(row["Fin"], list):
            row["Fin"] = [row["Fin"]]
        for start, end in zip(row["Inicio"], row["Fin"]):
            rows.append(
                {
                    "Tarea": row["Tarea"],
                    "Inicio": start,
                    "Fin": end,
                    "Modulo": row["Modulo"],
                }
            )

    # Create an interactive Gantt chart
    expanded_data = pd.DataFrame(rows)
    print("expanded_data:", expanded_data)
    expanded_data["Inicio"] = pd.to_datetime(expanded_data["Inicio"])
    expanded_data["Fin"] = pd.to_datetime(expanded_data["Fin"])
    # Add 23 hours and 59 minutes to each value in the "Fin" column
    expanded_data["Fin_mas_uno"] = expanded_data["Fin"] + pd.Timedelta(days=1)

    expanded_data["fechas"] = [
        g + " - " + k
        for g, k in zip(
            expanded_data["Inicio"].dt.strftime("%d %b"),
            expanded_data["Fin"].dt.strftime("%d %b"),
        )
    ]

    # https://plotly.com/python-api-reference/generated/plotly.express.timeline.html
    # https://plotly.com/python/figure-labels/
    # https://github.com/plotly/plotly.py/blob/master/doc/python/gantt.md
    fig = px.timeline(
        expanded_data,
        x_start="Inicio",
        x_end="Fin_mas_uno",
        y="Tarea",
        color="Modulo",
        title="Diagrama de Gantt para el TFM de Juan Marinero",
        hover_data={
            "Tarea": True,
            "Inicio": False,
            "Fin": False,
            "Modulo": False,
            "Fin_mas_uno": False,
            "fechas": True,
        },
    )

    fig.update_yaxes(
        autorange="reversed"
    )  # otherwise tasks are listed from the bottom up

    # Customize the figure layout
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Tareas",
        yaxis_title_font_size=40,
        xaxis_type="date",
        title_font_size=40,
        title_xanchor="left",
        title_y=0.95,
        xaxis=dict(
            showgrid=False,
            showline=True,
            showticklabels=True,
            tickangle=0,
            ticks="outside",
            tickfont=dict(family="Arial", size=15, color="black"),
            tickformat="%d %b",
            ticklabelposition="outside bottom",
        ),
        legend=dict(
            font=dict(family="Arial", size=20, color="black"),
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
        ),
        width=1200,  # Adjust the width as needed
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=[
            "2024-02-28",
            "2024-03-12",
            "2024-03-26",
            "2024-05-21",
            "2024-06-18",
            "2024-07-07",
        ],
        ticktext=[
            "28 febrero<br>Inicio M1",
            "12 marzo<br>Fin M1",
            "26 marzo<br>Find M2",
            "21 mayo<br>Fin M3",
            "18 junio<br>Fin M4",
            "7 julio<br><b>Defensa</b>",
        ],
    )

    # Show the Gantt chart
    fig.show()


def get_df():
    events = [
        "M1: Definición del TFM",
        "M2: Estado del arte o análisis de mercado del proyecto",
        "M3: Diseño e implementación del trabajo",
        "M4: Redacción de la documentación del TFM",
        "M5: Defensa del proyecto",
    ]

    genre, sub_project, start, end = list(), list(), list(), list()

    genre.append(events[0])
    sub_project.append("Justificación y motivación del proyecto")
    start.append("2024-02-28")
    end.append("2024-03-07")

    genre.append(events[0])
    sub_project.append("Metodología y planificación")
    start.append("2024-03-08")
    end.append("2024-03-12")

    genre.append(events[1])
    sub_project.append("Búsqueda del conjunto de datos")
    start.append("2024-03-13")
    end.append("2024-03-22")

    genre.append(events[1])
    sub_project.append("Estudio del estado del arte y la literatura")
    start.append("2024-03-13")
    end.append("2024-03-22")

    genre.append(events[1])
    sub_project.append("Elección del conjunto de datos y técnicas")
    start.append("2024-03-23")
    end.append("2024-03-26")

    genre.append(events[2])
    sub_project.append("Análisis del conjunto de datos")
    start.append("2024-03-27")
    end.append("2024-04-03")

    genre.append(events[2])
    sub_project.append("Preparación del conjunto de datos")
    start.append("2024-04-04")
    end.append("2024-04-18")

    genre.append(events[2])
    sub_project.append("Implementación de los modelos")
    start.append("2024-04-19")
    end.append("2024-05-07")

    genre.append(events[2])
    sub_project.append("Evaluación del mejor modelo")
    start.append("2024-05-08")
    end.append("2024-05-21")

    genre.append(events[2])
    sub_project.append("Conclusiones y resultados")
    start.append("2024-05-12")
    end.append("2024-05-21")

    genre.append(events[3])
    sub_project.append("Redacción de la memoria")
    start.append("2024-05-22")
    end.append("2024-06-11")

    genre.append(events[3])
    sub_project.append("Correcciones en la memoria")
    start.append("2024-06-12")
    end.append("2024-06-18")

    genre.append(events[4])
    sub_project.append("Preparación de la defensa")
    start.append("2024-06-19")
    end.append("2024-07-07")

    genre.append(events[4])
    sub_project.append("Defensa")
    start.append("2024-07-07")
    end.append("2024-07-08")

    df = pd.DataFrame(
        {"Modulo": genre, "Tarea": sub_project, "Inicio": start, "Fin": end}
    )
    #  print("df:", df)
    return df


def main():
    #  https://developers.google.com/chart/interactive/docs/gallery/ganttchart#no-dependencies

    df = get_df()

    create_gantt_chart(df)


if __name__ == "__main__":
    main()


def plot_Gantt():
    # Define the start and end dates for each main event
    start_dates = [
        datetime(2024, 2, 28),
        datetime(2024, 3, 13),
        datetime(2024, 3, 27),
        datetime(2024, 5, 22),
        datetime(2024, 6, 19),
    ]
    end_dates = [
        datetime(2024, 3, 12),
        datetime(2024, 3, 26),
        datetime(2024, 5, 21),
        datetime(2024, 6, 18),
        datetime(2024, 7, 7),
    ]

    # Define the main event names
    main_events = [
        "M1: Definición del TFM",
        "M2: Estado del arte o análisis de mercado del proyecto",
        "M3: Diseño e implementación del trabajo",
        "M4: Redacción de la documentación del TFM",
        "M5: Defensa del proyecto",
    ]

    # Define the subevents and their durations for each main event
    subevents = [
        [
            ("Justificación y motivación del proyecto", 0.8),
            ("Metodología y planificación", 0.2),
        ],
        [
            ("Búsqueda del conjunto de datos", 0.8),
            ("Estudio del estado del arte y la literatura", 0.8),
            ("Elección del conjunto de datos y técnicas", 0.2),
        ],
        [
            ("Análisis del conjunto de datos", 0.18),
            ("Preparación del conjunto de datos", 0.07),
            ("Implementación de los modelos", 0.5),
            ("Evaluación del mejor modelo", 0.07),
            ("Conclusiones y resultados", 0.18),
        ],
        [("Redacción de la memoria", 0.65), ("Correcciones en la memoria", 0.35)],
        [("Preparación de la defensa", 0.5), ("Defensa", 0.5)],
    ]

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Set the y-axis ticks and labels
    ax.set_yticks(range(len(main_events)))
    ax.set_yticklabels(main_events)

    # Set the x-axis limits and ticks
    ax.set_xlim(start_dates[0], end_dates[-1])
    ax.set_xticks(start_dates)
    ax.set_xticklabels([date.strftime("%d %b") for date in start_dates])

    # Draw the main events
    for i, (start_date, end_date) in enumerate(zip(start_dates, end_dates)):
        ax.broken_barh(
            [(start_date, end_date - start_date)],
            (i - 0.4, 0.8),
            facecolor="lightgray",
            edgecolor="black",
        )
        ax.text(start_date, i, main_events[i], va="center", ha="right", rotation=90)

    # Draw the subevents
    for i, event_subevents in enumerate(subevents):
        for subevent, duration in event_subevents:
            start_date = start_dates[i]
            end_date = start_date + timedelta(
                days=(end_dates[i] - start_dates[i]).days * duration
            )
            ax.broken_barh(
                [(start_date, end_date - start_date)],
                (i - 0.2, 0.4),
                facecolor="white",
                edgecolor="black",
            )
            ax.text(start_date, i - 0.1, subevent, va="center", ha="right", rotation=90)

    # Set the title and axis labels
    ax.set_title("Gantt Diagram")
    ax.set_xlabel("Date")
    ax.set_ylabel("Event")

    # Show the plot
    plt.show()


if __name__ == "__main__":
    pass
    #  get_Gantt()
