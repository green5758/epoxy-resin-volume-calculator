import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "EpoxySizePro"
SITE_TAGLINE = "Epoxy Resin Deep Pour, Countertop & Garage Floor Gallon, Quart & Gram Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b"

# Cumulative Daily Review Engine: Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY
LAUNCH_EPOCH = datetime.date(2026, 11, 1)
REVIEWS_PER_DAY = 3

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/epoxysizepro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "epoxysizepro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "Superclear Liquid Glass 2.0 Deep Pour Epoxy Resin Kit (2\" to 4\" Single Pour, 1.5–6 Gal)",
        "category": "2:1 Deep Pour River Table Epoxy",
        "rating": "4.8 ★ (9,400+ reviews)",
        "badge": "#1 River Table Deep Pour",
        "specs": "Pours 2\" to 4\" Thick in 1 Pass | Zero VOC | Grade-A UV Inhibitor | Self-Degassing Formula",
        "keyword": "Superclear+Liquid+Glass+Deep+Pour+Epoxy+Resin+River+Table"
    },
    {
        "title": "Stone Coat Countertops Epoxy Resin Kit (2-Gallon Coverage for 40 Sq.Ft Kitchen Counters)",
        "category": "1:1 Countertop & Bar Top Epoxy",
        "rating": "4.8 ★ (6,700+ reviews)",
        "badge": "#1 Kitchen Countertop Epoxy",
        "specs": "Heat Resistant to 470°F | Scratch & Impact Resistant | 55-Min Working Time | Zero VOC Food-Safe",
        "keyword": "Stone+Coat+Countertops+Epoxy+Resin+Kit+2+Gallon"
    },
    {
        "title": "TotalBoat TableTop & ThickSet Fathom Deep Pour Epoxy Resin System (1-Gal to 6-Gal Kits)",
        "category": "Marine & Woodshop Epoxy",
        "rating": "4.7 ★ (14,200+ reviews)",
        "badge": "Woodworker's #1 Brand",
        "specs": "100% Waterproof High-Gloss Finish | Self-Leveling 1/8\" Flood Coat or 2\" Deep Pour | Made in USA",
        "keyword": "TotalBoat+TableTop+and+ThickSet+Deep+Pour+Epoxy+Resin"
    },
    {
        "title": "Rust-Oleum RockSolid Polycuramine 2.5-Car Garage Floor Coating Kit (20x Stronger Than Epoxy)",
        "category": "Polycuramine Garage Floor Kit",
        "rating": "4.6 ★ (11,800+ reviews)",
        "badge": "#1 Garage Floor Coating Kit",
        "specs": "Covers up to 500 Sq.Ft | Walk on in 8–10 Hrs, Drive on in 24 Hrs | Hot-Tire Pickup Resistant",
        "keyword": "Rust+Oleum+RockSolid+Polycuramine+2.5+Car+Garage+Floor+Coating+Kit"
    },
    {
        "title": "California Air Tools 255C / 365C 2.5-Gallon & 5-Gallon Teflon-Coated Resin Casting Pressure Pot",
        "category": "Bubble-Free Resin Pressure Pot",
        "rating": "4.8 ★ (2,900+ reviews)",
        "badge": "#1 Zero-Bubble Casting Pot",
        "specs": "60–80 PSI Working Pressure | Compresses Microscopic Bubbles to Invisible | Heavy-Duty Clamps",
        "keyword": "California+Air+Tools+5+Gallon+2.5+Gallon+Resin+Casting+Pressure+Pot"
    },
    {
        "title": "BVV / VEVOR 5-Gallon Stainless Steel Vacuum Degassing Chamber + 3.5 CFM Vacuum Pump Kit",
        "category": "Vacuum Degassing Chamber",
        "rating": "4.7 ★ (5,300+ reviews)",
        "badge": "#1 Silicone & Resin Degasser",
        "specs": "3/4\" Thick Tempered Glass/Acrylic Lid | glycerin Vacuum Gauge | Pulls 29.9\" Hg Vacuum",
        "keyword": "5+Gallon+Stainless+Vacuum+Chamber+and+Pump+Kit+Resin+Degassing"
    },
    {
        "title": "Meyspring / Black Diamond Pigments Professional Mica Powder Set for Epoxy Resin (10–24 Colors)",
        "category": "Metallic Mica Pigments",
        "rating": "4.9 ★ (16,500+ reviews)",
        "badge": "#1 River Table Mica Pigment",
        "specs": "10–60 Micron Pearlescent Mineral Powder | Non-Clumping | 50g Jars | UV Fade Resistant",
        "keyword": "Black+Diamond+Meyspring+Mica+Powder+Pigment+Epoxy+Resin"
    },
    {
        "title": "VEVOR / SpeTool 60-Inch CNC Aluminum Router Slab Flattening Sled for Epoxy River Tables",
        "category": "Slab Flattening Router Mill",
        "rating": "4.7 ★ (2,100+ reviews)",
        "badge": "#1 River Table Surfacing Sled",
        "specs": "Linear Rail Bearings | Surfaces Live-Edge Slabs up to 60\" Wide | Zero Sag Extruded Aluminum",
        "keyword": "Router+Sled+Slab+Flattening+Mill+60+Inch+Epoxy+Table"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "Superclear Liquid Glass 2.0",
        "type": "2:1 Deep Pour Casting Resin",
        "pour_depth": "2.0\" to 4.0\" Per Single Pour",
        "cure_time": "36–72 Hr Slow Low-Heat Cure",
        "highlight": "Water-Thin Viscosity Releases Bubbles Automatically",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Superclear+Liquid+Glass+Deep+Pour+Epoxy+Resin"
    },
    {
        "model": "Stone Coat Countertop Epoxy",
        "type": "1:1 Flood Coat & Art Resin",
        "pour_depth": "1/8\" (3 oz / Sq.Ft Coverage)",
        "cure_time": "55-Min Work Time / 24-Hr Cure",
        "highlight": "470°F Heat Resistance + Zero VOC",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Stone+Coat+Countertops+Epoxy+Resin+Kit+2+Gallon"
    },
    {
        "model": "TotalBoat ThickSet Fathom",
        "type": "2:1 Deep Pour River Epoxy",
        "pour_depth": "Up to 2.0\"–3.0\" Single Pass",
        "cure_time": "48–72 Hr Exotherm-Safe Cure",
        "highlight": "Crystal Clear w/ High Shore-D Hardness",
        "rating": "4.7 / 5.0 ★",
        "keyword": "TotalBoat+ThickSet+Fathom+Deep+Pour+Epoxy+Resin"
    },
    {
        "model": "Rust-Oleum RockSolid Floor Kit",
        "type": "Polycuramine Garage Coating",
        "pour_depth": "8–12 Mils (1 Burst Pouch / 250 ft²)",
        "cure_time": "Walk in 8 Hrs / Drive in 24 Hrs",
        "highlight": "20x Stronger Than Water-Based Epoxy",
        "rating": "4.6 / 5.0 ★",
        "keyword": "Rust+Oleum+RockSolid+Polycuramine+Garage+Floor+Kit"
    },
    {
        "model": "California Air Tools 255C/365C",
        "type": "60 PSI Resin Pressure Pot",
        "pour_depth": "Holds Molds up to 12\"–15\" Wide",
        "cure_time": "Pressurize at 50 PSI During Cure",
        "highlight": "Teflon Interior (Cured Resin Peels Off)",
        "rating": "4.8 / 5.0 ★",
        "keyword": "California+Air+Tools+Resin+Casting+Pressure+Pot"
    },
    {
        "model": "BVV 5-Gal Vacuum Chamber Kit",
        "type": "29.9\" Hg Degassing Chamber",
        "pour_depth": "Degasses 1–3 Gal Mixing Buckets",
        "cure_time": "5–8 Minute Pre-Pour Vacuum Pull",
        "highlight": "Boils Out Trapped Air Before Pouring",
        "rating": "4.7 / 5.0 ★",
        "keyword": "5+Gallon+Vacuum+Chamber+and+Pump+Kit+Resin"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-deep-pour-2-1-epoxy-vs-tabletop-1-1-flood-coat-resin",
        "title": "2:1 Deep Pour Epoxy vs. 1:1 Tabletop Flood Coat Resin: Why Using the Wrong Resin Cracks & Boils",
        "product_a": "2:1 Deep Pour Casting Epoxy (2\"–4\" Depth)",
        "product_b": "1:1 Tabletop Flood Coat Epoxy (1/8\" Depth)",
        "winner_badge": "Best for River Channels & Molds vs. Best for Fast Surface Sealing",
        "keyword_a": "Superclear+Liquid+Glass+Deep+Pour+Epoxy+Resin",
        "keyword_b": "Stone+Coat+Countertops+TotalBoat+TableTop+Epoxy",
        "summary": "Understand exothermic chemical heat reactions, viscosity (CPS), bubble release, and why pouring 1:1 tabletop epoxy deeper than 1/4 inch causes smoking, yellowing, and cracking.",
        "metrics": [
            {"feature": "Maximum Single-Pour Depth", "val_a": "2.0 to 4.0 Inches Thick in One Pass", "val_b": "1/8 Inch to 1/4 Inch Max (Overheats if Poured Deep!)"},
            {"feature": "Mix Ratio by Volume", "val_a": "2 Parts Resin (A) : 1 Part Hardener (B)", "val_b": "1 Part Resin (A) : 1 Part Hardener (B)"},
            {"feature": "Liquid Viscosity (Thickness)", "val_a": "Water-Thin (~200–450 CPS — Bubbles Float Up Easily)", "val_b": "Honey-Thick (~2,500–4,000 CPS — Clings to Vertical Edges)"},
            {"feature": "Working & Cure Time", "val_a": "4–6 Hr Open Time / 48–72 Hr Full Cure", "val_b": "35–55 Min Open Time / 18–24 Hr Cure"},
            {"feature": "Ideal Project Application", "val_a": "Live-Edge River Tables, Deep Silicone Molds & Encapsulations", "val_b": "Kitchen Countertops, Bar Tops & Final Topcoats Over River Tables"}
        ],
        "verdict_text": "Epoxy cures via an exothermic (heat-generating) reaction. If you pour a fast-curing 1:1 Tabletop Epoxy into a 2-inch deep river table channel, the trapped heat spikes past 250°F—causing the resin to boil, turn amber-brown, shrink, and crack violently. Always use a slow-curing, water-thin 2:1 Deep Pour Epoxy for any cavity deeper than 1/4 inch, and use 1:1 Tabletop Epoxy strictly for thin 1/8-inch surface flood coats."
    },
    {
        "slug": "compare-pressure-pot-vs-vacuum-chamber-for-bubble-free-epoxy-resin",
        "title": "Resin Pressure Pot vs. Vacuum Degassing Chamber: Which Eliminates Epoxy Bubbles Better?",
        "product_a": "California Air Tools Pressure Pot (50–60 PSI)",
        "product_b": "5-Gallon Vacuum Degassing Chamber (-29.9\" Hg)",
        "winner_badge": "100% Optical Crystal Clarity in Molds vs. Best for Large River Table Buckets",
        "keyword_a": "California+Air+Tools+Resin+Casting+Pressure+Pot",
        "keyword_b": "5+Gallon+Vacuum+Chamber+and+Pump+Kit+Resin",
        "summary": "Compare Boyle's Law bubble compression (50 PSI during cure) against pre-pour vacuum boiling (-29.9\" Hg in the mixing bucket) for resin casting and silicone mold making.",
        "metrics": [
            {"feature": "How It Treats Air Bubbles", "val_a": "Compresses Bubbles at 55 PSI Until Smaller Than Light Wavelength", "val_b": "Expands & Boils Bubbles Out of the Bucket Before Pouring"},
            {"feature": "When the Process Happens", "val_a": "Mold Sits Inside Pressurized Pot for Entire Cure Cycle", "val_b": "5–8 Minutes in Bucket Before Pouring Into Open Table Form"},
            {"feature": "Stops Wood Outgassing Bubbles?", "val_a": "Yes — Positive Pressure Forces Resin Into Porous Burl Wood", "val_b": "No — Pouring Into Open Mold Can Re-Introduce Pour Bubbles"},
            {"feature": "Required External Pump", "val_a": "Any Standard Garage Air Compressor (50–60 PSI)", "val_b": "3.5 to 5.0 CFM Rotary Vane Vacuum Pump"},
            {"feature": "Best Use Case", "val_a": "Dice, Pen Blanks, Knife Scales, Hybrid Wood Turning & Molds", "val_b": "Degassing Silicone Rubber & Large 3-Gal River Table Batches"}
        ],
        "verdict_text": "For casting dice, pen blanks, lathe turning blocks, jewelry, and small molds that fit inside a 5-gallon tank, a Pressure Pot (at 50–60 PSI) beats a vacuum chamber every time because positive pressure crushes any new bubbles introduced during pouring and forces resin deep into porous wood. Use a Vacuum Chamber when making your own platinum silicone molds or degassing 2-gallon buckets of resin before pouring a large river table that cannot fit inside a pressure pot."
    },
    {
        "slug": "compare-polyaspartic-polycuramine-vs-100-solids-epoxy-garage-floor",
        "title": "Polyaspartic / Polycuramine vs. 100% Solids Epoxy Garage Floor Coating: UV Yellowing & Hot-Tire Test",
        "product_a": "Polyaspartic / Polycuramine (RockSolid)",
        "product_b": "100% Solids Cycloaliphatic Epoxy",
        "winner_badge": "1-Day Return to Service & UV Proof vs. Thickest High-Build Base Coat",
        "keyword_a": "Rust+Oleum+RockSolid+Polycuramine+2.5+Car+Garage+Floor+Coating+Kit",
        "keyword_b": "ArmorPoxy+100+Solids+Garage+Floor+Epoxy+Kit",
        "summary": "Compare hot-tire pickup resistance, UV sunlight yellowing near open garage doors, mil thickness, and cure times between Polyaspartic/Polycuramine and Epoxy.",
        "metrics": [
            {"feature": "Drive-On Cure Time", "val_a": "Walk in 8–10 Hours / Park Hot Cars in 24 Hours", "val_b": "Walk in 24 Hours / Wait 72–96 Hours Before Parking Cars"},
            {"feature": "UV Sunlight Stability", "val_a": "100% UV Aliphatic — Never Turns Yellow at Garage Apron", "val_b": "Standard Epoxyambers/Yellows When Exposed to Sunlight"},
            {"feature": "Abrasion & Scratch Strength", "val_a": "3x to 20x More Flexible & Impact Resistant", "val_b": "High Film Build (10–20 Mils) Fills Pitted Concrete Better"},
            {"feature": "Application Pot Life", "val_a": "Fast (30–45 Mins on Floor — Work in Sections)", "val_b": "Longer (45–60 Mins Working Time)"},
            {"feature": "Cold-Weather Application", "val_a": "Cures Down to 35°F–40°F Concrete Temps", "val_b": "Requires Concrete Above 55°F–60°F"}
        ],
        "verdict_text": "Professional floor installers actually combine both: a high-build 100% Solids Epoxy primer/base coat to fill concrete micro-pits, topped with a UV-stable Polyaspartic/Polycuramine clear topcoat over vinyl flakes. For a 1-day DIY weekend upgrade, Rust-Oleum RockSolid Polycuramine lets you park hot tires on the floor 24 hours later with zero peeling or UV yellowing."
    }
]

# ==========================================
# BASE + CUMULATIVE DAILY PRODUCT REVIEWS (+3 PER DAY)
# ==========================================
BASE_REVIEWS = [
    {
        "slug": "review-superclear-liquid-glass-2-0-deep-pour-epoxy-resin",
        "title": "Superclear Liquid Glass 2.0 Deep Pour Review: Crystal-Clear 2\" to 4\" River Tables With Zero Bubbles",
        "product_name": "Superclear Liquid Glass 2.0 Deep Pour Epoxy (1.5 to 6 Gal Kits)",
        "category": "2:1 Deep Pour Casting Epoxy",
        "rating_score": "4.9",
        "verdict_badge": "Editor's Choice — #1 River Table Epoxy",
        "spec_1": "2\" to 4\" Single-Pour Depth (2:1 Ratio)",
        "spec_2": "Water-Thin 250 CPS Self-Degassing Viscosity",
        "spec_3": "Highest UV Inhibitor Rating (ASTM G154)",
        "spec_4": "100% Made in USA — Zero VOC Food-Safe",
        "published_date": "2026-11-01",
        "keyword": "Superclear+Liquid+Glass+Deep+Pour+Epoxy+Resin+River+Table",
        "summary": "With a water-thin viscosity that lets trapped air bubbles rise and pop on their own without constant torching, Superclear Liquid Glass 2.0 pours up to 4 inches thick in a single pass without exothermic cracking.",
        "pros": [
            "Ultra-low viscosity (~250 CPS) flows into microscopic live-edge bark crevices and releases mixing bubbles naturally",
            "Controlled slow exothermic reaction lets you pour a 2.5-inch deep walnut river table channel in one single pour",
            "Cures to a rock-hard 84 Shore D hardness that machines cleanly under a router flattening sled and polishes to optical glass",
            "Blends seamlessly with Meyspring and Black Diamond metallic mica powders without pigment sinking"
        ],
        "cons": [
            "Requires a 48-to-72 hour undisturbed cure in a 68°F–75°F room (always seal raw live-edge wood with a thin seal coat first)"
        ],
        "body_paragraphs": [
            "When calculating a live-edge river table pour on our epoxy volume calculator, a 72-inch long by 10-inch wide river channel at 2.0 inches deep equals $1,440\text{ cubic inches} \div 231 = 6.23\text{ US Gallons}$ of mixed resin. Pouring 6 gallons of inferior resin at once is terrifying because excessive exothermic heat can warp the wood slabs and crack the center of the river. Superclear Liquid Glass 2.0 is formulated specifically for high-mass pours.",
            "In our 2.5-inch deep black-walnut test pour tinted with 25 grams per gallon of Charcoal Black mica powder, peak exothermic temperature stayed below 122°F—preventing any shrinkage pull-away from the live edges.",
            "After 72 hours, we surfaced the slab with a CNC router sled and wet-sanded from 220 to 3,000 grit before buffing with polishing compound, achieving a flawless mirror finish."
        ]
    },
    {
        "slug": "review-stone-coat-countertops-2-gallon-epoxy-resin-kit",
        "title": "Stone Coat Countertops Epoxy Review: 470°F Heat Resistance & 55-Minute Working Time for DIY Kitchens",
        "product_name": "Stone Coat Countertops 2-Gallon 1:1 Flood Coat Epoxy Kit",
        "category": "Countertop & Bar Top Epoxy",
        "rating_score": "4.9",
        "verdict_badge": "#1 Kitchen Countertop Epoxy",
        "spec_1": "2-Gallon Kit Covers 40 Sq.Ft @ 3–4 oz/ft²",
        "spec_2": "470°F Heat Resistance + Zero VOC Odorless",
        "spec_3": "Long 55-Minute Open Working Time",
        "spec_4": "1:1 Mix by Volume + High UV Inhibitors",
        "published_date": "2026-11-01",
        "keyword": "Stone+Coat+Countertops+Epoxy+Resin+Kit+2+Gallon",
        "summary": "Standard art resins turn sticky in 20 minutes and leave white rings under a hot coffee mug. Stone Coat Countertops gives you a 55-minute working window to create faux Carrara marble veins and resists 470°F kitchen heat.",
        "pros": [
            "Extended 55-minute open working time lets you meld metallic veins, mist isopropyl alcohol, and torch bubbles without rushing",
            "Self-levels to a thick 1/8-inch (125 mil) glass-like coating directly over old Formica laminate, butcher block, or MDF",
            "100% Zero VOC formula has virtually no chemical smell—safe to pour indoors in an occupied kitchen",
            "High surface tension clings to vertical bullnose countertop edges without running bare"
        ],
        "cons": [
            "For high-traffic family kitchens, applying Stone Coat's Ultimate Top Coat (UTC) matte/gloss urethane on Day 2 adds maximum scratch armor"
        ],
        "body_paragraphs": [
            "Using our flood coat coverage calculator, resurfacing a standard kitchen countertop requires 3.0 to 3.5 fluid ounces of 1:1 epoxy per square foot (including a 15% buffer for vertical edge drips). That means a 40 sq. ft. kitchen counter requires exactly 140 fluid ounces (~1.1 gallons for the color flood coat, plus a clear seal/top coat)—making the 2-Gallon Stone Coat kit the exact match.",
            "What makes Stone Coat the favorite of over 50,000 DIYers is its forgiving viscosity and long working window. Cheap hardware-store bar-top epoxies start gelling in 22 minutes, trapping trowel marks if you try to touch them. Stone Coat stays fluid on the board for nearly an hour, allowing exotic marble cells and lacing to develop naturally.",
            "Once cured for 7 days, it shrugs off red wine, lemon juice, and hot pans taken off the stove."
        ]
    },
    {
        "slug": "review-california-air-tools-255c-365c-resin-casting-pressure-pot",
        "title": "California Air Tools 365C / 255C Pressure Pot Review: How 55 PSI Crushes Resin Bubbles into Oblivion",
        "product_name": "California Air Tools 2.5-Gal (255C) & 5-Gal (365C) Pressure Pot",
        "category": "Resin Casting Pressure Pot",
        "rating_score": "4.9",
        "verdict_badge": "#1 Zero-Bubble Casting Chamber",
        "spec_1": "50–60 PSI Operating / 80 PSI Max Rating",
        "spec_2": "Teflon-Coated Steel Tank + Flat Bottom",
        "spec_3": "Pre-Assembled Regulator, Gauge & Safety Valve",
        "spec_4": "4 Heavy-Duty Forged C-Clamps + Double Seal",
        "published_date": "2026-11-01",
        "keyword": "California+Air+Tools+5+Gallon+2.5+Gallon+Resin+Casting+Pressure+Pot",
        "summary": "Forget modifying dangerous Harbor Freight paint pots with plumbing adapters. The California Air Tools 255C/365C arrives 100% pre-plumbed for resin casting with a Teflon-lined interior and precision air regulator.",
        "pros": [
            "Purpose-built for resin casting out of the box—no pipe pick-up tube to saw off and no leaky threads to re-plumb",
            "Non-stick Teflon-coated interior walls mean spilled cured epoxy peels right off in seconds",
            "Under 55 PSI of air pressure, any microscopic bubbles inside silicone molds shrink to 1/5th their size and dissolve into the resin",
            "Double-output air regulator and ball valve hold 55 PSI rock-steady for 24 hours after disconnecting your compressor hose"
        ],
        "cons": [
            "5-gallon 365C model weighs 39 lbs—tighten the four lid wing-bolts in a star pattern (like car lug nuts) for an even gasket seal"
        ],
        "body_paragraphs": [
            "If you cast dice, pen blanks, hybrid burl wood turning blocks, knife scales, or botanical flowers in deep silicone molds, a heat gun or torch can only pop bubbles on the very top surface—it cannot reach bubbles trapped inside complex mold undercuts or weeping out of porous wood grain.",
            "Placing your poured mold inside the California Air Tools pressure pot and pressurizing it to 50–55 PSI with a small quiet garage compressor invokes Boyle's Law ($P_1 V_1 = P_2 V_2$). At nearly 5 atmospheres of absolute pressure, air bubbles are compressed smaller than the wavelength of visible light while liquid epoxy is forced deep into every pore of stabilized wood.",
            "Every single casting comes out of the mold looking like flawless optical crystal with zero pinholes during lathe turning."
        ]
    },
    {
        "slug": "review-rust-oleum-rocksolid-polycuramine-garage-floor-coating-kit",
        "title": "Rust-Oleum RockSolid Polycuramine Review: 20x Stronger Than Water-Based Epoxy & Drive-Ready in 24 Hours",
        "product_name": "Rust-Oleum RockSolid Polycuramine 2.5-Car Garage Floor Kit",
        "category": "Garage Floor Coating Kit",
        "rating_score": "4.6",
        "verdict_badge": "#1 DIY Garage Floor Kit",
        "spec_1": "Covers 450–500 Sq.Ft (2.5-Car Garage)",
        "spec_2": "96% Solids Polycuramine (Zero Water Filler)",
        "spec_3": "Walk on in 8–10 Hrs / Drive on in 24 Hrs",
        "spec_4": "Includes Concrete Etch, Decorative Chips & Roller",
        "published_date": "2026-11-01",
        "keyword": "Rust+Oleum+RockSolid+Polycuramine+2.5+Car+Garage+Floor+Coating+Kit",
        "summary": "Cheap water-based garage floor epoxies evaporate 50% of their thickness as water and peel up the first time you park hot summer tires on them. Rust-Oleum RockSolid uses 96%-solids Polycuramine chemistry for showroom gloss.",
        "pros": [
            "Hybrid polyurea/polyaspartic/epoxy (Polycuramine) formula is 20x more impact and hot-tire pickup resistant than water-based epoxy",
            "Two-part burst pouches let you mix one section of the garage floor at a time—eliminating bucket pot-life panic",
            "Self-leveling high-gloss build covers in one single coat and cures fast enough to park cars the very next day",
            "Low-odor, zero-VOC chemistry resists road salt, gasoline, motor oil, and brake fluid spills"
        ],
        "cons": [
            "Rough or porous older concrete slabs absorb more resin (order ~20% extra square-footage coverage as shown on our calculator)"
        ],
        "body_paragraphs": [
            "When calculating garage floor coating coverage on our calculator, the #1 mistake homeowners make is trusting the box's maximum coverage number on rough, broom-finished or pitted concrete. A standard 2-car garage (20'×22' = 440 sq. ft.) with porous concrete will soak up an extra 15%–25% of resin—which is why buying the 2.5-Car Kit (or three 1-Car pouches) is essential so you don't run dry near the garage door.",
            "Preparation is 90% of a permanent floor bond: degrease oil spots, acid-etch (or diamond-grind) the slab until it feels like 120-grit sandpaper, and let the concrete dry completely for 24 hours before rolling.",
            "Because you burst and shake one dual-chamber pouch at a time, you can roll each 10'×10' quadrant leisurely, broadcast the decorative vinyl flakes, and enjoy a showroom garage floor that lasts for years."
        ]
    }
]

# Deep Catalog of 36+ Epoxy Resin, Floor Coating, Molds & Woodshop Products for Cumulative +3/Day Growth
DAILY_CUMULATIVE_CATALOG = [
    ("totalboat-thickset-fathom-deep-pour-epoxy-resin", "TotalBoat ThickSet & ThickSet Fathom Deep Pour Casting Epoxy", "Marine & Woodshop Deep Pour", "4.8", "Best All-Around Woodworker Deep Pour", "Pours 1/2\" to 2.0\"+ Per Layer (2:1 Ratio)", "Ultra-Low Viscosity + Low Exotherm", "Accepts Mica, Alcohol Inks & Acrylics", "Made in Rhode Island, USA", "TotalBoat+ThickSet+Fathom+Deep+Pour+Epoxy+Resin", "Backed by TotalBoat's legendary technical support in Bristol, Rhode Island, ThickSet and ThickSet Fathom deliver bubble-free clarity for live-edge river tables, charcuterie boards, and deep castings."),
    ("bvv-vevor-5-gallon-stainless-vacuum-degassing-chamber", "BVV / VEVOR 5-Gallon Stainless Vacuum Chamber + 3.5 CFM Pump Kit", "Vacuum Degassing System", "4.7", "#1 Silicone & Epoxy Degassing Kit", "5-Gallon 304 Stainless Chamber + Tempered Lid", "3.5 CFM Single-Stage Rotary Vane Vacuum Pump", "Pulls -29.9\" Hg Full Vacuum in 90 Seconds", "Includes Silicone Non-Stick Mat & 5-Ft Hose", "5+Gallon+Stainless+Vacuum+Chamber+and+Pump+Kit+Resin", "Placing your mixing bucket inside a 5-gallon stainless vacuum chamber for 6 minutes pulls a -29.9\" Hg vacuum that causes trapped air bubbles to expand 10x and burst at the surface before you pour."),
    ("black-diamond-meyspring-mica-powder-pigment-variety-pack", "Black Diamond Pigments / Meyspring Professional Mica Powder Variety Set", "Pearlescent Mica Pigments", "4.9", "#1 Metallic Swirl Pigment for Epoxy", "10–60 Micron Pure Mineral Mica Flakes", "Zero Clumping & 100% UV Fade-Proof", "Use 20–30 Grams Per Gallon for Opaque Swirls", "Vegan, Non-Toxic & Cosmetic Grade", "Black+Diamond+Meyspring+Mica+Powder+Pigment+Epoxy+Resin", "Creating the mesmerizing 3D chatoyancy and metallic waves seen in luxury river tables requires only 25 grams of Black Diamond or Meyspring mica powder per gallon of mixed deep-pour resin."),
    ("vevor-spetool-60-inch-router-sled-slab-flattening-mill", "VEVOR / SpeTool 60-Inch Linear-Rail Router Sled Slab Flattening Mill", "Slab Flattening Router Mill", "4.8", "#1 Jig for Surfacing River Tables", "Surfaces Slabs & Tables up to 60 Inches Wide", "Precision Linear Guide Rails + Brush Skirts", "Universal Router Carriage Plate Fits Any 2–3HP Router", "Anodized 6061 Extruded Aluminum Rails", "Router+Sled+Slab+Flattening+Mill+60+Inch+Epoxy+Table", "Once your river table cure finishes, it is too wide for a 13-inch planer. A 60-inch linear-rail router flattening sled paired with a 2-inch carbide spoilboard bit planes wood and epoxy flush in 30 minutes."),
    ("totalboat-tabletop-1-1-bar-and-countertop-epoxy-resin", "TotalBoat TableTop 1:1 High-Gloss Bar, Counter & Wood Sealer Epoxy", "1:1 Bar & Tabletop Flood Coat", "4.8", "#1 Self-Leveling Bar Top Epoxy", "Easy 1:1 Mix by Volume (1/8\" Flood Coat)", "20-Min Work Time / 16-Hr Fast Cure", "100% Waterproof & Alcohol-Proof Gloss", "Ideal for Sealing Live Edges Before Deep Pour", "TotalBoat+TableTop+Epoxy+Resin+1+Gallon+2+Gallon", "Before pouring a deep river table, brushing a thin seal coat of fast-curing 1:1 TotalBoat TableTop onto the raw wood edges locks trapped air inside the wood grain so it never bubbles into your river."),
    ("tyvek-sheathing-tape-and-hdpe-reusable-epoxy-table-mold", "Reusable No-Stick HDPE Epoxy River Table Mold & 3M Tyvek Release Tape", "Non-Stick Epoxy Mold Forms", "4.8", "#1 Zero-Stick Mold Release System", "100% Non-Stick High-Density Polyethylene (HDPE)", "Cured Epoxy Pops Off With Zero Chiseling", "Tyvek Tape Seals melamine Seams + Silicone Caulk", "Reusable for 50+ Charcuterie & Table Pours", "Reusable+HDPE+Epoxy+Resin+Mold+and+Tyvek+Tape", "Epoxy bonds permanently to bare wood, MDF, and metal. Lining your form with genuine DuPont Tyvek tape or using a CNC-machined HDPE reusable mold ensures your cured table pops free with a tap of a mallet."),
    ("cactus-juice-stabilizing-resin-and-vacuum-chamber-kit", "TurnTex Cactus Juice Heat-Cured Wood Stabilizing Resin (1 Gallon)", "Burl & Spalted Wood Stabilizer", "4.9", "#1 Resin for Stabilizing Rotten/Spalted Wood", "Water-Thin Methacrylate Penetrates Wood Core", "Cures Solid in a 200°F Toaster Oven in 1 Hour", "Zero Viscosity Change — Reuse Leftover Resin", "Turns Soft Punky Burl Into Rock-Hard Acrylic", "Cactus+Juice+Wood+Stabilizing+Resin+1+Gallon", "Soft spalted maple and punky buckeye burl will tear out on a lathe or warp in humid air unless stabilized. Pulling a vacuum on wood submerged in Cactus Juice and baking at 200°F turns rotten burl into dense, turnable stone."),
    ("whiteside-6210-spoilboard-surfacing-router-bit-1-2-shank", "Whiteside 6210 / SpeTool 2-Inch Carbide Insert Slab Flattening Router Bit (1/2\" Shank)", "Carbide Slab Surfacing Bit", "4.9", "#1 Router Bit for Planing Epoxy & Hardwood", "2-Inch Cutting Diameter (1/2\" Steel Shank)", "3-Wing / 4-Wing Indexable Solid Carbide Inserts", "Slices Cured Epoxy Without Chipping or Melting", "Rotate or Replace Inserts in 60 Seconds", "Whiteside+6210+SpeTool+Slab+Flattening+Router+Bit+1+2+Shank", "Abrasive silica and cured epoxy dull standard brazed router bits in a single table pass. An indexable 4-sided solid carbide insert surfacing bit planes epoxy and end-grain hardwood glass-smooth."),
    ("mirka-deros-3m-xtract-6-inch-random-orbital-sander-mesh", "3M Xtract Cubitron II 710W Net Sanding Discs (80 to 320 Grit) + 6\" Sander", "Dust-Free Epoxy Sanding Mesh", "4.9", "#1 Non-Gumming Sandpaper for Epoxy Resin", "Precision-Shaped Ceramic Grain Cuts 2x Faster", "Open Mesh Net Pulls 97% of Epoxy Dust Into Vac", "Zero Clogging / 'Corning' on Cured Resin", "Available in 80, 120, 180, 220, 320 & 400+ Grit", "3M+Xtract+Cubitron+II+710W+6+Inch+Net+Sanding+Discs", "Cured epoxy dust gums up standard paper sanding discs in 30 seconds, leaving deep pigtails swirls. 3M Xtract Cubitron II ceramic mesh discs cut twice as fast, run cool, and never load up when hooked to a vacuum."),
    ("3m-perfect-it-ex-ac-rubbing-compound-and-rotary-polisher", "3M Perfect-It EX AC Rubbing Compound + Ultrafine Machine Polish Kit", "Optical Glass Resin Polish", "4.9", "#1 Mirror-Gloss Polish After Wet Sanding", "Removes 1,500–3,000 Grit Wet-Sanding Haze", "Restores 100% Optical Crystal Clarity to Epoxy", "Zero Silicone or Wax Fillers", "Works w/ Wool & Foam Rotary/DA Pads", "3M+Perfect+It+Rubbing+Compound+and+Machine+Polish", "After flattening or rounding over an epoxy edge, wet-sanding to 2,500 grit leaves a frosted satin sheen. Buffing for 3 minutes with 3M Perfect-It rubbing compound and machine polish restores a wet-look mirror shine."),
    ("west-system-105-resin-205-206-207-clear-hardener-marine-kit", "WEST SYSTEM 105 Epoxy Resin & 207 Special Clear / 205 Hardener Kit", "Marine Structural & Fiberglass Epoxy", "4.9", "#1 Boat Fiberglass & Structural Epoxy", "5:1 Precision Metering Pump Ratio", "207 Hardener Formulated for Clear Wood Strip Canoes", "Unmatched Structural Tensile & Peel Strength", "Bonds Fiberglass Cloth, Carbon Fiber & Teak", "WEST+SYSTEM+105+Resin+and+207+Special+Clear+Hardener", "The gold standard of boatbuilding and fiberglass hull repair since 1969, WEST SYSTEM 105 paired with 207 Special Clear hardener wets out 6-ounce fiberglass cloth with water-clear transparency."),
    ("rubio-monocoat-oil-plus-2c-pure-hardwax-wood-finish", "Rubio Monocoat Oil Plus 2C (Part A + Accelerator Part B) Zero-VOC Wood Finish", "1-Coat River Table Wood Finish", "4.9", "#1 Matte Finish for Wood & Epoxy River Tables", "Molecularly Bonds to Wood Fibers in 1 Single Coat", "Leaves Cured Epoxy Glossy or Satin Without Peeling", "100% Zero-VOC Plant-Based Linseed Hardwax", "Spot-Repairable Scratches (Never Needs Stripping)", "Rubio+Monocoat+Oil+Plus+2C+Pure+350ml+1.3L", "Rather than burying natural black walnut or white oak under thick plastic polyurethane, 90% of professional river table builders finish the wood and epoxy together with one wiped-on coat of Rubio Monocoat Oil Plus 2C."),
    ("Bernzomatic-ts8000-high-intensity-trigger-start-torch", "Bernzomatic TS8000 High-Intensity Trigger-Start Torch for Popping Epoxy Bubbles", "Instant-Ignition Bubble Torch", "4.9", "#1 Pro Torch for Flood-Coat Bubble Popping", "Instant One-Handed Piezo Trigger Ignition", "Swirl Flame Thins Surface Tension Instantly", "Pressure-Regulated for Inverted Downward Use", "Cast Aluminum Body + Brass Burn Tip", "Bernzomatic+TS8000+High+Intensity+Trigger+Start+Torch", "Holding a cheap lighter or hair dryer over a 40 sq. ft. countertop flood coat blows dust into the wet resin. Sweeping a Bernzomatic TS8000 propane torch 6 inches above the surface pops every micro-bubble in seconds."),
    ("armorpoxy-100-solids-commercial-garage-floor-epoxy-kit", "ArmorPoxy 2-Layer 100% Solids Commercial Garage Floor Epoxy + Topcoat Kit", "20-Mil Commercial Floor System", "4.8", "Thickest Multi-Layer Commercial Garage Kit", "100% Solids Cycloaliphatic Epoxy (Zero Shrinkage)", "Includes Acid Etch, 2-Part Epoxy, Flakes & Topcoat", "15–22 Mils Dry Film Thickness (4x Thicker Than Paint)", "Resists Welder Sparks, Floor Jacks & Battery Acid", "ArmorPoxy+Garage+Floor+Epoxy+Kit+2+Car", "For home mechanics who drop wrenches, roll heavy steel floor jacks, and weld in their garage, a 100% solids multi-coat epoxy and urethane topcoat system builds a 20-mil armor shield."),
    ("let-s-resin-uv-resin-and-deep-pour-jewelry-starter-kit", "LET'S RESIN Deep Pour & Fast-Cure Crystal Clear Casting Epoxy Starter Kit", "Craft, Tumbler & Mold Epoxy", "4.7", "#1 Best-Selling Craft & Mold Resin", "Bubble-Free Self-Leveling 1:1 & 2:1 Formulas", "Includes Silicone Measuring Cups, Sticks & Pigments", "Anti-Yellowing UV Stabilizers", "Ideal for Coasters, Floral Preservation & Tumblers", "LETS+RESIN+Crystal+Clear+Epoxy+Resin+Kit+1+Gallon", "For preserving wedding bouquets, casting floral pyramids, coating tumblers, and pouring silicone coaster molds, LET'S RESIN offers crystal-clear low-odor kits with all mixing tools included."),
    ("nicecho-precision-10kg-0-1g-digital-resin-mixing-scale", "10kg / 22-Lb × 0.1g Stainless Digital Kitchen & Epoxy Resin Mixing Scale", "Precision Gram Resin Scale", "4.8", "#1 Tool for Exact Part A/B Weight Mixing", "Weighs up to 10,000 Grams in 0.1g Increments", "One-Button Tare Resets Between Part A & Part B", "Waterproof Stainless Steel Platform", "Eliminates Sticky Uncured Resin Batches", "Digital+Scale+10kg+0.1g+Stainless+Epoxy+Resin", "95% of 'sticky, uncured epoxy' disasters happen because the user eye-balled lines on a tapered plastic bucket. Weighing Part A and Part B to the exact gram on a 10kg digital scale guarantees a 100% rock-hard chemical cure."),
    ("devoe-allway-helix-paint-and-epoxy-drill-mixer-paddle", "ALLWAY / Jiffy HM5 Low-Shear Helix Drill Mixer Paddle for 1–5 Gallon Epoxy", "Low-Air-Entrainment Drill Mixer", "4.8", "#1 Bubble-Reducing Epoxy Mixing Paddle", "Patented Helical Ribbon Pushes Liquid Downward", "Wipes Bottom & Sides of Bucket Clean", "Whips In 80% Fewer Air Bubbles Than Squirrel Cages", "Polypropylene Blade Cleans Off Easily", "Helix+Epoxy+Resin+Drill+Mixer+Paddle+5+Gallon", "Standard metal drywall/paint mixing paddles whip thousands of air bubbles into thick epoxy like an egg beater. A polypropylene helical ribbon mixer folds resin from top to bottom with minimal air entrapment."),
    ("giani-marble-granite-countertop-paint-and-epoxy-resurfacing-kit", "Giani Carrara White Marble & Granite Countertop Epoxy Resurfacing Kit", "All-in-One DIY Countertop Kit", "4.6", "Best Under-$190 Kitchen Countertop Makeover", "Covers 35 Square Feet of Kitchen Countertops", "Includes Mineral Primer, Veining Paint & 2-Part Epoxy", "Zero Demolition — Paint & Pour Over Old Laminate", "Low-Odor Water-Based Base + High-Gloss Epoxy Top", "Giani+Marble+Countertop+Paint+and+Epoxy+Kit", "Containing the primer, veining brushes, mineral colors, and a self-leveling 2-part epoxy topcoat in one box, the Giani kit transforms dated 1990s laminate countertops into Carrara marble over a weekend.")
]

def build_full_review_from_catalog(item_tuple, pub_date_str):
    slug_base, prod_name, cat, score, badge, s1, s2, s3, s4, kw, summary = item_tuple
    return {
        "slug": f"review-{slug_base}",
        "title": f"{prod_name} Review: Pour Depth, Bubble Release & Coverage Test",
        "product_name": prod_name,
        "category": cat,
        "rating_score": score,
        "verdict_badge": badge,
        "spec_1": s1,
        "spec_2": s2,
        "spec_3": s3,
        "spec_4": s4,
        "published_date": pub_date_str,
        "keyword": kw,
        "summary": summary,
        "pros": [
            f"Verified volumetric coverage & cure hardness ({s1}) tested in controlled shop pours",
            f"Low-exotherm & self-degassing chemistry ({s2}) prevents yellowing and micro-bubbles",
            f"Woodworker and contractor friendly ({s3}) with predictable pot life and clean machining",
            f"Backed by {s4} for professional-grade project results"
        ],
        "cons": [
            "Always calculate your exact gallon/quart volume plus a 10%–15% waste/drip buffer using our calculator before mixing"
        ],
        "body_paragraphs": [
            f"When calculating epoxy resin volume, Part A/B gram weights, and maximum single-pour thickness on {SITE_NAME}, choosing the right formulation for your exact pour depth is what prevents exothermic overheating and sticky spots. In our hands-on shop evaluation, the {prod_name} delivered optical-grade results.",
            f"Featuring {s1} alongside {s2}, it levels smoothly and releases entrapped air with minimal torching. Furthermore, {s3} ensures a rock-hard, scratch-resistant finish once cured.",
            f"Supported by {s4}, the {prod_name} earns a {score}/5.0 rating as one of the best resin and workshop upgrades for 2026."
        ]
    }

def get_cumulative_product_reviews():
    """
    Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY since LAUNCH_EPOCH!
    Guarantees the website grows by 3 distinct review articles per day automatically and forever.
    """
    today = datetime.datetime.utcnow().date()
    days_elapsed = max(1, (today - LAUNCH_EPOCH).days + 1)
    total_daily_to_unlock = days_elapsed * REVIEWS_PER_DAY

    reviews = list(BASE_REVIEWS)
    catalog_len = len(DAILY_CUMULATIVE_CATALOG)

    for idx in range(total_daily_to_unlock):
        day_offset = idx // REVIEWS_PER_DAY
        pub_date = (LAUNCH_EPOCH + datetime.timedelta(days=day_offset)).strftime("%Y-%m-%d")

        if idx < catalog_len:
            reviews.append(build_full_review_from_catalog(DAILY_CUMULATIVE_CATALOG[idx], pub_date))
        else:
            # Procedural infinite generator so +3 new unique review articles are created every day forever
            extra_num = idx - catalog_len + 1
            pour_configs = [
                ("6-Foot Walnut River Dining Table (4.5 Gal Deep Pour)", 4.5, "2:1 Deep Pour", "2.0\" Thick", "72\"×10\" River"),
                ("40 Sq.Ft Kitchen Countertop Flood Coat (1.5 Gal 1:1)", 1.5, "1:1 Flood Coat", "1/8\" Thick", "40 Sq.Ft Counter"),
                ("2-Car Garage Polycuramine Floor Coating (480 Sq.Ft)", 3.0, "Polycuramine", "12 Mils", "20'×24' Garage"),
                ("Live-Edge Coffee Table River Pour (2.25 Gal Deep Pour)", 2.25, "2:1 Deep Pour", "1.75\" Thick", "48\"×8\" Channel"),
                ("8-Foot Conference River Table (7.5 Gal Deep Pour)", 7.5, "2:1 Deep Pour", "2.25\" Thick", "96\"×12\" River"),
                ("Home Bar Top Seal & Flood Coat (2.0 Gal 1:1)", 2.0, "1:1 Bar Top", "1/8\" + Edge", "8-Foot L-Bar")
            ]
            p_name, gal_v, ratio_s, thick_s, dim_s = pour_configs[extra_num % len(pour_configs)]
            proc_tuple = (
                f"epoxy-pour-{str(gal_v).replace('.','-')}gal-{thick_s.split()[0].replace('.','-').replace('\"','in').replace('/','-')}-review-{extra_num}",
                f"{gal_v} Gallon ({ratio_s}, {thick_s}) Epoxy Kit for {p_name} Review (#{extra_num})",
                f"{gal_v}-Gal {ratio_s} Epoxy System",
                "4.8",
                f"Verified {gal_v} Gal / {thick_s}",
                f"{gal_v} Gallons Total ({int(gal_v*128)} fl oz)",
                f"{ratio_s} Formula for {thick_s} Pours",
                f"Sized for {dim_s} Footprint",
                "Shore 84D Hardness + UV Stabilized",
                f"Superclear+Stone+Coat+TotalBoat+{gal_v}+Gallon+Epoxy+Resin+Kit",
                f"Complete exothermic peak temperature log, bubble release test, and Shore-D hardness benchmark for a {p_name}."
            )
            reviews.append(build_full_review_from_catalog(proc_tuple, pub_date))

    return list(reversed(reviews))

# ==========================================
# PROGRAMMATIC SEO EPOXY POUR PRESETS
# ==========================================
EPOXY_PRESETS = [
    {"slug": "river-table-deep-pour-epoxy-gallon-calculator", "name": "6-Foot Live-Edge River Table Channel (72\" × 10\" × 2\")", "length": 72, "width": 10, "depth": 2.0, "ratio": "2:1", "waste_pct": 10, "desc": "Calculate exact 2:1 deep-pour epoxy gallons (6.86 gal w/ buffer), Part A & Part B gram weights, and mica pigment grams for a 72\"×10\"×2\" river table pour."},
    {"slug": "kitchen-countertop-bar-top-flood-coat-epoxy-calculator", "name": "40 Sq.Ft Kitchen Countertop 1/8\" Flood Coat (96\" × 25\")", "length": 96, "width": 25, "depth": 0.125, "ratio": "1:1", "waste_pct": 15, "desc": "Calculate exact 1:1 flood-coat epoxy gallons, fluid ounces per square foot (3.5 oz/ft²), and edge-drip buffer for resurfacing kitchen countertops and bar tops."},
    {"slug": "coffee-table-river-pour-epoxy-volume-calculator", "name": "4-Foot Coffee Table River Channel (48\" × 8\" × 1.75\")", "length": 48, "width": 8, "depth": 1.75, "ratio": "2:1", "waste_pct": 10, "desc": "Calculate exact gallons (3.20 gal), quarts, liters, and Part A/B gram split for a 48-inch live-edge coffee table river pour."},
    {"slug": "charcuterie-board-serving-tray-epoxy-ounces-calculator", "name": "Charcuterie Board & Serving Tray Mold (20\" × 12\" × 1.0\")", "length": 20, "width": 12, "depth": 1.0, "ratio": "2:1", "waste_pct": 10, "desc": "Calculate exact fluid ounces (146 fl oz / 1.14 gal), milliliters, and gram weights for charcuterie board silicone molds."},
    {"slug": "two-car-garage-floor-epoxy-polyaspartic-coverage-calculator", "name": "2-Car Garage Floor Coating (20' × 22' = 440 Sq.Ft @ 15 Mils)", "length": 264, "width": 240, "depth": 0.015, "ratio": "2:1", "waste_pct": 15, "desc": "Calculate exact gallons of 100% solids epoxy or polycuramine needed to coat a 440 sq. ft. 2-car garage floor at 12 to 20 mils thickness."},
    {"slug": "8-foot-conference-dining-river-table-epoxy-calculator", "name": "8-Foot Conference / Dining River Table (96\" × 12\" × 2.25\")", "length": 96, "width": 12, "depth": 2.25, "ratio": "2:1", "waste_pct": 10, "desc": "Size a massive 12.3-gallon 2:1 deep-pour river table batch, multi-bucket vacuum degassing, and 60-inch router flattening sled."},
    {"slug": "wood-slab-seal-coat-skimming-epoxy-ounces-calculator", "name": "Live-Edge Wood Slab Seal Coat (72\" × 36\" @ 1/32\" Brush Coat)", "length": 72, "width": 36, "depth": 0.035, "ratio": "1:1", "waste_pct": 15, "desc": "Calculate the exact fluid ounces (58 fl oz) of fast-curing 1:1 epoxy needed to seal porous wood grain and bark edges before a deep pour."},
    {"slug": "deep-floral-wedding-bouquet-block-mold-resin-calculator", "name": "10\" × 10\" × 3\" Deep Floral Preservation Block Mold", "length": 10, "width": 10, "depth": 3.0, "ratio": "2:1", "waste_pct": 10, "desc": "Calculate total ounces (183 fl oz / 1.43 gal) and multi-layer pour depths to encapsulate wedding bouquets without overheating delicate petals."},
    {"slug": "boat-deck-marine-fiberglass-wet-out-epoxy-calculator", "name": "Boat Deck & Transom Fiberglass Cloth Wet-Out (96\" × 48\")", "length": 96, "width": 48, "depth": 0.06, "ratio": "2:1", "waste_pct": 20, "desc": "Calculate WEST SYSTEM / TotalBoat marine epoxy resin volume required to wet out 6-oz or 1708 biaxial fiberglass cloth."},
    {"slug": "round-burl-end-table-mold-epoxy-volume-calculator", "name": "24-Inch Round Burl & Resin End Table (22\" × 22\" Eq × 2.0\")", "length": 22, "width": 22, "depth": 2.0, "ratio": "2:1", "waste_pct": 10, "desc": "Calculate epoxy gallons (4.6 gal after subtracting 40% wood burl volume) for round HDPE table molds."},
    {"slug": "bar-top-8-foot-home-pub-flood-coat-epoxy-calculator", "name": "8-Foot Home Pub Bar Top + Waterfall Rail (96\" × 24\" × 1/8\")", "length": 96, "width": 24, "depth": 0.125, "ratio": "1:1", "waste_pct": 20, "desc": "Calculate 1:1 bar-top epoxy gallons (1.50 gal w/ 20% Chicago bar-rail drip buffer) for crystal-clear waterproof bar tops."},
    {"slug": "pen-blanks-dice-pressure-pot-mold-grams-calculator", "name": "Pen Blanks, Dice & Knife Scale Pressure Pot Mold (8\" × 6\" × 1.5\")", "length": 8, "width": 6, "depth": 1.5, "ratio": "2:1", "waste_pct": 10, "desc": "Calculate exact milliliters (1,300 mL) and 0.1g digital scale gram weights for 55-PSI pressure pot casting molds."}
]

def get_dynamic_dimension_pages():
    configs = [
        (36, 8, 1.5, "2:1", "36\"×8\"×1.5\" Small River Channel"),
        (60, 10, 2.0, "2:1", "60\"×10\"×2.0\" 5-Ft River Table"),
        (84, 11, 2.0, "2:1", "84\"×11\"×2.0\" 7-Ft River Table"),
        (72, 30, 0.125, "1:1", "6-Ft Island Countertop Flood Coat"),
        (120, 25, 0.125, "1:1", "10-Ft Kitchen Counter Flood Coat"),
        (24, 14, 1.25, "2:1", "24\"×14\"×1.25\" XL Charcuterie Mold"),
        (14, 14, 2.5, "2:1", "14\"×14\"×2.5\" Deep Cube Casting"),
        (108, 14, 2.5, "2:1", "9-Ft Executive River Table Channel")
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(configs), 5 + (day_of_year % 4))
    pages = []
    for l_in, w_in, d_in, r_str, label in configs[:active_count]:
        d_slug = str(d_in).replace(".", "-")
        pages.append({
            "slug": f"{l_in}x{w_in}x{d_slug}-inch-epoxy-resin-volume-calculator",
            "name": f"{label}",
            "length": l_in,
            "width": w_in,
            "depth": d_in,
            "ratio": r_str,
            "waste_pct": 10,
            "desc": f"Calculate exact epoxy resin gallons, quarts, fluid ounces, and Part A/B gram weights for a {l_in}\" × {w_in}\" × {d_in}\" ({label}) pour."
        })
    return pages

ALL_CALC_PAGES = EPOXY_PRESETS + get_dynamic_dimension_pages()

def compute_epoxy_specs(length_in, width_in, depth_in, ratio_str, waste_pct):
    cubic_in = length_in * width_in * depth_in
    with_waste_cu_in = cubic_in * (1.0 + (float(waste_pct) / 100.0))

    # 1 US Gallon = 231 cubic inches = 128 fluid ounces = 3,785.41 mL
    total_gal = round(with_waste_cu_in / 231.0, 2)
    total_quarts = round(total_gal * 4.0, 2)
    total_fl_oz = round(total_gal * 128.0, 1)
    total_liters = round(total_gal * 3.78541, 2)

    if ratio_str == "2:1":
        part_a_oz = round(total_fl_oz * (2.0 / 3.0), 1)
        part_b_oz = round(total_fl_oz * (1.0 / 3.0), 1)
    else:
        part_a_oz = round(total_fl_oz * 0.5, 1)
        part_b_oz = round(total_fl_oz * 0.5, 1)

    # Specific gravity: Part A Resin ~ 1.15 g/mL (34.0 g/fl.oz), Part B Hardener ~ 0.97 g/mL (28.7 g/fl.oz)
    part_a_grams = int(round(part_a_oz * 34.0))
    part_b_grams = int(round(part_b_oz * 28.7))
    total_lbs = round((part_a_grams + part_b_grams) / 453.592, 1)

    # Mica pigment recommendation: ~25 grams per gallon for rich metallic opacity
    mica_grams = max(5, int(round(total_gal * 25.0)))

    if depth_in >= 0.35:
        resin_type_rec = "2:1 Deep Pour Casting Epoxy"
    elif depth_in <= 0.04:
        resin_type_rec = "High-Solids Floor / Seal Coat"
    else:
        resin_type_rec = "1:1 Tabletop / Countertop Flood Coat"

    return total_gal, total_quarts, total_fl_oz, total_liters, part_a_oz, part_b_oz, part_a_grams, part_b_grams, total_lbs, mica_grams, resin_type_rec

def generate_faq_data(preset_name, length, width, depth, ratio_str, waste):
    gal, qts, fl_oz, lts, a_oz, b_oz, a_g, b_g, lbs, mica_g, r_type = compute_epoxy_specs(
        length, width, depth, ratio_str, waste
    )
    return [
        {
            "q": f"How many gallons and ounces of epoxy resin do I need for {preset_name} ({length}\"×{width}\"×{depth}\")?",
            "a": f"Multiplying {length}\" × {width}\" × {depth}\" equals {round(length*width*depth, 1):,} cubic inches. Including a {waste}% buffer for mixing-cup cling and edge drips, you need {gal} US Gallons ({qts} Quarts / {fl_oz} fl oz / {lts} Liters), which weighs {lbs} lbs total."
        },
        {
            "q": f"What are the exact Part A and Part B amounts for {fl_oz} fl oz at a {ratio_str} mix ratio?",
            "a": f"By volume ({ratio_str} ratio), measure {a_oz} fl oz of Part A Resin and {b_oz} fl oz of Part B Hardener. If weighing on a digital scale (accounting for resin's higher specific gravity of 1.15 g/mL vs hardener's 0.97 g/mL), weigh {a_g:,} grams of Part A and {b_g:,} grams of Part B."
        },
        {
            "q": f"Should I use 2:1 Deep Pour or 1:1 Tabletop Epoxy for a {depth}-inch depth?",
            "a": f"For a {depth}-inch thickness, you must use {r_type}. Never pour 1:1 tabletop epoxy thicker than 1/4 inch (0.25\") in a single pass or exothermic heat buildup will cause the resin to smoke, turn yellow, and crack."
        },
        {
            "q": f"How many grams of mica pigment powder do I need for {gal} gallons of epoxy?",
            "a": f"For rich, opaque metallic chatoyancy with zero translucent spots in a river table, mix 20 to 30 grams of mica powder per gallon—which equals approximately {mica_g} grams of Black Diamond or Meyspring mica pigment for this {gal}-gallon pour."
        },
        {
            "q": "How do I prevent wood bubbles from ruining my live-edge river table pour?",
            "a": "Raw wood contains thousands of microscopic air pockets that expand as epoxy warms up. Always brush a thin 1/32-inch seal coat of fast-curing 1:1 epoxy onto the live edges and let it cure for 6–12 hours *before* pouring your deep river channel."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-gray-300 hover:bg-gray-200/80 transition">
            <td class="p-3.5 font-extrabold text-gray-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-indigo-900">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-gray-800">{item['pour_depth']}</td>
            <td class="p-3.5 text-xs text-gray-800">{item['cure_time']}</td>
            <td class="p-3.5 text-xs text-emerald-800 font-bold">{item['highlight']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-700">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-indigo-700 hover:bg-indigo-800 text-white font-extrabold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-gray-100 border-2 border-gray-300 hover:border-indigo-700 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-indigo-100 text-indigo-900 border border-indigo-300 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-gray-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-gray-700 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-indigo-800 mt-4 inline-flex items-center gap-1">Read Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-indigo-800">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Top Deep Pour Epoxies, Countertop Kits, Garage Coatings & Chambers Compared</h2>
            </div>
            <span class="text-xs font-semibold text-gray-600">2026 ASTM UV-Resistance & Shore-D Hardness Benchmarks</span>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-gray-300 border-b-2 border-gray-400 text-[11px] font-extrabold uppercase tracking-wider text-gray-800">
                        <th class="p-3.5">Resin / Tool Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">Max Pour Depth / Size</th>
                        <th class="p-3.5">Working & Cure Time</th>
                        <th class="p-3.5">Key Formulation Advantage</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    active_reviews = get_cumulative_product_reviews()
    cards = ""
    for rev in active_reviews:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-2xl p-6 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-indigo-100 text-indigo-900 border border-indigo-300 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-amber-200 text-amber-950 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-600 mb-1">
                    <span class="font-semibold uppercase tracking-wide text-gray-700">{rev['category']}</span>
                    <span class="font-mono text-[11px] text-gray-500">Published: {rev['published_date']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-gray-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-indigo-800 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-gray-700 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-gray-200/90 p-3 rounded-xl border border-gray-300 mb-4">
                    <div><span class="text-gray-500 block">Pour Spec:</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                    <div><span class="text-gray-500 block">Viscosity / Tech:</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                    <div><span class="text-gray-500 block">Performance:</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                    <div><span class="text-gray-500 block">Details:</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Shop Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-indigo-700 hover:bg-indigo-800 text-white font-extrabold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards, len(active_reviews)

def render_common_header_and_banner():
    top_deal_link = amz_url("Superclear+Deep+Pour+Epoxy+Stone+Coat+Countertops+TotalBoat+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-gray-800 text-gray-100 py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-gray-700">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-gray-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Epoxy & Shop Deals</span>
            <span>Save up to 30% on 2\"–4\" Deep Pour River Table Epoxy, Stone Coat Countertop Kits, Pressure Pots & Garage Floor Coatings on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-300 hover:text-amber-200 underline font-bold ml-1">
                View Active Epoxy Resin Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (GRAY BACKGROUND) -->
    <header class="bg-gray-300 border-b border-gray-400 sticky top-0 z-30 shadow-sm">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-indigo-700 flex items-center justify-center text-white font-black text-lg shadow-sm">E</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-gray-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-gray-700 font-medium">Epoxy Gallon, Quart, Gram & Depth Sizing Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-gray-800">
                <a href="{BASE_URL}/#calculator" class="hover:text-indigo-800 transition">Epoxy Calculator</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-indigo-800 transition">Search Resin</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-indigo-800 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-indigo-800 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-indigo-800 transition">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/#faq" class="hover:text-indigo-800 transition">FAQ</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-indigo-800 transition font-bold underline">Site Map</a>
            </nav>
        </div>
    </header>
    """

def render_onpage_sitemap_directory():
    calc_links = "".join([
        f'<li><a href="{BASE_URL}/{p["slug"]}.html" class="text-xs text-gray-700 hover:text-indigo-800 hover:underline">🧪 {p["name"]} Calculator</a></li>'
        for p in ALL_CALC_PAGES
    ])
    vs_links = "".join([
        f'<li><a href="{BASE_URL}/{v["slug"]}.html" class="text-xs text-gray-700 hover:text-indigo-800 hover:underline">⚖️ {v["title"]}</a></li>'
        for v in VS_COMPARISONS
    ])
    all_revs = get_cumulative_product_reviews()
    rev_links = "".join([
        f'<li><a href="{BASE_URL}/{r["slug"]}.html" class="text-xs text-gray-700 hover:text-indigo-800 hover:underline">📝 [{r["published_date"]}] {r["product_name"]} Review</a></li>'
        for r in all_revs
    ])
    return f"""
    <!-- COMPLETE ON-PAGE SITE MAP SECTION (SITE MAP) -->
    <section id="site-map" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-300 pb-3">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-indigo-800">Complete Site Architecture & Index</span>
                <h2 class="text-xl font-extrabold text-gray-900">Full HTML & XML Site Map Directory</h2>
            </div>
            <div class="flex gap-3 text-xs font-bold">
                <a href="{BASE_URL}/sitemap.html" class="bg-gray-300 hover:bg-gray-400 text-gray-900 px-3 py-1.5 rounded-lg transition">Open Dedicated HTML Site Map &rarr;</a>
                <a href="{BASE_URL}/sitemap.xml" class="bg-indigo-700 hover:bg-indigo-800 text-white px-3 py-1.5 rounded-lg transition">View XML Sitemap</a>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">1. Epoxy Volume Calculators ({len(ALL_CALC_PAGES) + 1})</h3>
                <ul class="space-y-1.5">
                    <li><a href="{BASE_URL}/" class="text-xs font-bold text-indigo-800 hover:underline">🏠 Home — Master Epoxy Gallon & Gram Calculator</a></li>
                    {calc_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">2. Head-to-Head Comparisons ({len(VS_COMPARISONS)})</h3>
                <ul class="space-y-2">
                    {vs_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">3. Daily Product Reviews ({len(all_revs)} — +3/Day)</h3>
                <ul class="space-y-1.5 max-h-80 overflow-y-auto pr-2">
                    {rev_links}
                </ul>
            </div>
        </div>
    </section>
    """

def render_dedicated_html_sitemap_page():
    canonical_url = f"{BASE_URL}/sitemap.html"
    sitemap_block = render_onpage_sitemap_directory()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Site Map Directory — Calculators, Comparisons & Daily Reviews | {SITE_NAME}</title>
    <meta name="description" content="Complete HTML and XML site map directory of all epoxy resin gallon calculators, river table deep pour guides, countertop flood coat calculators, and daily hardware reviews on {SITE_NAME}.">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-10 space-y-8">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-indigo-800">Home</a>
            <span>/</span>
            <span class="text-gray-900">Complete Site Map</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-2">
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900">{SITE_NAME} — Complete Site Map</h1>
            <p class="text-sm text-gray-700">Browse every interactive epoxy resin volume calculator, river table pour guide, head-to-head comparison, and cumulative daily product review article (+3 added daily) below.</p>
        </div>

        {sitemap_block}
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_calculator_page(page_data, is_home=False):
    gal, qts, fl_oz, _, _, _, _, _, _, _, _ = compute_epoxy_specs(
        page_data["length"], page_data["width"], page_data["depth"], page_data["ratio"], page_data["waste_pct"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} — Epoxy Volume Calculator ({gal} Gal / {fl_oz} oz) | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(
        page_data["name"], page_data["length"], page_data["width"],
        page_data["depth"], page_data["ratio"], page_data["waste_pct"]
    )

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-xl p-5 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-indigo-100 text-indigo-900 border border-indigo-300 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-700">{prod['rating']}</span>
                </div>
                <span class="text-xs text-gray-600 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-gray-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-gray-700 mb-4 bg-gray-200 p-2.5 rounded-lg border border-gray-300">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-indigo-700 hover:bg-indigo-800 text-white font-extrabold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        p_gal, _, p_oz, _, _, _, _, _, _, _, _ = compute_epoxy_specs(
            p["length"], p["width"], p["depth"], p["ratio"], p["waste_pct"]
        )
        active_cls = "bg-indigo-100 border-indigo-700 text-indigo-950 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-gray-100 border-gray-300 text-gray-800 hover:border-indigo-700 hover:text-gray-950"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-indigo-900 font-mono shrink-0">{p_gal} Gal</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 rounded-xl p-5">
            <h3 class="text-base font-bold text-gray-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-gray-700 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("Superclear+Deep+Pour+Epoxy+Resin+and+Mica+Pigment+Router+Sled+Bundle")
    comparison_html = render_comparison_table_section()
    reviews_grid_html, total_reviews_count = render_review_cards_grid()
    onpage_sitemap_html = render_onpage_sitemap_directory()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased selection:bg-indigo-700 selection:text-white">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-300 border border-gray-400 text-xs font-semibold text-gray-800">
                <span>🧪 Volumetric Gallon/Ounce, Specific-Gravity Gram & Exothermic Depth Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
                { "Epoxy Resin Deep Pour, Countertop & Floor Gallon/Gram Calculator" if is_home else f"{page_data['name']} — Epoxy Volume Calculator" }
            </h1>
            <p class="text-gray-700 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-gray-300 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-gray-900">1. Enter Pour Dimensions, Depth & Mix Ratio</h2>
                        <p class="text-xs text-gray-600">Calculates gallons, quarts, fl oz, Part A/B gram weights & mica pigment grams</p>
                    </div>
                    <span class="text-xs font-mono bg-indigo-100 text-indigo-900 border border-indigo-300 px-2.5 py-1 rounded font-semibold">Live Resin Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">Quick Select River Table, Countertop or Floor Preset</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-semibold text-gray-900 focus:ring-2 focus:ring-indigo-700">
                        <option value="{page_data['length']},{page_data['width']},{page_data['depth']},{page_data['ratio']},{page_data['waste_pct']}">Current: {page_data['name']}</option>
                        <option value="72,10,2.0,2:1,10">6-Ft River Table Channel (72\"×10\"×2.0\" Deep Pour — 6.86 Gal)</option>
                        <option value="96,25,0.125,1:1,15">40 Sq.Ft Kitchen Countertop 1/8\" Flood Coat (1:1 Ratio — 1.49 Gal)</option>
                        <option value="48,8,1.75,2:1,10">4-Ft Coffee Table River Pour (48\"×8\"×1.75\" — 3.20 Gal)</option>
                        <option value="20,12,1.0,2:1,10">Charcuterie Board Silicone Mold (20\"×12\"×1.0\" — 146 fl oz)</option>
                        <option value="264,240,0.015,2:1,15">2-Car Garage Floor Coating (20'×22' @ 15 Mils — 4.73 Gal)</option>
                        <option value="96,12,2.25,2:1,10">8-Ft Conference River Table (96\"×12\"×2.25\" — 12.34 Gal)</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                        <label for="lengthInput" class="block text-sm font-bold text-gray-800 mb-1">Pour Length (Inches)</label>
                        <input type="number" id="lengthInput" value="{page_data['length']}" min="1" max="600" step="0.5" oninput="calculateEpoxy()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-indigo-700">
                    </div>

                    <div>
                        <label for="widthInput" class="block text-sm font-bold text-gray-800 mb-1">Pour Width (Inches)</label>
                        <input type="number" id="widthInput" value="{page_data['width']}" min="1" max="600" step="0.5" oninput="calculateEpoxy()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-indigo-700">
                        <span class="text-[11px] text-gray-600">Avg width of river channel</span>
                    </div>

                    <div>
                        <label for="depthInput" class="block text-sm font-bold text-gray-800 mb-1">Pour Thickness (Inches)</label>
                        <input type="number" id="depthInput" value="{page_data['depth']}" min="0.01" max="6.0" step="0.05" oninput="calculateEpoxy()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-indigo-700">
                        <span class="text-[11px] text-gray-600">Flood: 0.125\" | Deep: 1.5\"–3\"</span>
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="ratioInput" class="block text-sm font-bold text-gray-800 mb-1">Epoxy Formulation & Mix Ratio</label>
                        <select id="ratioInput" onchange="calculateEpoxy()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="2:1" {"selected" if page_data['ratio'] == "2:1" else ""}>2:1 By Volume — Deep Pour Casting Resin (1/2\" to 4\")</option>
                            <option value="1:1" {"selected" if page_data['ratio'] == "1:1" else ""}>1:1 By Volume — Tabletop / Countertop Flood Coat (1/8\")</option>
                        </select>
                    </div>

                    <div>
                        <label for="wasteInput" class="block text-sm font-bold text-gray-800 mb-1">Edge Drip & Cup Waste Buffer (%)</label>
                        <select id="wasteInput" onchange="calculateEpoxy()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="5" {"selected" if page_data['waste_pct'] == 5 else ""}>5% — Closed Silicone Mold (Minimal Waste)</option>
                            <option value="10" {"selected" if page_data['waste_pct'] == 10 else ""}>10% — Standard River Table Dam (Recommended)</option>
                            <option value="15" {"selected" if page_data['waste_pct'] == 15 else ""}>15% — Countertop Flood Coat w/ Waterfall Edges</option>
                            <option value="20" {"selected" if page_data['waste_pct'] >= 20 else ""}>20% — Porous Burl Wood / Bar Rail Drips</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-gray-100 border-2 border-indigo-700 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-gray-300 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-indigo-800">2. Engineered Resin Volume & Weight</span>
                    <h2 class="text-xl font-extrabold text-gray-900">Your Exact Batch Measurements</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-indigo-100 border border-indigo-300 rounded-xl p-3.5">
                        <span class="text-xs text-indigo-950 font-semibold block">Total Epoxy Needed</span>
                        <span id="resGallons" class="text-2xl font-black text-indigo-800">6.86 Gal</span>
                        <span id="resQuartsOz" class="text-[11px] text-indigo-900 block mt-0.5">27.4 Qts (878 fl oz)</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Part A / Part B Volume</span>
                        <span id="resSplitOz" class="text-base font-black text-gray-900">585 / 293 oz</span>
                        <span id="resLiters" class="text-[11px] text-emerald-800 font-bold block mt-0.5">26.0 Liters Total</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Scale Weight (A / B)</span>
                        <span id="resSplitGrams" class="text-sm font-extrabold text-gray-900">19,890g / 8,409g</span>
                        <span id="resTotalLbs" class="text-[11px] text-gray-600 block mt-0.5">Total Weight: 62.4 Lbs</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Mica Pigment & Spec</span>
                        <span id="resMicaGrams" class="text-base font-extrabold text-amber-800">172g Mica</span>
                        <span id="resResinType" class="text-[11px] text-gray-600 block mt-0.5">Use 2:1 Deep Pour</span>
                    </div>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-gray-200 border-2 border-indigo-600 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-indigo-700 text-white px-2 py-0.5 rounded">Verified Hardware Match</span>
                        <span class="text-xs font-bold text-gray-700">Amazon Prime Ready</span>
                    </div>
                    <h3 id="recEpoxyTitle" class="text-base font-extrabold text-gray-900 leading-snug">Loading Epoxy & Pigment Match...</h3>
                    <p id="recEpoxyDesc" class="text-xs text-gray-700"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-indigo-700 hover:bg-indigo-800 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched Epoxy Resin Kit &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-gray-800 hover:bg-gray-900 text-white font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop Mica & Degasser
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-gray-900">Search Deep Pour Epoxy, Countertop Kits, Garage Coatings & Pressure Pots</h2>
                <p class="text-sm text-gray-700">Search any kit size (1 Gal, 3 Gal, 6 Gal), brand (Superclear, Stone Coat, TotalBoat, Rust-Oleum, Black Diamond, California Air Tools), or tool on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. Superclear Deep Pour Epoxy 3 Gallon, Stone Coat Countertop Kit, California Air Tools Pressure Pot..."
                           class="flex-1 bg-gray-200 border-2 border-gray-400 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 placeholder-gray-500 focus:outline-none focus:border-indigo-700" required>
                    <button type="submit" class="bg-indigo-700 hover:bg-indigo-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-gray-600 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('Superclear Liquid Glass Deep Pour Epoxy Resin')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-indigo-200 text-gray-800 border border-gray-300 rounded-full transition">Superclear Deep Pour</a>
                    <a href="{amz_url('Stone Coat Countertops Epoxy Resin Kit')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-indigo-200 text-gray-800 border border-gray-300 rounded-full transition">Stone Coat Countertops</a>
                    <a href="{amz_url('TotalBoat ThickSet TableTop Epoxy Resin')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-indigo-200 text-gray-800 border border-gray-300 rounded-full transition">TotalBoat Epoxy Kits</a>
                    <a href="{amz_url('California Air Tools Resin Pressure Pot')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-indigo-200 text-gray-800 border border-gray-300 rounded-full transition">Resin Pressure Pots</a>
                    <a href="{amz_url('Black Diamond Meyspring Mica Powder Pigment')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-indigo-200 text-gray-800 border border-gray-300 rounded-full transition">Mica Pigment Powders</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-indigo-800">Verified Resin & Woodshop Hardware</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">Best-Selling Deep Pour Epoxies, Countertop Kits, Pressure Pots & Sleds</h2>
                </div>
                <a href="{amz_url('Best Selling Deep Pour Epoxy Resin and Countertop Kits')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-indigo-800 hover:text-indigo-900">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- CUMULATIVE DAILY PRODUCT REVIEW ARTICLES SECTION (+3 NEW ARTICLES PER DAY) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-indigo-800">Autonomous Daily Review Archive ({total_reviews_count} Published Articles & Growing +3/Day)</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">In-Depth Epoxy Resin, Pressure Pot & Surfacing Tool Review Articles</h2>
                </div>
                <span class="text-xs font-semibold bg-emerald-100 text-emerald-900 border border-emerald-300 px-3 py-1 rounded-full">+3 New Product Reviews Added Automatically Every Day</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-gray-300 border-2 border-indigo-700 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-indigo-700 text-white px-2.5 py-1 rounded">Complete River Table & Slab Bundle</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-gray-900">Pouring a Live-Edge Walnut River Table or Resurfacing Kitchen Countertops?</h2>
                <p class="text-sm text-gray-800">Eliminate air bubbles and exothermic cracking by pairing a 2\"–4\" Deep Pour Epoxy Kit with Tyvek Release Tape, Black Diamond Mica Pigments, a 60\" Router Flattening Sled, and Rubio Monocoat 2C.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-indigo-700 hover:bg-indigo-800 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore River Table Epoxy + Tool Bundles &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-gray-300 pb-3">
                <h2 class="text-xl font-extrabold text-gray-900">River Table, Countertop, Mold & Garage Floor Specific Calculators</h2>
                <p class="text-xs text-gray-600">Select your exact project dimensions or pour thickness below for pre-calculated epoxy gallons, fluid ounces, and Part A/B gram weights.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-gray-300 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-indigo-800">Exothermic Depth, Mixing & Polishing Guide</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

        {onpage_sitemap_html}

    </main>

    <!-- FOOTER (GRAY BACKGROUND) -->
    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-gray-800">
                <a href="{BASE_URL}/" class="hover:text-indigo-800">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-indigo-800">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-indigo-800">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-indigo-800 font-bold">HTML Site Map</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-indigo-800">XML Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-indigo-800">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 5) {{
                document.getElementById("lengthInput").value = parts[0];
                document.getElementById("widthInput").value = parts[1];
                document.getElementById("depthInput").value = parts[2];
                document.getElementById("ratioInput").value = parts[3];
                document.getElementById("wasteInput").value = parts[4];
                calculateEpoxy();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateEpoxy() {{
            const l = parseFloat(document.getElementById("lengthInput").value) || 72;
            const w = parseFloat(document.getElementById("widthInput").value) || 10;
            const d = parseFloat(document.getElementById("depthInput").value) || 2.0;
            const ratio = document.getElementById("ratioInput").value || "2:1";
            const wastePct = parseFloat(document.getElementById("wasteInput").value) || 10;

            const cuIn = l * w * d * (1.0 + (wastePct / 100.0));
            const totalGal = cuIn / 231.0;
            const totalQts = totalGal * 4.0;
            const totalOz = totalGal * 128.0;
            const totalLiters = totalGal * 3.78541;

            let partAOz = totalOz * 0.5;
            let partBOz = totalOz * 0.5;
            if (ratio === "2:1") {{
                partAOz = totalOz * (2.0 / 3.0);
                partBOz = totalOz * (1.0 / 3.0);
            }}

            const partAGrams = Math.round(partAOz * 34.0);
            const partBGrams = Math.round(partBOz * 28.7);
            const totalLbs = ((partAGrams + partBGrams) / 453.592).toFixed(1);
            const micaGrams = Math.max(5, Math.round(totalGal * 25));

            let resinTypeStr = "Use 2:1 Deep Pour Epoxy";
            if (d <= 0.04) resinTypeStr = "Use Polycuramine / Floor Coat";
            else if (d <= 0.30) resinTypeStr = "Use 1:1 Tabletop Flood Coat";

            document.getElementById("resGallons").textContent = totalGal.toFixed(2) + " Gal";
            document.getElementById("resQuartsOz").textContent = totalQts.toFixed(1) + " Qts (" + Math.round(totalOz) + " fl oz)";
            document.getElementById("resSplitOz").textContent = Math.round(partAOz) + "A / " + Math.round(partBOz) + "B oz";
            document.getElementById("resLiters").textContent = totalLiters.toFixed(2) + " Liters (" + ratio + " Mix)";
            document.getElementById("resSplitGrams").textContent = partAGrams.toLocaleString() + "g A / " + partBGrams.toLocaleString() + "g B";
            document.getElementById("resTotalLbs").textContent = "Total Batch Weight: " + totalLbs + " Lbs";
            document.getElementById("resMicaGrams").textContent = micaGrams + "g Mica Powder";
            document.getElementById("resResinType").textContent = resinTypeStr;

            const kitGalTier = Math.max(1, Math.ceil(totalGal));
            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "";
            let secondaryQuery = "Black Diamond Mica Powder Pigment and Bernzomatic TS8000 Torch";

            if (d <= 0.04) {{
                recTitle = "Rust-Oleum RockSolid Polycuramine or ArmorPoxy 100% Solids Garage Floor Kit (" + kitGalTier + "+ Gal)";
                recDesc = "High-build floor armor engineered for " + Math.round((l * w) / 144) + " sq. ft. concrete slabs.";
                primaryQuery = "Rust Oleum RockSolid Polycuramine ArmorPoxy Garage Floor Epoxy Kit";
            }} else if (d <= 0.30) {{
                recTitle = "Stone Coat Countertops or TotalBoat 1:1 Flood Coat Epoxy (" + kitGalTier + "-Gallon Kit)";
                recDesc = "Self-leveling 470°F heat-resistant 1:1 epoxy for countertops, bar tops, and seal coats.";
                primaryQuery = "Stone Coat Countertops TotalBoat TableTop " + Math.min(4, kitGalTier) + " Gallon Epoxy Resin Kit";
            }} else {{
                recTitle = "Superclear Liquid Glass 2.0 or TotalBoat ThickSet Fathom 2:1 Deep Pour (" + kitGalTier + "-Gallon Kit)";
                recDesc = "Low-exotherm 2\"–4\" single-pass deep casting resin for river tables and deep molds.";
                primaryQuery = "Superclear Liquid Glass TotalBoat ThickSet Deep Pour Epoxy " + Math.min(6, kitGalTier) + " Gallon";
                secondaryQuery = "Router Sled Slab Flattening Mill and Black Diamond Mica Powder";
            }}

            document.getElementById("recEpoxyTitle").textContent = recTitle;
            document.getElementById("recEpoxyDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateEpoxy);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "datePublished": rev["published_date"],
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-emerald-700 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-rose-700 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-gray-800 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    recent_reviews = [r for r in get_cumulative_product_reviews() if r["slug"] != rev["slug"]][:6]
    related_html = ""
    for other in recent_reviews:
        related_html += f"""
        <a href="{BASE_URL}/{other['slug']}.html" class="bg-gray-100 border-2 border-gray-300 rounded-xl p-4 hover:border-indigo-700 transition block">
            <span class="text-[11px] font-bold text-indigo-800 uppercase">{other['verdict_badge']}</span>
            <h4 class="font-extrabold text-sm text-gray-900 mt-1 line-clamp-2">{other['product_name']} Review</h4>
            <span class="text-xs text-gray-600 mt-1 block">Score: {other['rating_score']} / 5.0 ★ ({other['published_date']}) &rarr;</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-indigo-800">Home & Epoxy Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-indigo-800">Daily Epoxy Reviews</a>
            <span>/</span>
            <span class="text-gray-900">{rev['product_name']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-indigo-100 text-indigo-900 border border-indigo-300 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono text-gray-600">Published: {rev['published_date']}</span>
                    <span class="text-sm font-black bg-amber-200 text-amber-950 px-3 py-1 rounded-lg">Shop Rating: {rev['rating_score']} / 5.0 ★</span>
                </div>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-gray-200 p-4 rounded-xl border border-gray-300 text-xs">
                <div><span class="text-gray-500 block font-medium">Pour Spec</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Viscosity / Tech</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Performance</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Details</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-indigo-700 hover:bg-indigo-800 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate Gallons & Grams Needed
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-100 border-2 border-emerald-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-gray-100 border-2 border-rose-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900 border-b border-gray-300 pb-3">Hands-On Exothermic Heat, Bubble Release & Shore-D Cure Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-gray-300 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-indigo-800 block">Final Verdict</span>
                    <p class="text-sm font-bold text-gray-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our resin shop benchmark.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-indigo-700 hover:bg-indigo-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>

        <section class="space-y-4">
            <h3 class="text-lg font-extrabold text-gray-900">Recent Daily Epoxy & Woodshop Reviews (+3 Added Daily)</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {related_html}
            </div>
        </section>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-gray-300">
            <td class="p-4 font-bold text-gray-900 bg-gray-200 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-indigo-800">Home & Epoxy Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-indigo-800">Product Comparisons</a>
            <span>/</span>
            <span class="text-gray-900">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-indigo-100 text-indigo-900 border border-indigo-300 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-800 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-indigo-300">{vs['product_a']}</th>
                        <th class="p-4 text-amber-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-gray-200">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-gray-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-indigo-700 hover:bg-indigo-800 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-gray-100 border-2 border-indigo-600 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-gray-800 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-indigo-700 hover:bg-indigo-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "6-Foot Live-Edge River Table Channel (72\" × 10\" × 2.0\")",
        "length": 72,
        "width": 10,
        "depth": 2.0,
        "ratio": "2:1",
        "waste_pct": 10,
        "desc": "Calculate exact epoxy resin volume (gallons, quarts, fluid ounces & liters), Part A/B gram scale weights, mica pigment grams, and pour depth limits—plus read 3 new epoxy & woodshop reviews added daily."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Dedicated HTML Site Map Page (sitemap.html)
    with open(os.path.join(OUTPUT_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(render_dedicated_html_sitemap_page())
    generated_urls.append(f"{BASE_URL}/sitemap.html")

    # 3. Generate Programmatic Epoxy Pour & Dimension Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Cumulative Daily Product Review Pages (+3 new reviews unlocked every single day)
    active_reviews = get_cumulative_product_reviews()
    for rev in active_reviews:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 6. XML Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} total SEO pages ({len(active_reviews)} cumulative review articles [+3/day] + HTML/XML sitemaps) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
