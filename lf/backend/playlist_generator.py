from dataclasses import dataclass

from clients.cover_image_generator_client import CoverImageGeneratorClient
from clients.playlist_description_generator_client import PlaylistDescriptionGeneratorClient
import uuid

def image_cover_prompt(tracks: list[str]):
    # Format track list for context
    track_list = "\n".join(f"- {track}" for track in tracks[:100])  # Limit to first 100 tracks
    return f"""
        You are a music lover and graphic designer tasked with creating an album cover image for a playlist.
        Use your knowledge of the artists, genres, and themes of the songs to design a visually compelling cover that captures the mood and essence of the playlist.
        Create an album cover image for a playlist with the following tracks:
        
{track_list}

        Design a visually compelling album cover that captures the mood and essence of these songs.
        The image should be cohesive, professional, and suitable for a playlist cover.
        Consider the themes, genres, and emotional tone of the tracks when choosing colors and imagery.
        Make it visually interesting and memorable.
    """


def description_prompt(tracks: list[str]):
    # Format track list for context
    track_list = "\n".join(f"- {track}" for track in tracks[:100])  # Limit to first 100 tracks
    return f"""
        You are a music enthusiast and copywriter tasked with writing a playlist description.
        Use your knowledge of the artists, genres, and themes of the songs to craft a compelling description that captures the mood and vibe of the playlist.
        Create an engaging playlist description for a playlist containing these tracks:
        
{track_list}

        Write a compelling 2-3 sentence description that:
        - Captures the overall mood and vibe of the playlist
        - Highlights what makes these songs work well together
        - Entices listeners to play the playlist
        
        Be creative, authentic, and avoid generic phrases.
    """


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