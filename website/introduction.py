import dash_bootstrap_components as dbc
import dash_html_components as html


LAYOUT = html.Div(
    [
        html.Div(
            [
                dbc.Row(
                    dbc.Col(
                        html.P("Age VS Survival", style={"padding-top": "50px"}),
                        style={"width": 8, "text-align": "center", "fontSize": 70},
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        html.P(
                            [
                                "Feel free to report errors, provide feedback or ask questions about our work ",
                                html.A(
                                    "here",
                                    href="https://github.com/HMS-Internship/Website/discussions",
                                ),
                                ".",
                            ],
                            style={"padding-top": "25px"},
                        ),
                        style={"width": 8, "text-align": "center", "fontSize": 24},
                    ),
                ),
                html.Div([html.Br(), html.Br()]),
            ],
            style={"padding-bottom": 100},
        ),
        html.Div(
            [
                html.H4(
                    [
                        html.A(
                            "Alan Le Goallec",
                            href="https://www.linkedin.com/in/alan-le-goallec-1990/",
                            style={"color": "white"},
                        ),
                        html.Sup("1, 2,+"),
                        ", ",
                        html.A(
                            "Théo Vincent",
                            href="https://www.linkedin.com/in/theo-vincent/",
                            style={"color": "white"},
                        ),
                        html.Sup("1,+"),
                        " and ",
                        html.A(
                            "Chirag J. Patel",
                            href="https://www.linkedin.com/in/chirag-j-patel/",
                            style={"color": "white"},
                        ),
                        html.Sup("1*"),
                    ],
                    style={"font-size": "22px"},
                ),
                html.H5(
                    [
                        html.Sup("1"),
                        html.A(
                            "Department of Biomedical Informatics, Harvard Medical School, Boston, MA, 02115, USA",
                            href="https://dbmi.hms.harvard.edu/",
                            style={"color": "white"},
                        ),
                        ", ",
                        html.Sup("2"),
                        html.A(
                            "Department of Systems, Synthetic and Quantitative Biology, Harvard University, Cambridge, MA, 02118, USA",
                            href="https://sysbio.med.harvard.edu/",
                            style={"color": "white"},
                        ),
                        ", ",
                        html.Sup("+"),
                        "Co-first authors, ",
                        html.Sup("*"),
                        "Corresponding author",
                    ],
                    style={"font-size": "16px"},
                ),
            ],
            style={
                "position": "fixed",
                "bottom": 0,
                "width": "100%",
                "background": "#0070FF",
                "line-height": 2,
                "text-align": "center",
                "color": "white",
                "Font-size": 14,
                "font-weight": "bold",
                "text-shadow": "0 1px 0 #84BAFF",
                "box-shadow": "0 0 15px #00214B",
                "padding-top": 15,
                "padding-bottom": 15,
            },
        ),
    ]
)
