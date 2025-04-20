import os
from prompts import rpg_system_prompt
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY")
)

def generate_story():
    response = client.responses.create(
        model="gpt-4o",
        input=[{"role": "system", "content": rpg_system_prompt},
        {"role": "user", "content": "Generate a great engaging five chapter story."}
   ],
    text={
    "format": {
        "type": "json_schema",
        "name": "game story chapters",
        "description": "Chapters 1 to 5 for the dungeon game",
        "strict": True,
        "schema": {
            "type": "array",
                    "description": "Array of five chapters",
                    "items": {
                        "type": "object",
                        "properties": {
                            "room_description": {
                                "type": "string",
                                "description": "A short description of the room that the character enters"
                            },
                            "chapter_story": {
                                "type": "string",
                                "description": "The story for this particular chapter"
                            }
                        },
                        "additionalProperties": False,
                        "required": ["room_description", "chapter_story"]
                    }
            },
            "required": ["room_description", "chapter_story"],
            "additionalProperties": False
        }
    }

    )

    return response.output_text
