# Contributing to TIDES

Thank you for contributing to the TIDES Project. This document outlines the process for contributing to the project and documents the governance roles and approach for decision-making. Where [TIDES Governance][TIDES-governance] and this document differ, the [TIDES Governance][TIDES-governance] shall take precedence.

[contributor-registration]: https://forms.office.com/Pages/ResponsePage.aspx?id=i_a_3SpIc0WB4P74FWpP0Hpd6kyRp1VEg8rnx5-CwORUMFFGTzBYRktEMkJRWVg4Qlg3SkM0VEJKVi4u
[TIDES-governance]: https://tides-transit.github.io/TIDES/governance/
[TIDES-Board]:https://tides-transit.github.io/TIDES/governance/#tides-board-of-directors
[TIDES-Contributor]:https://tides-transit.github.io/TIDES/governance/#tides-contributor
[TIDES-Manager]:https://tides-transit.github.io/TIDES/governance/#tides-manager
[TIDES-Stakeholder]: https://tides-transit.github.io/TIDES/governance/#tides-stakeholder

## Becoming a TIDES Contributor

As defined in the [TIDES Governance][TIDES-governance], a [TIDES-Contributor][TIDES-contributor] has the rights to:

- Create issues, discussions, and pull requests in the TIDES repository.
- Vote in decisions on changes to the TIDES spec and other aspects of TIDES.

These roles and responsibilities are further detailed in the [TIDES Governance][TIDES-governance] and documents linked to from it.  

Individuals may request to be a Contributor by completing [the registration form][contributor-registration]that includes acknowledgement of the [Contributor Agreement](#tides-contributor-license-agreement) and [Code of Conduct](#tides-code-of-conduct).

## How to Contribute

1. Become a [TIDES Contributor](#becoming-a-tides-contributor)
2. Follow [setup](#setup) instructions if you'd like to contribute code or provide code reviews.
3. Offer to help research an issue
4. Offer to help resolve an issue with a pull-request
5. Offer to review a pull-request

!!! warning

    By making any contribution to the projects, contributors self-certify to the [Contributor Agreement](#tides-contributor-license-agreement).

### Setup

1. Make sure you have a [GitHub](https://github.com/) account.
2. Make sure you have [git](https://git-scm.com/downloads), a terminal (e.g. Mac Terminal, CygWin, etc.), and a text editor installed on your local machine. Optionally, you will likely find it easier to use [GitHub Desktop](https://desktop.github.com/), an IDE instead of a simple text editor like [VSCode](https://code.visualstudio.com/), [Eclipse](https://www.eclipse.org/), [Sublime Text](https://www.sublimetext.com/), etc.
3. [Clone the repository locally](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository). Non-registered contributors should [fork the repository](https://github.com/TIDES-transit/TIDES/fork) first, since they will be unable to push branches directly to the main repository.
4. Install development requirements packages `pip install -r requirements.txt` or in a virtual environment.

!!! tip "Using a virtual environment"

    It is often helpful to install requirements for vairous projects inside a virtual environment rather than in your main python installation. Some virtual environments to consider include: [`conda`](https://docs.conda.io/),[`pipenv`](https://pipenv.pypa.io/en/latest/index.html),[`poetry`](https://python-poetry.org/), and [`rye`](https://github.com/mitsuhiko/rye).

### Contribution Workflow

1. [Create a branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository) to work on a new issue (or checkout an existing one where the issue is being worked on).  
2. Make your changes.
3. Run `tests/test_local_spec` script to check and fix formatting, validate profile and schemas with frictionless and with each other, and confirm that documentation can be built locally.
4. Run `tests/test_samples_to_local` script to check if samples conform to any changes to the spec.
5. [Commit](#commits) your work in `git`
6. `push` your changes to Github and submit a [`pull request`](#pull-requests)

### Issues

Create issues to start discussion on a new topic. If the issue is associated with a pull
request, be sure to link the two. There are shortcuts [here](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword)

### Pull Requests

Use the following guidance in creating and responding to pull requests

- Keep pull requests small and focused. One issue is best.
- Link Pull Requests to Issues as appropriate.
- Complete the pull request template as best you can.
- In order to run all GitHub Actions automations, contributors with adequate permissions (i.e. Registered Contributors) should submit pull requests from a branch on the main repo, rather than from a fork.

### Commits

Use the following guidance for commits

- Provide a short, clear title. Capitalize. No period at the end
- Wrap the body of text at 72 characters

### Continuous Integration / Continuous Deployment

We leverage [Github Actions](https://github.com/features/actions) workflows to flag potentially erronious contributions and build, preview and deploy documentation that is in sync with the schema definition files.

Workflows are defined in `/.github/workflows/` include the following:

| **File** | **Description** |
| ------- | ----- |
| `validate_package_schema.yml` | Validates Data Package definition |
| `validate_table_schemas.yml` | Validates Schema Files |
| `docs.yml` | Builds and deploys documentation |

??? info "`docs.yml` Process"

    ```mermaid
    flowchart LR

    setup-python --> pip["pip install docs/requirements.txt"]
    pip["pip install docs/requirements.txt"] --> gh_mike["mike"]
    gh_mike["mike"] --> gh-pages/branch-name
    ```

### Documentation

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

## TIDES Contributor License Agreement

By making any contribution to the projects, contributors self-certify to the the [TIDES Contributor Agreement](CLA.md).

## License to Use

The TIDES specification is licensed under the Apache License 2.0 as defined in the [LICENSE][license].

## Project Governance

The TIDES Project Governance and the roles within are detailed in the [TIDES-governance][TIDES-governance] documentation.  At this time, the following people fulfill the TIDES roles:

### Roles

- [**TIDES Board**][TIDES-Board]
    - John Levin, Metro Transit (Minneapolis-St. Paul, MN)
- **Board Coordinator**: *TBD*
- [**TIDES Manager**][TIDES-Manager]: *Currently in discussion*
- **Program Manager**: *TBD*
- [**TIDES-Contributors**][TIDES-Contributor]: [List of Contributors](contributors.md)
- [**TIDES-Stakeholders**][TIDES-Stakeholder]: Anyone who has an interest in or could be directly affected by the TIDES specification and tools.

### [GitHub Access Levels](https://docs.github.com/en/organizations/managing-access-to-your-organizations-repositories/repository-roles-for-an-organization)

| **Role**            | **Access Level**   |
|---------------------|--------------------|
| Board               | Admin              |
| Program Manager     | Admin              |
| Board Coordinator   | Triage             |
| Manager             | Triage             |
| Contributor Group   | Triage             |
| Stakeholder         | Read/Create Issues |

## Review and Approval Process

Prior to release of Version 1.0 of the specification, the TIDES Board will have final approval of all changes. All Contributors are permitted and encouraged to discuss and comment on issues and pull requests and make recommendations for changes to the specification.

Following v1.0, TIDES will adhere to a change management policy currently in development.

## TIDES Code of Conduct

Contributors to the TIDES Project are expected to read and follow the [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md) for the project.
