from PIL import Image, ImageOps
import os

images = [
    ("/Users/danilo/.gemini/antigravity/brain/86da3a94-3a51-4c6c-abdb-a88870a5ebc8/about_person_1773540342348.png", "/Users/danilo/Documents/GitHub/brcel-site-novo-2026/Buyer files/assets/img/home-1/about/superhero.png", 508, 789),
    ("/Users/danilo/.gemini/antigravity/brain/86da3a94-3a51-4c6c-abdb-a88870a5ebc8/about_pattern_1773540356579.png", "/Users/danilo/Documents/GitHub/brcel-site-novo-2026/Buyer files/assets/img/home-1/about/eplay.png", 131, 668),
    ("/Users/danilo/.gemini/antigravity/brain/86da3a94-3a51-4c6c-abdb-a88870a5ebc8/about_phone_1773540371233.png", "/Users/danilo/Documents/GitHub/brcel-site-novo-2026/Buyer files/assets/img/home-1/about/game-controller.png", 861, 982),
    ("/Users/danilo/.gemini/antigravity/brain/86da3a94-3a51-4c6c-abdb-a88870a5ebc8/game_01_1773540404689.png", "/Users/danilo/Documents/GitHub/brcel-site-novo-2026/Buyer files/assets/img/home-1/game/game-01.jpg", 450, 333),
    ("/Users/danilo/.gemini/antigravity/brain/86da3a94-3a51-4c6c-abdb-a88870a5ebc8/game_02_1773540420212.png", "/Users/danilo/Documents/GitHub/brcel-site-novo-2026/Buyer files/assets/img/home-1/game/game-02.jpg", 450, 333),
    ("/Users/danilo/.gemini/antigravity/brain/86da3a94-3a51-4c6c-abdb-a88870a5ebc8/game_3_1773540434598.png", "/Users/danilo/Documents/GitHub/brcel-site-novo-2026/Buyer files/assets/img/home-1/game/game-3.jpg", 450, 333),
    ("/Users/danilo/.gemini/antigravity/brain/86da3a94-3a51-4c6c-abdb-a88870a5ebc8/top_image_1773540474097.png", "/Users/danilo/Documents/GitHub/brcel-site-novo-2026/Buyer files/assets/img/home-1/game/top-image.jpg", 460, 991),
    ("/Users/danilo/.gemini/antigravity/brain/86da3a94-3a51-4c6c-abdb-a88870a5ebc8/game_bg_1773540488857.png", "/Users/danilo/Documents/GitHub/brcel-site-novo-2026/Buyer files/assets/img/home-1/game/bg.jpg", 330, 330),
    ("/Users/danilo/.gemini/antigravity/brain/86da3a94-3a51-4c6c-abdb-a88870a5ebc8/cta_img_1773540504252.png", "/Users/danilo/Documents/GitHub/brcel-site-novo-2026/Buyer files/assets/img/home-1/cta-img.png", 480, 315)
]

for src, dst, w, h in images:
    if os.path.exists(src):
        img = Image.open(src)
        if dst.endswith('.jpg'):
            img = img.convert('RGB')
        
        # calculate aspect ratio aware crop
        img_cropped = ImageOps.fit(img, (w, h), Image.Resampling.LANCZOS, centering=(0.5, 0.5))
        img_cropped.save(dst)
        print(f"Processed {dst}")
    else:
        print(f"Source not found: {src}")
