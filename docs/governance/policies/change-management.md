# TIDES Change Management Policy

[TIDES-governance]:../../governance.md
[data-package]: ../../datapackage.md

!!! tip

    When capitalized in this document, the words “MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" refer to their respective definitions in [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119).

!!! tip

    Definitions of various roles such as TIDES Board, TIDES Manager and TIDES Contributor refer to their respective definitions in the [TIDES Governance Policy][TIDES-governance].

Over time, the TIDES data standard will need to evolve to meet stakeholder needs.  Changes may include the addition of new tables, new fields to existing tables, or the modification of existing fields.  Occasionally this may also include significant structural changes which may not be backwards compatible with existing datasets.

The change management process covers:

* [Change-making Process](#change-making-process): how normative content of the TIDES specification is changed
* [Versioning and Release Processes](#version-numbering): how changes are identified
* [Version Control](#version-control): how the change process, versioning, and releases are managed in practice

## Principles

The revision process is designed with the following principles in mind:

!!! success "Merit"

    * Changes should have a clear purpose.
    * Consequences of a change should be evaluated from the perspective of different affected stakeholder groups.
    * Changes should be prioritized by the community.

!!! success "Openness + Transparency"

    * Discussion and decisions about changes should be publicly noticed and accessible.
    * Change-making process should be straight-forward and easy to follow.
    * Change proposals should have a reliable timeline for being decided on and incorporated.
    * Each change (or bundled set of changes) should be identified by assigning a new [version number](#version-numbering).

!!! success "Efficiency"

    * Change-making process should be simple for simple changes.
    * Complex changes should be made with careful consideration.
    * Streamlined, purpose-driven change management should be applied to maximize stakeholder efficiency.
    * Changes should be straightforward to incorporate by existing TIDES users.
    * Significant changes, especially those which are not backwards compatible with existing datasets, should be limited in number and in frequency in order to limit the number of times existing processes and tools need to be re-engineered.
        * A significant change merits a new version number.

## Change-Making Process

This change-making process covers all [normative content](#normative-content) changes to the TIDES specification.

### Normative Content

[**Normative**](https://en.wikipedia.org/wiki/Normativity#Standards_documents) **Content** is the prescriptive part of a standard**. It sets the rules to be followed in order to be evaluated as compliant with the standard, and from which no deviation is permitted.

??? info "Normative Content in TIDES"

    In the TIDES data schemas, the following properties are considered normative content within any `schema.json` file:

    * `name`
    * `primaryKey`
    * `missingValues`
    * `type`
    * `constraints`

    Similarly, the entirety of the [TIDES Data Package Profile][data-package] is considered normative with the **exception** of the following properties:

    * `description`
    * `context`
    * `examples`

**Non-normative content** is the non-prescriptive, or ‘descriptive’, part of a standard. This may include analogies, synonyms, explanations, illustrations, context, and examples. In the event non-normative content contradicts normative content, the normative content is to be followed.

??? info "Non-Normative Content in TIDES"

    Changes outside the `/spec` are all considered non-normative. Within the `/spec` folder, non-normative changes to the specification are typically limited to the following properties in the `tides-datapackage-profile.json` and any `...schema.json`file:

    * `description`
    * `examples`
    * `context`

### Change-making Stages

The process by which normative changes are made to the TIDES data specification occurs in the following stages:

| Stage | When | Who (led by) |
|-----|-----|-----|
| Need Identification | Anytime | Anyone |
| Prioritization | Quarterly (or as determined by TIDES Board or TIDES Manager) | Contributors (Manager) |
| Proposal Development  | Prioritized quarter | Working Group (Manager) |
| Review + Adoption | Pull request for proposed change submitted after consensus in the Working Group | Working Group (Manager) |
| Implementation | When decision made to consensus achieved on proposal | Working Group (Manager) |
| Released | Next quarterly release | Manager |

Each of these stages is discussed in more detail below.

=== ":fontawesome-solid-seedling: Need Identification"

    :material-calendar-start: Any TIDES Contributor identifies a need that should be addressed in the TIDES specification.

    :material-checkbox-multiple-marked-circle-outline: **Actions**:

    * A TIDES Contributor submits an issue to GitHub which identifies the need that they would like addressed and a rough assessment of its addressable audience.
    * TIDES Manager triages issue and asks for more detail from the Contributor if needed.
    * TIDES Manager determines if issue resolution would require a normative change.

    :material-check-underline: **Resolution**: TIDES Manager puts issue into consideration for next quarterly issue prioritization

=== ":material-chevron-triple-up: Prioritization"

    :material-calendar-start: The TIDES Manager starts a development cycle after or near the end of a quarterly release.

    :material-checkbox-multiple-marked-circle-outline: **Actions**:

    - [ ] TIDES Manager to solicit feedback from TIDES Contributors on which needs to prioritize.
    - [ ] TIDES Manager to propose a set of needs that the community will focus on resolving based on feedback and available community capacity.
    - [ ] TIDES Board will approve a set of needs to focus on based on TIDES Manager’s proposal and TIDES Contributors’ feedback.

    :material-check-underline: **Resolution**:  TIDES Manager will create a Milestone for the next release in GitHub and fill it with the issues the Board prioritized.

=== ":material-pencil: Proposal Development"

    :material-calendar-start: TIDES Manager, in consultation with the TIDES Board and TIDES Contributors, convenes an Issue Working Group to address a prioritized issue or set of interrelated issues.

    :material-checkbox-multiple-marked-circle-outline: **Actions**:

    - [ ] TIDES Manager convenes an Issue Working Group to develop a resolution to the issue.
    - [ ] The TIDES Manager will invite those who have expressed interest in the issue (including the issue creator and commenters) and who they believe will have an interest in the topic to take part on the Issue Working Group. They will also solicit participation from all TIDES Contributors.
    - [ ] Working Group members document discussion points about approach in the relevant github issue.
    - [ ] While consensus will be sought, if the Working Group members cannot come to a unanimous agreement about the solution, the TIDES Manager may ask the TIDES Board to make a decision after hearing feedback from various perspectives.
    - [ ] Working Group members update the schema and documentation according to the proposal on a feature branch.

    :material-check-underline: **Resolution**: Working Group submits a pull request to the `develop` branch.

=== ":octicons-comment-discussion-24: Review + :material-vote: Adoption"

    :material-calendar-start: TIDES Manager invites people outside of the Working Group to review and comment on the proposal

    :material-checkbox-multiple-marked-circle-outline: **Actions**:

    - [ ] The TIDES Manager MUST invite people outside of the Working Group to review and comment on the Pull Request for the proposal for a minimum of two weeks, making sure TIDES Contributors with different roles and backgrounds have had a chance to consider it.
    - [ ] The TIDES Manager MUST review the proposal for consistency with the Open Standards Definition maintained by the [Mobility Data Interoperability Principles](http://interoperablemobility.org).
    - [ ] The TIDES Manager MUST offer tools, services and  assistance to any TIDES Contributor who is unable to fluidly interact with the tooling used in the review process.
    - [ ] A minimum of three TIDES Contributors outside the Working Group MUST publicly comment on each proposal for it to move forward  and indicate a score of:
        * Accepted;
        * Accepted with minor changes; or
        * Substantially revised.
    - [ ] If 100% of reviewers accept, the proposal is adopted without need for further discussion.
    - [ ] If any reviewer accepts with minor changes, the suggested change must be considered by the Working Group.
        * If the Working Group decides to incorporate the edited proposal will be re-circulated for some period time greater than 72 hours and previous reviewers notified.  If nobody objects to the change in that time, it is adopted.
        * If the Working Group does not agree with the suggested change, they may appeal to the TIDES Board to make a final decision about its necessity.
    - [ ] If any reviewer requests substantial changes, they must also agree to work with the working group on developing an alternative solution to the need.
        * If the working group believes the substantial change request is invalid or without merit, they may appeal to the TIDES Board to make a final decision about if revisions are necessary.

    :material-check-underline: **Resolution:** Change as represented in the pull request from the feature branch is approved and merged into the `develop` branch.

=== ":fontawesome-solid-gears: Implementation"

    :material-calendar-start: Final change proposal is approved - although initial work can begin ahead of this.

    :material-checkbox-multiple-marked-circle-outline: **Actions**:

    - [ ] TIDES Manager MUST ensure the relevant accompanying documentation fleshed out.
    - [ ] TIDES Manager MUST ensure [Changelog](https://keepachangelog.com/en/1.1.0/) fully documented.
    - [ ] TIDES Manager MUST ensure sample datasets updated or added which support the new feature.
    - [ ] TIDES Manager MUST ensure any relevant updates to continuous integration and testing are completed.
    - [ ] TIDES Manager MAY make any number of [pre-release](#pre-releases)(s).
    - [ ] TIDES Manager MUST identify and ensure resolution of relevant conflicts among proposals as overseen by the TIDES Board or their designee.

    :material-check-underline: **Resolution**: [Requirements for release are met](#releases).

=== ":material-send-check: Release"

    :material-calendar-start: **Initiated**: On a quarterly schedule maintained by the TIDES Manager.

    :material-checkbox-multiple-marked-circle-outline: **Actions**:  See [Release Management](#versions-and-release-management).

### Expedited Change Management

This section outlines an expedited process for implementing changes in response to **Urgent Needs** which are critical to maintaining the security, compliance, or operational functionality of TIDES balancing rapid response with informed, transparent decision-making.

???+ info ":material-clock-fast: Urgent Needs"

    Urgent needs MUST pose significant risks to security, compliance, or the operational integrity of stakeholder systems. These MAY include necessary revisions due to legal mandates, critical security vulnerabilities, or severe technical inaccuracies that directly impair system functionalities. Urgent needs SHOULD necessitate an implementation timeline which is inconsistent with the normal [change-making process](#change-making-process).

#### Process

=== ":material-bell-ring-outline: Identification"

    Stakeholders SHOULD promptly report urgent needs to the TIDES Manager, detailing the problem and its potential impact.

=== ":material-head-question: Rapid Evaluation"

    The TIDES Manager MUST convene a group of at least 2 TIDES Contributors of their choosing to swiftly assess the issue's urgency and validity.

    1. If it meets their threshold for an urgent need, they forward a list of their proposed Urgent Working Group Members to the TIDES Board.
    2. The Urgent Working Group Members SHOULD contain representatives of TIDES Contributors affected stakeholder groups.
    3. The Urgent Working Group size SHOULD be at least three and reflect the scale of the problem and also need for agile decision making.  
    4. The TIDES Board MAY object to their characterization of the need as urgent.
    5. The TIDES Board MAY make changes to the Urgent Working Group members.
    6. If the TIDES Board fails to respond within 48 hours, the Urgent Working Group MAY proceed with their implicit approval.

=== ":material-pencil: Solution Identification"

    The Urgent Working Group, managed by the TIDES Manager, MUST identify a solution that meets the urgent need and document it as a PR to the `main` repository branch – outside the normal release cycle.  

=== ":material-vote: Decision-Making"

    A supermajority of the Urgent Working Group members MUST approve the proposed change to meet the urgent need.  If the decision is deadlocked, the decision is escalated to the TIDES Board.

=== ":fontawesome-solid-gears: Implementation"

    The rest of the implementation and release cycle mirrors the main [change-making process](#change-making-process).

## Versions and Release Management

A release is an official version of the TIDES data specification which can be referenced in perpetuity by a version number. The process by which a new release is made and determination of a version number is discussed below.

### Releases

!!! question "What triggers a release?"

    Each change to normative content in the `main` branch of the TIDES github repository MUST be considered a new release and assigned a [version number](#version-numbering).

Requirements:

- [ ] Each release MUST contain one or more changes to [normative content](#normative-content) which have been approved through the change-making process.
- [ ] Each release MUST be reviewed and approved in GitHub by 2+ members of the Board – or their designees – for accuracy and consistency with the changes’ intent.
- [ ] Each release MUST be tagged with its [version number](#version-numbering).
- [ ] Each release MUST have documentation available.
- [ ] Each release MUST have an entry in CHANGELOG.md.
- [ ] Each release MUST be [specified as a release on Github](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).
- [ ] Each release MUST be noticed to any TIDES mailing lists or discussion groups.
- [ ] Each release SHOULD have sample datasets (real or exemplary) which cover the normative changes in the release.

#### Pre-releases

!!! question "When might we create a pre-release?"

    Pre-releases MAY be made in order to evaluate and work on incrementally-approved changes.

    Each approved change to normative content in the `develop` branch of the TIDES github repository MAY be considered a pre-release and assigned a pre-release version number.

Requirements:

- [ ] Each pre-release MUST contain one or more changes to [normative content](#normative-content) which have been approved through the change-making process.
- [ ] Each pre-release MUST be reviewed and approved in GitHub by 1+ members of the board – or their designees – for accuracy and consistency with the changes’ intent.
- [ ] Pre-releases MUST be tagged with an appropriate pre-release version number:
    * Pre-releases that have incorporated all the normative changes for the target-release MUST have a **beta** version number;
    * otherwise, they MUST receive an **alpha** version number.
- [ ] Each pre-release MUST have documentation available.
- [ ] Each pre-release MUST have an entry in CHANGELOG.md.
- [ ] ach pre-release MAY be [specified as a pre-release on Github](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).

#### Release Frequency

!!! question "How often do we make new releases?"

    Barring significant unexpected events:

    * Major releases SHOULD be limited to no more than once per year;
    * Minor releases MAY be expected approximately quarterly.

### Version Numbering

TIDES [releases](#releases) MUST be reflected by an incremental version number based on a [semantic versioning](https://semver.org/) policy as detailed below.

=== "Releases"
    - [ ] Release versions MUST be named with incremental increases to the format [`<MAJOR>`](https://semver.org/#spec-item-8).[`<MINOR>`](https://semver.org/#spec-item-7).

=== "Pre-releases"

    - [ ] Pre-release versions MUST be named with the [`<MAJOR>`](https://semver.org/#spec-item-8).[`<MINOR>`](https://semver.org/#spec-item-7) of their target release name and appended with either:

    * `-alpha.<NUMBER>` where NUMBER starts at 1 and increases by 1 for each alpha release of that target release.
    * `-beta.<NUMBER>` where NUMBER starts at 1 and increases by 1 for each beta release of that target release.

!!! info "What is a Major vs Minor version?"

    * **Major** versions reflect backwards-incompatible changes
    * **Minor** versions change the [normative content](#normative-content) in a way that is backwards-compatible

!!! warning

    Non-normative changes MUST NOT increment the TIDES version.

## Version Control

**TIDES SHOULD be managed in Github or a  similar version-control tool.**

The following branches SHOULD always be maintained:

=== "`main`"
    Fully approved and documented [versions](#versions-and-release-management) of TIDES whereby:

    - [ ] Each commit reflecting a normative change MUST be tagged with [TIDES version number](#version-numbering).
    - [ ] Each commit reflecting a normative change MUST be released as a TIDES release version.
    - [ ] SHOULD only be committed to with an approved PR whereby:
        * PRs with normative changes MUST come from the `develop` branch.
        * If PRs come from the `develop` branch, they MUST be reviewed and approved in GitHub by 2+ members of the Board – or their designees – for accuracy and consistency with the changes’ intent and r[equirements for full release](#releases).
        * If PRs contain non-normative content, they MUST be reviewed and approved in GitHub by 2+ members of the board – or their designees – for accuracy and consistency with the changes’ intent.

=== "`develop`"
    Approved and staged versions of TIDES, awaiting full documentation, sample datasets, and next [quarterly release cycle](#release-schedule) whereby:

    - [ ] TIDES Manager MAY release commits periodically as a [pre-release](#pre-releases)(s).
    - [ ] SHOULD only be updated from `main` branch or PRs whereby:
        * TIDES Manager SHOULD periodically update this branch with any non-normative changes accepted into `main`.
        * PRs MUST be approved by TIDES Manager or their designee  and their approval MUST represent that:
            * the [governance process](#contributor-review-adoption) for approving a normative change to the standard has been met; and
            * that the change meets all the requirements outlined in the [pre-release requirements](#pre-releases).

=== "Feature Branches"

    All development by contributors SHOULD take place on _feature branches_ whereby.

    - [ ] Each branch SHOULD represent a maximum of one [change proposa](#change-making-stages)l.
    - [ ] Feature branches in the TIDES version control repository which have not been updated in 6 months MAY be archived.

## Attribution

**_This change management policy is adapted from:_**

* [Open Contracting Data Standard](https://standard.open-contracting.org/latest/en/governance/)

## Revision History

### v1.0 2023-11-29 Initial Version

* Converted from [draft document](https://docs.google.com/document/d/1UyQDlpdfz2oMwh9kFIby-Z6jDxArZmsY6WQyIl3sQBA/edit?usp=sharing)
