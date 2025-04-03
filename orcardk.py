#!/usr/bin/env python3
"""
RecursiveDevKit - A tool for AI-assisted recursive software development

This CLI tool helps manage the RecursiveDevKit framework files and workflow,
making it easier to maintain context and generate effective prompts for
AI assistants.
"""

import argparse
import os
import datetime
import re
import sys
from pathlib import Path

VERSION = "0.1.0"

class RecursiveDevKit:
    """Main class for managing the RecursiveDevKit framework."""
    
    def __init__(self, project_dir="."):
        """Initialize the tool with project directory."""
        self.project_dir = project_dir
        self.context_file = os.path.join(project_dir, "project-context.md")
        self.state_file = os.path.join(project_dir, "development-state.md")
        self.prompt_file = os.path.join(project_dir, "prompt-template.md")
    
    def init(self, project_name, description, phases="3", initial_phase="Initialization"):
        """Initialize a new project with the framework files."""
        # Check if files already exist
        if os.path.exists(self.context_file) or os.path.exists(self.state_file) or os.path.exists(self.prompt_file):
            confirm = input("Framework files already exist. Overwrite? (y/n): ")
            if confirm.lower() != "y":
                print("Initialization canceled.")
                return
        
        # Create project-context.md
        context = f"""# Project Context

## Definition
{description}

## Current Phase: 1/{phases} - {initial_phase}
Progress: 0% complete

## Architecture
- Core system: Initial implementation pending
  - Base components: To be determined
- Infrastructure: Initial setup pending

## Dependencies
- None yet

## Development Principles
- Modularity
- Testability
- Maintainability
- Clear interfaces
- Documentation

## Technical Requirements
- Reliable operation
- Good performance
- Proper error handling
"""
        
        # Create development-state.md
        state = """# Development State

## High Priority
- CURRENT TASK: Initialize project structure
- COMPLETION CRITERIA: Repository structure and base files created
- WORKING FILES: Initial repository setup
- INTEGRATION POINTS: None yet

## Completed
- Framework initialization

## Next Tasks
1. Define initial architecture
   - Files: architecture documents, diagrams
   - Integration: Overall system design
2. Set up core components
   - Files: base implementation files
   - Integration: Component interfaces

## Challenges
- None yet

## Decisions
- Using RecursiveDevKit framework for development
  - Rationale: Structured approach to AI-assisted development
  - Alternatives: Ad-hoc prompting, traditional development
"""
        
        # Create prompt-template.md
        prompt = f"""Continue developing {project_name} focusing on the following task:

## Current Focus
- Task: Initialize project structure
- Files: Initial repository setup
- Integration points: None yet
- Completion criteria: Repository structure and base files created

## Project Context
- Project: {project_name} - {description}
- Current phase: 1/{phases} - {initial_phase}
- Progress: 0% complete
- Key architecture: Initial implementation pending
- Development principles: Modularity, Testability, Maintainability

## Current State
- Completed: Framework initialization
- Next tasks: Define initial architecture, Set up core components
- Challenges: None yet
- Recent decisions: Using RecursiveDevKit framework for development

## Implementation Requirements
1. The implementation should follow the project's development principles
2. Code should be properly documented with comments
3. Handle edge cases and potential errors
4. Integrate well with existing components
5. Be testable and maintainable

Please provide:
1. Implementation code for the current task including:
   - File paths and full implementation code
   - Any necessary changes to dependent files
   - Clear comments explaining key functionality

2. Updated task status for development-state.md:
   - Brief description of implementation approach
   - Key implementation details to document
   - Next logical task to tackle

3. Any architecture updates needed

4. Verification approach:
   - How to verify the implementation works correctly
   - Edge cases to test
   - Integration test approach if applicable
"""
        
        # Create directory if it doesn't exist
        os.makedirs(self.project_dir, exist_ok=True)
        
        # Write files
        with open(self.context_file, "w") as f:
            f.write(context)
        
        with open(self.state_file, "w") as f:
            f.write(state)
        
        with open(self.prompt_file, "w") as f:
            f.write(prompt)
        
        print(f"✅ Initialized {project_name} with RecursiveDevKit framework")
        print(f"   Created: {self.context_file}")
        print(f"   Created: {self.state_file}")
        print(f"   Created: {self.prompt_file}")
    
    def update_prompt(self, custom_focus=None):
        """Generate a new prompt based on current context and state."""
        # Check if files exist
        if not os.path.exists(self.context_file) or not os.path.exists(self.state_file):
            print("⚠️  Error: Context or state file not found. Run 'init' first.")
            return
        
        # Read context file
        with open(self.context_file, "r") as f:
            context = f.read()
        
        # Read state file
        with open(self.state_file, "r") as f:
            state = f.read()
        
        # Extract project name and description
        project_info = "Project"  # Default
        project_name = "Project"
        project_desc = ""
        
        # Extract from context file
        definition_match = re.search(r"## Definition\n(.*?)(?=\n##|\Z)", context, re.DOTALL)
        if definition_match:
            project_desc = definition_match.group(1).strip()
            project_info = f"{project_name} - {project_desc}"
        
        # Extract phase info
        phase_info = "Current phase"
        phase_match = re.search(r"## Current Phase: (.*?)\nProgress: (.*?)%", context, re.DOTALL)
        if phase_match:
            phase_info = f"{phase_match.group(1).strip()}"
            progress = f"{phase_match.group(2).strip()}"
        
        # Extract architecture
        arch_info = "Initial architecture"
        arch_match = re.search(r"## Architecture\n(.*?)(?=\n##|\Z)", context, re.DOTALL)
        if arch_match:
            arch_components = []
            for line in arch_match.group(1).strip().split("\n"):
                if line.startswith("- "):
                    arch_components.append(line[2:].strip())
            arch_info = ", ".join(arch_components)
        
        # Extract principles
        principles_info = "Modularity, Maintainability"
        principles_match = re.search(r"## Development Principles\n(.*?)(?=\n##|\Z)", context, re.DOTALL)
        if principles_match:
            principles = []
            for line in principles_match.group(1).strip().split("\n"):
                if line.startswith("- "):
                    principle_name = line[2:].split(":")[0].strip()
                    principles.append(principle_name)
            principles_info = ", ".join(principles)
        
        # Extract current task
        current_task = "implementation"  # Default
        if custom_focus:
            current_task = custom_focus
        else:
            task_match = re.search(r"- CURRENT TASK: (.*?)(?=\n|-|\Z)", state, re.DOTALL)
            if task_match:
                current_task = task_match.group(1).strip()
        
        # Extract completion criteria
        completion_criteria = "Task complete"
        criteria_match = re.search(r"- COMPLETION CRITERIA: (.*?)(?=\n|-|\Z)", state, re.DOTALL)
        if criteria_match:
            completion_criteria = criteria_match.group(1).strip()
        
        # Extract working files
        working_files = "relevant files"
        files_match = re.search(r"- WORKING FILES: (.*?)(?=\n|-|\Z)", state, re.DOTALL)
        if files_match:
            working_files = files_match.group(1).strip()
        
        # Extract integration points
        integration_points = "related components"
        integration_match = re.search(r"- INTEGRATION POINTS: (.*?)(?=\n|-|\Z)", state, re.DOTALL)
        if integration_match:
            integration_points = integration_match.group(1).strip()
        
        # Extract completed tasks
        completed_tasks = []
        completed_section = re.search(r"## Completed\n(.*?)(?=\n##|\Z)", state, re.DOTALL)
        if completed_section:
            for line in completed_section.group(1).strip().split("\n"):
                if line.startswith("- "):
                    completed_tasks.append(line[2:].strip())
        completed_info = ", ".join(completed_tasks[-3:])  # Last 3 completed tasks
        
        # Extract next tasks
        next_tasks = []
        next_section = re.search(r"## Next Tasks\n(.*?)(?=\n##|\Z)", state, re.DOTALL)
        if next_section:
            for line in next_section.group(1).strip().split("\n"):
                if re.match(r"^\d+\.\s", line):
                    task_name = re.sub(r"^\d+\.\s", "", line).strip()
                    next_tasks.append(task_name)
        next_info = ", ".join(next_tasks[:3])  # Next 3 tasks
        
        # Extract challenges
        challenges = []
        challenge_section = re.search(r"## Challenges\n(.*?)(?=\n##|\Z)", state, re.DOTALL)
        if challenge_section and "None yet" not in challenge_section.group(1):
            for line in challenge_section.group(1).strip().split("\n"):
                if line.startswith("- "):
                    challenge_name = line[2:].split(":")[0].strip()
                    challenges.append(challenge_name)
        challenge_info = ", ".join(challenges) if challenges else "None identified"
        
        # Extract recent decisions
        decisions = []
        decision_section = re.search(r"## Decisions\n(.*?)(?=\n##|\Z)", state, re.DOTALL)
        if decision_section:
            for line in decision_section.group(1).strip().split("\n"):
                if line.startswith("- "):
                    decision_name = line[2:].split(":")[0].strip()
                    decisions.append(decision_name)
        decision_info = ", ".join(decisions[-2:]) if decisions else "No recent decisions"
        
        # Create new prompt
        prompt = f"""Continue developing the project focusing on the following task:

## Current Focus
- Task: {current_task}
- Files: {working_files}
- Integration points: {integration_points}
- Completion criteria: {completion_criteria}

## Project Context
- Project: {project_info}
- Current phase: {phase_info}
- Progress: {progress}% complete
- Key architecture: {arch_info}
- Development principles: {principles_info}

## Current State
- Completed: {completed_info}
- Next tasks: {next_info}
- Challenges: {challenge_info}
- Recent decisions: {decision_info}

## Implementation Requirements
1. The implementation should follow the project's development principles
2. Code should be properly documented with comments
3. Handle edge cases and potential errors
4. Integrate well with existing components
5. Be testable and maintainable

Please provide:
1. Implementation code for the current task including:
   - File paths and full implementation code
   - Any necessary changes to dependent files
   - Clear comments explaining key functionality

2. Updated task status for development-state.md:
   - Brief description of implementation approach
   - Key implementation details to document
   - Next logical task to tackle

3. Any architecture updates needed

4. Verification approach:
   - How to verify the implementation works correctly
   - Edge cases to test
   - Integration test approach if applicable
"""
        
        # Write new prompt
        with open(self.prompt_file, "w") as f:
            f.write(prompt)
        
        print(f"✅ Updated prompt for task: {current_task}")
        print(f"   Prompt saved to {self.prompt_file}")
    
    def update_state(self, task_completed=None, next_task=None, criteria=None, files=None, integration=None, reset=False):
        """Update the development state file with completed and next tasks."""
        # Check if file exists
        if not os.path.exists(self.state_file):
            print("⚠️  Error: State file not found. Run 'init' first.")
            return
        
        # Read state file
        with open(self.state_file, "r") as f:
            state_content = f.read()
        
        # If reset is requested, reset the state file
        if reset:
            # Keep only the structure
            state_content = """# Development State

## High Priority
- CURRENT TASK: Initialize phase
- COMPLETION CRITERIA: Phase initialization complete
- WORKING FILES: Initial phase files
- INTEGRATION POINTS: None yet

## Completed
- Previous phase completion

## Next Tasks
1. First task in new phase
   - Files: To be determined
   - Integration: To be determined

## Challenges
- None yet

## Decisions
- Phase transition
  - Rationale: Previous phase completed
  - Alternatives: Continue previous phase
"""
        
        # Update completed tasks
        if task_completed:
            # Extract current task
            current_task = "implementation"
            task_match = re.search(r"- CURRENT TASK: (.*?)(?=\n|-|\Z)", state_content, re.DOTALL)
            if task_match:
                current_task = task_match.group(1).strip()
            
            # Add to completed section
            completed_pattern = r"(## Completed\n)"
            completed_replacement = f"\\1- {current_task}: {task_completed}\n"
            state_content = re.sub(completed_pattern, completed_replacement, state_content)
        
        # Update current task
        if next_task:
            # Update the CURRENT TASK
            state_content = re.sub(r"- CURRENT TASK: .*?\n", f"- CURRENT TASK: {next_task}\n", state_content)
            
            # Update completion criteria if provided
            if criteria:
                state_content = re.sub(r"- COMPLETION CRITERIA: .*?\n", f"- COMPLETION CRITERIA: {criteria}\n", state_content)
            
            # Update working files if provided
            if files:
                state_content = re.sub(r"- WORKING FILES: .*?\n", f"- WORKING FILES: {files}\n", state_content)
            
            # Update integration points if provided
            if integration:
                state_content = re.sub(r"- INTEGRATION POINTS: .*?\n", f"- INTEGRATION POINTS: {integration}\n", state_content)
        
        # Write updated state
        with open(self.state_file, "w") as f:
            f.write(state_content)
        
        action = "Reset" if reset else "Updated"
        print(f"✅ {action} development state")
        if task_completed:
            print(f"   Marked task as completed: {task_completed}")
        if next_task:
            print(f"   New current task: {next_task}")
    
    def update_phase(self, new_phase=None, progress=None):
        """Update the project phase in the context file."""
        # Check if file exists
        if not os.path.exists(self.context_file):
            print("⚠️  Error: Context file not found. Run 'init' first.")
            return
        
        # Read context file
        with open(self.context_file, "r") as f:
            context_content = f.read()
        
        # Update phase if provided
        if new_phase:
            context_content = re.sub(r"## Current Phase: .*?\n", f"## Current Phase: {new_phase}\n", context_content)
        
        # Update progress if provided
        if progress:
            context_content = re.sub(r"Progress: .*?%", f"Progress: {progress}%", context_content)
        
        # Write updated context
        with open(self.context_file, "w") as f:
            f.write(context_content)
        
        print(f"✅ Updated project phase: {new_phase}")
        if progress:
            print(f"   Progress: {progress}%")

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="RecursiveDevKit - Framework for AI-assisted development",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s init "My Project" --description "A new software project"
  %(prog)s prompt
  %(prog)s state --completed "Implemented basic file structure" --next "Create module X"
  %(prog)s phase --new "2/3 - Feature Development" --progress "0"
        """
    )
    parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a new project")
    init_parser.add_argument("project_name", help="Name of the project")
    init_parser.add_argument("--description", "-d", default="A software project", help="Project description")
    init_parser.add_argument("--phases", "-p", default="3", help="Number of planned phases")
    init_parser.add_argument("--initial-phase", "-i", default="Initialization", help="Name of the first phase")
    
    # Update prompt command
    prompt_parser = subparsers.add_parser("prompt", help="Generate a new prompt based on current state")
    prompt_parser.add_argument("--focus", "-f", help="Override the current task focus")
    
    # Update state command
    state_parser = subparsers.add_parser("state", help="Update the development state")
    state_parser.add_argument("--completed", "-c", help="Description of completed work")
    state_parser.add_argument("--next", "-n", help="Next task to focus on")
    state_parser.add_argument("--criteria", help="Completion criteria for next task")
    state_parser.add_argument("--files", help="Working files for next task")
    state_parser.add_argument("--integration", help="Integration points for next task")
    state_parser.add_argument("--reset", action="store_true", help="Reset state for new phase")
    
    # Update phase command
    phase_parser = subparsers.add_parser("phase", help="Update the project phase")
    phase_parser.add_argument("--new", help="New phase (e.g., '2/3 - Feature Development')")
    phase_parser.add_argument("--progress", help="Phase progress percentage (without %)")
    
    args = parser.parse_args()
    
    devkit = RecursiveDevKit()
    
    if args.command == "init":
        devkit.init(args.project_name, args.description, args.phases, args.initial_phase)
    elif args.command == "prompt":
        devkit.update_prompt(args.focus)
    elif args.command == "state":
        devkit.update_state(args.completed, args.next, args.criteria, args.files, args.integration, args.reset)
    elif args.command == "phase":
        devkit.update_phase(args.new, args.progress)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
