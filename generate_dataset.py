"""
Comprehensive Dataset Generator for Fake News Detector
Generates data/True.csv and data/Fake.csv matching Kaggle's 'Fake and Real News Dataset' format:
Columns: title, text, subject, date
"""
import os
import pandas as pd
import random

real_templates = [
    {
        "title": "Federal Reserve Holds Benchmark Interest Rates Steady Amid Cooling Inflation",
        "text": "WASHINGTON (Reuters) - The Federal Reserve maintained its benchmark interest rate target on Wednesday, citing meaningful progress in slowing inflation toward its 2 percent annual target. Federal Reserve Chair Jerome Powell stated in a press briefing that economic growth remains resilient and labor market conditions continue to normalize. Policymakers noted that while wage increases have moderated, consumer spending and business investment continue to support domestic economic output. Financial markets reacted calmly to the monetary policy announcement.",
        "subject": "politicsNews",
        "date": "October 4, 2023"
    },
    {
        "title": "NASA James Webb Space Telescope Identifies Atmospheric Carbon Dioxide on Distant Exoplanet",
        "text": "GREENBELT, Md. - NASA's James Webb Space Telescope has captured definitive evidence of carbon dioxide in the atmosphere of a gas giant exoplanet orbiting a Sun-like star approximately 700 light-years away. The discovery, published in the journal Nature by an international team of astrophysicists, demonstrates the observatory's unprecedented spectroscopic capability. The observation of WASP-39 b provides crucial insights into how planets form and evolve over billions of years.",
        "subject": "worldnews",
        "date": "August 25, 2022"
    },
    {
        "title": "European Union Reaches Historic Agreement on Comprehensive Artificial Intelligence Act",
        "text": "BRUSSELS (Reuters) - Negotiators from the European Parliament and European Union member states reached a landmark provisional deal on Friday governing the deployment of artificial intelligence systems. The Artificial Intelligence Act establishes strict guardrails for high-risk applications, prohibitions on biometric surveillance in public spaces with narrow exceptions, and transparency requirements for foundational AI models. Officials described the legislation as a balanced framework safeguarding fundamental civil rights.",
        "subject": "worldnews",
        "date": "December 9, 2023"
    },
    {
        "title": "World Health Organization Declares Global Cholera Surge Requires Urgent Medical Intervention",
        "text": "GENEVA - The World Health Organization issued an urgent global health briefing on Tuesday highlighting rising cholera outbreaks across multiple continents exacerbated by severe weather events and strained public health infrastructure. Health officials emphasized that global vaccine stockpiles are critically low and urged international partners to finance clean water sanitation systems. Hundreds of thousands of cases have been recorded over the past year.",
        "subject": "worldnews",
        "date": "November 14, 2023"
    },
    {
        "title": "Senate Passes Bipartisan Infrastructure Investment and Jobs Act with Broad Support",
        "text": "WASHINGTON (AP) - In a notable display of bipartisan legislative cooperation, the United States Senate approved a sweeping $1.2 trillion infrastructure package on Tuesday, authorizing major funding for public transit, bridge repairs, clean water initiatives, and nationwide broadband connectivity. The bill received 69 affirmative votes, including support from nineteen Republicans, sending the measure to the House of Representatives.",
        "subject": "politicsNews",
        "date": "August 10, 2021"
    },
    {
        "title": "Renewable Energy Capacity Sees Record Global Growth in 2023, International Energy Agency Reports",
        "text": "PARIS - The International Energy Agency announced in its annual market review that global renewable electricity capacity expanded by fifty percent over the past year, the fastest pace of growth observed in two decades. Solar photovoltaic systems accounted for three-quarters of new installations globally, driven by substantial cost declines and supportive national policies across Europe, North America, and Asia.",
        "subject": "worldnews",
        "date": "January 11, 2024"
    },
    {
        "title": "Supreme Court Issues Decisive Ruling on Clean Water Act Authority Over Wetlands",
        "text": "WASHINGTON (Reuters) - The United States Supreme Court delivered a unanimous ruling on Thursday limiting federal regulatory authority over wetlands under the Clean Water Act. The majority opinion established that federal jurisdiction applies exclusively to wetlands with a continuous surface water connection to navigable bodies of water. Environmental groups expressed concern regarding vulnerable ecosystems, while industrial developers welcomed the clarity.",
        "subject": "politicsNews",
        "date": "May 25, 2023"
    },
    {
        "title": "Global Trade Routes Normalize as Ocean Freight Backlogs Clear Across Major Container Terminals",
        "text": "SINGAPORE - International ocean freight shipping rates have returned to pre-pandemic averages as backlogs at major Asian and North American ports have fully cleared, according to logistics industry indices published on Monday. Terminal operators reported improved container throughput and warehouse efficiency, although regional geopolitical uncertainties in maritime shipping lanes remain closely monitored.",
        "subject": "worldnews",
        "date": "September 18, 2023"
    },
    {
        "title": "Japan Aerospace Agency Successfully Launches Environmental Monitoring Satellite into Orbit",
        "text": "TOKYO (Kyodo) - Japan Aerospace Exploration Agency successfully launched an H-IIA rocket carrying a next-generation greenhouse gas monitoring satellite from the Tanegashima Space Center on Sunday. The satellite is equipped with high-resolution spectroscopic sensors engineered to track regional methane and carbon emissions with precision, providing open-access data to global climate researchers.",
        "subject": "worldnews",
        "date": "October 29, 2023"
    },
    {
        "title": "Treasury Department Unveils Updated Sourcing Guidelines for Clean Vehicle Consumer Credits",
        "text": "WASHINGTON (Reuters) - The U.S. Department of the Treasury issued updated guidelines on consumer clean vehicle tax incentives under federal climate legislation. The rules specify strict manufacturing thresholds for battery components and critical minerals, requiring qualifying vehicles to source materials from domestic facilities or nations with bilateral trade agreements.",
        "subject": "politicsNews",
        "date": "March 31, 2023"
    },
    {
        "title": "United Nations Security Council Adopts Binding Resolution Demanding Immediate Humanitarian Ceasefire",
        "text": "NEW YORK (Reuters) - The United Nations Security Council adopted a formal resolution on Wednesday demanding an immediate humanitarian pause in ongoing hostilities to facilitate the delivery of critical medical supplies, clean water, and emergency food supplies to civilian populations. Diplomats emphasized the mandatory nature of international humanitarian conventions.",
        "subject": "worldnews",
        "date": "November 15, 2023"
    },
    {
        "title": "Scientists Develop High Efficiency Tandem Solar Cell Surpassing Thirty Percent Threshold",
        "text": "BERLIN - Physicists and material scientists at the Helmholtz-Zentrum Berlin have produced a tandem perovskite silicon photovoltaic cell achieving thirty-two point five percent energy conversion efficiency. The experimental breakthrough, documented in Science, combines traditional silicon substrates with nanostructured perovskite layers that absorb broader light frequencies. Industrial scaling initiatives are currently underway.",
        "subject": "worldnews",
        "date": "December 19, 2022"
    },
    {
        "title": "Labor Department Reports Sustained Job Growth as National Unemployment Rate Remains Low",
        "text": "WASHINGTON (AP) - The United States economy added 216,000 nonfarm payroll positions last month, keeping the national unemployment rate at 3.7 percent, according to figures released by the Bureau of Labor Statistics. The healthcare, government, and commercial construction sectors recorded the most significant employment increases, reflecting broader economic durability despite interest rate pressures.",
        "subject": "politicsNews",
        "date": "January 5, 2024"
    },
    {
        "title": "United Kingdom and European Union Sign Historic Windsor Framework on Post-Brexit Trade",
        "text": "LONDON (Reuters) - British Prime Minister Rishi Sunak and European Commission President Ursula von der Leyen formally ratified the Windsor Framework on Monday, resolving extensive disagreements regarding trade oversight between Great Britain and Northern Ireland. The bilateral pact establishes streamlined green channels for domestic British merchandise.",
        "subject": "worldnews",
        "date": "February 27, 2023"
    },
    {
        "title": "Centers for Disease Control Expands Laboratory Sequencing Network for Respiratory Illnesses",
        "text": "ATLANTA - The Centers for Disease Control and Prevention announced on Thursday an expanded genomic surveillance network in collaboration with state public health departments. The initiative will track genetic mutations across influenza strains and emerging viral variants to optimize future vaccine formulations and strengthen public health emergency protocols.",
        "subject": "politicsNews",
        "date": "October 12, 2023"
    },
    {
        "title": "International Monetary Fund Upgrades Global Economic Outlook Amid Disinflation Trends",
        "text": "WASHINGTON (Reuters) - The International Monetary Fund elevated its global economic forecast to 3.1 percent for the year, pointing to remarkable resilience across North American and major emerging economies. Chief economist Pierre-Olivier Gourinchas stated that headline inflation is decelerating faster than previously anticipated across most developed economies.",
        "subject": "worldnews",
        "date": "January 30, 2024"
    },
    {
        "title": "Department of Agriculture Projects Strong Grain Harvest Following Favorable Regional Weather",
        "text": "DES MOINES (Reuters) - The U.S. Department of Agriculture projected robust national corn and soybean yields following beneficial precipitation across Midwestern farm belts. Commodity markets registered lower grain futures following the monthly crop report, pointing toward stabilized feed expenses for agricultural producers.",
        "subject": "politicsNews",
        "date": "September 12, 2023"
    },
    {
        "title": "Germany Shuts Down Final Nuclear Power Plants in Landmark Clean Energy Transition",
        "text": "BERLIN (Reuters) - Germany formally disconnected its final three operating commercial nuclear power reactors on Saturday, completing a multi-decade transition away from nuclear power. Federal officials stated that substantial long-term investments in wind, solar, and power storage grids will ensure reliable electricity supplies while meeting national decarbonization targets.",
        "subject": "worldnews",
        "date": "April 15, 2023"
    },
    {
        "title": "Pentagon Establishes Specialized Research Division for Anomalous Aerial Phenomenon",
        "text": "WASHINGTON (AP) - The Department of Defense announced the operational opening of the All-domain Anomaly Resolution Office to scientifically evaluate and catalog unidentified aerial observations near sensitive military test zones. Pentagon leadership emphasized that disciplined sensor calibration, radar tracking, and airspace safety remain paramount.",
        "subject": "politicsNews",
        "date": "July 20, 2022"
    },
    {
        "title": "Glaciology Expedition Accesses Pristine Subglacial Lake Deep Beneath Antarctic Ice Sheet",
        "text": "MCMURDO STATION - An international research team funded by the National Science Foundation successfully drilled through eight hundred meters of Antarctic glacial ice to extract pristine water samples from a subglacial lake. Preliminary geochemical analysis confirmed flourishing microbial communities functioning in complete darkness under extreme hydrostatic pressures.",
        "subject": "worldnews",
        "date": "January 24, 2023"
    },
    {
        "title": "Federal Communications Commission Approves Auction Rules for Advanced Commercial Spectrum",
        "text": "WASHINGTON (Reuters) - The Federal Communications Commission voted to approve technical framework rules for mid-band wireless frequency allocations. Commissioners emphasized that the regulatory framework will expand high-speed broadband infrastructure to rural municipalities and spur next-generation technological innovation across the domestic telecommunications industry.",
        "subject": "politicsNews",
        "date": "November 2, 2023"
    },
    {
        "title": "Canada Signs Comprehensive Conservation Treaty with First Nations to Safeguard Boreal Forests",
        "text": "OTTAWA (Reuters) - Canadian federal ministers and Indigenous representatives jointly announced an $800 million conservation partnership safeguarding millions of hectares of northern boreal forest. The conservation pact creates collaborative stewardship reserves to protect woodland caribou habitat and conserve vital peatland carbon sinks.",
        "subject": "worldnews",
        "date": "December 7, 2022"
    },
    {
        "title": "Health Regulators Authorize World's First CRISPR Gene-Editing Treatment for Sickle Cell Disorder",
        "text": "LONDON (Reuters) - Health agencies in the United Kingdom and the United States granted regulatory authorization for Casgevy, the world's first medicine based on CRISPR gene editing. The milestone therapeutic intervention corrects defective hemoglobin genes in patients with sickle cell disease and beta thalassemia, substantially reducing painful vaso-occlusive crises.",
        "subject": "worldnews",
        "date": "November 16, 2023"
    },
    {
        "title": "Congress Approves National Defense Authorization Act with Substantial Bipartisan Majority",
        "text": "WASHINGTON (AP) - The United States Congress passed the annual National Defense Authorization Act on Thursday, authorizing military compensation increases, strategic defense partnerships, and advanced microelectronics research. Congressional leaders noted that consistent appropriations provide essential certainty for defense readiness.",
        "subject": "politicsNews",
        "date": "December 14, 2023"
    },
    {
        "title": "World Bank Pledges Major Capital Increase for Sustainable Infrastructure Projects",
        "text": "DUBAI (Reuters) - The World Bank Group committed forty-five percent of its annual loan portfolio toward climate-resilient infrastructure at the COP28 global summit. The financing facilities will support municipal clean water networks, agricultural irrigation upgrades, and renewable grid modernization across developing countries.",
        "subject": "worldnews",
        "date": "December 1, 2023"
    }
]

fake_templates = [
    {
        "title": "SHOCKING PROOF: Secret Underground Alien Base Discovered Beneath Denver International Airport",
        "text": "DENVER, CO - Whistleblowers have finally leaked classified blueprints proving that an enormous multi-level extraterrestrial fortress is operating directly underneath the Denver International Airport. Leaked documents claim that high-ranking world leaders regularly meet with reptilian overlords during scheduled runway maintenance. Government spokespeople refused to answer questions, confirming what truth seekers have known for decades: the Illuminati controls commercial air travel and is preparing an apocalyptic underground bunker for the elite.",
        "subject": "News",
        "date": "October 5, 2023"
    },
    {
        "title": "BOMBSHELL: Miracle Lemon Juice and Baking Soda Remedy Cures All Stage 4 Cancers in Just 48 Hours",
        "text": "Big Pharma does not want you to see this leaked secret! Independent holistic researchers have discovered that drinking warm lemon juice mixed with two spoons of baking soda completely dissolves all cancer tumors within 48 hours without chemotherapy. Doctors who spoke about this miracle remedy were immediately arrested and silenced by corrupt medical cartels. Share this post immediately before social media censors delete it forever!",
        "subject": "News",
        "date": "September 14, 2023"
    },
    {
        "title": "NASA ADMITS: The Moon Landing Was Filmed in a Hollywood Basement by Stanley Kubrick",
        "text": "In a stunning late-night confession, an alleged former NASA director released 35mm audio tapes proving the 1969 Apollo 11 lunar landing was entirely fabricated in a secure Hollywood studio. The whistleblower revealed that the American flag waved in studio air conditioning and the lunar dust was made of ground-up concrete. Mainstream media networks have imposed a total blackout on this explosive breaking report.",
        "subject": "News",
        "date": "November 20, 2023"
    },
    {
        "title": "EXPOSED: 5G Cell Towers Are Transmitting Mind Control Frequencies to Activate Nanochips in Tap Water",
        "text": "Patriots wake up! High-frequency 5G radio signals are secretly tuned to resonate with microscopic tracking nanobots that the globalist deep state has dumped into municipal water supplies. A brave rogue telecommunications engineer revealed that towers are calibrated to manipulate human brainwaves during prime-time hours to force obedience. Spread this urgent message to your local community before the signal is turned up to maximum power!",
        "subject": "News",
        "date": "December 3, 2023"
    },
    {
        "title": "BREAKING: Microchips Found Hidden Inside Standard Supermarket Potato Chips to Track Consumers",
        "text": "A shocking independent laboratory test revealed that top brand potato chips contain edible RFID tracking microchips designed to monitor citizen movements in grocery stores. The microchips bond to stomach linings and report biometric data back to centralized cloud servers owned by foreign oligarchs. Share this warning before your family eats another bite of processed snack foods!",
        "subject": "News",
        "date": "August 18, 2023"
    },
    {
        "title": "LEAKED MEMO: Secret Society Plans to Block Out the Sun with Giant Mirrors to Control Weather",
        "text": "An anonymous top-secret briefing document smuggled out of a Swiss Alpine chalet reveals plans by billionaires to launch orbital space mirrors that will dim natural sunlight over independent nations. The radical scheme aims to force farmers to purchase synthetic artificial groceries manufactured in factory bioreactors. The mainstream press has been paid billions in advertising cash to dismiss the document as mere conspiracy.",
        "subject": "News",
        "date": "October 11, 2023"
    },
    {
        "title": "SCANDAL: Famous Tech Billionaire Caught on Hot Mic Admitting Climate Change is a Hoax Created for Profit",
        "text": "A leaked audio recording captured during an exclusive private dinner reveals a world-famous technology billionaire laughing with hedge fund managers as he admitted global warming data was completely fabricated on computer simulations to justify trillions in carbon taxes. The billionaire can be heard boasting about investing in fake renewable energy subsidies while flying on twelve private jets a week.",
        "subject": "News",
        "date": "January 8, 2024"
    },
    {
        "title": "UNBELIEVABLE: Antarctic Explorers Find Entrance to Hollow Earth Civilization with Woolly Mammoths",
        "text": "A rebel expedition sailing near the South Pole has reportedly entered a massive ice cave leading directly into the center of the hollow Earth. Explorers transmitted video footage of living woolly mammoths grazing in tropical valleys warmed by an inner core sun. World military navies have scrambled patrol boats to intercept the team and confiscate their camera memory cards.",
        "subject": "News",
        "date": "July 19, 2023"
    },
    {
        "title": "RED ALERT: World Leaders Secretly Replaced by Synthetic Androids with Rubber Masks",
        "text": "A renowned computer scientist who previously worked for clandestine government black sites has come forward claiming that over eighty percent of current world leaders are sophisticated robotic clones operated by artificial neural networks. The scientist provided photographic evidence of malfunctioning synthetic blinking patterns and unusual earlobe seams visible during recent televised summits.",
        "subject": "News",
        "date": "February 14, 2024"
    },
    {
        "title": "SHOCK CLAIM: Drinking Salt Water and Cinnamon Reverses Aging Process by Twenty Years Overnight",
        "text": "Dermatologists and cosmetic surgeons are panicking after an underground biologist proved that drinking three cups of heavily salted boiling water with raw cinnamon reverses cellular aging in less than twenty-four hours. Thousands of people are throwing away their expensive prescriptions after watching forbidden tutorial videos on encrypted messaging networks. Medical authorities are furiously trying to ban cinnamon sales nationwide.",
        "subject": "News",
        "date": "December 22, 2023"
    },
    {
        "title": "CONFIRMED: Government Spying on Citizens Through Bathroom Mirrors via Hidden Quantum Lenses",
        "text": "A former intelligence contractor has published a tell-all book claiming that all modern bathroom mirrors manufactured since 2015 contain microscopic quantum sensor lenses embedded inside the reflective glass backing. The surveillance apparatus transmits real-time video streams to a subterranean datacenter underneath the Pentagon. The Department of Justice has threatened the author with life imprisonment.",
        "subject": "News",
        "date": "September 29, 2023"
    },
    {
        "title": "MUST READ: Historic Ancient Pyramid Discovered on Mars by Rogue Amateur Astronomer with Cheap Telescope",
        "text": "A backyard stargazer in Ohio using a three-hundred-dollar telescope captured crystal-clear footage of an ancient Egyptian-style pyramid on the surface of Mars with flowing water canals. NASA immediately dispatched federal agents to seize the astronomer's telescope and hard drives, but backup images were already uploaded to decentralised internet forums across Eastern Europe.",
        "subject": "News",
        "date": "October 22, 2023"
    },
    {
        "title": "TERRIFYING TRUTH: Smart Refrigerator Hacks Household WiFi to Send Private Conversations to Advertisers",
        "text": "If you own a smart appliance, throw it in the trash now! Cybersecurity vigilantes have cracked open firmware updates revealing that smart refrigerators record continuous audio from kitchen conversations and sell psychological emotional profiles to shadowy dark-web marketing syndicates. The appliances even monitor when you open the door to time advertisements when your willpower is at its weakest.",
        "subject": "News",
        "date": "November 8, 2023"
    },
    {
        "title": "TREASON: Secret Treaty Signed to Disband the Military and Replace Soldiers with Robotic Cyborgs",
        "text": "Classified documents retrieved from a shredding facility prove that top defense officials signed an illegal pact to decommission domestic armed forces by next year and deploy autonomous killer cyborgs across major metropolitan highways. The robotic units are programmed to enforce martial law with zero human emotion or constitutional rights.",
        "subject": "News",
        "date": "January 19, 2024"
    },
    {
        "title": "MIRACLE DISCOVERY: Ancient Frequency Tone Heals Broken Bones and Cleans Arteries in Five Minutes",
        "text": "Sound engineers working in ancient Egyptian crypts have rediscovered an acoustic vibration tone that instantaneously mends bone fractures and cleans plaque from clogged coronary arteries without surgery. Hospital administrators are desperately bribing search engines to hide this ancient frequency because it will bankrupt global surgical centers in a single week.",
        "subject": "News",
        "date": "August 30, 2023"
    },
    {
        "title": "CLASSIFIED REVEAL: Scientists Create Hybrid Human-Dolphin Chimeras in Secret Underwater Lab",
        "text": "Divers exploring an off-limits marine sanctuary discovered an underwater research facility where rogue geneticists have successfully bred hybrid human-dolphin humanoids designed for deep-sea espionage missions. The chimera subjects can communicate telepathically and breathe underwater without scuba gear. Naval authorities deployed special forces to seal off the marine trench.",
        "subject": "News",
        "date": "October 16, 2023"
    },
    {
        "title": "THE GREAT RESET: Cash Will Be Rendered Illegal by Midnight Friday Worldwide in Surprise Move",
        "text": "Emergency leaked memos from international banking cartels declare that paper currency will be completely demonetized and outlawed starting this Friday at midnight. Citizens who fail to deposit their cash into central bank digital tokens will forfeit all savings and face immediate asset freezing. Spread this warning to everyone you know before ATM machines are disabled!",
        "subject": "News",
        "date": "February 2, 2024"
    },
    {
        "title": "SMOKING GUN: Weather Manipulation Cannons Spotted on Mountain Peaks Creating Artificial Hurricanes",
        "text": "Hikers in the Rocky Mountains stumbled upon a heavily guarded military installation featuring giant electromagnetic cloud cannons pointed directly into the upper atmosphere. Local whistleblowers confirmed these ionization cannons are actively utilized by shadowy deep-state syndicates to manufacture category five hurricanes and steer them toward targeted agricultural states.",
        "subject": "News",
        "date": "September 5, 2023"
    },
    {
        "title": "BOMBSHELL EVIDENCE: The Earth is Expanding Like a Balloon and Scientists Are Covering It Up",
        "text": "Geophysicists who were fired from top universities have united to publish satellite measurement proof that the planet is physically expanding at a rate of five meters every year. The expansion threatens to crack the oceans open into magma chambers, but global leaders are deliberately concealing the phenomenon to prevent worldwide panic and bank runs.",
        "subject": "News",
        "date": "November 27, 2023"
    },
    {
        "title": "VIRAL PROOF: Celebrities Are Using Alien Blood Transfusions to Stop Aging and Stay Young",
        "text": "An insider nurse at a luxury Beverly Hills private clinic revealed that Hollywood A-listers pay millions of dollars each month for extraterrestrial blood transfusions smuggled from crashed spacecraft at Area 51. The cosmic DNA completely halts wrinkles and grey hair. Social media moderators are deleting all video interviews with the nurse at lightning speed.",
        "subject": "News",
        "date": "December 30, 2023"
    },
    {
        "title": "URGENT ALERT: Government Planes Spraying Chemical Fog to Erase Citizens' Short-Term Memories",
        "text": "Flight radar enthusiasts have tracked unmarked cargo planes flying zigzag patterns over suburban areas releasing heavy chemical plumes specifically engineered to induce cognitive fog and short-term memory loss. The sinister operation prevents residents from remembering high gas prices and broken campaign promises ahead of municipal elections.",
        "subject": "News",
        "date": "January 14, 2024"
    },
    {
        "title": "SHOCKING REPORT: Time Traveler from 2085 Arrives with Warnings of Synthetic AI Takeover",
        "text": "A man claiming to be a chronological traveler from the year 2085 passed a series of polygraph lie-detector tests conducted by independent investigators. He produced holographic memory chips displaying futuristic city ruins conquered by self-replicating artificial intelligence. Intelligence agents arrested the man hours after the video went viral on underground web forums.",
        "subject": "News",
        "date": "August 2, 2023"
    },
    {
        "title": "EXPOSED: Deep State Planted Artificial Clones of Mount Rushmore to Hide Nuclear Silos",
        "text": "Declassified contractor logs prove that the famous stone faces at Mount Rushmore are actually hollow fiberglass replicas built over an underground missile launch complex during the height of the Cold War. Tourists visiting the monument are subjected to infrared brain scanners disguised as visitor center binoculars.",
        "subject": "News",
        "date": "October 31, 2023"
    },
    {
        "title": "WAKE UP: Secret Sound Frequencies in Commercial Pop Music Programmed to Induce Retail Spending",
        "text": "A rebel sound mixer has exposed subconscious audio frequencies embedded in top radio pop tracks that stimulate dopamine receptors linked to impulsive credit card purchases. Big retail conglomerates pay record labels hundreds of millions to insert the subliminal spending triggers into catchy song hooks.",
        "subject": "News",
        "date": "December 5, 2023"
    },
    {
        "title": "THE FINAL CONSPIRACY: Global Telecom Giants Using Solar Eclipses to Reset Citizen Biometric Databases",
        "text": "Astrophysics renegades warn that upcoming solar eclipses are scheduled events used by multinational conglomerates to momentarily disable satellite encryption while citizen biometric identity profiles are secretly synchronized across global mainframe nodes. Citizens are advised to stay indoors and disconnect all electronic devices during the eclipse.",
        "subject": "News",
        "date": "February 24, 2024"
    }
]

# Create expanded datasets by applying realistic journalistic variations and topic blends
all_real = []
all_fake = []

# Expand real articles with diverse reporting agencies and contexts
reporters = ["Reuters", "Associated Press", "Bloomberg News", "The Wall Street Journal", "Financial Times", "Agence France-Presse"]
cities = ["WASHINGTON", "GENEVA", "LONDON", "TOKYO", "BERLIN", "PARIS", "NEW YORK", "BRUSSELS", "OTTAWA", "CANBERRA"]

for item in real_templates:
    all_real.append(item)
    # Generate variations
    for i in range(3):
        rep = random.choice(reporters)
        city = random.choice(cities)
        var_text = f"{city} ({rep}) - According to official agency records released on the record, {item['text'].split('- ', 1)[-1] if '- ' in item['text'] else item['text']}"
        all_real.append({
            "title": f"Official Update: {item['title']}" if i % 2 == 0 else f"Report: {item['title']}",
            "text": var_text,
            "subject": item["subject"],
            "date": item["date"]
        })

for item in fake_templates:
    all_fake.append(item)
    # Generate variations
    intros = [
        "DO NOT IGNORE THIS REPORT! Anonymous whistleblowers have confirmed that ",
        "BREAKING EXCLUSIVE: Leaked shadow government cables obtained by underground journalists prove that ",
        "SHARE EVERYWHERE BEFORE CENSORED: Shocking leaked footage and classified memos demonstrate that "
    ]
    for idx, intro in enumerate(intros):
        var_text = f"{intro}{item['text']}"
        all_fake.append({
            "title": f"MUST SEE: {item['title']}" if idx % 2 == 0 else f"ALERT: {item['title']}",
            "text": var_text,
            "subject": "News",
            "date": item["date"]
        })

df_true = pd.DataFrame(all_real)
df_fake = pd.DataFrame(all_fake)

os.makedirs("data", exist_ok=True)
df_true.to_csv("data/True.csv", index=False)
df_fake.to_csv("data/Fake.csv", index=False)

print(f"Generated data/True.csv ({len(df_true)} rows) and data/Fake.csv ({len(df_fake)} rows).")
