# Contributing to TIDES

Thank you for contributing to the TIDES Project. This document outlines the process for contributing to the project and documents the governance roles and approach for decision-making. Where [TIDES Governance][TIDES-governance] and this document differ, the [TIDES Governance][TIDES-governance] shall take precedence.

[contributor registration form]: https://docs.google.com/forms/d/e/1FAIpQLSfQUjKHfV64uDBAYAt0OSPgYCe_BGgcAPWXi-m0PSlX6edCIQ/viewform?usp=header
[code of conduct]:./docs/governance/policies/code_of_conduct.md
[CLA]:./docs/governance/policies/CLA.md
[change-policy]:./docs/governance/policies/change-management.md
[doc-building]:./docs/documentation.md
[TIDES-governance]: ./docs/governance.md
[TIDES-contributor]:./docs/governance.md/#tides-contributor

## Becoming a TIDES Contributor

As defined in the [TIDES Governance][TIDES-governance], a [TIDES-Contributor][TIDES-contributor] has the rights to:

- Create issues, discussions, and pull requests in the TIDES repository.
- Vote in decisions on changes to the TIDES spec and other aspects of TIDES.

These roles and responsibilities are further detailed in the [TIDES Governance][TIDES-governance] and documents linked to from it.  

Individuals may request to be a Contributor by completing [the registration form][contributor registration form] that includes acknowledgement of the [Contributor Agreement](#tides-contributor-license-agreement) and [Code of Conduct](#tides-code-of-conduct).

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

1. [Create a feature branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository) to work on a new issue (or checkout an existing one where the issue is being worked on).  
2. Make your changes.
3. Run `tests/test_local_spec` script to check and fix formatting, validate profile and schemas with frictionless and with each other, and confirm that documentation can be built locally.
4. Run `tests/test_samples_to_local` script to check if samples conform to any changes to the spec.
5. [Commit](#commits) your work in `git`
6. `push` your changes to Github and submit a [`pull request`](#pull-requests)

!!! tip "Create a feature branch on a clone of `tides-transit/TIDES`, not a fork"

    If you have the permissions (which you should if you are a TIDE Contributor), you should complete your work on a feature branch from a **clone** of the main TIDES repository (`tides-transit/TIDES`) rather than a fork of it (e.g. `my-github-handle/TIDES`) so that when you submit a pull request the continuous integration tests will have the right permissions to run. 

### Issues

Create issues to start discussion on a new topic. If the issue is associated with a pull
request, be sure to link the two. There are shortcuts [here](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword)

### Pull Requests

Use the following guidance in creating and responding to pull requests

- Keep pull requests small and focused. One issue is best.
- Link Pull Requests to Issues as appropriate.
- Complete the pull request template as best you can.
- In order to run all GitHub Actions automations, contributors with adequate permissions (i.e. Registered Contributors) should submit pull requests from a branch on the main repo, rather than from a fork.

!!! tip "If you worked from a fork"

    If you worked from a fork of the `TIDES/tides-transit` repo instead of a feature branch of a clone of the `TIDES/tides-transit` repo, you will not have the right permissions to run the continuous integration tests when you submit a pull request.  To remedy, please push the branch of your local fork to a feature branch of the main repository:

    ```sh
    git remote add upstream git@github.com/TIDES-transit/TIDES.git
    git push upstream <my-feature-branch-name>
    ``` 

    ...and now you should be able to submit a pull request from that feature branch which should have the permission to run the continuous integration tests.

    Run into a permissions issue with that command? Make sure you a registered contributor and that you have accepted the resulting invitation to join the `tides-transit` team on Github. 

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

[More information about updating and building TIDES documentation...][doc-building]

## TIDES Contributor License Agreement

By making any contribution to the projects, contributors self-certify to the the [TIDES Contributor Agreement][CLA].

## License to Use

The TIDES specification is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt) (code) and [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) (sample data, specification, and documentation) as defined in <LICENSES> file.

## Project Governance

The TIDES Project Governance and the roles within are detailed in the [TIDES governance][TIDES-governance] documentation.

### [GitHub Access Levels](https://docs.github.com/en/organizations/managing-access-to-your-organizations-repositories/repository-roles-for-an-organization)

| **Role**            | **Access Level**   |
|---------------------|--------------------|
| Board               | Admin              |
| Program Manager     | Admin              |
| Board Coordinator   | Write              |
| Manager             | Write              |
| Contributor Group   | Write              |
| Stakeholder         | Read/Create Issues |

## Review and Approval Process

The TIDES Board has final approval of all *normative* changes changes to the specificaiton and project governance. All Contributors are permitted and encouraged to discuss and comment on issues and pull requests and make recommendations for changes to the specification.  Contributions made as a pull request by Contributors which do not make any changes to the `/spec` or `/docs/governance` directories may be approved by a another Contributor if it passes the continuous integration tests.

Following v1.0, TIDES will adhere to this [change management and versioning policy][change-policy].

## TIDES Code of Conduct

Contributors to the TIDES Project are expected to read and follow the [code of conduct] for the project.
