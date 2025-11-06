"""GitFam CLI - Interactive family tree builder."""

import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
import questionary
from questionary import Style

from .commands import init, add_member, add_branch, build_web, generate_metadata

console = Console()

custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),
    ('question', 'bold'),
    ('answer', 'fg:#00bcd4 bold'),
    ('pointer', 'fg:#673ab7 bold'),
    ('highlighted', 'fg:#673ab7 bold'),
    ('selected', 'fg:#00bcd4'),
    ('separator', 'fg:#cc5454'),
    ('instruction', ''),
    ('text', ''),
])


@click.group()
@click.version_option()
def main():
    """
    GitFam - Preserve your family's legacy.
    
    Interactive CLI tool for building and managing your family history.
    """
    pass


@main.command()
@click.option('--path', default='.', help='Path to initialize GitFam project')
def init_project(path):
    """Initialize a new GitFam project."""
    console.print(Panel.fit(
        "[bold cyan]Welcome to GitFam![/bold cyan]\n\n"
        "Let's set up your family history project.",
        title="🌳 GitFam Setup"
    ))
    
    init.initialize_project(Path(path))


@main.command()
@click.option('--branch', help='Family branch name (e.g., smith-california)')
def add_family_member(branch):
    """Add a new family member interactively."""
    add_member.add_family_member_interactive(branch)


@main.command()
def create_branch():
    """Create a new family branch."""
    add_branch.create_family_branch_interactive()


@main.command()
@click.option('--output', default='./web', help='Output directory for web viewer')
def generate_website(output):
    """Generate a static website from your family tree."""
    console.print("[cyan]Building family tree website...[/cyan]")
    build_web.generate_static_site(Path(output))


@main.command()
@click.option('--format', type=click.Choice(['json', 'yaml', 'summary']), default='summary', help='Output format')
@click.option('--branch', help='Generate metadata for specific branch only')
def metadata(format, branch):
    """Generate metadata and statistics for your family tree."""
    generate_metadata.generate_metadata(output_format=format, branch=branch)


@main.command()
def quick_start():
    """Quick start wizard - set up everything interactively."""
    console.print(Panel.fit(
        "[bold cyan]GitFam Quick Start Wizard[/bold cyan]\n\n"
        "This wizard will help you:\n"
        "• Create your first family branch\n"
        "• Add your first family member\n"
        "• Set up the project structure\n\n"
        "[dim]Press Ctrl+C at any time to cancel[/dim]",
        title="🚀 Quick Start"
    ))
    
    if not questionary.confirm(
        "Ready to begin?",
        style=custom_style,
        default=True
    ).ask():
        console.print("[yellow]Setup cancelled.[/yellow]")
        return
    
    if not Path('families').exists():
        console.print("\n[yellow]No GitFam project found in current directory.[/yellow]")
        if questionary.confirm(
            "Initialize GitFam here?",
            style=custom_style,
            default=True
        ).ask():
            init.initialize_project(Path('.'))
        else:
            console.print("[red]Please run this command from a GitFam project directory.[/red]")
            return
    
    console.print("\n[bold cyan]Step 1: Create Your Family Branch[/bold cyan]")
    add_branch.create_family_branch_interactive()
    
    console.print("\n[bold cyan]Step 2: Add Your First Family Member[/bold cyan]")
    
    branches = [d.name for d in Path('families').iterdir() if d.is_dir() and not d.name.startswith('.')]
    if branches:
        branch = questionary.select(
            "Which family branch?",
            choices=branches,
            style=custom_style
        ).ask()
        
        if branch:
            add_member.add_family_member_interactive(branch)
    
    console.print(Panel.fit(
        "[bold green]✓ Setup Complete![/bold green]\n\n"
        "Your GitFam project is ready!\n\n"
        "[bold]Next steps:[/bold]\n"
        "• Add more family members: [cyan]gitfam add-family-member[/cyan]\n"
        "• Record interviews using the guide in templates/\n"
        "• Generate a website: [cyan]gitfam generate-website[/cyan]\n"
        "• Commit your changes: [cyan]git add . && git commit[/cyan]",
        title="🎉 All Set!"
    ))


if __name__ == '__main__':
    main()
