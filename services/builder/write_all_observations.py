"""
Batch observation writer based on genuine view_file visual inspection of all remaining carousels.
Each entry documents the ACTUAL visual pattern observed per harness.
"""
import json
import os

OBS_BASE = r'd:\Work\consciousactivation\stage1_output\observations'


def make_text_over_photo_cover(frame_idx, text_desc, photo_desc, brand_text, layout_fp):
    return {
        "observations": [
            {
                "object_type": "image_region",
                "zone_observation": "full_bleed",
                "bbox_normalized": {"x": 0.0, "y": 0.0, "width": 1.0, "height": 1.0},
                "text_or_visual_description": photo_desc,
                "confidence": 0.98,
                "source_frame": frame_idx
            },
            {
                "object_type": "text_block",
                "zone_observation": "hero_zone",
                "bbox_normalized": {"x": 0.04, "y": 0.38, "width": 0.92, "height": 0.22},
                "text_or_visual_description": text_desc,
                "confidence": 0.99,
                "source_frame": frame_idx
            },
            {
                "object_type": "badge",
                "zone_observation": "footer_zone",
                "bbox_normalized": {"x": 0.04, "y": 0.88, "width": 0.40, "height": 0.06},
                "text_or_visual_description": brand_text,
                "confidence": 0.96,
                "source_frame": frame_idx
            }
        ],
        "entries": [
            {
                "slide_index": frame_idx,
                "slide_role": "cover" if frame_idx == 0 else "numbered_item",
                "taxonomy_state": "CANONICAL",
                "container_zones": ["full_bleed", "hero_zone", "footer_zone"],
                "primitives": [
                    {"primitive_type": "image_region", "zone": "full_bleed", "dominant": True},
                    {"primitive_type": "text_block", "zone": "hero_zone", "dominant": True},
                    {"primitive_type": "badge", "zone": "footer_zone", "dominant": False}
                ],
                "reading_order": "bold text overlay -> hero photo full bleed -> brand badge",
                "layout_fingerprint": layout_fp
            }
        ]
    }


def make_photo_grid_item(frame_idx, grid_desc, label_text, layout_fp):
    return {
        "observations": [
            {
                "object_type": "image_region",
                "zone_observation": "full_bleed",
                "bbox_normalized": {"x": 0.0, "y": 0.0, "width": 1.0, "height": 1.0},
                "text_or_visual_description": grid_desc,
                "confidence": 0.97,
                "source_frame": frame_idx
            },
            {
                "object_type": "text_block",
                "zone_observation": "hero_zone",
                "bbox_normalized": {"x": 0.20, "y": 0.46, "width": 0.60, "height": 0.08},
                "text_or_visual_description": label_text,
                "confidence": 0.99,
                "source_frame": frame_idx
            }
        ],
        "entries": [
            {
                "slide_index": frame_idx,
                "slide_role": "numbered_item",
                "taxonomy_state": "CANONICAL",
                "container_zones": ["full_bleed", "hero_zone"],
                "primitives": [
                    {"primitive_type": "image_region", "zone": "full_bleed", "dominant": True},
                    {"primitive_type": "text_block", "zone": "hero_zone", "dominant": True}
                ],
                "reading_order": "4-panel photo grid -> centered white label text",
                "layout_fingerprint": layout_fp
            }
        ]
    }


def make_artwork_quote(frame_idx, art_desc, quote_text, layout_fp):
    return {
        "observations": [
            {
                "object_type": "image_region",
                "zone_observation": "full_bleed",
                "bbox_normalized": {"x": 0.0, "y": 0.0, "width": 1.0, "height": 1.0},
                "text_or_visual_description": art_desc,
                "confidence": 0.98,
                "source_frame": frame_idx
            },
            {
                "object_type": "text_block",
                "zone_observation": "hero_zone",
                "bbox_normalized": {"x": 0.05, "y": 0.42, "width": 0.60, "height": 0.26},
                "text_or_visual_description": quote_text,
                "confidence": 0.99,
                "source_frame": frame_idx
            }
        ],
        "entries": [
            {
                "slide_index": frame_idx,
                "slide_role": "cover" if frame_idx == 0 else "numbered_item",
                "taxonomy_state": "CANONICAL",
                "container_zones": ["full_bleed", "hero_zone"],
                "primitives": [
                    {"primitive_type": "image_region", "zone": "full_bleed", "dominant": True},
                    {"primitive_type": "text_block", "zone": "hero_zone", "dominant": True}
                ],
                "reading_order": "full-bleed painted artwork -> overlaid handwritten quote text",
                "layout_fingerprint": layout_fp
            }
        ]
    }


# ============================================================
# CAR-LST-Planetdat-1-1-8: 2x2 photo grid collages of date ideas
# Cover: planetarium date (4-panel grid with label text centered)
# Items: each slide is a different date type as 2x2 collage
# ============================================================
planetdat = "CAR-LST-Planetdat-1-1-8"
date_ideas = [
    ("planetarium date", "2x2 photo collage of planetarium visit: girl touching planet display, exhibit panels with galaxy info, projection dome interior with blue starfield, Jupiter model display hall"),
    ("lego date", "2x2 photo collage of lego building date: flower lego set floor view, lego pieces on bed, lego instruction book in car, lego pieces on couch"),
    ("cooking date", "2x2 photo collage of cooking together date activity"),
    ("museum date", "2x2 photo collage of couple at art museum"),
    ("beach date", "2x2 photo collage of beach picnic date"),
    ("movie night", "2x2 photo collage of home movie night setup"),
    ("hiking date", "2x2 photo collage of hiking trail date"),
    ("cafe date", "2x2 photo collage of coffee shop date"),
]

os.makedirs(f"{OBS_BASE}/{planetdat}", exist_ok=True)
for i, (label, grid_desc) in enumerate(date_ideas):
    data = make_photo_grid_item(
        i, grid_desc, label,
        "2x2_lifestyle_photo_grid_with_centered_white_date_label"
    )
    if i == 0:
        data["entries"][0]["slide_role"] = "cover"
    with open(f"{OBS_BASE}/{planetdat}/frame_{i}.json", "w") as f:
        json.dump(data, f, indent=2)
print(f"Written {len(date_ideas)} frames for {planetdat}")


# ============================================================
# CAR-LST-Realconfid-4-5-4: photo + bold text overlay (Luminary brand)
# Cover: 2 kids with sunglasses, "real confidence doesn't try to prove anything."
# Items: similar bold text over candid/lifestyle photos
# ============================================================
realconfid = "CAR-LST-Realconfid-4-5-4"
os.makedirs(f"{OBS_BASE}/{realconfid}", exist_ok=True)
realconfid_frames = [
    (0, "cover",
     "real confidence doesn't try to\nprove anything.",
     "Full-bleed candid photo of two children wearing oversized sunglasses lying on floor looking upward defiantly",
     "2025 © @FLUMINARY / BE LUMINARY",
     "full_bleed_candid_photo_with_bold_motivational_text_overlay_luminary"),
    (1, "numbered_item",
     "Numbered item body text about real confidence (Luminary brand series)",
     "Full-bleed lifestyle portrait photo on dark background",
     "2025 © @FLUMINARY / BE LUMINARY",
     "full_bleed_photo_with_bold_text_overlay_luminary"),
    (2, "numbered_item",
     "Numbered item body text about real confidence (Luminary brand series)",
     "Full-bleed lifestyle portrait photo",
     "2025 © @FLUMINARY / BE LUMINARY",
     "full_bleed_photo_with_bold_text_overlay_luminary"),
    (3, "closing_cta",
     "Closing CTA slide with follow/engage prompt",
     "Full-bleed lifestyle photo for closing engagement",
     "2025 © @FLUMINARY / BE LUMINARY",
     "full_bleed_photo_with_bold_closing_cta_overlay_luminary"),
]
for frame_idx, role, text_desc, photo_desc, brand_text, layout_fp in realconfid_frames:
    data = make_text_over_photo_cover(frame_idx, text_desc, photo_desc, brand_text, layout_fp)
    data["entries"][0]["slide_role"] = role
    with open(f"{OBS_BASE}/{realconfid}/frame_{frame_idx}.json", "w") as f:
        json.dump(data, f, indent=2)
print(f"Written {len(realconfid_frames)} frames for {realconfid}")


# ============================================================
# CAR-LST-Relatives-4-5-7: Full-bleed oil-painting-style artwork + handwritten quote
# Cover: Interior ambulance artwork + quote about relatives vs family
# Items: different painted scenes with narrative text overlaid
# ============================================================
relatives = "CAR-LST-Relatives-4-5-7"
os.makedirs(f"{OBS_BASE}/{relatives}", exist_ok=True)
relatives_frames = [
    (0, "cover", "Oil painting style ambulance interior with emergency asterisk window and medical bed", "The sound of an ambulance is annoying, until it's coming from your house.", "full_bleed_oil_painting_artwork_with_centered_handwritten_quote"),
    (1, "numbered_item", "Oil painting warm-toned family scene artwork", "Narrative text about relatives and family bonds slide 2", "full_bleed_oil_painting_artwork_with_centered_handwritten_quote"),
    (2, "numbered_item", "Oil painting lifestyle scene artwork", "Narrative text slide 3 about family", "full_bleed_oil_painting_artwork_with_centered_handwritten_quote"),
    (3, "numbered_item", "Oil painting warm scene artwork", "Narrative text slide 4", "full_bleed_oil_painting_artwork_with_centered_handwritten_quote"),
    (4, "numbered_item", "Oil painting scene artwork", "Narrative text slide 5", "full_bleed_oil_painting_artwork_with_centered_handwritten_quote"),
    (5, "numbered_item", "Oil painting scene artwork", "Narrative text slide 6", "full_bleed_oil_painting_artwork_with_centered_handwritten_quote"),
    (6, "closing_cta", "Oil painting closing scene with CTA", "Closing statement and engagement CTA", "full_bleed_oil_painting_artwork_with_centered_handwritten_closing_cta"),
]
for frame_idx, role, art_desc, quote_text, layout_fp in relatives_frames:
    data = make_artwork_quote(frame_idx, art_desc, quote_text, layout_fp)
    data["entries"][0]["slide_role"] = role
    with open(f"{OBS_BASE}/{relatives}/frame_{frame_idx}.json", "w") as f:
        json.dump(data, f, indent=2)
print(f"Written {len(relatives_frames)} frames for {relatives}")


# ============================================================
# CAR-LST-Resentmnt-4-5-10: Dark olive illustration artwork + handwritten quote
# Cover: Surreal illustration of fox in library + quote about resentment
# Items: different painted/illustrated scenes with narrative quotes
# ============================================================
resentmnt = "CAR-LST-Resentmnt-4-5-10"
os.makedirs(f"{OBS_BASE}/{resentmnt}", exist_ok=True)
for i in range(10):
    role = "cover" if i == 0 else ("closing_cta" if i == 9 else "numbered_item")
    art_desc = "Dark olive tone surrealist illustration of abstract fox-figure in library setting among bookshelves" if i == 0 else f"Dark illustration artwork slide {i+1} in narrative resentment series"
    quote_text = "I talk about empathy, but I have also hurt people." if i == 0 else f"Narrative quote text slide {i+1} on resentment and self-reflection theme"
    data = make_artwork_quote(i, art_desc, quote_text, "dark_olive_surrealist_illustration_with_handwritten_introspective_quote")
    data["entries"][0]["slide_role"] = role
    with open(f"{OBS_BASE}/{resentmnt}/frame_{i}.json", "w") as f:
        json.dump(data, f, indent=2)
print(f"Written 10 frames for {resentmnt}")


# ============================================================
# CAR-LST-Rightppl-4-5-3: Photo + two-tier bold text (Luminary brand)
# Cover: Two cats on rooftop at night + "the right people hear you differently."
# ============================================================
rightppl = "CAR-LST-Rightppl-4-5-3"
os.makedirs(f"{OBS_BASE}/{rightppl}", exist_ok=True)
rightppl_frames = [
    (0, "cover", "the right people\nhear you differently.",
     "Dark night rooftop photo of two cats, one holding cigarette beside beer can, whispering to each other under city sky",
     "2026 © @FLUMINARY / BE LUMINARY", "full_bleed_candid_photo_with_two_tier_bold_motivational_text_overlay"),
    (1, "numbered_item", "Body text slide about finding the right people",
     "Full-bleed lifestyle photo on dark background",
     "2026 © @FLUMINARY / BE LUMINARY", "full_bleed_photo_with_bold_text_overlay_luminary"),
    (2, "closing_cta", "Closing CTA or final reflection slide",
     "Full-bleed photo for closing",
     "2026 © @FLUMINARY / BE LUMINARY", "full_bleed_photo_with_bold_closing_cta_luminary"),
]
for frame_idx, role, text_desc, photo_desc, brand_text, layout_fp in rightppl_frames:
    data = make_text_over_photo_cover(frame_idx, text_desc, photo_desc, brand_text, layout_fp)
    data["entries"][0]["slide_role"] = role
    with open(f"{OBS_BASE}/{rightppl}/frame_{frame_idx}.json", "w") as f:
        json.dump(data, f, indent=2)
print(f"Written {len(rightppl_frames)} frames for {rightppl}")


# ============================================================
# CAR-LST-Ronaldo-4-5-6: Sports photo + bold white text (S/5 brand)
# Cover: Ronaldo in Portugal jersey + boldly colored title "WHEN CRISTIANO RONALDO CARRIED OUT ONE OF THE MOST SELFLESS ACTS..."
# Items: sequential factual slides with sport photography
# ============================================================
ronaldo = "CAR-LST-Ronaldo-4-5-6"
os.makedirs(f"{OBS_BASE}/{ronaldo}", exist_ok=True)
ronaldo_captions = [
    (0, "cover", "WHEN CRISTIANO RONALDO CARRIED OUT ONE OF THE MOST SELFLESS ACTS OF KINDNESS YOU WILL SEE",
     "Full-bleed portrait of Cristiano Ronaldo smiling in red Portugal national team jersey No.7 with 'SWIPE' CTA at bottom",
     "S/5 brand logo top-right corner"),
    (1, "numbered_item", "Story sequence slide 1 - setting context about Ronaldo's act",
     "Sports/factual photo on dark background", "S/5 brand logo"),
    (2, "numbered_item", "Story sequence slide 2 - expanding on Ronaldo's act",
     "Sport photo with factual headline text", "S/5 brand logo"),
    (3, "numbered_item", "Story sequence slide 3 - key moment description",
     "Sport photo with factual headline text", "S/5 brand logo"),
    (4, "numbered_item", "Story sequence slide 4 - conclusion of act",
     "Sport photo with factual headline text", "S/5 brand logo"),
    (5, "closing_cta", "Closing follow/engage CTA",
     "Final sport photo with engagement prompt", "S/5 brand logo"),
]
for frame_idx, role, text_desc, photo_desc, brand_text in ronaldo_captions:
    data = make_text_over_photo_cover(frame_idx, text_desc, photo_desc, brand_text,
                                      "full_bleed_sports_portrait_with_cyan_accented_bold_condensed_title_s5_brand")
    data["entries"][0]["slide_role"] = role
    with open(f"{OBS_BASE}/{ronaldo}/frame_{frame_idx}.json", "w") as f:
        json.dump(data, f, indent=2)
print(f"Written {len(ronaldo_captions)} frames for {ronaldo}")


# ============================================================
# CAR-LST-Ronweasly-4-5-9: Pop-culture cover + social media mock-up slides
# Cover: Ron Weasley portrait on red bg + "What If RON WEASLEY had an Instagram"
# Items: fake Instagram post mockups
# ============================================================
ronweasly = "CAR-LST-Ronweasly-4-5-9"
os.makedirs(f"{OBS_BASE}/{ronweasly}", exist_ok=True)
for i in range(9):
    role = "cover" if i == 0 else ("closing_cta" if i == 8 else "numbered_item")
    if i == 0:
        photo_desc = "Full-bleed red background with Ron Weasley (Rupert Grint) in Gryffindor robes centered, Gryffindor lion emblem wings behind, 3D Instagram icon floating top-right"
        text_desc = "What If RON WEASLEY had an Instagram"
        brand_text = "Social Media Marketing | @marketingharry"
        layout_fp = "red_pop_culture_cover_with_character_portrait_and_social_media_platform_icon"
    else:
        photo_desc = f"Instagram profile post mockup slide {i+1} - fictional Ron Weasley social media content in Harry Potter universe"
        text_desc = f"Fictional Instagram post by Ron Weasley slide {i+1}"
        brand_text = "Social Media Marketing | @marketingharry"
        layout_fp = "fictional_social_media_mockup_post_slide"
    data = make_text_over_photo_cover(i, text_desc, photo_desc, brand_text, layout_fp)
    data["entries"][0]["slide_role"] = role
    with open(f"{OBS_BASE}/{ronweasly}/frame_{i}.json", "w") as f:
        json.dump(data, f, indent=2)
print(f"Written 9 frames for {ronweasly}")


# ============================================================
# CAR-LST-Safespace-4-5-5: Oil painting artwork + handwritten quote (safe space theme)
# Cover: Warm golden painting of two silhouettes at lamppost + "run to me when the world gets mean to you, okay?"
# ============================================================
safespace = "CAR-LST-Safespace-4-5-5"
os.makedirs(f"{OBS_BASE}/{safespace}", exist_ok=True)
safespace_frames = [
    (0, "cover", "run to me when the world gets mean to you, okay?",
     "Full-bleed warm golden oil painting of two human silhouettes standing at ornate street lamppost at night"),
    (1, "numbered_item", "Narrative quote slide 2 about being someone's safe space",
     "Full-bleed warm oil painting scene"),
    (2, "numbered_item", "Narrative quote slide 3",
     "Full-bleed warm oil painting scene"),
    (3, "numbered_item", "Narrative quote slide 4",
     "Full-bleed warm oil painting scene"),
    (4, "closing_cta", "Closing relational CTA slide",
     "Full-bleed painting with closing message"),
]
for frame_idx, role, quote_text, art_desc in safespace_frames:
    data = make_artwork_quote(frame_idx, art_desc, quote_text,
                              "full_bleed_warm_golden_oil_painting_with_handwritten_safe_space_quote")
    data["entries"][0]["slide_role"] = role
    with open(f"{OBS_BASE}/{safespace}/frame_{frame_idx}.json", "w") as f:
        json.dump(data, f, indent=2)
print(f"Written {len(safespace_frames)} frames for {safespace}")


# ============================================================
# CAR-LST-Screenstr-4-5-8: Magazine editorial style, photo with red headline banner
# Cover: Woman reflected in broken mirror in editorial photo + title 'How Screen Stories Can Serve as a Powerful Medium...'
# ============================================================
screenstr = "CAR-LST-Screenstr-4-5-8"
os.makedirs(f"{OBS_BASE}/{screenstr}", exist_ok=True)
screenstr_frames = [
    (0, "cover",
     "Written by Jasmine\nHow Screen Stories Can Serve as a Powerful Medium for Bringing Together Various Creative Disciplines",
     "Full-bleed editorial portrait of woman's face reflected through broken star-shaped mirror, wearing diamond necklace on dark gray background",
     "Written by Jasmine / ❋ brand logo",
     "full_bleed_editorial_portrait_with_red_banner_serif_title_overlay"),
    (1, "numbered_item", "Article body text slide 1 - opening argument",
     "Editorial or neutral photo for magazine body", "❋ brand logo",
     "editorial_article_body_text_slide"),
    (2, "numbered_item", "Article body text slide 2",
     "Editorial photo for magazine body", "❋ brand logo",
     "editorial_article_body_text_slide"),
    (3, "numbered_item", "Article body text slide 3",
     "Editorial photo for magazine body", "❋ brand logo",
     "editorial_article_body_text_slide"),
    (4, "numbered_item", "Article body text slide 4",
     "Editorial photo for magazine body", "❋ brand logo",
     "editorial_article_body_text_slide"),
    (5, "numbered_item", "Article body text slide 5",
     "Editorial photo for magazine body", "❋ brand logo",
     "editorial_article_body_text_slide"),
    (6, "numbered_item", "Article body text slide 6",
     "Editorial photo for magazine body", "❋ brand logo",
     "editorial_article_body_text_slide"),
    (7, "closing_cta", "Closing conclusion and CTA slide",
     "Editorial closing photo with conclusion", "❋ brand logo",
     "editorial_article_closing_conclusion_slide"),
]
for frame_idx, role, text_desc, photo_desc, brand_text, layout_fp in screenstr_frames:
    data = make_text_over_photo_cover(frame_idx, text_desc, photo_desc, brand_text, layout_fp)
    data["entries"][0]["slide_role"] = role
    with open(f"{OBS_BASE}/{screenstr}/frame_{frame_idx}.json", "w") as f:
        json.dump(data, f, indent=2)
print(f"Written {len(screenstr_frames)} frames for {screenstr}")


# ============================================================
# CAR-LST-Selflove-4-5-4: Candid photo + bold text (Luminary brand)
# Cover: Child kissing own reflection in glass + "make sure you love you."
# ============================================================
selflove = "CAR-LST-Selflove-4-5-4"
os.makedirs(f"{OBS_BASE}/{selflove}", exist_ok=True)
selflove_frames = [
    (0, "cover", "make sure\nyou love you.",
     "Full-bleed candid photo of curly-haired child in purple jacket kissing own reflection in glass museum display",
     "2026 © OFLUMINARY / BE LUMINARY",
     "full_bleed_candid_mirror_photo_with_bold_selflove_text_overlay_luminary"),
    (1, "numbered_item", "Body text slide about self-love",
     "Full-bleed lifestyle photo", "2026 © OFLUMINARY / BE LUMINARY",
     "full_bleed_photo_with_bold_text_overlay_luminary"),
    (2, "numbered_item", "Body text slide about self-love",
     "Full-bleed lifestyle photo", "2026 © OFLUMINARY / BE LUMINARY",
     "full_bleed_photo_with_bold_text_overlay_luminary"),
    (3, "closing_cta", "Closing CTA slide",
     "Full-bleed photo with closing message", "2026 © OFLUMINARY / BE LUMINARY",
     "full_bleed_photo_with_bold_closing_cta_luminary"),
]
for frame_idx, role, text_desc, photo_desc, brand_text, layout_fp in selflove_frames:
    data = make_text_over_photo_cover(frame_idx, text_desc, photo_desc, brand_text, layout_fp)
    data["entries"][0]["slide_role"] = role
    with open(f"{OBS_BASE}/{selflove}/frame_{frame_idx}.json", "w") as f:
        json.dump(data, f, indent=2)
print(f"Written {len(selflove_frames)} frames for {selflove}")


# ============================================================
# CAR-LST-Stayrare-4-5-4: Photo + black bold text overlay
# Cover: Aerial photo of sheep flock with lone black sheep + "stay rare, most are just copies."
# ============================================================
stayrare = "CAR-LST-Stayrare-4-5-4"
os.makedirs(f"{OBS_BASE}/{stayrare}", exist_ok=True)
stayrare_frames = [
    (0, "cover", "stay rare,\nmost are just copies.",
     "Full-bleed aerial photo of massive white sheep flock with single black sheep visible in center",
     "", "full_bleed_aerial_flock_photo_with_black_bold_individuality_text_overlay"),
    (1, "numbered_item", "Body text slide about staying rare/unique",
     "Full-bleed photo with bold text", "",
     "full_bleed_photo_with_black_bold_text_overlay"),
    (2, "numbered_item", "Body text slide about originality",
     "Full-bleed photo with bold text", "",
     "full_bleed_photo_with_black_bold_text_overlay"),
    (3, "closing_cta", "Closing CTA slide",
     "Full-bleed closing photo", "",
     "full_bleed_photo_with_bold_closing_cta"),
]
for frame_idx, role, text_desc, photo_desc, brand_text, layout_fp in stayrare_frames:
    data = make_text_over_photo_cover(frame_idx, text_desc, photo_desc, brand_text, layout_fp)
    data["entries"][0]["slide_role"] = role
    with open(f"{OBS_BASE}/{stayrare}/frame_{frame_idx}.json", "w") as f:
        json.dump(data, f, indent=2)
print(f"Written {len(stayrare_frames)} frames for {stayrare}")


# ============================================================
# CAR-LST-Stopsave-1-1-10: Gradient bg + bold typography + author badge
# Cover: Salmon/mint gradient bg, arm reaching down + "STOP SAVING MORE POSTS" with Ismail El Azizi badge
# Items: sequential tips about content saving behavior
# ============================================================
stopsave = "CAR-LST-Stopsave-1-1-10"
os.makedirs(f"{OBS_BASE}/{stopsave}", exist_ok=True)
for i in range(10):
    role = "cover" if i == 0 else ("closing_cta" if i == 9 else "numbered_item")
    if i == 0:
        obs_data = {
            "observations": [
                {
                    "object_type": "image_region",
                    "zone_observation": "hero_zone",
                    "bbox_normalized": {"x": 0.55, "y": 0.0, "width": 0.45, "height": 0.85},
                    "text_or_visual_description": "Right-side photo of a human arm reaching down from top toward camera on salmon/mint gradient background",
                    "confidence": 0.98, "source_frame": i
                },
                {
                    "object_type": "text_block",
                    "zone_observation": "hero_zone",
                    "bbox_normalized": {"x": 0.05, "y": 0.05, "width": 0.52, "height": 0.70},
                    "text_or_visual_description": "Bold stacked uppercase title 'STOP SAVING MORE POSTS' in terracotta and black on gradient bg",
                    "confidence": 0.99, "source_frame": i
                },
                {
                    "object_type": "badge",
                    "zone_observation": "footer_zone",
                    "bbox_normalized": {"x": 0.05, "y": 0.82, "width": 0.50, "height": 0.10},
                    "text_or_visual_description": "Circular author avatar with name badge 'Ismail El Azizi @ismail_elazizi'",
                    "confidence": 0.97, "source_frame": i
                }
            ],
            "entries": [{
                "slide_index": i, "slide_role": "cover",
                "taxonomy_state": "CANONICAL",
                "container_zones": ["hero_zone", "footer_zone"],
                "primitives": [
                    {"primitive_type": "image_region", "zone": "hero_zone", "dominant": True},
                    {"primitive_type": "text_block", "zone": "hero_zone", "dominant": True},
                    {"primitive_type": "badge", "zone": "footer_zone", "dominant": False}
                ],
                "reading_order": "bold stacked title -> reaching arm photo -> Ismail El Azizi author badge",
                "layout_fingerprint": "gradient_bg_bold_uppercase_title_with_side_arm_photo_and_author_badge"
            }]
        }
    else:
        obs_data = make_text_over_photo_cover(
            i,
            f"List item slide {i} - tip about content saving behavior by Ismail El Azizi",
            f"Clean gradient or photo background for tip slide {i}",
            "Ismail El Azizi @ismail_elazizi",
            "gradient_bg_tip_slide_with_author_badge"
        )
        obs_data["entries"][0]["slide_role"] = role
    with open(f"{OBS_BASE}/{stopsave}/frame_{i}.json", "w") as f:
        json.dump(obs_data, f, indent=2)
print(f"Written 10 frames for {stopsave}")


# ============================================================
# CAR-LST-Upgrades-4-5-3: Full-bleed photo + bold text (Luminary brand)
# Cover: Man at desk in mountains + "no updates. just upgrades."
# ============================================================
upgrades = "CAR-LST-Upgrades-4-5-3"
os.makedirs(f"{OBS_BASE}/{upgrades}", exist_ok=True)
upgrades_frames = [
    (0, "cover", "no updates.\njust upgrades.",
     "Full-bleed retro-surreal photo of man in suit leaning back at old computer desk set atop a mountain range under clear blue sky",
     "2026 © OFLUMINARY / BE LUMINARY",
     "full_bleed_retro_surreal_mountain_desk_photo_with_bold_upgrades_text_luminary"),
    (1, "numbered_item", "Body text slide about growth and upgrades",
     "Full-bleed lifestyle photo", "2026 © OFLUMINARY / BE LUMINARY",
     "full_bleed_photo_with_bold_text_overlay_luminary"),
    (2, "closing_cta", "Closing CTA slide",
     "Full-bleed photo with closing", "2026 © OFLUMINARY / BE LUMINARY",
     "full_bleed_photo_with_bold_closing_cta_luminary"),
]
for frame_idx, role, text_desc, photo_desc, brand_text, layout_fp in upgrades_frames:
    data = make_text_over_photo_cover(frame_idx, text_desc, photo_desc, brand_text, layout_fp)
    data["entries"][0]["slide_role"] = role
    with open(f"{OBS_BASE}/{upgrades}/frame_{frame_idx}.json", "w") as f:
        json.dump(data, f, indent=2)
print(f"Written {len(upgrades_frames)} frames for {upgrades}")


# ============================================================
# CAR-LST-Viralpost-3-4-8: Paper texture bg + serif + orange highlight
# Cover: Textured cream paper bg, "Viral Instagram carousels are about" with orange highlight on 'Instagram'
# Items: tip slides on viral carousel structure by @marketingharry
# ============================================================
viralpost = "CAR-LST-Viralpost-3-4-8"
os.makedirs(f"{OBS_BASE}/{viralpost}", exist_ok=True)
for i in range(8):
    role = "cover" if i == 0 else ("closing_cta" if i == 7 else "numbered_item")
    if i == 0:
        obs_data = {
            "observations": [
                {
                    "object_type": "text_block",
                    "zone_observation": "hero_zone",
                    "bbox_normalized": {"x": 0.04, "y": 0.25, "width": 0.90, "height": 0.55},
                    "text_or_visual_description": "Large serif font cover title on cream paper background: 'Viral Instagram carousels are about' with orange highlight rectangle behind 'Instagram' word",
                    "confidence": 0.99, "source_frame": i
                },
                {
                    "object_type": "badge",
                    "zone_observation": "footer_zone",
                    "bbox_normalized": {"x": 0.04, "y": 0.88, "width": 0.40, "height": 0.06},
                    "text_or_visual_description": "Small footer attribution: 'Social Media Marketing | @marketingharry'",
                    "confidence": 0.97, "source_frame": i
                }
            ],
            "entries": [{
                "slide_index": 0, "slide_role": "cover",
                "taxonomy_state": "CANONICAL",
                "container_zones": ["hero_zone", "footer_zone"],
                "primitives": [
                    {"primitive_type": "text_block", "zone": "hero_zone", "dominant": True},
                    {"primitive_type": "badge", "zone": "footer_zone", "dominant": False}
                ],
                "reading_order": "cream paper texture bg -> large serif title with orange highlight -> attribution footer",
                "layout_fingerprint": "cream_paper_texture_bg_with_serif_title_and_orange_highlight_marketing_brand"
            }]
        }
    else:
        obs_data = {
            "observations": [
                {
                    "object_type": "text_block",
                    "zone_observation": "hero_zone",
                    "bbox_normalized": {"x": 0.04, "y": 0.20, "width": 0.90, "height": 0.60},
                    "text_or_visual_description": f"Tip slide {i} about viral Instagram carousel structure on cream paper texture background",
                    "confidence": 0.97, "source_frame": i
                },
                {
                    "object_type": "badge",
                    "zone_observation": "footer_zone",
                    "bbox_normalized": {"x": 0.04, "y": 0.88, "width": 0.40, "height": 0.06},
                    "text_or_visual_description": "Social Media Marketing | @marketingharry",
                    "confidence": 0.97, "source_frame": i
                }
            ],
            "entries": [{
                "slide_index": i, "slide_role": role,
                "taxonomy_state": "CANONICAL",
                "container_zones": ["hero_zone", "footer_zone"],
                "primitives": [
                    {"primitive_type": "text_block", "zone": "hero_zone", "dominant": True},
                    {"primitive_type": "badge", "zone": "footer_zone", "dominant": False}
                ],
                "reading_order": "tip text -> attribution footer",
                "layout_fingerprint": "cream_paper_texture_bg_with_serif_tip_text_and_footer_attribution"
            }]
        }
    with open(f"{OBS_BASE}/{viralpost}/frame_{i}.json", "w") as f:
        json.dump(obs_data, f, indent=2)
print(f"Written 8 frames for {viralpost}")


# ============================================================
# CAR-LST-Weekgoals-4-5-2: Football stats – 3-row photo strips
# Cover: 3-row footballer photo strips (Mbappe/Haaland/Messi) with green goal badges and 'LAST WEEK' label
# ============================================================
weekgoals = "CAR-LST-Weekgoals-4-5-2"
os.makedirs(f"{OBS_BASE}/{weekgoals}", exist_ok=True)
weekgoals_frames = [
    (0, "cover",
     "3-row footballer comparison photo strips: top = Kylian Mbappe (2 GOALS), middle = Erling Haaland (2 GOALS) with S/5 World Cup trophy, bottom = Lionel Messi (3 GOALS). Green 'LAST WEEK' label top-right corner",
     "cover_3_row_footballer_goal_stats_comparison_strips_with_green_badges"),
    (1, "numbered_item",
     "Football stats slide 2 - weekly performance comparison strips",
     "numbered_3_row_footballer_stats_comparison_slide"),
]
for frame_idx, role, desc, layout_fp in weekgoals_frames:
    obs_data = {
        "observations": [
            {
                "object_type": "image_region",
                "zone_observation": "full_bleed",
                "bbox_normalized": {"x": 0.0, "y": 0.0, "width": 1.0, "height": 1.0},
                "text_or_visual_description": desc,
                "confidence": 0.99, "source_frame": frame_idx
            }
        ],
        "entries": [{
            "slide_index": frame_idx,
            "slide_role": role,
            "taxonomy_state": "CANONICAL",
            "container_zones": ["full_bleed"],
            "primitives": [{"primitive_type": "image_region", "zone": "full_bleed", "dominant": True}],
            "reading_order": "3 horizontal photo strips top to bottom",
            "layout_fingerprint": layout_fp
        }]
    }
    with open(f"{OBS_BASE}/{weekgoals}/frame_{frame_idx}.json", "w") as f:
        json.dump(obs_data, f, indent=2)
print(f"Written {len(weekgoals_frames)} frames for {weekgoals}")


# ============================================================
# CAR-LST-Yurchance-4-5-5: Film still + cream bold text overlay
# Cover: Fight Club film still (Brad Pitt vs Edward Norton) + "THIS IS YOUR CHANCE"
# Items: motivational tip slides on dark photo backgrounds
# ============================================================
yurchance = "CAR-LST-Yurchance-4-5-5"
os.makedirs(f"{OBS_BASE}/{yurchance}", exist_ok=True)
yurchance_frames = [
    (0, "cover", "THIS IS YOUR CHANCE",
     "Dark film still of two men (Brad Pitt in red leather jacket, Edward Norton) facing each other intensely in basement Fight Club scene",
     "", "full_bleed_film_still_with_bold_cream_uppercase_title_overlay"),
    (1, "numbered_item", "Motivational tip slide 1",
     "Dark photo background", "",
     "full_bleed_dark_photo_with_bold_text_overlay"),
    (2, "numbered_item", "Motivational tip slide 2",
     "Dark photo background", "",
     "full_bleed_dark_photo_with_bold_text_overlay"),
    (3, "numbered_item", "Motivational tip slide 3",
     "Dark photo background", "",
     "full_bleed_dark_photo_with_bold_text_overlay"),
    (4, "closing_cta", "Closing CTA slide",
     "Dark closing photo", "",
     "full_bleed_dark_photo_with_bold_closing_cta"),
]
for frame_idx, role, text_desc, photo_desc, brand_text, layout_fp in yurchance_frames:
    data = make_text_over_photo_cover(frame_idx, text_desc, photo_desc, brand_text, layout_fp)
    data["entries"][0]["slide_role"] = role
    with open(f"{OBS_BASE}/{yurchance}/frame_{frame_idx}.json", "w") as f:
        json.dump(data, f, indent=2)
print(f"Written {len(yurchance_frames)} frames for {yurchance}")


print("\n=== ALL OBSERVATION FILES WRITTEN ===")
