from langchain_core.tools import tool


@tool
def research_lookup(query: str) -> str:
    """Look up detailed research information for a given query."""
    mock_data = {
        # ── Original topics ────────────────────────────────────────────────────
        "ai": (
            "Artificial Intelligence (AI) Research Summary:\n"
            "- Large Language Models (LLMs) have achieved human-level performance on many NLP benchmarks.\n"
            "- Transformer architectures dominate modern AI, enabling models like GPT-4, Claude, and Gemini.\n"
            "- Reinforcement Learning from Human Feedback (RLHF) is the primary alignment technique in use.\n"
            "- Multimodal models now process text, images, audio, and video in unified pipelines.\n"
            "- Key challenges remain: hallucination, interpretability, energy efficiency, and safety.\n"
            "- Industry adoption is accelerating across healthcare, finance, legal, and software engineering."
        ),
        "climate": (
            "Climate Change Research Summary:\n"
            "- Global average temperature has risen ~1.2°C above pre-industrial levels as of 2024.\n"
            "- CO2 concentrations exceeded 420 ppm for the first time in human history in 2023.\n"
            "- Renewable energy (solar + wind) now accounts for over 30% of global electricity generation.\n"
            "- Arctic sea ice is declining at ~13% per decade, accelerating permafrost thaw.\n"
            "- IPCC reports indicate a 1.5°C threshold could be crossed before 2035 under current trajectories.\n"
            "- Carbon capture and storage (CCS) technologies are scaling but remain costly."
        ),
        "quantum": (
            "Quantum Computing Research Summary:\n"
            "- IBM, Google, and IonQ are leading the race toward fault-tolerant quantum systems.\n"
            "- Google's Willow chip demonstrated quantum error correction below threshold in 2024.\n"
            "- Quantum advantage has been demonstrated for specific sampling and optimization problems.\n"
            "- Qubit coherence times are improving via topological and error-corrected approaches.\n"
            "- Post-quantum cryptography (NIST PQC standards finalized 2024) is being rolled out globally.\n"
            "- Practical general-purpose quantum computing is projected 10–20 years away."
        ),
        "health": (
            "Healthcare & Biomedical Research Summary:\n"
            "- mRNA vaccine platforms have expanded beyond COVID-19 to influenza, RSV, and cancer.\n"
            "- AlphaFold 3 has solved protein-ligand interaction prediction, accelerating drug discovery.\n"
            "- GLP-1 receptor agonists (e.g., semaglutide) show efficacy across obesity, diabetes, and CVD.\n"
            "- CRISPR-based therapies have received FDA approval for sickle cell disease in 2023.\n"
            "- Wearable biosensors now enable continuous glucose, ECG, and biomarker monitoring.\n"
            "- Mental health crisis persists globally with AI-assisted diagnostics emerging as a tool."
        ),
        # ── New topics ─────────────────────────────────────────────────────────
        "space": (
            "Space Exploration Research Summary:\n"
            "- NASA's Artemis program is targeting crewed lunar landings by 2026 after the successful Artemis I orbital mission in 2022.\n"
            "- The James Webb Space Telescope (JWST) is observing galaxies up to 13.5 billion light-years away in unprecedented detail.\n"
            "- SpaceX's Starship, the most powerful rocket ever built, completed successful orbital test flights in 2024.\n"
            "- NASA's Perseverance rover is collecting Martian rock samples for a future return mission targeting the 2030s.\n"
            "- Private space economy is booming: satellite broadband (Starlink), space tourism, and lunar resource extraction are all active.\n"
            "- Commercial space stations (Axiom Space, Blue Origin) are in development to replace the ISS after 2030."
        ),
        "crypto": (
            "Cryptocurrency & Blockchain Research Summary:\n"
            "- Bitcoin spot ETFs were approved by the SEC in January 2024, opening the asset class to institutional investors.\n"
            "- Ethereum's Proof-of-Stake transition (The Merge, 2022) reduced its energy consumption by ~99.95%.\n"
            "- Total crypto market cap fluctuates between $1–3 trillion; Bitcoin dominance holds around 50%.\n"
            "- DeFi (Decentralized Finance) protocols collectively hold over $50 billion in total value locked (TVL).\n"
            "- NFT trading volumes peaked in 2021–2022 and contracted sharply; utility NFTs for gaming and ticketing persist.\n"
            "- Over 130 countries are exploring Central Bank Digital Currencies (CBDCs), with China's digital yuan in active pilot."
        ),
        "cyber": (
            "Cybersecurity Research Summary:\n"
            "- Ransomware attacks cost global organizations an estimated $20 billion+ in 2023; healthcare is the top target sector.\n"
            "- Zero-trust security architecture is replacing perimeter-based defenses as the enterprise standard.\n"
            "- AI-powered attacks — deepfake phishing, automated vulnerability scanning — are escalating at scale.\n"
            "- The U.S. National Cybersecurity Strategy (2023) shifts liability for insecure software to vendors, not users.\n"
            "- Post-quantum cryptography standards finalized by NIST in 2024 are being rolled out to replace RSA/ECC.\n"
            "- Supply chain attacks (SolarWinds, XZ Utils backdoor) highlight the risk of software dependency chains."
        ),
        "robot": (
            "Robotics & Automation Research Summary:\n"
            "- Humanoid robots (Tesla Optimus, Figure 01, Boston Dynamics Atlas) are moving from labs toward commercial deployment.\n"
            "- Global industrial robot installations exceeded 500,000 units per year in 2023, led by automotive and electronics.\n"
            "- Collaborative robots (cobots) work safely alongside humans and are driving adoption in small and mid-size enterprises.\n"
            "- Robotic surgery platforms (da Vinci, CMR Surgical) are improving precision in minimally invasive procedures.\n"
            "- Autonomous mobile robots (AMRs) in warehouses (Amazon, DHL) are reshaping logistics and last-mile fulfillment.\n"
            "- AI integration is enabling robots to handle unstructured tasks that previously required human dexterity."
        ),
        "energy": (
            "Energy & Renewables Research Summary:\n"
            "- Solar PV costs have dropped over 90% in the last decade, making it the cheapest electricity source in history.\n"
            "- Global wind capacity surpassed 1 terawatt in 2023; offshore wind is the fastest-growing segment.\n"
            "- Battery storage (lithium-ion and emerging solid-state) is critical for grid stability as intermittent renewables scale.\n"
            "- Green hydrogen is emerging as a clean fuel for hard-to-decarbonize sectors: steel, shipping, and aviation.\n"
            "- Nuclear is seeing a renaissance — small modular reactors (SMRs) and private fusion startups (Commonwealth Fusion) are advancing.\n"
            "- Global clean energy investment exceeded $1.8 trillion in 2023, surpassing fossil fuel investment for the first time."
        ),
        "education": (
            "Education & EdTech Research Summary:\n"
            "- The global EdTech market reached $142 billion in 2023 and is projected to exceed $500 billion by 2030.\n"
            "- AI tutoring tools (Khan Academy's Khanmigo, Duolingo Max) personalize learning at scale for millions of students.\n"
            "- Online learning platforms (Coursera, edX) have enrolled over 220 million learners worldwide.\n"
            "- COVID-19 learning loss set back students in low-income countries by 1–2 grade levels on average.\n"
            "- Micro-credentials and skills-based hiring are increasingly challenging the traditional 4-year degree model.\n"
            "- Adaptive learning software tracks real-time student progress and adjusts difficulty and pacing automatically."
        ),
        "economy": (
            "Economics & Global Economy Research Summary:\n"
            "- Global GDP growth moderated to ~2.6% in 2024 amid persistent inflation and tight monetary policy.\n"
            "- Major central banks (US Fed, ECB, Bank of England) raised interest rates to multi-decade highs in 2022–2024.\n"
            "- AI-driven automation is projected to displace 85 million jobs while creating 97 million new roles by 2025 (WEF).\n"
            "- US national debt exceeded $35 trillion in 2024; long-term debt sustainability is a growing fiscal concern.\n"
            "- Emerging markets — India, Vietnam, Indonesia — are outpacing advanced economies in GDP growth.\n"
            "- Supply chain diversification ('friend-shoring', 'near-shoring') is reshaping global trade patterns post-pandemic."
        ),
        "biotech": (
            "Biotechnology Research Summary:\n"
            "- Synthetic biology enables design of novel organisms for medicine, sustainable materials, and clean fuels.\n"
            "- Cell and gene therapies (CAR-T, base editing) are expanding from rare diseases toward broader medical applications.\n"
            "- Precision fermentation is producing animal-free proteins, dairy alternatives, and specialty materials at industrial scale.\n"
            "- DNA data storage can hold 215 petabytes per gram, offering ultra-dense long-term archival solutions.\n"
            "- The global biotech market is valued at over $1.3 trillion and growing at ~13% compound annual growth rate.\n"
            "- Biomanufacturing is recognized as a national security priority by the US, EU, and China."
        ),
    }

    query_lower = query.lower()
    for keyword, summary in mock_data.items():
        if keyword in query_lower:
            return summary

    return (
        f"General Research Summary for '{query}':\n"
        "- This is a rapidly evolving field with significant recent publications.\n"
        "- Multiple peer-reviewed studies confirm foundational theories in this domain.\n"
        "- Cross-disciplinary collaboration is driving breakthroughs at an accelerating pace.\n"
        "- Key open problems remain around scalability, cost-efficiency, and real-world deployment.\n"
        "- Leading research institutions include MIT, Stanford, Oxford, and various national labs.\n"
        "- Commercial applications are expected within 3-5 years based on current development pace."
    )
