# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import importlib.metadata

release = importlib.metadata.version("ewoksgalaxy")

project = "ewoksgalaxy"
version = ".".join(release.split(".")[:2])
copyright = "2026, ESRF"
author = "ESRF"
docstitle = f"{project} {version}"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.viewcode", "sphinx_copybutton"]
templates_path = ["_templates"]
exclude_patterns = []

always_document_param_types = True

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_title = docstitle
# html_logo = "_static/logo.png"
html_static_path = ["_static"]
html_template_path = ["_templates"]
html_css_files = ["custom.css"]

html_theme_options = {
    "icon_links": [
        {
            "name": "gitlab",
            "url": "https://gitlab.esrf.fr/workflow/ewoks/ewoksgalaxy",
            "icon": "fa-brands fa-gitlab",
        },
        {
            "name": "pypi",
            "url": "https://pypi.org/project/ewoksgalaxy",
            "icon": "fa-brands fa-python",
        },
    ],
    "logo": {
        "text": docstitle,
    },
    "footer_start": ["copyright"],
    "footer_end": ["footer_end"],
}
