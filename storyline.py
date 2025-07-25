from classes import Storyline, Chapter
from clients import generate_story

chapter_one = Chapter(
    room_description="The air is thick with the scent of decay as you enter a vast, stone chamber. Cracked sarcophagi line the walls, and strange symbols are etched into the floor.",
    chapter_story="You’ve found your way into the crypt, an ancient burial site that was sealed long ago. The markings on the walls seem to pulse faintly as you walk, as if they are watching you. As you pass one of the sarcophagi, the lid shifts, and you hear the sound of something stirring inside. You must decide whether to investigate or avoid the ominous signs and continue through the dungeon.",
)
chapter_two = Chapter(
    room_description="A long, narrow corridor stretches ahead, its walls lined with black banners that flutter despite the lack of wind. The darkness here feels alive.",
    chapter_story="The shadows in this hall seem to move on their own, creeping along the walls like sentient beings. Your every step echoes, as if the dungeon itself is aware of your presence. Strange whispers fill your ears, urging you to turn back, but ahead you can see flickering light. As you venture deeper, the shadows become more aggressive, reaching out to ensnare you unless you can find a way to dispel their grip.",
)
chapter_three = Chapter(
    room_description="The room is lined with rusted iron bars and thick chains that rattle unnervingly. Faint, sorrowful wails fill the air, emanating from unseen prisoners.",
    chapter_story="You’ve entered the forsaken prison where the souls of traitors and outcasts are trapped for eternity. As you walk through, ghostly figures claw at the bars, their faces twisted in torment. They plead for release, but you know better than to trust them. At the far end of the room, an eerie glowing artifact is locked behind a cage, and you feel its pull, as if it holds the key to something far greater—and far darker.",
)
chapter_four = Chapter(
    room_description="A deep chasm stretches before you, filled with bubbling lava. The stone bridges across it are old and cracked, and the air shimmers with heat.",
    chapter_story="The Pit of Eternal Flame is a cursed place, where the dead are burned in endless fire. The lava churns violently, and the heat is almost unbearable, but the only way forward is across one of the fragile bridges. As you step carefully, a distant figure emerges from the flames, a fiery guardian who seeks to test your worth. The question is simple: survive the trial, or become another soul consumed by the flames.",
)
chapter_five = Chapter(
    room_description="A massive throne room unfolds before you, where the air is thick with dread. The throne is made of black obsidian, and ancient runes glow faintly along the walls.",
    chapter_story="At the center of this room sits the Throne of the Abyss, a dark seat of unimaginable power. Here, the dungeon’s true master waits—an ancient, corrupted ruler who has been trapped in this place for centuries. As you approach the throne, his voice booms through the chamber, offering you a deal: bow before him and gain power, or face certain annihilation. But the true cost of his offer is hidden, and your final decision will seal the fate of not just the dungeon, but the entire realm.",
)
chapters = [chapter_one, chapter_two, chapter_three, chapter_four, chapter_five]
story = Storyline()
