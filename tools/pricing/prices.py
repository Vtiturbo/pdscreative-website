"""
PDS Creative price list, single source of truth (November 2026).

Every price is set about 30% below a typical London rate ("london"), researched from published
2026 UK price guides (London sits at the top of the UK ranges, roughly 15-33% higher).
Run build.py to regenerate the pricing PDF and the data on pricing.html from this file.
"""

DISCOUNT_TARGET = 0.30
EDITION = "November 2026"

# id: name, price, london (typical London price), unit, note/details
BRAND = {
    "logo":  {"name": "Logo design", "price": 1395, "london": 2000,
              "desc": "Primary logo, two variations and icon, colour palette and fonts"},
    "kit":   {"name": "Brand identity kit", "price": 2695, "london": 3900,
              "desc": "Full logo suite, colours, fonts, brand guidelines, business card and social profile design"},
}

SITES = {
    "launch":    {"name": "Launch", "price": 2450, "london": 3500, "best": "Sole traders and new businesses", "days": "5 working days",
                  "feats": ["Up to 5 pages", "Custom design, hand-coded", "On-page SEO and AI search-ready", "Contact form, maps and social links", "2 rounds of revisions"], "care": "essential"},
    "signature": {"name": "Signature", "price": 4195, "london": 6000, "best": "Established local businesses", "days": "5 working days", "popular": True,
                  "feats": ["Up to 10 pages plus blog", "Fully bespoke design", "Booking or enquiry system", "SEO, AI search and Google Business Profile", "2 rounds of revisions"], "care": "growth"},
    "flagship":  {"name": "Flagship", "price": 8395, "london": 12000, "best": "Brands selling online or needing custom features", "days": "10–15 working days", "from": True,
                  "feats": ["Up to 20 pages plus custom templates", "Online shop, memberships and payments", "Keyword plan, schema and local SEO pages", "CRM and booking integrations", "3 rounds of revisions"], "care": "partner"},
}

SOCIAL = {
    "makeover": {"name": "Social media makeover", "price": 875, "london": 1250,
                 "desc": "New profile look for Instagram, Facebook, TikTok and LinkedIn: profile picture, banners, bio, highlight covers and 12 post and story templates"},
    "grid":     {"name": "Instagram launch grid", "price": 625, "london": 900,
                 "desc": "9 designed launch posts with captions, made from your brand and shoot"},
    "static":   {"name": "Advert pack: 5 image ads", "price": 875, "london": 1250,
                 "desc": "5 ads for Instagram, Facebook and Google, each in feed, story and banner sizes, with 2 headline options"},
    "video":    {"name": "Advert pack: 3 video ads", "price": 2550, "london": 3675,
                 "desc": "3 short video ads (15–30 seconds) filmed and edited for feed, stories, Reels and YouTube"},
}

PHOTO = {
    "half":     {"name": "Brand photo shoot, half day", "price": 665, "london": 950, "desc": "40+ edited images: your team, premises, products and work"},
    "full":     {"name": "Brand photo shoot, full day", "price": 1095, "london": 1600, "desc": "80+ images, multiple locations and team headshots"},
    "headshot": {"name": "Team headshots", "price": 50, "london": 75, "unit": " / person", "desc": "Consistent on-site headshots, minimum 6 people"},
    "event_half": {"name": "Event coverage, half day", "price": 415, "london": 600, "desc": "Launches, openings and corporate events"},
    "event_full": {"name": "Event coverage, full day", "price": 665, "london": 950, "desc": "Launches, openings and corporate events"},
}

VIDEO = {
    "film":  {"name": "Brand film", "price": 3395, "london": 4900, "desc": "60–90 second film for your homepage, plus 3 vertical cuts for social"},
    "reels": {"name": "Social reels pack", "price": 1395, "london": 2000, "desc": "4 short vertical videos for Reels, TikTok and Shorts from one shoot"},
    "combo": {"name": "Photo + film day", "price": 3995, "london": 6500, "desc": "Full-day brand photo shoot and brand film together"},
}

EXTRAS = {
    "page":  {"name": "Additional page", "price": 195},
    "gbp":   {"name": "Google Business Profile setup", "price": 195},
    "pay":   {"name": "Booking or payments integration", "price": 350},
    "audit": {"name": "Website audit (credited if you go ahead)", "price": 149},
}

CARE = {
    "secure":    {"name": "Secure", "price": 42, "london": 60, "best": "Sites that rarely change", "disc": 0.0},
    "essential": {"name": "Essential", "price": 89, "london": 130, "best": "Occasional updates", "disc": 0.05},
    "growth":    {"name": "Growth", "price": 195, "london": 280, "best": "Sites that bring in enquiries", "disc": 0.10, "popular": True},
    "partner":   {"name": "Partner", "price": 385, "london": 550, "best": "Sites that drive sales", "disc": 0.15},
}
CARE_ROWS = [
    ("Hosting, SSL, domain", ["Yes", "Yes", "Yes", "Yes"]),
    ("Updates & security", ["Monthly", "Weekly", "Weekly", "Weekly + urgent fixes in 24h"]),
    ("Backups & uptime alerts", ["Daily", "Daily", "Daily", "Daily + off-site copy"]),
    ("Edits included", ["Billed hourly", "1 hour / month", "3 hours / month", "6 hours / month"]),
    ("Response time", ["3 working days", "2 working days", "Next working day", "Same working day"]),
    ("Monthly report", ["Uptime & backups", "+ visitor numbers", "+ enquiries & top pages", "+ insights & recommendations"]),
    ("SEO & AI search", ["—", "—", "Monthly tune-up, Google Business posts", "+ new SEO page each quarter"]),
    ("Strategy call", ["—", "—", "Quarterly, 30 min", "Monthly, 45 min"]),
    ("Photo, video & design discount", ["—", "5%", "10%", "15%"]),
]

SUBS = {
    "seasonal": {"name": "Seasonal", "price": 220, "london": 317,
                 "feats": ["One half-day shoot every quarter", "30 edited images per shoot", "Website refreshed with your new images"]},
    "monthly":  {"name": "Monthly", "price": 625, "london": 900, "popular": True,
                 "feats": ["One 2-hour shoot every month", "30 edited images plus video clips", "Added to your website, ready for social"]},
    "studio":   {"name": "Studio", "price": 2695, "london": 3900,
                 "feats": ["Two half-day photo and video shoots a month", "40 edited images with every shoot", "4 reels every month"]},
}
BUNDLES = [
    {"name": "Always Fresh", "care": "growth", "sub": "monthly", "price": 745},
    {"name": "Partner Studio", "care": "partner", "sub": "studio", "price": 2795},
]

# Complete packages: everything a new business needs to look ready, in one price.
PACKAGES = {
    "startup":  {"name": "Start-Up Kit", "price": 4495, "days": "Ready in 5 working days",
                 "best": "New businesses that need to look established from day one",
                 "includes": {"brand": "logo", "site": "launch", "social": ["makeover"], "photo": "half", "video": []},
                 "lines": ["Logo design with colours and fonts", "Launch website, up to 5 pages", "Social media makeover", "Half-day brand photo shoot"]},
    "launch":   {"name": "Brand Launch", "price": 9495, "days": "Ready in 5 working days", "popular": True,
                 "best": "Businesses launching or relaunching with a full brand",
                 "includes": {"brand": "kit", "site": "signature", "social": ["makeover", "grid", "static"], "photo": "half", "video": ["reels"]},
                 "lines": ["Brand identity kit and guidelines", "Signature website, up to 10 pages", "Social media makeover + Instagram launch grid", "Half-day brand photo shoot", "4 social reels", "5 image adverts"]},
    "complete": {"name": "Complete Brand", "price": 16995, "days": "Ready in 10–15 working days", "from": True,
                 "best": "Brands selling online or launching with paid advertising",
                 "includes": {"brand": "kit", "site": "flagship", "social": ["makeover", "grid", "static", "video"], "photo": "combo", "video": []},
                 "lines": ["Brand identity kit and guidelines", "Flagship website with online shop", "Social media makeover + Instagram launch grid", "Photo + film day with brand film", "5 image adverts + 3 video adverts"]},
}


def london_of_package(p):
    inc = p["includes"]
    total = BRAND[inc["brand"]]["london"] + SITES[inc["site"]]["london"]
    total += sum(SOCIAL[s]["london"] for s in inc["social"])
    total += (VIDEO[inc["photo"]] if inc["photo"] == "combo" else PHOTO[inc["photo"]])["london"]
    total += sum(VIDEO[v]["london"] for v in inc["video"])
    return total


def separate_of_package(p):
    inc = p["includes"]
    total = BRAND[inc["brand"]]["price"] + SITES[inc["site"]]["price"]
    total += sum(SOCIAL[s]["price"] for s in inc["social"])
    total += (VIDEO[inc["photo"]] if inc["photo"] == "combo" else PHOTO[inc["photo"]])["price"]
    total += sum(VIDEO[v]["price"] for v in inc["video"])
    return total


def all_items():
    for group in (BRAND, SITES, SOCIAL, PHOTO, VIDEO, CARE, SUBS):
        for k, v in group.items():
            yield k, v
    for k, p in PACKAGES.items():
        yield k, {"name": p["name"], "price": p["price"], "london": london_of_package(p)}


def check():
    """Every priced item must be at least ~30% below its London benchmark."""
    bad = []
    for k, v in all_items():
        if "london" in v:
            below = 1 - v["price"] / v["london"]
            if below < 0.29:
                bad.append((v["name"], round(below * 100, 1)))
    for b in BUNDLES:
        sep = CARE[b["care"]]["price"] + SUBS[b["sub"]]["price"]
        assert b["price"] < sep, b
    for k, p in PACKAGES.items():
        assert p["price"] < separate_of_package(p), k
    return bad


if __name__ == "__main__":
    for k, v in all_items():
        if "london" in v:
            print(f"{v['name']:<34} £{v['price']:>6,}  London £{v['london']:>6,}  {round((1 - v['price'] / v['london']) * 100)}% below")
    for k, p in PACKAGES.items():
        print(f"{p['name']}: separately £{separate_of_package(p):,}, package £{p['price']:,}")
    print("Under 29% below:", check())
