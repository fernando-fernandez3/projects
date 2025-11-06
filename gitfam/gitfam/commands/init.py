"""Initialize a new GitFam project."""

import shutil
from pathlib import Path
from rich.console import Console

console = Console()


def initialize_project(project_path: Path):
    """Initialize a new GitFam project with all necessary directories and files."""
    project_path = project_path.resolve()
    
    # Create directory structure
    dirs = [
        'families',
        'templates',
        'tools',
        'docs',
    ]
    
    console.print(f"\n[cyan]Initializing GitFam project in: {project_path}[/cyan]\n")
    
    for dir_name in dirs:
        dir_path = project_path / dir_name
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            console.print(f"✓ Created {dir_name}/")
        else:
            console.print(f"• {dir_name}/ already exists")
    
    # Create .gitattributes for Git LFS
    gitattributes_content = """# GitFam - Git LFS Configuration
*.mp4 filter=lfs diff=lfs merge=lfs -text
*.mov filter=lfs diff=lfs merge=lfs -text
*.avi filter=lfs diff=lfs merge=lfs -text
*.mkv filter=lfs diff=lfs merge=lfs -text
*.pdf filter=lfs diff=lfs merge=lfs -text
"""
    
    gitattributes_path = project_path / '.gitattributes'
    if not gitattributes_path.exists():
        gitattributes_path.write_text(gitattributes_content, encoding='utf-8')
        console.print("✓ Created .gitattributes")
    
    # Create .gitignore
    gitignore_content = """# GitFam
.DS_Store
Thumbs.db
*.tmp
.vscode/
.idea/
__pycache__/
*.pyc
venv/
node_modules/
web/
"""
    
    gitignore_path = project_path / '.gitignore'
    if not gitignore_path.exists():
        gitignore_path.write_text(gitignore_content, encoding='utf-8')
        console.print("✓ Created .gitignore")
    
    # Create README placeholder
    readme_path = project_path / 'families' / '.gitkeep'
    if not readme_path.exists():
        readme_path.write_text("# Family branches will be created here\n", encoding='utf-8')
        console.print("✓ Created families/.gitkeep")
    
    console.print("\n[bold green]✓ GitFam project initialized![/bold green]")
    console.print("\n[bold]Next steps:[/bold]")
    console.print("1. Run [cyan]gitfam quick-start[/cyan] for guided setup")
    console.print("2. Or manually create branches with [cyan]gitfam create-branch[/cyan]")
    console.print("3. Initialize git: [cyan]git init && git add . && git commit -m 'Initial commit'[/cyan]")
