import os
from prompts import rpg_system_prompt
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY")
)


class StoryModel(BaseModel):
    class ChapterModel(BaseModel):
        room_description: str
        chapter_story: str
    chapters: list[ChapterModel]

def generate_story():
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[{"role": "system", "content": rpg_system_prompt},
        {"role": "user", "content": "Generate a great engaging five chapter story."}
   ],
    response_format=StoryModel

    )

    return response.choices[0].message.parsed.chapters
