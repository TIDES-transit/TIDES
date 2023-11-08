# Contributing to TIDES

Thank you for contributing to the TIDES Project. This document defines the roles and process for contributing to the project and documents the governance roles and approach for decision-making.

## Roles

There are two types of contributors to TIDES:

* Registered Contributors can create and respond to issues and can generate and comment on pull requests, and
* All other Stakeholders can create and respond to issues.

All contributors and stakeholders are asked to adhere to the [Code of Conduct](#code-of-conduct).

To become a registered Contributor, fill out the registration form at [this link][contributor-registration].

## How to Contribute

Contributions should be offered through GitHub issues and pull requests.

By making any contribution to the projects, contributors self-certify to the [Contributor Agreement](#contributor-agreement).

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

* Keep pull requests small and focused. One issue is best.
* Link Pull Requests to Issues as appropriate.
* Complete the pull request template as best you can.
* In order to run all GitHub Actions automations, contributors with adequate permissions (i.e. Registered Contributors) should submit pull requests from a branch on the main repo, rather than from a fork.

### Commits

Use the following guidance for commits

* Provide a short, clear title. Capitalize. No period at the end
* Wrap the body of text at 72 characters

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

## Contributor Agreement

By making any contribution to the projects, contributors self-certify to the following Contributor Agreement:

By making a contribution to this project, I certify that:
>  
> a. The contribution was created in whole or in part by me and I have the right to submit it under the open source license indicated in the file; or
>  
> b. The contribution is based upon previous work that, to the best of my knowledge, is covered under an appropriate open source license and I have the right under that license to submit that work with modifications, whether created in whole or in part by me, under the same open source license (unless I am permitted to submit under a different license), as indicated in the file; or
>  
> c. The contribution was provided directly to me by some other person who certified (a), (b) or (c) and I have not modified it.
>  
> d. I understand and agree that this project and the contribution are public and that a record of the contribution (including all personal information I submit with it, including my sign-off) is maintained indefinitely and may be redistributed consistent with this project or the open source license(s) involved.
>  
Attribution: This Contributor Agreement is adapted from the node.js project available here: <https://github.com/nodejs/node/blob/main/CONTRIBUTING.md>.

## License to Use

The TIDES specification is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt) (code) and [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) (sample data, specification, and documentation) as defined in <LICENSES> file.

## Project Governance

Ahead of Version 1.0 release, the governance for the TIDES specification is being kept limited and lightweight. The governance approach will be revisited as release of Version 1.0 approaches.

Development of the TIDES specification shall be managed by the following groups:

* [Leadership Group](#leadership-group)
* [Product Management Team](#product-management-team)
* [Registered Contributors](#registered-contributors)
* [All Other Stakeholders](#stakeholder-group)

These groups will have the following rights and responsibilities:

### Leadership Group

The Leadership Group is responsible for overall direction and decision-making on the project including:

* approval of registered contributors
* creation, scoping, and management of working groups
* approval of the final specification for Version 1.0
* approval of changes to project governance

Leadership Group Members

* John Levin, Metro Transit (Minneapolis-St. Paul, MN)

Leadership Group Member [GitHub Access](https://docs.github.com/en/organizations/managing-access-to-your-organizations-repositories/repository-roles-for-an-organization): Admin

### Product Management Team

The Product Management Team (PMT) is responsible for creating and maintaining backbone standards infrastructure, processes, and resources to support the development of the TIDES specification. The PMT will support Leadership in developing, reviewing, and recommending for approval changes to the draft specification. The PMT will support Contributors and Stakeholders in their work on the specification.  

PMT Group Members

* Hunter Owens, Caltrans
* Jameelah Young, Jarvus Innovations (on behalf of Caltrans)
* Soren Spicknall, Jarvus Innovations (on behalf of Caltrans)
* Elizabeth Sall, UrbanLabs LLC (on behalf of Caltrans)
* Benjamin Bressette, Caltrans
* Joey Reid, Metro Transit (Minneapolis-St. Paul, MN)

PMT Group Member [GitHub Access](https://docs.github.com/en/organizations/managing-access-to-your-organizations-repositories/repository-roles-for-an-organization): Admin

### Registered Contributors

Registered Contributors actively work to develop the TIDES specification. They propose additions, modifications, and improvements to the specification through issues and pull requests in this GitHub repository.

Registered Contributors must request [here][contributor-registration] to be registered in order to gain access. Requests to become a Contributor must be approved by project Leadership.

Registered Contributor Group Members:

The list of registered contributors is maintained in the [contributors.md](contributors.md) file.

Registered Contributor Group [GitHub Access](https://docs.github.com/en/organizations/managing-access-to-your-organizations-repositories/repository-roles-for-an-organization): Write

### Stakeholder Group

Stakeholders will be informed about progress on TIDES and given the opportunity to review the specification as it is developed. They may provide comments on the specification by creating or responding to Issues in this repository. Stakeholders are not able to generate or comment on pull requests. To be included as a TIDES Stakeholder, join the TIDES Project Google Group.

Stakeholder Group Membership:

* Members of the TIDES Project Google Group
* Others who have expressed interest in following progress or contributing to TIDES, but who have not requested to be a registered Contributor

Stakeholder Group [GitHub Access](https://docs.github.com/en/organizations/managing-access-to-your-organizations-repositories/repository-roles-for-an-organization): Read/Create Issues (same as general public)

## Review and Approval Process

Prior to release of Version 1.0 of the specification, the PMT and Leadership will have final approval of all changes. All Contributors are permitted and encouraged to discuss and comment on issues and pull requests and make recommendations for changes to the specification.

Leadership will convene a governance group to refine this and decide the approval process for Version 1.0 and the governance and approval process for future revisions to the specification.

## Code of Conduct

Contributors to the TIDES Project are expected to read and follow the [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md) for the project.

[contributor-registration]: https://forms.office.com/Pages/ResponsePage.aspx?id=i_a_3SpIc0WB4P74FWpP0Hpd6kyRp1VEg8rnx5-CwORUMFFGTzBYRktEMkJRWVg4Qlg3SkM0VEJKVi4u
