"""Add a new family member."""

from pathlib import Path
from datetime import datetime
from rich.console import Console
import questionary
from questionary import Style
import yaml

console = Console()

custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),
    ('question', 'bold'),
    ('answer', 'fg:#00bcd4 bold'),
    ('pointer', 'fg:#673ab7 bold'),
    ('highlighted', 'fg:#673ab7 bold'),
])


def add_family_member_interactive(branch_name: str = None):
    """Interactively add a new family member."""
    
    console.print("\n[bold cyan]Add a Family Member[/bold cyan]\n")
    
    # Select branch if not provided
    if not branch_name:
        families_path = Path('families')
        if not families_path.exists():
            console.print("[red]Error: No families directory found. Run 'gitfam init-project' first.[/red]")
            return
        
        branches = [d.name for d in families_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        if not branches:
            console.print("[yellow]No family branches found. Create one first with 'gitfam create-branch'[/yellow]")
            return
        
        branch_name = questionary.select(
            "Which family branch?",
            choices=branches,
            style=custom_style
        ).ask()
        
        if not branch_name:
            return
    
    # Get member information
    console.print(f"\n[dim]Adding member to: {branch_name}[/dim]\n")
    
    full_name = questionary.text(
        "Full name:",
        style=custom_style,
        validate=lambda text: len(text) > 0 or "Name cannot be empty"
    ).ask()
    
    if not full_name:
        return
    
    birth_year = questionary.text(
        "Birth year (YYYY):",
        style=custom_style,
        validate=lambda text: text.isdigit() and len(text) == 4 or "Enter a 4-digit year"
    ).ask()
    
    if not birth_year:
        return
    
    birth_date = questionary.text(
        "Full birth date (YYYY-MM-DD) - optional, press Enter to skip:",
        style=custom_style,
        default=""
    ).ask()
    
    birth_place = questionary.text(
        "Birth place (City, State/Country):",
        style=custom_style,
        default=""
    ).ask()
    
    current_residence = questionary.text(
        "Current residence (or leave blank):",
        style=custom_style,
        default=""
    ).ask()
    
    # Ask about relationships
    console.print("\n[bold]Relationships[/bold] (we'll add these to the profile)")
    add_relationships = questionary.confirm(
        "Add family relationships now?",
        style=custom_style,
        default=True
    ).ask()
    
    relationships = []
    if add_relationships:
        while True:
            rel_type = questionary.select(
                "Relationship type:",
                choices=['child_of', 'parent_of', 'spouse_of', 'sibling_of', 'Done adding relationships'],
                style=custom_style
            ).ask()
            
            if rel_type == 'Done adding relationships':
                break
            
            rel_person = questionary.text(
                f"Related person (name-birthyear):",
                style=custom_style
            ).ask()
            
            if rel_person:
                relationships.append({'type': rel_type, 'person': rel_person})
    
    # Create directory structure
    member_slug = full_name.lower().replace(' ', '-') + '-' + birth_year
    member_path = Path('families') / branch_name / 'members' / member_slug
    
    if member_path.exists():
        console.print(f"[red]Error: Member '{member_slug}' already exists![/red]")
        return
    
    # Create directories
    member_path.mkdir(parents=True)
    (member_path / 'interviews' / 'videos').mkdir(parents=True)
    (member_path / 'photos').mkdir()
    (member_path / 'documents').mkdir()
    
    # Create profile
    profile_content = f"""---
# Basic Information
name: {full_name}
birth_date: {birth_date if birth_date else birth_year}
birth_place: {birth_place}
current_residence: {current_residence}

# Family Relationships
relationships:
"""
    
    for rel in relationships:
        profile_content += f"  - type: {rel['type']}\n    person: {rel['person']}\n"
    
    if not relationships:
        profile_content += "  # Add relationships here\n"
    
    profile_content += f"""
# Key Life Events
major_events:
  # Add important life events here
  # - date: YYYY-MM-DD
  #   event: Description

# Interviews
interviews:
  # Will be populated as you conduct interviews
  # - date: YYYY-MM-DD
  #   topics: [childhood, career, family, advice]
  #   video_files: [interview-part1.mp4]
  #   notes_file: interview-YYYY-MM-DD.md
---

# {full_name}

## Biography

[Write a brief overview of {full_name.split()[0]}'s life - a few paragraphs covering their story, what defined them, what they're known for in the family]

## Early Life & Childhood

[Details about their upbringing, where they grew up, childhood memories, family situation]

## Education

[Schools attended, areas of study, formative educational experiences]

## Career & Work Life

[Professional journey, jobs held, career accomplishments, work philosophy]

## Family Life

[Marriage(s), children, parenting approach, family values]

## Interests & Hobbies

[What they love to do, passions, how they spend free time]

## Values & Life Philosophy

[Core beliefs, what they stand for, lessons learned, advice for future generations]

## Legacy & Impact

[How they influenced others, what they'll be remembered for, gifts they gave to the family]

## Important Dates

- **Born:** {birth_date if birth_date else birth_year} in {birth_place if birth_place else '[location]'}
- **Married:** [Date and place]
- **Children:** [Names and birth years]

## Photos & Media

[Link to photos in the photos/ directory]

## Related Documents

[Links to documents in documents/ directory]

## Notes & Memories

[Space for family members to add their own memories and stories about this person]

---

*Profile created: {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    profile_path = member_path / 'profile.md'
    profile_path.write_text(profile_content, encoding='utf-8')
    
    # Create README
    readme_content = f"""# {full_name} (b. {birth_year})

## Quick Links
- [Full Profile](profile.md)
- [Interviews](interviews/)
- [Photos](photos/)
- [Documents](documents/)

## Interview Status
- [ ] Initial interview scheduled
- [ ] Childhood & early life
- [ ] Career & work
- [ ] Family stories
- [ ] Wisdom & advice

## To-Do
- [ ] Scan childhood photos
- [ ] Record video interview
- [ ] Get copies of important documents
- [ ] Follow up questions from first interview

## Notes
[Add any quick notes or reminders here]
"""
    
    readme_path = member_path / 'README.md'
    readme_path.write_text(readme_content, encoding='utf-8')
    
    console.print(f"\n[bold green]✓ Created profile for {full_name}[/bold green]")
    console.print(f"Location: {member_path}")
    
    # Ask if they want to add another member
    add_another = questionary.confirm(
        "\nWould you like to add another family member?",
        style=custom_style,
        default=True
    ).ask()
    
    if add_another:
        console.print("")
        return add_family_member_interactive(branch_name)  # Recursive call with same branch
    else:
        console.print("\n[bold]Next steps:[/bold]")
        console.print(f"• Edit the profile: [cyan]{profile_path}[/cyan]")
        console.print(f"• Add photos to: [cyan]{member_path / 'photos'}[/cyan]")
        console.print(f"• Schedule an interview using: [cyan]templates/interview-questions.md[/cyan]")
        console.print("\n[dim]Remember to commit your changes:[/dim]")
        console.print(f"[dim]git add . && git commit -m 'Added family members'[/dim]")
    
    return member_slug
