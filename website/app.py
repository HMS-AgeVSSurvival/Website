import dash
import dash_bootstrap_components as dbc
import dash_auth

APP = dash.Dash(
    name=__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    assets_url_path="data",
    assets_folder="../data",  # from __name__
    title="Age VS Survival",
)

dash_auth.BasicAuth(APP, {"alan": "legoallec", "chirag": "patel", "theo": "vincent"})

APP.config.suppress_callback_exceptions = True

APP.index_string = """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""
