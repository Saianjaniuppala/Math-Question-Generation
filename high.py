import random
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

QUESTIONS = [
    {
        "title": "Probability in Book Selection",
        "template": "A library has {fiction} fiction, {nonfiction} nonfiction, and {reference} reference books. If a student picks 2 books at random, what's the probability both are {target}?",
        "subject": "Quantitative Math",
        "unit": "Data Analysis & Probability",
        "topic": "Probability",
        "difficulty": "moderate",
        "generate": lambda: {
            'fiction': random.randint(3, 7),
            'nonfiction': random.randint(2, 5),
            'reference': random.randint(1, 4),
            'target': random.choice(['fiction', 'nonfiction', 'reference'])
        },
        "explain": lambda data: (
            f"Total books = {data['fiction'] + data['nonfiction'] + data['reference']}\n"
            f"First pick: {data[data['target']]}/{data['fiction'] + data['nonfiction'] + data['reference']}\n"
            f"Second pick: {data[data['target']]-1}/{data['fiction'] + data['nonfiction'] + data['reference']-1}\n"
            f"Probability: ({data[data['target']]}/{data['fiction'] + data['nonfiction'] + data['reference']}) × "
            f"({data[data['target']]-1}/{data['fiction'] + data['nonfiction'] + data['reference']-1}) = "
            f"{data[data['target']]*(data[data['target']]-1)}/{(data['fiction']+data['nonfiction']+data['reference'])*(data['fiction']+data['nonfiction']+data['reference']-1)}"
        )
    },
    {
        "title": "Cylinder Volume Calculation",
        "template": "A cylindrical tank has diameter {diameter}m and height {height}m. Using π≈3.14, what's its volume in liters? (1m³=1000L)",
        "subject": "Quantitative Math",
        "unit": "Geometry",
        "topic": "Volume",
        "difficulty": "hard",
        "generate": lambda: {
            'diameter': random.randint(4, 12)*2,
            'height': random.randint(3, 10)
        },
        "explain": lambda data: (
            f"Radius = {data['diameter']/2}m\n"
            f"Volume = πr²h = 3.14 × ({data['diameter']/2})² × {data['height']}\n"
            f"= 3.14 × {pow(data['diameter']/2,2)} × {data['height']}\n"
            f"= {3.14*pow(data['diameter']/2,2)*data['height']:.2f}m³\n"
            f"Convert to liters: {3.14*pow(data['diameter']/2,2)*data['height']:.2f} × 1000 = "
            f"{int(3.14*pow(data['diameter']/2,2)*data['height']*1000):,}L"
        )
    }
]

def generate_question(question):
    """Generate a complete question with options and explanation"""
    data = question["generate"]()
    
    # Calculate correct answer
    if "Probability" in question["title"]:
        total = data['fiction'] + data['nonfiction'] + data['reference']
        correct = (data[data['target']]/total) * ((data[data['target']]-1)/(total-1))
        correct_str = f"{data[data['target']]*(data[data['target']]-1)}/{(total)*(total-1)}"
    else:
        correct = 3.14 * pow(data['diameter']/2, 2) * data['height'] * 1000
        correct_str = f"{int(correct):,}L"
    
    if "Probability" in question["title"]:
        options = [
            f"{random.randint(1, data[data['target']]-1)}/{total*(total-1)}",
            f"{data[data['target']]}/{total}",
            correct_str,
            f"{data[data['target']]}/{total-1}",
            f"1/{total}"
        ]
    else:
        options = [
            f"{int(correct*0.5):,}L", 
            f"{int(3.14*data['diameter']*data['height']*1000):,}L", 
            correct_str,
            f"{int(3.14*pow(data['diameter']/2,2)*data['height']):,}L", 
            f"{int(3.14*pow(data['diameter'],2)*data['height']*1000):,}L" 
        ]
    
    random.shuffle(options)
    correct_index = options.index(correct_str)
    
    return {
        "question": question["template"].format(**data),
        "options": options,
        "correct": correct_index,
        "explanation": question["explain"](data),
        "metadata": {
            "title": question["title"],
            "subject": question["subject"],
            "unit": question["unit"],
            "topic": question["topic"],
            "difficulty": question["difficulty"]
        }
    }

def display_question(q):
    """Display formatted question with Rich"""
    console.print(Panel.fit(
        f"[bold]{q['metadata']['title']}[/bold] ([italic]{q['metadata']['difficulty']}[/italic])",
        subtitle=f"{q['metadata']['subject']} > {q['metadata']['unit']} > {q['metadata']['topic']}"
    ))
    
    console.print(f"\n{q['question']}\n")
    table = Table(show_header=False, padding=(0, 2))
    for i, opt in enumerate(q['options']):
        prefix = "[green]✓[/green]" if i == q['correct'] else "○"
        table.add_row(f"{prefix} {chr(65+i)}) {opt}")
    console.print(table)
    
    console.print("\n[bold]Explanation:[/bold]")
    console.print(q['explanation'])

def main():
    console.print("[bold cyan]Random Math Questions Generator[/bold cyan]\n", justify="center")
    selected_questions = random.sample(QUESTIONS, 2)
    
    for i, q in enumerate(selected_questions):
        generated = generate_question(q)
        display_question(generated)
        if i < len(selected_questions)-1:
            console.print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()