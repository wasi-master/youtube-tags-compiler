import YoutubeTags
import questionary
from YoutubeTags import videotags
from youtubesearchpython import VideosSearch
from rich.progress import track
from rich.console import Console

console = Console()
while True:
    search_term = console.input("[red]Enter search term:[/] ")
    with console.status('Searching'):
        videos = VideosSearch(search_term, limit = 10).result()["result"]

    for n, video in enumerate(videos, start=1):
        console.print(f"[yellow]{n}.[/][cyan]{video['title']}[/] by [green]{video['channel']['name']}")
        console.print(f"[red]{video['link']}[/]")

    selected_videos = questionary.checkbox('Select videos', choices=map(str, range(1, 10))).ask()
    if not selected_videos:
        exit()

    link_list = [v['link'] for v in [videos[int(n)] for n in selected_videos]]
    best_tags = []
    for link in track(link_list, description="Loading tags"):
        tags = videotags(link)
        best_tags += map(str.strip, filter(None, tags.split(",")))

    tags_formatted = ", ".join(list(set(best_tags)))
    console.print(f"[red][green]{len(best_tags)}[/] Tags gotten. Total [green]{len(tags_formatted)}[/] characters[/]")
    print(tags_formatted)
    with open(f"{search_term}-{'-'.join(selected_videos)}.txt", "w", encoding="utf-8") as f:
        f.write(tags_formatted)
        console.print(f"Tags saved to [green]{search_term}-{'-'.join(selected_videos)}.txt[/]")
    do_again = questionary.confirm("Do you want to do it again?").ask()
    if not do_again:
        break
    else:
        console.print("[blue]---------------------------------------------------[/]")

