"""Create a new family branch."""

from pathlib import Path
from rich.console import Console
import questionary
from questionary import Style

console = Console()

custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),
    ('question', 'bold'),
    ('answer', 'fg:#00bcd4 bold'),
])


def create_family_branch_interactive():
    """Interactively create a new family branch."""
    
    console.print("\n[bold cyan]Create a Family Branch[/bold cyan]")
    console.print("A branch represents a family line, usually by surname and location.\n")
    
    # Get branch name
    branch_name = questionary.text(
        "Branch name (e.g., 'smith-california'):",
        style=custom_style,
        validate=lambda text: len(text) > 0 or "Branch name cannot be empty"
    ).ask()
    
    if not branch_name:
        return
    
    branch_name = branch_name.lower().replace(' ', '-')
    
    # Get description
    description = questionary.text(
        "Brief description:",
        style=custom_style,
        default=f"{branch_name.title()} family branch"
    ).ask()
    
    if not description:
        return
    
    # Create the branch
    branch_path = Path('families') / branch_name
    
    if branch_path.exists():
        console.print(f"[red]Error: Branch '{branch_name}' already exists![/red]")
        return
    
    # Create directory structure
    branch_path.mkdir(parents=True)
    (branch_path / 'members').mkdir()
    
    # Create README
    readme_content = f"""# {description.title()}

## Overview

[Add a brief description of this family branch - geographical location, time period covered, key ancestors]

## Family Tree

```
[Create a simple text-based family tree here]

Example:
├── Grandparent Name (b. 1920)
│   ├── Parent Name (b. 1945)
│   │   ├── Child Name (b. 1970)
│   │   └── Child Name (b. 1972)
│   └── Parent Name (b. 1948)
```

## Key Locations

- [City, State/Country] (Years)

## Notable Events

- **[Year]**: [Description of important family event]

## Family Members

See the [members](members/) directory for individual profiles.

## Interview Progress

- [ ] [Person Name] - Initial interview
- [ ] [Person Name] - Follow-up interview

## Notes

[Additional information about this family branch]
"""
    
    readme_path = branch_path / 'README.md'
    readme_path.write_text(readme_content, encoding='utf-8')
    
    console.print(f"\n[bold green]✓ Created family branch: {branch_name}[/bold green]")
    console.print(f"Location: {branch_path}")
    
    # Ask if they want to add a member now
    add_member_now = questionary.confirm(
        "\nWould you like to add a family member to this branch now?",
        style=custom_style,
        default=True
    ).ask()
    
    if add_member_now:
        from . import add_member
        console.print("")
        add_member.add_family_member_interactive(branch_name)
    else:
        console.print("\n[bold]Next steps:[/bold]")
        console.print(f"• Add family members: [cyan]gitfam add-family-member --branch {branch_name}[/cyan]")
        console.print(f"• Edit the README: [cyan]{readme_path}[/cyan]")
    
    return branch_name
