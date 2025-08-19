from agents.tool_agent.tool_agent import ToolAgent

# Initialize ToolAgent with all tools
agent = ToolAgent(tool_names=["web_search", "pdf_parser", "memory"])

# 1. Search for papers
search_result = agent.run({
    "tool": "web_search",
    "args": {"query": "graph neural networks"}
})
print("\n[Step 1] Search Result Keys:", search_result.keys())

# Pick one paper
papers = search_result["result"].get("papers", [])
if not papers:
    print("❌ No papers found.")
    exit()
paper = papers[0]
pdf_url = paper["pdf_url"]

print(f"\n[Step 2] Using first paper: {paper['title']}")

# 2. Parse PDF
parse_result = agent.run({
    "tool": "pdf_parser",
    "args": {"pdf_path": f"data/papers/{pdf_url.split('/')[-1]}"}
})
print("[Step 2] Parsed length:", parse_result["result"]["length"])

paper_id = paper["pdf_url"].split("/")[-1].replace(".pdf", "")


# 3. Store in Memory
agent.run({
    "tool": "memory",
    "args": {
        "action": "store",
        "paper_id": paper["id"],
        "key": "parsed_text",
        "value": parse_result["result"]["text"][:500]  # just first 500 chars
    }
})

# 4. Load from Memory
load_result = agent.run({
    "tool": "memory",
    "args": {"action": "load", "paper_id": paper["id"], "key": "parsed_text"}
})
print("\n[Step 4] Loaded from memory:", load_result["result"][:200])
