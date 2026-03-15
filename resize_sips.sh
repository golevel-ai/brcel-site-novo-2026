#!/bin/bash

function process_image {
    src=$1
    dst=$2
    w=$3
    h=$4
    
    # max dimension
    max_dim=$w
    if [ "$h" -gt "$w" ]; then
        max_dim=$h
    fi
    
    # temporary work file
    tmp_file="/tmp/temp_crop_${max_dim}.png"
    cp "$src" "$tmp_file"
    
    # resize proportionally so the max dimension matches
    sips -Z "$max_dim" "$tmp_file" > /dev/null
    
    # then crop to exact dimensions from center (sips -c height width)
    sips -c "$h" "$w" "$tmp_file" --out "$dst" > /dev/null
    
    echo "Processed $dst"
}

process_image "/Users/danilo/.gemini/antigravity/brain/86da3a94-3a51-4c6c-abdb-a88870a5ebc8/about_person_1773540342348.png" "/Users/danilo/Documents/GitHub/brcel-site-novo-2026/Buyer files/assets/img/home-1/about/superhero.png" 508 789
process_image "/Users/danilo/.gemini/antigravity/brain/86da3a94-3a51-4c6c-abdb-a88870a5ebc8/about_pattern_1773540356579.png" "/Users/danilo/Documents/GitHub/brcel-site-novo-2026/Buyer files/assets/img/home-1/about/eplay.png" 131 668
process_image "/Users/danilo/.gemini/antigravity/brain/86da3a94-3a51-4c6c-abdb-a88870a5ebc8/about_phone_1773540371233.png" "/Users/danilo/Documents/GitHub/brcel-site-novo-2026/Buyer files/assets/img/home-1/about/game-controller.png" 861 982

process_image "/Users/danilo/.gemini/antigravity/brain/86da3a94-3a51-4c6c-abdb-a88870a5ebc8/game_01_1773540404689.png" "/Users/danilo/Documents/GitHub/brcel-site-novo-2026/Buyer files/assets/img/home-1/game/game-01.jpg" 450 333
process_image "/Users/danilo/.gemini/antigravity/brain/86da3a94-3a51-4c6c-abdb-a88870a5ebc8/game_02_1773540420212.png" "/Users/danilo/Documents/GitHub/brcel-site-novo-2026/Buyer files/assets/img/home-1/game/game-02.jpg" 450 333
process_image "/Users/danilo/.gemini/antigravity/brain/86da3a94-3a51-4c6c-abdb-a88870a5ebc8/game_3_1773540434598.png" "/Users/danilo/Documents/GitHub/brcel-site-novo-2026/Buyer files/assets/img/home-1/game/game-3.jpg" 450 333

process_image "/Users/danilo/.gemini/antigravity/brain/86da3a94-3a51-4c6c-abdb-a88870a5ebc8/top_image_1773540474097.png" "/Users/danilo/Documents/GitHub/brcel-site-novo-2026/Buyer files/assets/img/home-1/game/top-image.jpg" 460 991
process_image "/Users/danilo/.gemini/antigravity/brain/86da3a94-3a51-4c6c-abdb-a88870a5ebc8/game_bg_1773540488857.png" "/Users/danilo/Documents/GitHub/brcel-site-novo-2026/Buyer files/assets/img/home-1/game/bg.jpg" 330 330
process_image "/Users/danilo/.gemini/antigravity/brain/86da3a94-3a51-4c6c-abdb-a88870a5ebc8/cta_img_1773540504252.png" "/Users/danilo/Documents/GitHub/brcel-site-novo-2026/Buyer files/assets/img/home-1/cta-img.png" 480 315

echo "All done"
