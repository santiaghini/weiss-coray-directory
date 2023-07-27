from shiny import App, render, ui
import shinyswatch

from utils import load_data

data = load_data()
TITLE = "Wyss-Coray Lab"
DOI_URL = "https://doi.org/"
PUBMED_URL = "https://pubmed.ncbi.nlm.nih.gov/"

sortby_choices = ["Newest", "Oldest", "Alphabetical"]


def sort_data(data):
    return sorted(data, key=lambda x: x["date"], reverse=True)
data = sort_data(data)


def create_tabs():
    return ui._navs.NavSetPillList(
        *[
            ui.nav(
                ui.div(
                    entry["title"] + " ",
                    ui.div(entry["date"], class_="badge bg-secondary"),
                ),
                ui.h2(entry["title"]),
                ui.br(),
                ui.navset_tab(
                    # elements ----
                    ui.nav(
                        "Abstract",
                        # ui.h5("Abstract"),
                        ui.br(),
                        ui.p(entry["abstract"]),
                        # Publication
                        ui.div(
                            ui.strong("Publication: "),
                            ui.a(entry["publication"]["text"], href=entry["publication"]["url"]),
                        ),
                        # Website
                        ui.div(
                            ui.strong("Website: "),
                            ui.a(entry["website"]["text"], href=entry["website"]["url"]),
                        ) if "website" in entry else None,
                        # DOI
                        ui.div(
                            ui.strong("DOI: "),
                            ui.a(entry["doi"], href=DOI_URL+entry['doi']),
                        ),
                        # PubMed
                        ui.div(
                            ui.strong("PubMed: "),
                            ui.a(entry["pubmed"], href=PUBMED_URL+entry['pubmed']),
                        ),
                        # Date
                        ui.div(
                            ui.strong("Date: "),
                            ui.span(entry["date"]),
                        ),
                    ),
                )
            )
            for entry in data
        ],
        ul_class="nav nav-pills nav-stacked nowrap",
        id=None,
        selected=None
    )

### APP UI ###
app_ui = ui.page_fluid(
    # Following lines are attempt to make tabs scrollable, too hacky
    # {"style": "height: 100vh; padding-top: 1em;"},
    # ui.tags.style(
    #     """
    #     .nowrap {
    #         -webkit-flex-wrap: nowrap;
    #         flex-wrap: nowrap;
    #         }
    #     """
    # ),
    {"style": "padding-top: 1em;"},
    shinyswatch.theme.simplex(),
    ui.panel_title(TITLE),
    ui.br(),
    # ui.input_selectize("sortby", "Sort by", sortby_choices),
    create_tabs()
)

### SERVER ###
def server(input, output, session):
    @output
    @render.text
    def txt():
        return f"n*2 is {input.n() * 2}"


app = App(app_ui, server)
