import streamlit as st
import streamlit.components.v1 as components
def show_gallery():
    st.markdown("""
    <style>
        .main .block-container {
            padding-top: 0;
            padding-bottom: 0;
        }
        footer {visibility: hidden;}
        .stApp {
            background: #f5f5f5;
            overflow: hidden;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("India's Art and Culture")
    festivals = [
        {
            "name": "Diwali - The Grand Festival Of Lights",
            "description": "Diwali, one of the most prominent Hindu festivals of India, is celebrated with a lot of pomp and show. During this festival of lights, houses are decorated with clay lamps, candles, and Ashok leaves. People wear new clothes, participate in family puja, burst crackers, and share sweets with friends, families, and neighbours. It is the most popular festival in India",
            "things_to_do": "Light diyas, decorate your home, share sweets and gifts with family and loved ones",
            "date": "October 31(Thursday)",
            "image": "https://raw.githubusercontent.com/mohammedabsal/GeoBoost/main/assest/diw.jpg",
            "link": "https://en.wikipedia.org/wiki/Diwali"
        },
        {
            "name": "Holi-The Vibrant Festival Of Colours",
            "description": "Holi, the vibrant Festival of Colours, is one of India's most famous celebrations. On Holika Dahan, huge bonfires are lit with singing and dancing around them. The next day, people gather to splash each other with colorful powders, water guns, and balloons, filling the streets with joy and hues. It's a lively and joyous celebration of color, unity, and the arrival of spring.",
            "things_to_do": "",
            "date": "March 14,2025(Friday)",
            "image": "https://raw.githubusercontent.com/mohammedabsal/GeoBoost/main/assest/holi.jpg",
            "link": "https://en.wikipedia.org/wiki/Holi"
        },
        {
            "name": "Dussehra-Witness The Triumph Of Good Over Evil",
            "description": "Dussehra, or Vijayadashami, is a major Hindu festival celebrating the victory of good over evil. The burning of Ravana's effigy after 10 days of *Ramlila* is the main highlight. In Mysore, there's a grand procession with the palace lit up, while Kullu celebrates by welcoming mountain deities for 10 days. Each region adds its own unique touch to the festivities.",
            "things_to_do": "",
            "date": "October 12,2024(Saturday)",
            "image": "https://raw.githubusercontent.com/mohammedabsal/GeoBoost/main/assest/dhusu.jpg",
            "link": "https://en.wikipedia.org/wiki/Dussehra"
        },
        {
            "name": "Durga Pooja",
            "description": "Durga Puja, a grand Bengali celebration, is one of India's most cherished festivals. The 10-day event combines fasting, feasting, and worship of Goddess Durga, accompanied by cultural performances. Stunning Durga idols are placed in intricately designed pandals, where people gather in traditional attire for prayers, festivities, and pandal-hopping. The blend of devotion, artistry, and community spirit makes Durga Puja a truly vibrant spectacle.",
            "things_to_do": "",
            "date": "24th October(Tuesday)",
            "image": "https://raw.githubusercontent.com/mohammedabsal/GeoBoost/main/assest/dur.png",
            "link": "https://en.wikipedia.org/wiki/Durga_Puja"
        },
        {
            "name": "Ramadan / Eid –Ul-Fitr",
            "description": "Ramadan is the ninth and holiest month in the Islamic calendar, observed by Muslims through fasting from dawn to sunset, prayer, reflection, and charity. Fasting, or *sawm*, fosters self-discipline and empathy for the less fortunate. The month ends with Eid al-Fitr, a celebration of breaking the fast with prayers, feasts, and family gatherings",
            "things_to_do": "",
            "date": "March 31st(Monday),2025",
            "image": "https://raw.githubusercontent.com/mohammedabsal/GeoBoost/main/assest/ramadan_1.jpeg ",
            "link": "https://en.wikipedia.org/wiki/Ramadan"
        },
        {
            "name": "Christmas",
            "description": "Christmas is celebrated on December 25th, marking the birth of Jesus Christ. It is observed by Christians worldwide with church services, caroling, and gift-giving. The holiday features festive decorations, family gatherings, and a spirit of joy, peace, and goodwill, emphasizing love and generosity.",
            "things_to_do": "",
            "date": "25th December,2024",
            "image": "https://raw.githubusercontent.com/mohammedabsal/GeoBoost/main/assest/christ.jpg",
            "link": "https://en.wikipedia.org/wiki/Christmas"
        },
        {
            "name": "Onam",
            "description": "Onam, a major festival in India, is celebrated with vibrant traditions and community spirit. People wear traditional attire, decorate homes with Pookalam (floral patterns), and enjoy Onasadya, a grand meal of around 13 dishes. Festivities include Vallamkali (snake boat race), Kaikottikali (clap dance), Kathakali performances, and the lively Pulikali procession, where participants are painted as tigers and hunters. This festival marks the return of the mythical King Mahabali. Key highlights include the snake boat races, Kaikottikali dances, and majestic elephant processions. It takes place in Kerala during August or September.",
            "things_to_do": "",
            "date": "25th December,2024",
            "image": "https://raw.githubusercontent.com/mohammedabsal/GeoBoost/main/assest/onam_1.jpeg",
            "link": "https://en.wikipedia.org/wiki/Onam"
        },
        {
            "name": "Krishna Janmashtami",
            "description": "Janmashtami, a significant Hindu festival, marks the birth of Lord Krishna. Celebrated with fasting, temple visits, and midnight prayers, the festivities are especially grand in Mathura and Vrindavan. Children dress as Krishna, and temples showcase \"jhankis\" depicting his life. This festival occurs on the 8th day of Krishna Paksha in Bhadrapada, usually in August or September.",
            "things_to_do": "",
            "date": "25th December,2024",
            "image": "https://raw.githubusercontent.com/mohammedabsal/GeoBoost/main/assest/krishna_1.jpg",
            "link": "https://en.wikipedia.org/wiki/Krishna_Janmashtami"
        },
        {
            "name": "Bakrid",
            "description": "Bakrid, also known as Eid al-Adha, is an important Islamic festival celebrated with prayers, charity, and the symbolic sacrifice of an animal. It honors the willingness of Prophet Ibrahim to sacrifice his son in obedience to God. After prayers at the mosque, families gather for a feast, and the meat from the sacrifice is distributed among family, friends, and the needy. The festival promotes the spirit of giving and gratitude. Bakrid is observed on the 10th day of Dhu al-Hijjah, the last month of the Islamic lunar calendar.",
            "things_to_do": "",
            "date": "Friday, June 6th,2025",
            "image": "https://raw.githubusercontent.com/mohammedabsal/GeoBoost/main/assest/eid.jpg",
            "link": "https://en.wikipedia.org/wiki/Eid_al-Adha"
        },
        {
            "name": "Easter",
            "description": "Easter is a major Christian festival celebrating the resurrection of Jesus Christ from the dead. The day is marked with special church services, prayers, and joyful celebrations. Families often gather for festive meals, and traditions like Easter egg hunts and gifting chocolate eggs symbolize new life and rebirth. Easter is observed on the first Sunday after the first full moon following the spring equinox, usually in March or April. It is a time of hope, renewal, and joy for Christians worldwide.",
            "things_to_do": "",
            "date": "Sunday, April 20, 2025.",
            "image": "https://raw.githubusercontent.com/mohammedabsal/GeoBoost/main/assest/church.jpg",
            "link": "https://en.wikipedia.org/wiki/Easter"
        }
    ]

    # Generate HTML for each festival item
    festival_items = ""
    for i, festival in enumerate(festivals):
        active_class = "active" if i == 0 else ""
        festival_items += f"""
        <div class="item {active_class}" style="background-image: url('{festival['image']}')">
            <div class="content">
                <div class="name">{festival['name']}</div>
                <div class="des">{festival['description']}</div>
                {f'<div class="des">{festival["things_to_do"]}</div>' if festival["things_to_do"] else ""}
                <div class="des">{festival['date']}</div>
                <a href="{festival.get('link', '#')}" target="_blank"><button>See More</button></a>
            </div>
        </div>
        """

    custom_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>India's Cultural Festivals</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: Arial, sans-serif;
                overflow: hidden;
                height: 100vh;
                width: 100vw;
            }}
            
            .container {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: #f5f5f5;
            }}
            
            .slide {{
                position: relative;
                width: 100%;
                height: 100%;
            }}
            
            .item {{
                position: absolute;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                background-size: cover;
                background-position: center;
                transition: opacity 0.8s ease, transform 0.8s ease;
                opacity: 0;
                transform: scale(0.9);
                will-change: transform, opacity;
            }}
            
            .item.active {{
                opacity: 1;
                transform: scale(1);
                z-index: 1;
            }}
            
            .item .content {{
                position: absolute;
                bottom: 20%;
                left: 10%;
                width: 35%;
                padding: 2rem;
                background: rgba(0, 0, 0, 0.7);
                color: white;
                border-radius: 10px;
                backdrop-filter: blur(5px);
            }}
            
            .name {{
                font-size: 2rem;
                margin-bottom: 1rem;
                font-weight: bold;
            }}
            
            .des {{
                margin-bottom: 1rem;
                line-height: 1.5;
            }}
            
            button {{
                padding: 0.5rem 1rem;
                background: #FF8C00;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background 0.3s;
            }}
            
            button:hover {{
                background: #FF6F00;
            }}
            
            .nav-buttons {{
                position: fixed;
                bottom: 2rem;
                left: 50%;
                transform: translateX(-50%);
                z-index: 100;
                display: flex;
                gap: 1rem;
            }}
            
            .nav-btn {{
                width: 3rem;
                height: 3rem;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.7);
                border: none;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.2rem;
                transition: all 0.3s;
            }}
            
            .nav-btn:hover {{
                background: rgba(255, 140, 0, 0.9);
                color: white;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="slide">
                {festival_items}
            </div>
            
            <div class="nav-buttons">
                <button class="nav-btn prev"><i class="fas fa-arrow-left"></i></button>
                <button class="nav-btn next"><i class="fas fa-arrow-right"></i></button>
            </div>
        </div>

        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                const items = document.querySelectorAll('.item');
                const prevBtn = document.querySelector('.prev');
                const nextBtn = document.querySelector('.next');
                let currentIndex = 1; // Start with second item as active
                let isAnimating = false;
                
                // Initialize slider
                function initSlider() {{
                    items.forEach((item, index) => {{
                        item.classList.remove('active');
                        if (index === currentIndex) {{
                            item.classList.add('active');
                        }}
                    }});
                }}
                
                // Change slide with debounce
                function changeSlide(direction) {{
                    if (isAnimating) return;
                    isAnimating = true;
                    
                    // Fade out current slide
                    items[currentIndex].classList.remove('active');
                    
                    // Update index
                    if (direction === 'next') {{
                        currentIndex = (currentIndex + 1) % items.length;
                    }} else {{
                        currentIndex = (currentIndex - 1 + items.length) % items.length;
                    }}
                    
                    // Fade in new slide
                    setTimeout(() => {{
                        items[currentIndex].classList.add('active');
                        isAnimating = false;
                    }}, 800);
                }}
                
                // Event listeners with debounce
                prevBtn.addEventListener('click', () => changeSlide('prev'));
                nextBtn.addEventListener('click', () => changeSlide('next'));
                
                // Keyboard navigation
                document.addEventListener('keydown', (e) => {{
                    if (e.key === 'ArrowLeft') changeSlide('prev');
                    if (e.key === 'ArrowRight') changeSlide('next');
                }});
                
                // Initialize
                initSlider();
                
                // Preload all images
                function preloadImages() {{
                    const images = [
                        {', '.join([f'"{festival["image"]}"' for festival in festivals])}
                    ];
                    images.forEach(src => {{
                        const img = new Image();
                        img.src = src;
                    }});
                }}
                preloadImages();
            }});
        </script>
    </body>
    </html>
    """
    components.html(custom_html, height=800, scrolling=False)
    st.markdown("""
        <div class="footer">
            © 2025 GeoBoost. All rights reserved.
        </div>
    """, unsafe_allow_html=True)