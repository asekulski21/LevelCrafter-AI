Procedural Game Level Generator using LLM
A novel application of Large Language Models for procedurally generating playable dungeon levels in real-time. This project leverages open-source LLMs to create diverse, engaging, and validated game levels without manual design.
Project Overview
Problem Statement
Game level design is a time-consuming and expensive process in game development. Procedural generation can help, but traditional algorithms often produce repetitive or implausible layouts. This project explores whether modern LLMs can generate high-quality, playable game levels that are both structurally sound and creatively diverse.
Proposed Method
We utilize TinyLlama, an open-source 1.1B parameter language model, to generate ASCII-based dungeon levels through carefully crafted prompts. The system includes LLM-based generation that prompts TinyLlama to generate level layouts, post-processing for validation and correction of generated levels, playability validation through graph-based reachability analysis, quality metrics using a multi-dimensional evaluation framework, and visualization for real-time rendering of generated levels.
Data Sources
Seed examples consist of hand-crafted training examples representing different level archetypes including corridors, rooms, and mazes. The generated dataset includes dynamically created levels with associated metadata and quality metrics. Evaluation data provides comprehensive metrics for each generated level including playability, connectivity, difficulty, and diversity scores.
Key Features
This system uses an open-source LLM, specifically TinyLlama, with no API costs. It provides real-time generation, producing levels in seconds. Playability validation ensures levels are solvable. Quality metrics offer multi-dimensional evaluation. Visualization provides both ASCII and graphical rendering. Batch processing allows generation and evaluation of multiple levels. An interactive mode provides a user-friendly CLI interface.
Installation
Prerequisites
The system requires Python 3.8 or higher. It needs 8GB or more RAM, with 16GB recommended. A GPU is optional but recommended for faster generation.
Setup
To set up the system, clone the repository and navigate to the ProjectForAIClass directory. Install the requirements using pip install with the requirements.txt file. The first run will automatically download the TinyLlama model, which is approximately 2.2GB.
Usage
Interactive Mode (Recommended)
Run the command python main.py interactive to launch an interactive menu where you can generate single levels with custom parameters, generate multiple levels for batch evaluation, view example levels, and visualize and save generated levels.
Command-Line Interface
To generate a single level, use the command python main.py generate with parameters for difficulty, treasures, monsters, and options to visualize and save.
To generate multiple levels, use the command python main.py batch with parameters for count, difficulty, and options to visualize and save.
To view example levels, use the command python main.py examples with the visualize option.
To evaluate generated levels, use the command python main.py evaluate with parameters for source and limit.
Level Format
Levels are represented as ASCII grids with the following tiles. The hash symbol represents a wall. A period represents the floor. The letter P represents the player start position. The letter E represents the exit. The letter T represents treasure. The letter M represents a monster. The letter K represents a key. The letter D represents a door.
Architecture
Core Components
The LLM Engine in llm_engine.py loads and manages the TinyLlama model, handles tokenization and generation, and provides configurable sampling parameters.
The Level Generator in level_generator.py creates prompts from specifications, parses LLM output into level grids, and post-processes and validates levels.
The Level Validator in level_validator.py checks structural requirements for player and exit positions, performs reachability analysis using BFS, and calculates connectivity metrics.
The Evaluator in evaluator.py computes playability scores, measures level difficulty, calculates diversity across multiple levels, and aggregates batch statistics.
The Visualizer in visualizer.py provides ASCII rendering for terminal output, graphical rendering using matplotlib, and batch visualization capabilities.
The Dataset Manager in dataset_manager.py manages seed examples and generated levels, handles data persistence and loading, and exports datasets for analysis.
Evaluation Metrics
Individual Level Metrics
The playability score is a binary check for essential elements and exit reachability. The connectivity score measures the percentage of walkable tiles reachable from start. The difficulty score is a composite measure based on monster density, treasure density, and puzzle elements. Treasure density is the ratio of treasure tiles to total tiles. Monster density is the ratio of monster tiles to total tiles. The overall score is a weighted combination of all metrics.
Batch Metrics
The diversity score measures average pairwise difference between generated levels. Statistical aggregation provides mean, standard deviation, minimum, and maximum for all metrics. The playability rate shows the percentage of generated levels that are playable.
Project Structure
The project structure includes main.py as the main entry point and CLI, config.py for configuration and constants, llm_engine.py for LLM loading and inference, level_generator.py for level generation logic, level_validator.py for validation and analysis, evaluator.py for metrics and evaluation, visualizer.py for visualization tools, dataset_manager.py for data management, requirements.txt for Python dependencies, README.md as this file, REPORT.md for the academic report, and a data directory containing examples and generated subdirectories for seed example levels and generated levels respectively.
Technical Approach
Prompt Engineering
The system uses a structured prompt template that specifies difficulty level, dimensions, required game elements, and formatting constraints.
Post-Processing Pipeline
The pipeline includes parsing to extract level grid from LLM output, normalization to ensure correct dimensions, validation to add missing essential elements, and boundary enforcement to ensure walls around the perimeter.
Quality Assurance
Graph-based reachability analysis ensures the exit is accessible. Statistical analysis identifies outliers. Visual inspection occurs through the rendering system.
Results
The system demonstrates high playability with approximately 80-90 percent of generated levels immediately playable. It shows structural diversity with significant variation in level layouts. Controllable difficulty means the difficulty parameter effectively influences level characteristics. Fast generation produces levels in 2-10 seconds depending on hardware.
Limitations
LLM hallucination occasionally generates invalid syntax. Some structural patterns repeat across generations. Very complex puzzle logic is challenging. Larger models may produce better results than the current model size.
Future Work
Future improvements include fine-tuning the model on a larger corpus of game levels, implementing advanced puzzle generation such as multi-key systems, adding support for multiple game genres including platformers and roguelikes, developing an interactive level editor with AI suggestions, and creating multiplayer level generation with theme consistency.
Citations and Acknowledgements
Models and Libraries
TinyLlama by Zhang et al. (2024) available at https://github.com/jzhang38/TinyLlama. Transformers by Hugging Face available at https://github.com/huggingface/transformers. PyTorch by Paszke et al. (2019) described as an imperative style, high-performance deep learning library. Matplotlib by Hunter, J. D. (2007) as a 2D graphics environment.
Inspiration
Summerville et al. (2018) on procedural content generation via machine learning. Guzdial et al. (2018) on co-creative level design via machine learning. Procedural generation in games like Rogue, NetHack, and Spelunky.
Additional Resources
ASCII dungeon generation techniques, graph theory for level connectivity analysis, and LLM prompting strategies for structured output.
License
This project is created for academic purposes as part of CSI-4130/5130: Artificial Intelligence course.
Author
Created for CSI-4130/5130 Artificial Intelligence Course Project
Contact
For questions or collaboration opportunities, please open an issue on GitHub.
Note: This project uses open-source models and does not require any paid API keys. All generation happens locally.
