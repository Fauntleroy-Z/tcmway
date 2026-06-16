#!/usr/bin/env python3
"""
Generate all 23 TCM Way B&W hand-drawn comics using bl CLI + qwen-image-2.0.
Black-and-white ink style — Ollie character in grayscale, 2D flat, clean outlines.
"""
import subprocess
import os
import sys
import time

OUT_DIR = os.path.expanduser("~/tcmway-blog/images")
os.makedirs(OUT_DIR, exist_ok=True)

# ============================================================
# OLLIE B&W CHARACTER DESCRIPTION (for prompt)
# ============================================================
OLLIE_BW = (
    "MAIN CHARACTER Ollie: a cute owl mascot with medium gray head, "
    "triangular ear tufts, large round eyes with tiny white highlights, "
    "short triangular beak in dark gray, lighter gray belly, "
    "THIN delicate chain with a SMALL TINY circular yin-yang pendant "
    "(dark gray and light gray halves, proportional like a real necklace charm, only about 5% of body width), "
    "2D flat hand-drawn black ink illustration, clean black outlines, "
    "strictly monochrome grayscale, zero color information, "
    "no shading, no gradients, pure white background."
)

BANDW_PREFIX = (
    "PURE BLACK AND WHITE INK DRAWING, monochrome. "
    "2D flat hand-drawn cartoon, clean black outlines, "
    "strictly grayscale, zero chromatic information, black ink on white paper only. "
    "No warm tones, no cool tones, no color cast of any kind. "
    "Pure white background, no shading, no gradients. "
    "Hand-drawn ink comic style. "
)

BANDW_NEGATIVE = (
    "color, chromatic, warm tones, cool tones, red, orange, yellow, green, blue, purple, "
    "saturation, hue, RGB, sepia, tinted, toned, "
    "3D rendering, photorealistic, shading, gradients, shadows, "
    "large pendant, oversized jewelry, chunky necklace, medallion, big amulet, gaudy jewelry, "
    "blurred details, messy lines, extra limbs, deformed body, watermarks, text, words"
)
COMICS = {
    "01": {
        "title": "Why I Share TCM with the West",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about bridging Chinese medicine and Western anxiety: "
            "Panel 1 — A Westerner overwhelmed by stress, surrounded by pills, coffee cups, and digital screens, looking exhausted. "
            "Panel 2 — Ollie the owl appears carrying a ancient Chinese medical scroll, looking wise and calm. "
            "Panel 3 — A bridge forming between a modern Western city skyline and a traditional Chinese garden with herbs, Ollie standing at the center. "
            "Panel 4 — The Westerner now calm, drinking herbal tea, with Ollie beside them holding a banner 'TCM Way'."
        )
    },
    "02": {
        "title": "Exhausted After Sleep — Organ Clock",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about the ancient Chinese organ clock and why 8 hours of sleep isn't enough: "
            "Panel 1 — A person lying in bed looking exhausted, clock showing 7 AM, speech bubble 'I slept 8 hours... why am I wrecked?' "
            "Panel 2 — Ollie the owl holding up a 24-hour circular organ clock chart, pointing at 1-3 AM (Liver time) with a knowing expression. "
            "Panel 3 — Inside the body: Liver organ shown as a night-shift worker cleaning toxins at 2 AM, while the person is still awake scrolling phone. "
            "Panel 4 — The person in bed asleep by 11 PM, all five organs (Liver, Lungs, Heart, Spleen, Kidneys) shown as happy shift workers, Ollie giving a thumbs up."
        )
    },
    "03": {
        "title": "Qi Is Not Magic — It's Your Body's OS",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic explaining Qi as the body's operating system, not mystical energy: "
            "Panel 1 — A confused person looking at a diagram of the human body with swirling 'Qi' labeled 'Magic Energy?' and question marks. "
            "Panel 2 — Ollie the owl standing beside a giant computer monitor, pointing at system processes labeled 'Digestion', 'Circulation', 'Immunity' all running on 'Qi OS'. "
            "Panel 3 — Ollie holding a laptop showing task manager: Qi is the electricity that powers all programs — without it, nothing works. "
            "Panel 4 — The person now understanding, their body shown as a well-organized computer with all processes running smoothly, Ollie smiling beside them."
        )
    },
    "04": {
        "title": "Traffic Jam Inside Your Body",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about Qi stagnation as a traffic jam: "
            "Panel 1 — A person feeling bloated and irritable, shoulders tense, standing in a metaphor traffic jam of cars labeled 'Stressed', 'Frustrated', 'Stuck'. "
            "Panel 2 — Ollie the owl explaining Qi stagnation with a traffic map — red lines showing blocked energy flow through the body's meridians. "
            "Panel 3 — Ollie pointing to specific body areas: shoulder tension, bloated belly, headache — all connected by blocked Qi highways. "
            "Panel 4 — The person now walking freely through clear roads (meridians flowing), shoulders relaxed, smiling, Ollie beside them holding a sign 'Movement = Flow'."
        )
    },
    "05": {
        "title": "The Body Clock You Didn't Set",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about the ancient Chinese organ clock: "
            "Panel 1 — A person looking at their smartphone clock, confused about why they feel energized at certain hours and tired at others. "
            "Panel 2 — Ollie the owl presenting a 24-hour wheel showing organs punching in and out like factory workers: Liver 1-3AM, Lungs 3-5AM, Large Intestine 5-7AM, Stomach 7-9AM. "
            "Panel 3 — Ollie showing two scenarios: (left) person eating late at 11 PM with confused stomach worker, (right) person eating breakfast at 8 AM with happy stomach worker. "
            "Panel 4 — Person following the clock: eating at right times, sleeping at right times, all organ workers smiling in harmony, Ollie giving an approving nod."
        )
    },
    "06": {
        "title": "That Heavy Feeling — It's Not Laziness",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about dampness: "
            "Panel 1 — A person feeling heavy and sluggish, labeled 'lazy' by others, but the real issue shown as a wet sponge weighing them down. "
            "Panel 2 — Ollie the owl explaining dampness with a sponge metaphor: Spleen as a struggling dehumidifier unable to process excess moisture. "
            "Panel 3 — Ollie showing the causes: cold drinks, greasy food, damp environment — all pouring water onto the already soaked sponge. "
            "Panel 4 — Person eating warm foods (ginger, congee), the sponge drying out, body feeling light and energetic, Ollie celebrating the transformation."
        )
    },
    "07": {
        "title": "Six Signs of Health",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about the six signs of health: "
            "Panel 1 — A person looking at normal lab results but still feeling unwell, scratching their head in confusion. "
            "Panel 2 — Ollie the owl presenting six health indicators: appetite, bowels, sleep, warmth, clarity, mood — each shown as a glowing checkpoint. "
            "Panel 3 — The person checking each sign like a checklist: 'Sleeping through the night? Check. Hungry at mealtimes? Check. Warm hands? Check...' "
            "Panel 4 — All six checkmarks lit up green, the person feeling genuinely healthy, Ollie pointing at a sign 'Health is more than lab numbers'."
        )
    },
    "08": {
        "title": "Why Cold Hands Warn You",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about cold hands as a health warning: "
            "Panel 1 — A person with visibly cold blue-tinted hands, trying to warm them with a hot mug, looking concerned. "
            "Panel 2 — Ollie the owl explaining: the body is like a house, cold hands mean the heating system is pulling heat inward to protect vital organs. "
            "Panel 3 — Diagram of body showing heat retreating from extremities (hands, feet) to core (heart, lungs) — Ollie pointing at frozen pipes analogy. "
            "Panel 4 — The person drinking ginger tea, wearing warm socks, exercising lightly — heat flowing back to hands and feet, Ollie giving an encouraging gesture."
        )
    },
    "09": {
        "title": "Six-Layer Defense System",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about the body's six-layer defense: "
            "Panel 1 — Tiny pathogen warriors trying to invade a castle, representing a cold virus attacking the body. "
            "Panel 2 — Ollie showing the body as a castle with six concentric defensive walls labeled TaiYang, YangMing, ShaoYang, TaiYin, ShaoYin, JueYin. "
            "Panel 3 — Pathogen breaking through outer walls one by one, body mobilizing deeper immune defenses at each layer. "
            "Panel 4 — Strong immunity at the outer layer stops the invader early — Ollie as castle guardian raising a shield at TaiYang gate."
        )
    },
    "10": {
        "title": "Stop Feeding What You Fight",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about not feeding illness: "
            "Panel 1 — A person fighting fire with one hand while pouring gasoline with the other — metaphor for eating wrong foods while trying to heal. "
            "Panel 2 — Ollie stops them, showing a scale: left side 'What you consume' (cold drinks, sugar, fried food), right side 'What heals' (warm soup, vegetables). "
            "Panel 3 — The person switching: warm soup replacing cold drinks, vegetables replacing greasy food, steam rising from healthy bowl. "
            "Panel 4 — Fire extinguished, person feeling better, Ollie holding a sign 'Food is medicine' with a warm smile."
        )
    },
    "11": {
        "title": "Cold Is Never Just a Cold",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about the cold progression map: "
            "Panel 1 — A person sneezing, saying dismissively 'Just a cold.', while Ollie looks concerned in the background. "
            "Panel 2 — Ollie presents the Six-Channel Progression Map: a downward staircase showing cold descending through TaiYang → YangMing → ShaoYang → TaiYin → ShaoYin → JueYin with a 3-day deadline at each step. "
            "Panel 3 — Two paths diverge: (left) person takes cold medicine suppressing symptoms, cold goes deeper; (right) person uses traditional sweating method, cold expelled. "
            "Panel 4 — Person drinking hot ginger tea wrapped in blanket, sweating, cold defeated at day 1, Ollie cheering 'Sweat it out on Day 1!'."
        )
    },
    "12": {
        "title": "Liver Rules Everything",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about the Liver's central role: "
            "Panel 1 — A person with three separate problems: shoulder pain, IBS, and insomnia — shown as three disconnected complaint bubbles. "
            "Panel 2 — Ollie connects all three to one organ — the Liver as a central hub with wires connecting to shoulder, intestines, and brain. "
            "Panel 3 — Ollie shows the Liver as a General directing Qi flow — stress causes the General to freeze, blocking all traffic. "
            "Panel 4 — Stress relief restores flow: the Liver General back in command, Qi flowing freely, all three symptoms resolved, Ollie explains 'The Liver governs smooth flow'."
        )
    },
    "13": {
        "title": "The Medicine Character Contains Music",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about the Chinese character for medicine: "
            "Panel 1 — The Chinese character 藥 (medicine) breaks apart: the grass radical 艹 on top and the character 樂 (music) below, arrows showing the decomposition. "
            "Panel 2 — Ollie playing the ancient five-note scale (宫商角徵羽), each note connected by a line to a different organ: Heart, Liver, Spleen, Lungs, Kidneys. "
            "Panel 3 — Sound waves shown as healing energy reaching each organ, musical notes floating toward the body like medicine. "
            "Panel 4 — A person listening to healing music, body in perfect harmony, Ollie holding a musical note in one wing and an herb in the other, both glowing equally."
        )
    },
    "14": {
        "title": "Ten Questions Ancient Doctors Asked",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about the ten diagnostic questions: "
            "Panel 1 — Modern doctor staring at lab results on a screen, versus an ancient Chinese physician sitting with a patient asking detailed questions. "
            "Panel 2 — Ollie presents the ten questions radiating around a patient figure: sleep, appetite, bowels, urination, thirst, temperature, sweat, pain, emotions, menstruation. "
            "Panel 3 — Each question illuminating a different body part like a diagnostic map: 'How's your sleep?' lights up Heart, 'How's your appetite?' lights up Spleen. "
            "Panel 4 — A complete health picture emerges from the ten answers — Ollie shows a fully lit body diagram, caption: 'What questions reveal that labs miss.'"
        )
    },
    "15": {
        "title": "Your Tongue Knows Before Blood Tests",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about tongue diagnosis: "
            "Panel 1 — A person looking at normal blood test results that say 'all normal', but they feel unwell — confusion on their face. "
            "Panel 2 — Ollie holding up a tongue map: different zones of the tongue labeled with organ names (tip=Heart, sides=Liver, center=Spleen, back=Kidneys). "
            "Panel 3 — Three tongue examples being compared: pale swollen tongue (Yang deficiency), red tongue with yellow coat (Heat), purple tongue (Blood stasis). "
            "Panel 4 — The person looking in a mirror at their own tongue, Ollie nodding wisely: 'Your tongue shows patterns before lab tests catch them.'"
        )
    },
    "16": {
        "title": "Yin Yang — Not Good vs Evil",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about the yin-yang seesaw: "
            "Panel 1 — A simple wooden seesaw perfectly horizontal and balanced, Ollie sitting in the center looking happy, left side labeled 'YIN' right side 'YANG'. "
            "Panel 2 — Seesaw tilted down on right, Yang side heavy, Ollie sliding right looking surprised, speech bubble 'Too much Yang!'. "
            "Panel 3 — Seesaw tilted down on left, Yin side heavy (mirror of panel 2), Ollie sliding left looking dizzy, speech bubble 'Now too much Yin!'. "
            "Panel 4 — Seesaw back to almost-level with slight dynamic tilt, Ollie standing confidently near center, speech bubble 'Neither side wins. That is the point.'"
        )
    },
    "17": {
        "title": "Five Elements — Not a Personality Test",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about the Five Elements as an ecosystem: "
            "Panel 1 — A person doing an online 'Which element are you?' quiz, getting result 'You are WOOD!', looking confused. "
            "Panel 2 — Ollie shaking head, showing the Five Elements as a interconnected circle: Wood→Fire→Earth→Metal→Water→Wood, with arrows showing generating cycles. "
            "Panel 3 — Ollie demonstrating the controlling cycle: Water puts out Fire, Fire melts Metal, Metal cuts Wood, Wood holds Earth, Earth dams Water — a balanced ecosystem. "
            "Panel 4 — The five elements shown inside the human body as five organ systems (Liver-Wood, Heart-Fire, Spleen-Earth, Lungs-Metal, Kidneys-Water) all working together, Ollie nodding 'It's a system, not a type.'"
        )
    },
    "18": {
        "title": "Your Body Is a Kingdom",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about the body as a kingdom: "
            "Panel 1 — A person viewing their body as a machine with gears, pistons, and mechanical parts — a Western reductionist view. "
            "Panel 2 — Ollie reveals an alternative: the body as a kingdom with five palaces (Zang organs) each serving as a government department: Heart=Emperor, Liver=General, Spleen=Granary, Lungs=Prime Minister, Kidneys=Treasury. "
            "Panel 3 — Ollie as the Emperor coordinating all five organs with golden threads, each department doing its job in harmony. "
            "Panel 4 — The person now understanding their body as a well-run kingdom, all five palace departments working together, Ollie on the throne smiling proudly."
        )
    },
    "19": {
        "title": "Jing, Qi, Shen — The Three Treasures",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about the Three Treasures: "
            "Panel 1 — Garden scene: Ollie holding Russian nesting dolls — the largest labeled SHEN, middle QI, smallest JING — showing how they nest within each other. "
            "Panel 2 — Study room: computer metaphor — a desktop PC where Jing=Hardware (the physical body), Qi=Operating System (energy running everything), Shen=User (consciousness/spirit). "
            "Panel 3 — Meditation room: a human silhouette with three layered glowing zones — outer body (Jing), middle energy field (Qi), inner light (Shen). "
            "Panel 4 — Treasure room: Ollie guarding three plaques on the wall — JING (foundation), QI (vitality), SHEN (spirit) — with a banner 'Guard All Three'."
        )
    },
    "20": {
        "title": "What Zhang Zhongjing Knew",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about Zhang Zhongjing as the original pattern detective: "
            "Panel 1 — A detective office scene: Ollie wearing a tiny detective hat, holding a magnifying glass over a patient's case file labeled 'Mystery Illness'. "
            "Panel 2 — Ollie pointing at an ancient Chinese medical text 'Shang Han Lun' by Zhang Zhongjing (portrait shown), explaining 'He found the patterns 1800 years ago'. "
            "Panel 3 — Six pattern boxes laid out like a detective's evidence board: Tai Yang, Yang Ming, Shao Yang, Tai Yin, Shao Yin, Jue Yin — each with symptoms pinned to them. "
            "Panel 4 — Ollie connecting symptoms to the correct pattern box with string, solving the case: 'Pattern recognition, not guessing — Zhang Zhongjing's method still works today.'"
        )
    },
    "21": {
        "title": "Stop Fighting, Start Warming",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic comparing the body to a house in winter: "
            "Panel 1 — A person aggressively attacking a cold with cold medicines (ice cubes, cold pills) — fighting fire with ice, making things worse. "
            "Panel 2 — Ollie comparing the body to a house in winter: cold has entered through an open window (the body's surface), the thermostat (Yang Qi) is struggling. "
            "Panel 3 — Two approaches: (left) person blasting AC — body gets colder; (right) person adding warm blankets and hot soup — body warms up naturally. "
            "Panel 4 — The house (body) warm and cozy, fire burning in the hearth, person healthy and smiling, Ollie beside the fireplace: 'Stop fighting the cold. Start warming the body.'"
        )
    },
    "22": {
        "title": "Wind-Cold Is Not a Weather Report",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about Gui Zhi Tang vs Ma Huang Tang: "
            "Panel 1 — A person standing outside in windy cold weather, shivering, Ollie looking concerned. "
            "Panel 2 — Ollie asking the crucial question 'Do you sweat?', showing two paths: person with sweat (Gui Zhi Tang path), person without sweat (Ma Huang Tang path). "
            "Panel 3 — The sweating person receiving Gui Zhi Tang (Cinnamon Twig Decoction): gentle warming that harmonizes, shown as a mild sun warming the body. "
            "Panel 4 — The non-sweating person receiving Ma Huang Tang (Ephedra Decoction): stronger opening of pores, shown as steam rising from the body — Ollie explaining 'One question changes everything.'"
        )
    },
    "23": {
        "title": "Your Fever Might Be Your Friend",
        "prompt": (
            f"{BANDW_PREFIX}{OLLIE_BW} "
            "Four-panel comic about fever and the White Tiger formula: "
            "Panel 1 — A person with a thermometer showing high fever, looking worried and reaching for fever-reducing pills. "
            "Panel 2 — Ollie stopping them: 'Fever is your body fighting — don't shut it down.' Shows body as a battlefield where heat (fever) is the weapon against invaders. "
            "Panel 3 — Ollie introduces Bai Hu Tang (White Tiger Decoction): four herbs (Gypsum, Anemarrhena, Licorice, Rice) that cool without suppressing — shown as a white tiger gently cooling the battlefield. "
            "Panel 4 — Fever resolved naturally, person healthy, Ollie beside them: 'Support the fever, don't fight it. That's what the White Tiger formula does.'"
        )
    },
}


def generate_comic(num, prompt, max_retries=3):
    """Generate a single comic using bl CLI."""
    output_path = os.path.join(OUT_DIR, f"comic-{num}-bw.png")
    
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                [
                    "bl", "image", "generate",
                    "--model", "qwen-image-2.0",
                    "--prompt", prompt,
                    "--negative-prompt", BANDW_NEGATIVE,
                    "--size", "1024*1024",
                    "--watermark", "false",
                    "--output", output_path,
                ],
                capture_output=True,
                text=True,
                timeout=180,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )
            
            if result.returncode == 0:
                size_kb = os.path.getsize(output_path) / 1024 if os.path.exists(output_path) else 0
                print(f"  ✅ comic-{num}-bw.png ({size_kb:.0f}KB)")
                return True
            else:
                stderr = result.stderr[:300] if result.stderr else "no stderr"
                print(f"  ⚠️ Attempt {attempt+1} failed: {stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"  ⚠️ Attempt {attempt+1} timed out")
        except Exception as e:
            print(f"  ⚠️ Attempt {attempt+1} error: {e}")
        
        if attempt < max_retries - 1:
            wait = (attempt + 1) * 10
            print(f"  Retrying in {wait}s...")
            time.sleep(wait)
    
    print(f"  ❌ FAILED after {max_retries} attempts")
    return False


def main():
    total = len(COMICS)
    success = 0
    failed = []
    
    print("=" * 70)
    print(f"GENERATING {total} B&W HAND-DRAWN COMICS")
    print("Style: Black ink, 2D flat, Ollie grayscale, pure white BG")
    print("=" * 70)
    
    for num in sorted(COMICS.keys()):
        comic = COMICS[num]
        print(f"\n📖 #{num}: {comic['title']}")
        print(f"   Prompt length: {len(comic['prompt'])} chars")
        
        if generate_comic(num, comic['prompt']):
            success += 1
        else:
            failed.append(num)
        
        # Brief pause between generations
        if num != sorted(COMICS.keys())[-1]:
            time.sleep(3)
    
    print("\n" + "=" * 70)
    print(f"SUMMARY: {success}/{total} generated successfully")
    if failed:
        print(f"FAILED: {', '.join(failed)}")
    print("=" * 70)
    
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
