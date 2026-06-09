# Getting Started

> [!NOTE]
> If you would like to participate in TIDES community calls or subscribe for community updates, you can sign up via the [TIDES Community Interest Form](https://docs.google.com/forms/d/e/1FAIpQLSeb-YNZhnkn4PQ2yV25KvHJzyo40JtXPaTTWSLpDSRrwDpfEA/viewform).

If you are interested in adopting TIDES at your transit agency or other organization, this page can help you get started. 

## For leaders and executives

If you are a leader at an organization and you want your staff to start working on a TIDES adoption project, you will want to identify:

* **How TIDES aligns with your organization’s strategic priorities or initiatives** <br>
   TIDES can help with a variety of different use cases, from laying the foundation for a data warehouse to streamlining NTD reporting to preparing for an operational system migration. Which use case is most important for your organization? This will help set the technical direction and success criteria. For more information on general use cases for TIDES, see the ["TIDES: Transit Data Pipelines, Not Silos"](https://drive.google.com/file/d/1FeTWyRKnuIdj-SwxEiO8-xtUZQ_E0XzD/view) presentation. For more details on selected use cases, see [TIDES use case profiles](resources.md#use-case-profiles).

* **Technical feasibility** <br>
  A technical subject matter expert (someone with familiarity with operational data and/or analytics at your organization) can review [the section below](#for-technical-staff) to assess your organization’s technical readiness and approach.

* **Resourcing** <br>
  Once you have a sense for the technical feasibility, you can determine the right implementation pathway for your organization, whether that be procurement requirements for vendors, in-house work, consultant support, or a mix. 

## For technical staff

If you are a technical staff member getting started on a TIDES implementation, you will need the following:

* **Requirements for your use case (information gathered from your stakeholders)** <br>
  What do you need TIDES to do? The specific TIDES data that you need to produce and the format that it takes should be dictated by the use case. “Adopting TIDES” does not have to mean producing every single TIDES table at the same time. For example, NTD ridership reporting might dictate a different approach than a stop-level on-time performance dashboard. For more information on selected use cases, see [TIDES use case profiles](resources.md#use-case-profiles). Example requirements to consider:  
    * Data scope and features (what TIDES tables to produce and what type of analysis or reporting they need to support)  
    * Data format / access (how will the TIDES data be accessed by the downstream users?)  
    * Update frequency   
    * Alignment with other technical initiatives (for example, will this TIDES-based approach replace an existing workflow, or produce something net-new? Are new data tools being deployed at your organization that can be leveraged?)  
    * Cybersecurity and compliance (does the TIDES data you will produce contain any data that is considered PII or otherwise sensitive according to your organization’s policies? If so, what are the requirements for working with that data?)

* **Assess technical infrastructure** <br>
  Adopting TIDES does not require any specific tools or technologies, but it does require the technical capacity to ingest data, store it, transform it, and serve it to downstream systems (e.g., a business intelligence tool). Organizations can ingest, produce, or save TIDES in existing data infrastructure, or pair TIDES adoption with the deployment of new infrastructure and tools, depending on their needs and goals. For information on technical architecture considerations associated with TIDES, see [Implementation & Technical Architecture Guidance](resources.md#implementation-approaches-technical-architecture). For example code from other implementations, see [Implementation & Code Examples](resources.md#example-implementations-and-code).

* **Assess source data availability** <br>
  TIDES is a data format and to leverage it you will need access to the underlying data types from operational source systems: passenger counts, vehicle locations, or fare transactions. Once you have identified what TIDES table(s) are needed for your use case, you will need to ensure that you have access to the relevant source data, and that it meets your needs:
    * Does the source provide the core columns for the TIDES table(s) you want to produce? Compare the source data columns with the [TIDES table documentation](architecture.md#files-in-specification) and ensure it provides the required attributes. 
    * Do you have access to the location where the data is stored, and can you transfer it to the data environment where you will be working with it? 
    * Does the data update at the required frequency, and does your data infrastructure support the necessary update frequency?

* **Resourcing requirements** <br>
  Each organization will have a different approach to resourcing their TIDES initiatives. The previous requirements-gathering steps should clarify the scope of work to be done, and can then inform how that work can be performed, whether that be in-house, change or task orders to existing vendors, securing consultant support, or some combination. 
