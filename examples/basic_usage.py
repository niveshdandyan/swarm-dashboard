#!/usr/bin/env python3
"""
Basic usage example for swarm-dashboard.

This example demonstrates how to:
1. Launch the dashboard
2. Update agent task IDs for live tracking
3. Stop the dashboard
"""

from swarm_dashboard import launch_dashboard, update_agent_task_id, stop_dashboard


def main():
    # Define your agents
    agents = {
        "agent-1-core": {
            "role": "Core Architect",
            "wave": 1,
            "mission": "Set up project structure and dependencies",
        },
        "agent-2-backend": {
            "role": "Backend Developer",
            "wave": 2,
            "mission": "Build REST API endpoints",
        },
        "agent-3-frontend": {
            "role": "Frontend Developer",
            "wave": 2,
            "mission": "Create React components",
        },
        "agent-4-integration": {
            "role": "Integration Lead",
            "wave": 3,
            "mission": "Combine all outputs and test",
        },
    }

    # Launch dashboard
    swarm_dir = "/tmp/my-swarm-project"
    url = launch_dashboard(
        swarm_name="My Project Swarm",
        swarm_dir=swarm_dir,
        agents=agents,
        port=8080,
    )

    print(f"Dashboard launched: {url}")
    print(f"Swarm directory: {swarm_dir}")

    # After launching agents with Claude Code's Task tool,
    # update their task IDs for live activity tracking:
    #
    # task_result = Task(
    #     prompt="Build the backend API...",
    #     subagent_type="general-purpose",
    #     run_in_background=True
    # )
    # task_id = task_result["task_id"]  # Extract task ID
    #
    # update_agent_task_id(
    #     swarm_dir=swarm_dir,
    #     agent_id="agent-2-backend",
    #     task_id=task_id
    # )

    print("\nTo stop the dashboard later:")
    print(f"  stop_dashboard('{swarm_dir}')")


if __name__ == "__main__":
    main()
