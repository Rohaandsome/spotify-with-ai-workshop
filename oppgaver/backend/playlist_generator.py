from dataclasses import dataclass

from clients.cover_image_generator_client import CoverImageGeneratorClient
from clients.playlist_description_generator_client import PlaylistDescriptionGeneratorClient
import uuid

def image_cover_prompt(tracks: list[str]):
    songs = "\n".join(f"- {t}" for t in tracks[:20]) if tracks else "- various songs"
    return f"""You are an AI visual designer.

Given this playlist:
{songs}

Step 1: Analyze the playlist for:
- dominant mood (happy, sad, aggressive, calm, etc.)
- genre
- tempo/energy

Step 2: Translate this into a visual concept:
- color palette
- environment or scene
- style (minimalist, abstract, realistic, etc.)

Step 3: Generate an album cover based on this concept.

The result should be visually appealing, relevant to the music, and suitable as a cover image.
High quality, detailed, 4k, professional album cover, centered composition, no text."""


def description_prompt(tracks: list[str]):
    track_list = "\n".join(f"- {t}" for t in tracks[:20]) if tracks else "- various songs"
    return f"""Write an engaging and creative playlist description for a Spotify playlist.
The playlist contains these songs:
{track_list}

The description should:
- Capture the overall mood and vibe of the tracks
- Be 2-4 sentences long
- Sound inviting and exciting to potential listeners
- Reflect the musical style and energy of the songs
Write only the description text, with no extra commentary."""


class CoverGenerator:
    def __init__(self):
        self.image_generation_client = CoverImageGeneratorClient()

    def generate_cover_image(self, track_names: list[str]):
        prompt = image_cover_prompt(track_names)
        imageUrl = self.image_generation_client.generate_image(prompt)
        return imageUrl
    


class DescriptionGenerator:
    def __init__(self):
        self.description_generation_client = PlaylistDescriptionGeneratorClient()
    
    def generate_description(self, track_names: list[str]):
        prompt = description_prompt(track_names)
        description = self.description_generation_client.generate_description(prompt)
        return description