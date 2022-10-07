# Contributing to TIDES

Thank you for contributing to the TIDES Project.  This document defines the roles and process for contributing to the project and documents the governance roles and approach for decision-making.

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
2. Make sure you have [git](https://git-scm.com/downloads), a terminal (e.g. Mac Terminal, CygWin, etc.), and a text editor installed on your local machine.  Optionally, you will likely find it easier to use [GitHub Desktop](https://desktop.github.com/), an IDE instead of a simple text editor like [VSCode](https://code.visualstudio.com/), [Eclipse](https://www.eclipse.org/), [Sublime Text](https://www.sublimetext.com/), etc.  
3. [Fork the repository](https://github.com/TIDES-transit/TIDES/fork) into your own GitHub account and [clone it locally](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).  
4. [Create a branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository) to work on a new issue (or checkout an existing one where the issue is being worked on).  
5. Install [pre-commit](https://pre-commit.com/) so you can check your code and text formatting.
6. \[Optional\] [Install act](https://github.com/nektos/act) to run github actions locally.  

### Issues

Create issues to start discussion on a new topic.  If the issue is associated with a pull
request, be sure to link the two.  There are shortcuts [here](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword)

### Pull Requests

Use the following guidance in creating and responding to pull requests

* Keep pull requests small and focused. One issue is best.
* Link Pull Requests to Issues as appropriate.
* Complete the pull request template as best you can.

### Commits

Use the following guidance for commits

* Provide a short, clear title.  Capitalize. No period at the end
* Wrap the body of text at 72 characters

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

The TIDES specification is licensed under the Apache License 2.0 as defined in <LICENSE> file.

## Project Governance

Ahead of Version 1.0 release, the governance for the TIDES specification is being kept limited and lightweight. The governance approach will be revisited as release of Version 1.0 approaches.

Development of the TIDES specification shall be managed by the following groups:

* [Leadership Group](#leadership-group)
* [Product Management Team](#product-management-team)
* [Registered Contributors](#registered-contributors)
* [All Other Stakeholders](#stakeholders-group)

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

The Product Management Team (PMT) is responsible for creating and maintaining backbone standards infrastructure, processes, and resources to support the development of the TIDES specification.  The PMT will support Leadership in developing, reviewing, and recommending for approval changes to the draft specification.  The PMT will support Contributors and Stakeholders in their work on the specification.  

PMT Group Members

* Hunter Owens, Caltrans
* Jameelah Young, Jarv.us (on behalf of Caltrans)
* Elizabeth Sall, UrbanLabs LLC (on behalf of Caltrans)
* Benjamin Bressette, Caltrans
* Blake Fleisher, Jarv.us (on behalf of Caltrans)
* Joey Reid, Metro Transit (Minneapolis-St. Paul, MN)

PMT Group Member [GitHub Access](https://docs.github.com/en/organizations/managing-access-to-your-organizations-repositories/repository-roles-for-an-organization): Admin

### Registered Contributors

Registered Contributors actively work to develop the TIDES specification. They propose additions, modifications, and improvements to the speciation document through issues and pull requests in this GitHub repository.

Registered Contributors must request [here][contributor-registration] to be registered in order to gain access.  Requests to become a Contributor must be approved by project Leadership.

Registered Contributor Group Members:

The list of registered contributors is maintained in the [contributors.md](contributors.md) file.

Registered Contributor Group [GitHub Access](https://docs.github.com/en/organizations/managing-access-to-your-organizations-repositories/repository-roles-for-an-organization): Write

### Stakeholders Group

Stakeholders will be informed about progress on TIDES and given the opportunity to review the specification as it is developed.  They may provide comments on the specification by creating or responding to Issues in this repository.  Stakeholders are not able to generate or comment on pull requests.  To be included as a TIDES Stakeholder, join the TIDES Project Google Group.

Stakeholder Group Membership:

* Members of the TIDES Project Google Group
* Others who have expressed interest in following progress or contributing to TIDES, but who have not requested to be a registered Contributor

Stakeholder Group [GitHub Access](https://docs.github.com/en/organizations/managing-access-to-your-organizations-repositories/repository-roles-for-an-organization): Read/Create Issues (same as general public)

## Review and Approval Process

Prior to release of Version 1.0 of the specification, the PMT and Leadership will have final approval of all changes.   All Contributors are permitted and encouraged to discuss and comment on issues and pull requests and make recommendations for changes to the specification.

Leadership will convene a governance group to refine this and decide the approval process for Version 1.0 and the governance and approval process for future revisions to the specification.

## Code of Conduct

Contributors to the TIDES Project are expected to read and follow the [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md) for the project.

[contributor-registration]: https://forms.office.com/Pages/ResponsePage.aspx?id=i_a_3SpIc0WB4P74FWpP0Hpd6kyRp1VEg8rnx5-CwORUMFFGTzBYRktEMkJRWVg4Qlg3SkM0VEJKVi4u
