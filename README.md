# Tiktok content labeler
In deze _repository_ staat de code om video's van Tiktok binnen te halen, te transcriberen en daar thema's uit te destilleren. De bron van je video's is een bestand gemaakt met [Zeeschuimer](github.com/digitalmethodsinitiative/zeeschuimer) dat naar csv is omgezet met [Zeehaven](https://github.com/PublicDataLab/zeehaven). 

De code is geschreven in het kader van een cursus AI-gebruik door journalisten van het [Fonds Bijzondere Journalistieke Projecten](https://fondsbjp.nl).

## Benodigdheden
De code is geschreven in Python. Gebruik een moderne versie, en bij voorkeur een virtuele omgeving als `venv` of `conda` om de benodigde _libraries_ te installeren. Zie daarvoor `requirements.txt`. 

Verder heb je voor het transcribeergedeelte een lokale versie van OpenAI's Whisper-model nodig. 

## Scripts / stappenplan
- Plaats een Zeeschuimer-bestand (extensie `.csv`) in de `data/`-map (of in de root, waar je maar wilt).
- Pas het pad en je projectnaam aan in de `get_video_labels.py`. 
- Draai het script `get_video_labels.py`. Je hebt nu in je video-map de transcripten van al je video's en een `themes.txt`-bestand met daarin de door AI gevonden thema's.


