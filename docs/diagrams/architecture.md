graph TD
    A1[Raw image stacks] --> A[run_preprocess.py] 
    A --> B[preprocess.py]
    B --> C["Split Channels"]
    C --> D1[GFP stacks]
    C --> D2[RFP stacks]
    B --> E["Max Projection (GFP)"]
    E --> F[Max GFP Projection]

     H[Cellpose Masks png files] --> G[segmentation.py]
    F --> H

    I[analysis.py] --> J[segment_stacks]
    I --> K[find_active_slices]
    I --> L[cell_intensity]
    I --> M[save_processed_data]
    M --> N[Final CSV Output]

    O[Pipeline.py] --> G
    O --> I
    O --> P[Load Data]
    D1 --> P
    D2 --> P
    O --> Q[Plots]
    O --> R[Stats]
    R --> W[stats.csv]
    Q --> X1[plot.png]
    Q --> X2[plot.png]
    O --> S[Metadata]
    S --> V[metadata.json]

    T[plot_only.py] --> Q
    T --> S

    


    %% Highlighting outputs
    style A1 fill:#d6eaf8,stroke:#3498db,stroke-width:2px
    style D1 fill:#d6eaf8,stroke:#3498db,stroke-width:2px
    style D2 fill:#d6eaf8,stroke:#3498db,stroke-width:2px
    style F fill:#d6eaf8,stroke:#3498db,stroke-width:2px
    style H fill:#f9ebea,stroke:#e74c3c,stroke-width:2px
    style N fill:#d4f4dd,stroke:#2ecc71,stroke-width:2px
    style V fill:#d4f4dd,stroke:#2ecc71,stroke-width:2px
    style W fill:#d4f4dd,stroke:#2ecc71,stroke-width:2px
    style X1 fill:#d4f4dd,stroke:#2ecc71,stroke-width:2px
    style X2 fill:#d4f4dd,stroke:#2ecc71,stroke-width:2px
