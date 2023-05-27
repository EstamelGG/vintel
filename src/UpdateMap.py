import requests
import time
from vi import dotlan

def getSVG():
    DOTLAN_BASIC_URL = u"http://evemaps.dotlan.net/svg/{0}.svg"
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
        url = DOTLAN_BASIC_URL.format(dotlan.convertRegionName(region))
        region = dotlan.convertRegionName(region)
        output_path = r'mapSVG\\map_{0}.svg'.format(region)
        print("Download Region map : %s to %s from url:\"%s\"" % (region, output_path, url))
        req = requests.get(url, verify=False)
        content = req.text
        if content:
            if u"not found" not in content:
                with open(output_path, 'w') as f: f.write(content)
            else:
                print("%s not found" % region)
        else:
            print(req.status_code)
        time.sleep(0.1)

if __name__ == "__main__":
    getSVG()