import YoutubeTags
import questionary
from YoutubeTags import videotags
from youtubesearchpython import VideosSearch
from rich.progress import track
from rich.console import Console

console = Console()
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
    best_tags += filter(None, tags.split(","))

print(", ".join(list(set(best_tags))))
