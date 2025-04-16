flowchart TD
    %% External Entities
    User([User]) --> InputData[Raw Image Stacks]
    User --> SegMasks[Manual Cell Masks]

    %% Processes
    InputData --> P1[Split Channels]
    P1 --> GFP[GFP Channel]
    P1 --> RFP[RFP Channel]

    GFP --> P2[Max Projection]
    P2 --> GFP_Proj[Max GFP Projection]
    GFP_Proj --> User

    
    D6 --> P3[Load Data]
    D5 --> P3
    SegMasks --> P3[Load Data]

    P3 --> P4[Segment Stacks]
    P4 --> P5[Find Active Slices]
    P5 --> P6[Measure Copy Number]

    %% Outputs
    P6 --> CSV[Processed CSV Output]
    P6 --> Stats[Summary Statistics]
    P6 --> Plots[Intensity Plots]
    P6 --> Metadata[Metadata JSON]

    %% Data Stores (if applicable)
    Stats --> D1[(stats.csv)]
    Plots --> D2[(plot.png)]
    Metadata --> D3[(metadata.json)]
    CSV --> D4[(cell_data.csv)]
    GFP --> D5[(GFP.tif)]
    RFP --> D6[(RFP.tif)]

    %% Styles
    style P1 fill:#fef5e7,stroke:#f5b041,stroke-width:2px
    style P2 fill:#fef5e7,stroke:#f5b041,stroke-width:2px
    style P3 fill:#fef5e7,stroke:#f5b041,stroke-width:2px
    style P4 fill:#fef5e7,stroke:#f5b041,stroke-width:2px
    style P5 fill:#fef5e7,stroke:#f5b041,stroke-width:2px
    style P6 fill:#fef5e7,stroke:#f5b041,stroke-width:2px


    style InputData fill:#d6eaf8,stroke:#3498db,stroke-width:2px
    style SegMasks fill:#f9ebea,stroke:#e74c3c,stroke-width:2px

    style D1 fill:#d4f4dd,stroke:#2ecc71,stroke-width:2px
    style D2 fill:#d4f4dd,stroke:#2ecc71,stroke-width:2px
    style D3 fill:#d4f4dd,stroke:#2ecc71,stroke-width:2px
    style D4 fill:#d4f4dd,stroke:#2ecc71,stroke-width:2px
    style D5 fill:#d4f4dd,stroke:#2ecc71,stroke-width:2px
    style D6 fill:#d4f4dd,stroke:#2ecc71,stroke-width:2px
