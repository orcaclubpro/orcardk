# RecursiveDevKit

A streamlined framework for AI-assisted software development that enables structured, iterative improvement through intelligent prompting.

## What is RecursiveDevKit?

RecursiveDevKit is a lightweight framework designed to enhance software development productivity through structured collaboration with AI assistants like Claude. It provides:

- **Consistent Context Management**: Maintain project context across development iterations
- **Priority-Focused Development**: Keep high-priority tasks at the forefront
- **Recursive Improvement**: Iteratively build and enhance your software
- **Structured Documentation**: Automatically track progress and decisions

Unlike traditional development frameworks that focus on code structure or testing methodologies, RecursiveDevKit optimizes the interaction between human developers and AI assistants to create a seamless, productive workflow.

## Core Principles

1. **Phase-Based Development**: Break projects into clear phases with specific deliverables
2. **Context Continuity**: Maintain context across multiple AI interactions
3. **Priority-Driven Implementation**: Focus on critical path tasks first
4. **Recursive Enhancement**: Build on previous work systematically
5. **Minimal Documentation Overhead**: Document just enough to maintain context

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/recursive-devkit.git

# Navigate to the repository
cd recursive-devkit

# Install the CLI tool (optional)
pip install -e .
```

### Initialize a New Project

```bash
# Using the CLI tool
recursive-devkit init "My Project" --description "A new software project"

# Or manually create the core files:
# - project-context.md
# - development-state.md
# - prompt-template.md
```

### Development Workflow

1. **Initialize**: Set up your project with the core files
2. **Prompt**: Generate a prompt based on current state
3. **Implement**: Submit prompt to AI assistant and implement suggestions
4. **Update**: Update project state with completed work
5. **Repeat**: Generate a new prompt and continue development

```bash
# After implementing a task, update the state
recursive-devkit state --completed "Implemented feature X" --next "Create component Y"

# Generate a new prompt for AI assistance
recursive-devkit prompt

# Copy the content of prompt-template.md to your AI assistant
```

## Core Files

### project-context.md

Contains the high-level project information, including:
- Project definition and objectives
- Current development phase
- Key architectural components
- Core development principles

### development-state.md

Tracks the current state of development:
- High-priority tasks
- Completed work
- Next steps
- Current challenges

### prompt-template.md

Template for generating AI prompts:
- Current focus task
- Relevant project context
- Development state summary
- Clear request for implementation

## Advanced Usage

### Phase Transitions

When completing a development phase:

```bash
# Update project context with new phase
recursive-devkit phase --new "2/3 - Feature Development" --progress "0%"

# Reset development state with new phase tasks
recursive-devkit state --reset --next "Implement core feature"
```

### Custom Templates

You can customize the prompt template in `prompt-template.md` to fit your specific needs:
- Add specialized sections for your project
- Include more detailed technical requirements
- Customize output format requests

## Best Practices

1. **Focus on One Task**: Keep each prompt focused on a single, well-defined task
2. **Maintain Context**: Ensure relevant context is included in each prompt
3. **Document Challenges**: Record difficulties and open questions
4. **Validate Implementations**: Always verify AI-suggested implementations
5. **Update State Promptly**: Keep the development state current

## Example Project

See the `examples/` directory for a sample project using RecursiveDevKit:
- `examples/chat-app/`: A simple chat application built using the framework
- `examples/workflow/`: Step-by-step workflow demonstration

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT License - See [LICENSE](LICENSE) for details.
