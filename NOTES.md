# Presentation Notes and Reference

## How to Run

For the presentation, use:
```
python main.py demo
```

Or for interactive mode:
```
python main.py
```

---

## What Each File Does

### config.py
Stores settings: model name, dimensions, prompt template.

### llm_engine.py  
Loads TinyLlama model and generates text from prompts.

### level_generator.py
Creates prompts, sends to LLM, parses output, fixes errors.

### validator.py
Uses BFS algorithm to check if player can reach exit.

### evaluator.py
Calculates quality scores: playability, connectivity.

### visualizer.py
Displays levels as text or colored images.

### main.py
Menu system and demo mode.

---

## Key Concepts to Explain

### What is TinyLlama?
A 1.1 billion parameter language model. Open-source, runs locally, no API costs.

### What is BFS (Breadth-First Search)?
Graph algorithm that finds all reachable positions from a starting point. We use it to check if the exit is reachable from the player.

How it works:
1. Start at player position, add to queue
2. Take position from queue, mark as visited
3. Add all walkable neighbors to queue
4. Repeat until queue is empty
5. Check if exit was visited

### What is Post-Processing?
The LLM sometimes makes mistakes. Post-processing:
- Removes invalid characters
- Fixes level dimensions
- Adds player/exit if missing
- Ensures walls around border

### What is Prompt Engineering?
Designing the input text to get the desired output from the AI. Our prompt tells the LLM:
- What role to play (level designer)
- What format to use (ASCII grid)
- What elements to include (player, exit, monsters)

---

## Level Symbols

| Symbol | What it is |
|--------|-----------|
| # | Wall (can't walk through) |
| . | Floor (walkable) |
| P | Player start position |
| E | Exit (goal) |
| T | Treasure |
| M | Monster |

---

## Metrics Explained

**Playability**: Yes/No - can the player reach the exit?

**Connectivity**: 0.0 to 1.0 - what fraction of floor tiles are reachable from the player? Higher is better.

**Score**: 0.0 to 1.0 - overall quality combining playability, connectivity, and content.

---

## Common Questions and Answers

**Q: Why TinyLlama?**
A: It's open-source, free, and small enough to run on a laptop. Shows that even small LLMs can generate structured content.

**Q: How do you know a level is playable?**
A: BFS algorithm explores all tiles reachable from the player. If the exit is in that set, it's playable.

**Q: What if the AI outputs garbage?**
A: Post-processing cleans it up - removes bad characters, fixes dimensions, adds missing elements.

**Q: What's the playability rate?**
A: Around 80-90% of generated levels are playable without manual fixes.

**Q: How long does generation take?**
A: 2-10 seconds depending on hardware.

**Q: How is this different from traditional procedural generation?**
A: Traditional algorithms follow fixed rules. LLMs can understand concepts like "hard" or "maze-like" more naturally because they learned from text data.

**Q: What are the limitations?**
A: Sometimes generates invalid output (fixed by post-processing). Complex puzzles are difficult. Larger models would do better.

---

## Presentation Flow

1. Introduce the problem (level design is expensive)
2. Explain the solution (LLM + validation)
3. Run the demo
4. Show the metrics
5. Discuss results and limitations

---

## If Something Goes Wrong

If the model fails to load:
"The model requires significant memory. Let me show the example levels instead."

If generation produces bad output:
"This shows why we need post-processing - the AI sometimes makes mistakes."

If visualization doesn't work:
"The ASCII version shows the same information."

