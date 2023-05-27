from vi import dotlan
Regions = ["Aridia", "Black Rise", "The Bleak Lands", "Branch", "Cache", "Catch", "The Citadel",
                            "Cloud Ring", "Cobalt Edge", "Curse", "Deklein", "Delve", "Derelik", "Detorid", "Devoid",
                            "Domain", "Esoteria", "Essence", "Etherium Reach", "Everyshore", "Fade", "Feythabolis",
                            "The Forge", "Fountain", "Geminate", "Genesis", "Great Wildlands", "Heimatar", "Immensea",
                            "Impass",
                            "Insmother", "Kador", "The Kalevala Expanse", "Khanid", "Kor-Azor", "Lonetrek", "Malpais",
                            "Metropolis",
                            "Molden Heath", "Oasa", "Omist", "Outer Passage", "Outer Ring", "Paragon Soul",
                            "Period Basis",
                            "Perrigen Falls", "Placid", "Pochven", "Providence", "Pure Blind", "Querious",
                            "Scalding Pass",
                            "Sinq Laison", "Solitude", "The Spire", "Stain", "Syndicate", "Tash-Murkon", "Tenal",
                            "Tenerifis", "Tribute", "Vale of the Silent", "Venal", "Verge Vendor", "Wicked Creek"]
for region in Regions:
    region = dotlan.convertRegionName(region)
    output_path = r'mapSVG/map_{0}.svg'.format(region)
    basic = "            ('%s', '%s', 'DATA')," % (output_path, output_path)
    print(basic)