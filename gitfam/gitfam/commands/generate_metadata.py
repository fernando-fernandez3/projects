"""Generate metadata and statistics for family branches."""

import json
from pathlib import Path
from typing import Dict, List, Any
from rich.console import Console
from rich.table import Table
import yaml

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


def collect_branch_metadata(branch_path: Path) -> Dict[str, Any]:
    """Collect all metadata for a single family branch."""
    metadata = {
        'branch_name': branch_path.name,
        'members': [],
        'statistics': {
            'total_members': 0,
            'total_interviews': 0,
            'members_with_photos': 0,
            'members_with_videos': 0,
            'birth_year_range': None
        },
        'relationships': []
    }
    
    members_path = branch_path / 'members'
    if not members_path.exists():
        return metadata
    
    birth_years = []
    
    for member_path in members_path.iterdir():
        if not member_path.is_dir():
            continue
        
        profile_path = member_path / 'profile.md'
        if not profile_path.exists():
            continue
        
        try:
            content = profile_path.read_text(encoding='utf-8')
            frontmatter, _ = parse_frontmatter(content)
            
            # Extract birth year for statistics
            birth_date = frontmatter.get('birth_date', '')
            if birth_date:
                try:
                    year = int(str(birth_date).split('-')[0])
                    birth_years.append(year)
                except:
                    pass
            
            # Check for media
            has_photos = (member_path / 'photos').exists() and any((member_path / 'photos').iterdir())
            has_videos = (member_path / 'interviews' / 'videos').exists() and any((member_path / 'interviews' / 'videos').iterdir())
            
            if has_photos:
                metadata['statistics']['members_with_photos'] += 1
            if has_videos:
                metadata['statistics']['members_with_videos'] += 1
            
            # Count interviews
            interviews = frontmatter.get('interviews', [])
            metadata['statistics']['total_interviews'] += len(interviews)
            
            # Member data
            member_data = {
                'slug': member_path.name,
                'name': frontmatter.get('name', member_path.name),
                'birth_date': frontmatter.get('birth_date', ''),
                'birth_place': frontmatter.get('birth_place', ''),
                'current_residence': frontmatter.get('current_residence', ''),
                'relationships': frontmatter.get('relationships', []),
                'interviews': interviews,
                'has_photos': has_photos,
                'has_videos': has_videos,
                'major_events': frontmatter.get('major_events', [])
            }
            
            metadata['members'].append(member_data)
            metadata['statistics']['total_members'] += 1
            
            # Collect relationships for graph
            for rel in frontmatter.get('relationships', []):
                metadata['relationships'].append({
                    'from': member_path.name,
                    'to': rel.get('person', ''),
                    'type': rel.get('type', '')
                })
        
        except Exception as e:
            console.print(f"[yellow]Warning: Could not parse {member_path.name}: {e}[/yellow]")
            continue
    
    # Calculate birth year range
    if birth_years:
        metadata['statistics']['birth_year_range'] = {
            'earliest': min(birth_years),
            'latest': max(birth_years),
            'span': max(birth_years) - min(birth_years)
        }
    
    return metadata


def generate_metadata(output_format: str = 'json', branch: str = None):
    """Generate metadata for all branches or a specific branch."""
    
    console.print("\n[bold cyan]Generating Family Metadata[/bold cyan]\n")
    
    families_path = Path('families')
    if not families_path.exists():
        console.print("[red]Error: No families directory found.[/red]")
        return
    
    all_metadata = {
        'generated_at': None,
        'branches': [],
        'global_statistics': {
            'total_branches': 0,
            'total_members': 0,
            'total_interviews': 0,
            'members_with_media': 0
        }
    }
    
    # Import datetime here to set generation time
    from datetime import datetime
    all_metadata['generated_at'] = datetime.now().isoformat()
    
    # Collect metadata for each branch
    branches = []
    if branch:
        branch_path = families_path / branch
        if not branch_path.exists():
            console.print(f"[red]Error: Branch '{branch}' not found.[/red]")
            return
        branches = [branch_path]
    else:
        branches = [d for d in families_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    for branch_path in branches:
        console.print(f"• Processing {branch_path.name}...")
        branch_metadata = collect_branch_metadata(branch_path)
        all_metadata['branches'].append(branch_metadata)
        
        # Update global stats
        all_metadata['global_statistics']['total_members'] += branch_metadata['statistics']['total_members']
        all_metadata['global_statistics']['total_interviews'] += branch_metadata['statistics']['total_interviews']
        all_metadata['global_statistics']['members_with_media'] += (
            branch_metadata['statistics']['members_with_photos'] + 
            branch_metadata['statistics']['members_with_videos']
        )
    
    all_metadata['global_statistics']['total_branches'] = len(all_metadata['branches'])
    
    # Output based on format
    if output_format == 'json':
        output_file = Path('family-metadata.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_metadata, f, indent=2, ensure_ascii=False)
        console.print(f"\n[bold green]✓ Metadata saved to: {output_file}[/bold green]")
    
    elif output_format == 'yaml':
        output_file = Path('family-metadata.yaml')
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(all_metadata, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        console.print(f"\n[bold green]✓ Metadata saved to: {output_file}[/bold green]")
    
    elif output_format == 'summary':
        # Display summary in terminal
        display_summary(all_metadata)
    
    else:
        console.print(f"[red]Unknown format: {output_format}[/red]")


def display_summary(metadata: Dict[str, Any]):
    """Display a summary table in the terminal."""
    
    # Global statistics
    console.print("\n[bold cyan]📊 Global Statistics[/bold cyan]\n")
    
    stats_table = Table(show_header=False, box=None)
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="bold green")
    
    stats_table.add_row("Total Branches", str(metadata['global_statistics']['total_branches']))
    stats_table.add_row("Total Members", str(metadata['global_statistics']['total_members']))
    stats_table.add_row("Total Interviews", str(metadata['global_statistics']['total_interviews']))
    stats_table.add_row("Members with Media", str(metadata['global_statistics']['members_with_media']))
    
    console.print(stats_table)
    
    # Branch details
    console.print("\n[bold cyan]🌳 Branch Details[/bold cyan]\n")
    
    branch_table = Table(show_header=True)
    branch_table.add_column("Branch", style="cyan")
    branch_table.add_column("Members", justify="right", style="green")
    branch_table.add_column("Interviews", justify="right", style="yellow")
    branch_table.add_column("Photos", justify="right", style="magenta")
    branch_table.add_column("Videos", justify="right", style="blue")
    branch_table.add_column("Birth Years", style="dim")
    
    for branch in metadata['branches']:
        stats = branch['statistics']
        year_range = stats.get('birth_year_range')
        year_str = f"{year_range['earliest']}-{year_range['latest']}" if year_range else "N/A"
        
        branch_table.add_row(
            branch['branch_name'],
            str(stats['total_members']),
            str(stats['total_interviews']),
            str(stats['members_with_photos']),
            str(stats['members_with_videos']),
            year_str
        )
    
    console.print(branch_table)
    
    console.print("\n[dim]Run with --format json or --format yaml to save detailed metadata.[/dim]\n")
