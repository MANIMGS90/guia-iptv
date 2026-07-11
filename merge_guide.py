"""
Fusiona guide.xml (generado por iptv-org/epg desde mani_channels.xml)
con mani_extra_epg.xml (horarios inventados para canales 24/7 y genericos
que no existen como canal real en gatotv.com).

Uso en el workflow de GitHub Actions, despues del paso "npm run grab":
    python3 merge_guide.py guide.xml mani_extra_epg.xml guide.xml
"""
import sys
import xml.etree.ElementTree as ET

def main():
    main_path, extra_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

    main_tree = ET.parse(main_path)
    main_root = main_tree.getroot()

    extra_tree = ET.parse(extra_path)
    extra_root = extra_tree.getroot()

    # Los <channel> deben ir antes que los <programme> en un XMLTV valido
    channels = extra_root.findall('channel')
    programmes = extra_root.findall('programme')

    first_programme = main_root.find('programme')
    insert_at = list(main_root).index(first_programme) if first_programme is not None else len(list(main_root))

    for i, ch in enumerate(channels):
        main_root.insert(insert_at + i, ch)
    for p in programmes:
        main_root.append(p)

    main_tree.write(out_path, encoding='UTF-8', xml_declaration=True)
    print(f"Fusionado: +{len(channels)} canales, +{len(programmes)} programas -> {out_path}")

if __name__ == '__main__':
    main()
