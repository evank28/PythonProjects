"""
Quick script created to scrape hex colour codes from html snippet from a vendor
 \website
"""
from typing import Final
if __name__ == "main":
    HTML: Final[str] = """<span class="swatch swatch-color swatch-antique-cherry-red 
    selected" style="background-color:#bf3358;color:rgba(191,51,88,0.5);" 
    title="Antique Cherry Red" data-value="antique-cherry-red"> Antique 
    Cherry Red</span><span class="swatch swatch-color swatch-antique-sapphire 
    " style="background-color:#3594c6; color:rgba(53,148,198,0.5);" 
    title="Antique Sapphire" data-value="antique-sapphire">Antique 
    Sapphire</span> <span class="swatch swatch-color swatch-ash-grey" 
    style="background-color:#e8e8e8;color:rgba(232,232,232,0.5);" title="Ash 
    Grey" data-value="ash-grey">Ash Grey</span> <span class="swatch 
    swatch-color swatch-black " style="background-color:#0a0a0a;color:rgba(
    10,10,10,0.5);" title="Black" data-value="black">Black</span> e<span 
    class="swatch swatch-color swatch-carolina-blue " 
    style="background-color:#89bded;color:rgba(137,189,237,0.5);" 
    title="Carolina Blue" data-value="carolina-blue"> Carolina 
    Blue</span><span class="swatch swatch-color swatch-charcoal " 
    style="background-color:#6b6b6b;color:rgba(107,107,107,0.5);" 
    title="Charcoal" data-value="charcoal">Charcoal</span><span class="swatch 
    swatch-color swatch-cherry-red " 
    style="background-color:#c60035;color:rgba(198,0,53,0.5);" title="Cherry 
    Red" data-value="cherry-red">Cherry Red</span><span class="swatch 
    swatch-color swatch-dark-chocolate " 
    style="background-color:#634a2f;color:rgba(99,74,47,0.5);" title="Dark 
    Chocolate" data-value="dark-chocolate">Dark Chocolate</span><span 
    class="swatch swatch-color swatch-forest-green " 
    style="background-color:#105b0d;color:rgba(16,91,13,0.5);" title="Forest 
    Green" data-value="forest-green">Forest Green</span><span class="swatch 
    swatch-color swatch-gold " style="background-color:#ffca3a;color:rgba(
    255,202,58,0.5);" title="Gold" data-value="gold">Gold</span><span 
    class="swatch swatch-color swatch-graphite-heather " 
    style="background-color:#aaaaaa;color:rgba(170,170,170,0.5);" 
    title="Graphite Heather" data-value="graphite-heather">Graphite 
    Heather</span><span class="swatch swatch-color swatch-heliconia " 
    style="background-color:#e83c6f;color:rgba(232,60,111,0.5);" 
    title="Heliconia" data-value="heliconia">Heliconia</span><span 
    class="swatch swatch-color swatch-indigo-blue " 
    style="background-color:#7895a5;color:rgba(120,149,165,0.5);" 
    title="Indigo Blue" data-value="indigo-blue">Indigo Blue</span><span 
    class="swatch swatch-color swatch-irish-green " 
    style="background-color:#4cba4f;color:rgba(76,186,79,0.5);" title="Irish 
    Green" data-value="irish-green">Irish Green</span><span class="swatch 
    swatch-color swatch-light-blue " 
    style="background-color:#cee5ef;color:rgba(206,229,239,0.5);" 
    title="Light Blue" data-value="light-blue">Light Blue</span><span 
    class="swatch swatch-color swatch-light-pink " 
    style="background-color:#ffc9dd;color:rgba(255,201,221,0.5);" 
    title="Light Pink" data-value="light-pink">Light Pink</span><span 
    class="swatch swatch-color swatch-maroon " 
    style="background-color:#89374d;color:rgba(137,55,77,0.5);" 
    title="Maroon" data-value="maroon">Maroon</span><span class="swatch 
    swatch-color swatch-orange " style="background-color:#ef7840;color:rgba(
    239,120,64,0.5);" title="Orange" data-value="orange">Orange</span><span 
    class="swatch swatch-color swatch-purple " 
    style="background-color:#4c2d91;color:rgba(76,45,145,0.5);" 
    title="Purple" data-value="purple">Purple</span><span class="swatch 
    swatch-color swatch-red " style="background-color:#dd3333;color:rgba(221,
    51,51,0.5);" title="Red" data-value="red">Red</span><span class="swatch 
    swatch-color swatch-royal " style="background-color:#1e73be;color:rgba(
    30,115,190,0.5);" title="Royal" data-value="royal">Royal</span><span 
    class="swatch swatch-color swatch-safety-green " 
    style="background-color:#deff68;color:rgba(222,255,104,0.5);" 
    title="Safety Green" data-value="safety-green">Safety Green</span><span 
    class="swatch swatch-color swatch-safety-orange " 
    style="background-color:#ff7f3a;color:rgba(255,127,58,0.5);" 
    title="Safety Orange" data-value="safety-orange">Safety 
    Orange</span><span class="swatch swatch-color swatch-safety-pink " 
    style="background-color:#ff44e6;color:rgba(255,68,230,0.5);" 
    title="Safety Pink" data-value="safety-pink">Safety Pink</span><span 
    class="swatch swatch-color swatch-sand " 
    style="background-color:#ffefdb;color:rgba(255,239,219,0.5);" 
    title="Sand" data-value="sand">Sand</span><span class="swatch 
    swatch-color swatch-sapphire " 
    style="background-color:#3fbce2;color:rgba(63,188,226,0.5);" 
    title="Sapphire" data-value="sapphire">Sapphire</span><span class="swatch 
    swatch-color swatch-sport-grey " 
    style="background-color:#9b9b9b;color:rgba(155,155,155,0.5);" 
    title="Sport Grey" data-value="sport-grey">Sport Grey</span><span 
    class="swatch swatch-color swatch-white" 
    style="background-color:#f4f4f4;color:rgba(244,244,244,0.5);" 
    title="White" data-value="white">White</span></div> """

    names = HTML.split("\">")
    names = [token[:token.find("<")] for token in names][1:]

    codes = HTML.split("#")
    codes = [token[:token.find(";")] for token in codes][1:]

    count = 0
    for name in names:
        print(
            """<td style="background-color:#{}">{}</td>""".format(codes[count],
                                                                  name))
        if (count + 1) % 6 == 0:
            print("</tr><tr>")
        count += 1
