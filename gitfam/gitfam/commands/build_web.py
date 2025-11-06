"""Build static website from family tree."""

import re
from pathlib import Path
from typing import Dict, List, Any
from rich.console import Console
import yaml

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    from markdown import markdown
except ImportError:
    Environment = None
    markdown = None

console = Console()


def parse_frontmatter(content: str) -> tuple[Dict[str, Any], str]:
    """Parse YAML frontmatter from markdown file."""
    if not content.startswith('---'):
        return {}, content
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    
    try:
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2].strip()
        return frontmatter or {}, body
    except:
        return {}, content


def collect_family_data(families_path: Path) -> Dict[str, Any]:
    """Collect all family tree data from markdown files."""
    data = {
        'branches': [],
        'members': [],
        'stats': {
            'total_members': 0,
            'total_interviews': 0,
            'total_branches': 0
        }
    }
    
    if not families_path.exists():
        return data
    
    for branch_path in families_path.iterdir():
        if not branch_path.is_dir() or branch_path.name.startswith('.'):
            continue
        
        branch_data = {
            'name': branch_path.name,
            'display_name': branch_path.name.replace('-', ' ').title(),
            'path': branch_path.name,
            'members': []
        }
        
        # Read branch README if exists
        branch_readme = branch_path / 'README.md'
        if branch_readme.exists():
            content = branch_readme.read_text(encoding='utf-8')
            frontmatter, body = parse_frontmatter(content)
            branch_data['description'] = body.split('\n')[0].replace('#', '').strip()
        
        # Collect members
        members_path = branch_path / 'members'
        if members_path.exists():
            for member_path in members_path.iterdir():
                if not member_path.is_dir():
                    continue
                
                profile_path = member_path / 'profile.md'
                if not profile_path.exists():
                    continue
                
                content = profile_path.read_text(encoding='utf-8')
                frontmatter, body = parse_frontmatter(content)
                
                member_data = {
                    'slug': member_path.name,
                    'name': frontmatter.get('name', member_path.name),
                    'birth_date': frontmatter.get('birth_date', ''),
                    'birth_place': frontmatter.get('birth_place', ''),
                    'relationships': frontmatter.get('relationships', []),
                    'interviews': frontmatter.get('interviews', []),
                    'branch': branch_path.name,
                    'profile_content': body,
                    'has_photos': (member_path / 'photos').exists() and any((member_path / 'photos').iterdir()),
                    'has_videos': (member_path / 'interviews' / 'videos').exists() and any((member_path / 'interviews' / 'videos').iterdir())
                }
                
                branch_data['members'].append(member_data)
                data['members'].append(member_data)
                data['stats']['total_members'] += 1
                data['stats']['total_interviews'] += len(member_data['interviews'])
        
        data['branches'].append(branch_data)
        data['stats']['total_branches'] += 1
    
    return data


def generate_static_site(output_path: Path):
    """Generate a static HTML website from the family tree."""
    
    if Environment is None:
        console.print("[red]Error: Web generation requires additional dependencies.[/red]")
        console.print("[cyan]Install with: uv sync[/cyan]")
        return
    
    console.print("\n[bold cyan]Building GitFam Website[/bold cyan]\n")
    
    # Collect data
    families_path = Path('families')
    data = collect_family_data(families_path)
    
    console.print(f"Found: {data['stats']['total_members']} members across {data['stats']['total_branches']} branches")
    
    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Set up Jinja2
    templates_dir = Path(__file__).parent.parent / 'web_templates'
    if not templates_dir.exists():
        console.print(f"[yellow]Warning: Templates directory not found at {templates_dir}[/yellow]")
        console.print("[yellow]Creating default templates...[/yellow]")
        create_default_templates(templates_dir)
    
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    # Add markdown filter
    def markdown_filter(text):
        return markdown(text, extensions=['extra', 'codehilite'])
    
    env.filters['markdown'] = markdown_filter
    
    # Generate index page
    console.print("• Generating index.html")
    index_template = env.get_template('index.html')
    index_html = index_template.render(data=data)
    (output_path / 'index.html').write_text(index_html, encoding='utf-8')
    
    # Generate branch pages
    branch_template = env.get_template('branch.html')
    for branch in data['branches']:
        console.print(f"• Generating {branch['name']}.html")
        branch_html = branch_template.render(branch=branch, data=data)
        (output_path / f"{branch['name']}.html").write_text(branch_html, encoding='utf-8')
    
    # Generate member pages
    member_template = env.get_template('member.html')
    members_dir = output_path / 'members'
    members_dir.mkdir(exist_ok=True)
    
    for member in data['members']:
        console.print(f"• Generating members/{member['slug']}.html")
        member_html = member_template.render(member=member, data=data)
        (members_dir / f"{member['slug']}.html").write_text(member_html, encoding='utf-8')
    
    # Copy static assets
    console.print("• Copying static assets")
    create_static_assets(output_path / 'static')
    
    console.print(f"\n[bold green]✓ Website generated at: {output_path.absolute()}[/bold green]")
    console.print(f"\n[bold]To view:[/bold]")
    console.print(f"  Open: [cyan]{(output_path / 'index.html').absolute()}[/cyan]")
    console.print(f"  Or serve: [cyan]python -m http.server 8000 --directory {output_path}[/cyan]")


def create_default_templates(templates_dir: Path):
    """Create default HTML templates."""
    templates_dir.mkdir(parents=True, exist_ok=True)
    
    # Will be created in next step
    pass


def create_static_assets(static_dir: Path):
    """Create CSS and other static assets."""
    static_dir.mkdir(parents=True, exist_ok=True)
    
    # Will be created in next step
    pass
