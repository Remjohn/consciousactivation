# Creative Asset API Reference Guide

> **Purpose:** Platform-specific query structures for precise asset procurement.
> **Last Updated:** January 2026

---

## API Rate Limits Summary

| Platform | Rate Limit | Cost |
|----------|------------|------|
| **Giphy** | 100 req/hr (API), 1000 req/day (SDK) | FREE |
| **Pexels** | 200 req/hr, 20,000 req/month | FREE |
| **Unsplash** | 50 req/hr (Demo), higher with approval | FREE |
| **Pixabay** | 100 req/min | FREE |
| **Outscraper** | Lifetime AppSumo deal | FREE |

---

## 🌍 Language Strategy (CRITICAL)

> [!IMPORTANT]
> **Query language significantly impacts result quality.**

| Platform | Query Language | Reason |
|----------|----------------|--------|
| **Outscraper** | **NATIVE** (FR or EN) | Cultural specificity requires native terms |
| **Giphy** | English only | Better GIF/meme coverage |
| **Pexels** | English only | Larger indexed library |
| **Unsplash** | English only | International photographer base |
| **Pixabay** | English only | Multilingual but EN has best results |

### Examples

**French Client (Coach Adele):**
```
# Outscraper: FRENCH queries
"Maison Château Rouge Youssouf Fofana"
"syndrome méditerranéen racisme médical France"
"Kinkeliba thé longue vie ritual"

# All Others: ENGLISH queries
"celebration black joy" (not "célébration joie noire")
"healing hands meditation" (not "mains guérison méditation")
"morning light coffee" (not "lumière matin café")
```

**English Client:**
```
# Outscraper: ENGLISH queries
"holistic healing natural medicine"
"mindset breakthrough coaching"

# All Others: ENGLISH queries (same)
"celebration success moment"
"peaceful meditation nature"
```

**Implementation Note:**
The E-Roll skill should detect `strategy_brief.lang` and:
- Pass native language to Outscraper queries
- Force `lang=en` for all other API calls

## 1. GIPHY API (GIFs + Clips with Sound)

### Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /v1/gifs/search` | Search GIFs |
| `GET /v1/clips/search` | Search Clips (GIFs with Sound!) |
| `GET /v1/gifs/trending` | Trending GIFs |
| `GET /v1/gifs/translate` | Word → GIF translation |

### Search Parameters

```
api_key      (required)  Your API key
q            (required)  Search query (max 50 chars)
limit        (optional)  Results to return (default: 25, max: 50)
offset       (optional)  Starting position (default: 0)
rating       (optional)  g, pg, pg-13, r (default: r)
lang         (optional)  ISO 639-1 language code (default: en)
country_code (optional)  ISO 3166-1 alpha-2 country code
```

### GIPHY Clips: GIFs with Sound 🔊

**Endpoint:** `GET /v1/clips/search`

**What Makes Clips Special:**
- GIFs + Audio layer = Short-form video content
- Pre-cut to most shareable moments
- Official partner content (licensed!)
- Perfect for cultural/reaction moments

**Response includes:**
- Standard GIF object
- `video` property with all media formats
- Caption files (Subrip/WebVTT) when available

### Query Templates for Cultural DNA

```
# Cultural moments (use @channel for specific sources)
"@complex celebration black joy"
"#reaction mind blown"
"oprah you get a car"

# Tribal expressions
"black excellence"
"african dance celebration"
"healing energy spiritual"

# Pattern interrupts
"plot twist"
"wait what"
"mic drop"
```

### Python Example

```python
import requests

def search_giphy_clips(query, api_key, limit=6):
    """Search GIPHY Clips (GIFs with Sound)"""
    url = "https://api.giphy.com/v1/clips/search"
    params = {
        "api_key": api_key,
        "q": query,
        "limit": limit,
        "rating": "pg-13",
        "lang": "en"
    }
    response = requests.get(url, params=params)
    return response.json()["data"]
```

---

## 2. Pexels API (Photos + Videos)

### Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /v1/search` | Search photos |
| `GET /videos/search` | Search videos |
| `GET /v1/curated` | Curated photos |
| `GET /videos/popular` | Popular videos |

### Photo Search Parameters

```
query        (required)  Search term
orientation  (optional)  landscape, portrait, square
size         (optional)  large (24MP), medium (12MP), small (4MP)
color        (optional)  red, orange, yellow, green, turquoise, 
                         blue, violet, pink, brown, black, gray, white
                         OR hex code (#ffffff)
locale       (optional)  en-US, fr-FR, de-DE, es-ES, pt-BR, ja-JP...
page         (optional)  Page number (default: 1)
per_page     (optional)  Results per page (default: 15, max: 80)
```

### Video Search Parameters

```
query        (required)  Search term
orientation  (optional)  landscape, portrait, square
size         (optional)  large, medium, small
min_width    (optional)  Minimum width in pixels
min_height   (optional)  Minimum height in pixels
min_duration (optional)  Minimum duration in seconds
max_duration (optional)  Maximum duration in seconds
page         (optional)  Page number
per_page     (optional)  Results per page (max: 80)
```

### Query Templates for Mood Shots

```
# T1 Flesh (Close-ups)
"hands coffee morning" + orientation=portrait
"lips close up texture" + color=black

# T2 Private (Intimate spaces)
"bedroom morning light" + orientation=landscape
"bathroom mirror reflection" + color=white

# T3 Artifact (Real objects)
"notebook writing desk" + orientation=square
"coffee cup steam" + color=brown

# T8 Sensory (Textures)
"texture wood grain" + orientation=landscape
"fabric silk flowing" + color=white
```

### Python Example

```python
import requests

def search_pexels_videos(query, api_key, orientation="portrait", per_page=6):
    """Search Pexels Videos with precise filters"""
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": api_key}
    params = {
        "query": query,
        "orientation": orientation,
        "per_page": per_page,
        "min_duration": 3,
        "max_duration": 15
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()["videos"]
```

---

## 3. Unsplash API (High-Quality Photos)

### Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /search/photos` | Search photos |
| `GET /photos/random` | Random photo |
| `GET /collections/{id}/photos` | Collection photos |

### Search Parameters

```
query        (required)  Search term
page         (optional)  Page number (default: 1)
per_page     (optional)  Results per page (default: 10, max: 30)
order_by     (optional)  relevant, latest (default: relevant)
orientation  (optional)  landscape, portrait, squarish
color        (optional)  black_and_white, black, white, yellow, 
                         orange, red, purple, magenta, green, teal, blue
content_filter (optional) low, high (default: low)
lang         (optional)  ISO 639-1 language code (beta)
```

### Query Templates for Realistic Shots

```
# Documentary authenticity
"candid portrait natural light" + orientation=portrait
"street photography urban" + color=black_and_white

# Human imperfection
"wrinkles smile elderly" + orientation=portrait
"messy desk work from home" + orientation=landscape

# Environmental grounding
"city morning commute" + orientation=landscape
"nature meditation peaceful" + color=green
```

### Python Example

```python
import requests

def search_unsplash(query, access_key, orientation="portrait", color=None):
    """Search Unsplash with color and orientation filters"""
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "per_page": 6,
        "orientation": orientation,
        "content_filter": "high"
    }
    if color:
        params["color"] = color
    headers = {"Authorization": f"Client-ID {access_key}"}
    response = requests.get(url, headers=headers, params=params)
    return response.json()["results"]
```

---

## 4. Pixabay API (Photos + Videos)

### Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /api/` | Search images |
| `GET /api/videos/` | Search videos |

### Image Search Parameters

```
key          (required)  API key
q            (required)  Search term (max 100 chars, URL encoded)
lang         (optional)  cs, da, de, en, es, fr, id, it, hu, nl, no, 
                         pl, pt, ro, sk, fi, sv, tr, vi, th, bg, ru, 
                         el, ja, ko, zh (default: en)
image_type   (optional)  all, photo, illustration, vector (default: all)
orientation  (optional)  all, horizontal, vertical (default: all)
category     (optional)  backgrounds, fashion, nature, science, 
                         education, feelings, health, people, religion,
                         places, animals, industry, computer, food, 
                         sports, transportation, travel, buildings, 
                         business, music
min_width    (optional)  Minimum width
min_height   (optional)  Minimum height
colors       (optional)  grayscale, transparent, red, orange, yellow,
                         green, turquoise, blue, lilac, pink, white,
                         gray, black, brown
editors_choice (optional) true = only Editor's Choice images
safesearch   (optional)  true = only safe content (default: false)
order        (optional)  popular, latest (default: popular)
page         (optional)  Page number (default: 1)
per_page     (optional)  Results per page (3-200, default: 20)
```

### Video Search Parameters

Same as images, plus:
```
video_type   (optional)  all, film, animation (default: all)
```

### Query Templates

```
# Realistic documentary
"candid portrait" + image_type=photo + category=people
"office work business" + orientation=horizontal + category=business

# Mood/aesthetic
"nature peaceful zen" + category=nature + colors=green
"texture abstract" + category=backgrounds + colors=brown
```

### Python Example

```python
import requests

def search_pixabay_videos(query, api_key, category=None, per_page=6):
    """Search Pixabay Videos with category filter"""
    url = "https://pixabay.com/api/videos/"
    params = {
        "key": api_key,
        "q": query,
        "video_type": "film",
        "per_page": per_page,
        "safesearch": "true"
    }
    if category:
        params["category"] = category
    response = requests.get(url, params=params)
    return response.json()["hits"]
```

---

## 5. Outscraper (Google Images — Cultural DNA)

### Endpoint

```
GET https://api.outscraper.cloud/google-search-images
```

### Parameters

```
query        (required)  Search term
async        (optional)  false for sync (default: true)
```

### Key Advantage

**Cultural Specificity:** Unlike stock libraries, Outscraper returns real web images:
- Named cultural figures
- Specific brand imagery
- Historical/archival photos
- Meme origins

### Query Templates for Cultural DNA

```
# Named references (MOST EFFECTIVE)
"Maison Château Rouge Youssouf Fofana Bogolan"
"Fatima Douba naturopathe afro-holistique"
"Kinkeliba thé longue vie morning ritual"

# Cultural opposition
"syndrome méditerranéen racisme médical France"
"alimentation blanche poison fade"

# Tribal aesthetics
"Bogolan pattern textile Mali"
"Djeka leaves bain de feuilles ritual"
```

---

## Asset Portfolio Summary (56 Total)

| Category | Count | Primary Source | Fallback |
|----------|-------|----------------|----------|
| Cultural DNA Images | 24 | Outscraper | Bing |
| Cultural GIFs | 4 | Giphy GIFs | — |
| GIPHY Clips (Sound!) | 6 | Giphy Clips | — |
| Mood Images | 6 | Pexels | Unsplash → Pixabay |
| Mood Videos | 6 | Pexels Video | Pixabay Video |
| Realistic Images | 6 | Pexels | Pixabay |
| Realistic Videos | 4 | Pexels Video | Pixabay Video |
| **TOTAL** | **56** | — | — |

---

## Environment Variables Required

```env
# .env file
GIPHY_API_KEY=...
PEXELS_API_KEY=...
UNSPLASH_ACCESS_KEY=...
PIXABAY_API_KEY=...
OUTSCRAPER_API_KEY=...
SERPAPI_KEY=...  # For Bing fallback
```
