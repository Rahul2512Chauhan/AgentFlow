import argparse
import yaml
from utils.logger import log_info, log_error
from agents.planner_agent.planner_agent import PlannerAgent
from agents.tool_agent.tool_agent import ToolAgent


def run_workflow(workflow_config: dict):
    """Executes a workflow step by step."""
    results = {}
    for i, step in enumerate(workflow_config.get("workflow", []), 1):
        agent_name = step["agent"]
        params = step.get("params", {})

        log_info(f"[Runner] Step {i}: {agent_name} with params {params}")

        try:
            # create agent dynamically
            agent = globals().get(agent_name)
            if agent is None:
                # fallback → use ToolAgent for tool execution
                agent = ToolAgent(name=agent_name)

            agent_instance = agent() if callable(agent) else agent
            result = agent_instance.run(params)
            results[agent_name] = result
        except Exception as e:
            log_error(f"[Runner] Step {i} failed: {e}")
            results[agent_name] = {"status": "error", "message": str(e)}

    return results


def main():
    parser = argparse.ArgumentParser(description="Run AgentFlow workflows")
    parser.add_argument("--config", type=str, help="YAML config for workflow")
    parser.add_argument("--query", type=str, help="Natural language instruction")
    parser.add_argument("--num", type=int, default=3, help="Number of papers")
    parser.add_argument("--reset-cache", action="store_true", help="Reset PlannerAgent cache")
    args = parser.parse_args()

    if args.query:
        # 🔹 Use PlannerAgent (LLM or fallback)
        log_info(f"Running workflow from PlannerAgent: {args.query}")
        planner = PlannerAgent(reset_cache=args.reset_cache)
        workflow_config = planner.run({"instruction": args.query, "num_papers": args.num})
    else:
        # 🔹 Load rule-based workflow from YAML
        log_info(f"Running workflow from YAML: {args.config}")
        with open(args.config, "r") as f:
            workflow_config = yaml.safe_load(f)

    results = run_workflow(workflow_config)
    log_info("✅ Workflow completed")
    return results


if __name__ == "__main__":
    main()
