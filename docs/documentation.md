# Documentation

The documentation for the TIDES specification is available at <https://tides-transit.github.io/TIDES/> This site is automatically recreated each time a change is made to the specification.

When a change is pushed to the TIDES specification repository, Github Actions deployes the workflow `docs.yml` that rebuilds the files for the TIDES documentation site. When a pull request is opened from a branch on the main repository, a draft version of the docs is built for preview purposes via the same process. For security purposes, documentation is not automatically built on pull requests opened from forks.

??? info "Files used in TIDES Documentation"

    | **Name** |  **What it does** |
    | -------- | ----------------- |
    |`/.github/workflows/docs.yml` | <ul><li>Sets up python</li><li>Loads resources from /docs/requirements.txt</li><li>Runs mike</li></ul> |
    | `/docs/requirements.txt` | Lists resources needed to generate documentation |
    | `/mkdocs.yml` | Controls mkdocs:<ul><li>Defines look and feel of mkdocs</li><li>Specifies which mkdocs plug-ins to use</li><li>Specifies that mkdocs-macros should be used</li><li>Defines the structure of the documentation site</li><li>References /`docs/*.md` files as the major sections of the site</li></ul>
    | `main.py` | Defines macros used by mkdocs-macros, which can be referenced in the various markdown documentation files to generate markdown content, including from the Frictionless spec .json files |
    | `/docs/*.md` | These markdown files contain the content for the documentation site, either directly or by reference. |
    | `/docs/index.md` | Documentation homepage using content from README.me |
    | `/docs/architecture.md` | Documents the overall spec architcture using a list of spec tables generated from `tides.spec.json` and diagrams the relationships between tables with mermaid |
    | `/docs/tables.md` | Documents the detailed schemas for each table generated from `/spec/*.schema.json` |
    | `/docs/development.md` | Documents spec development processes using content from CONTRIBUTING.md and CODE_OF_CONDUCT.md |

??? info "Tools Used in TIDES Documentation"

    | **Name** |  **What it does** |
    | -------- | ----------------- |
    | GitHub Actions | Runs following workflow on each push to the TIDES github repository:  /.github/workflows/docs.yml |
    | mike | runs mkdocs and puts output in a folder in gh_pages branch which corresponds to the name of the branch (i.e. main, develop, pr-163, etc) <br> For new branches with documentation, adds an entry in `versions.json` |
    | `mkdocs` | Package which generates documentation from markdown and code |

??? info "Overview of Documentation Building Process"

    ```mermaid
    flowchart LR

    subgraph mkdocs["<b>mkdocs:</b> run on execution of mike"]
    md_mike["mike"] -->|runs for current branch| md_mkdocs["mkdocs"]
    md_mkdocs.yml["mkdocs.yml"] -->|specifieds parameters| md_mkdocs["mkdocs"]
    md_mkdocs_macros["mkdocs-macros"] -->|"plugin for"| md_mkdocs["mkdocs"]
    main.py[/"main.py"/] -->|defines macros in code available for| md_mkdocs_macros["mkdocs-macros"]
    end

    subgraph mkdocs-macros["<b>mkdocs-macros: </b>run on execution of mkdocs"]
    if_spec["architecture.md<br> <code>frictionless_spec('spec/tides.spec.json')</code>"]
    if_schemas["tables.md<br> <code>frictionless_schemas('spec/**.schema.json')</code>"]
    if_readme["index.md<br> <code>include_file('README.md'}</code>"]
    if_contributing["development.md<br> <code>include_file('contributing.md'}</code>"]
    end

    subgraph "/docs"
    index.md[/"<code>index.md</code>"/] -->|specified in| md_mkdocs.yml[/"mkdocs.yml"/]
    architecture.md[/"<code>architecture.md</code>"/] -->|specified in| md_mkdocs.yml
    tables.md[/"<code>tables.md</code>"/] -->|specified in| md_mkdocs.yml
    development.md[/"<code>development.md</code>"/] -->|specified in| md_mkdocs.yml
    end

    subgraph site["<b><code>/site</code>:</b> output of mkdocs"]
    index.html[/"<code>index.html</code>"/]
    development.html[/"<code>development.html</code>"/]
    architecture.html[/"<code>architecture.html</code>"/]
    tables.html[/"<code>tables.html</code>"/]
    end

    subgraph "/spec"
    spec[/"<code>*/schema.json</code>"/]
    schemas[/"<code>tides.spec.json</code>"/]
    end

    README[/"README.md"/]-->if_readme
    index.md-->if_readme
    if_readme --> index.html

    CONTRIBUTING[/"CONTRIBUTING.md"/]-->if_contributing
    development.md-->if_contributing
    if_contributing--> development.html

    tables.md-->if_schemas
    schemas-->if_schemas
    if_schemas--> tables.html

    architecture.md-->if_spec
    spec-->if_spec
    if_spec--> architecture.html
    ```
