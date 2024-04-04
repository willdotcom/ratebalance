import os
import xml.etree.ElementTree as ET

# Function to modify the XML file
def modify_xml(xml_file, rate_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    rate_tree = ET.parse(rate_file)
    rate_root = rate_tree.getroot()

    total_updated_lines = 0

    for monster in root.findall(".//DropItem"):
        exc_value = monster.get('Exc')
        name_value = monster.get('Name')

        for excellent_rate_config in rate_root.findall('.//ExcellentRate'):
            filter_by = excellent_rate_config.find('FilterBy')

            filter_exc = filter_by.get('Exc')
            filter_name = filter_by.get('Name')

            if (filter_exc is None or exc_value == filter_exc) and (filter_name is None or filter_name in name_value):
                rate = int(float(excellent_rate_config.get('Rate')))
                monster.set('Rate', str(rate))

                print(f"Modified Monster (MonsterID {monster.get('MonsterID')}):")
                print(f"  Modified Rate: {rate}")
                print("-" * 30)

                total_updated_lines += 1

        for normal_rate_config in rate_root.findall('.//ItemNormalRate'):
            filter_by = normal_rate_config.find('FilterBy')

            filter_exc = filter_by.get('Exc')

            if filter_exc is None or exc_value == filter_exc:
                rate = int(float(normal_rate_config.get('Rate')))
                monster.set('Rate', str(rate))

                print(f"Modified Monster (MonsterID {monster.get('MonsterID')}):")
                print(f"  Modified Rate: {rate}")
                print("-" * 30)

                total_updated_lines += 1

        for rate_change_config in rate_root.findall('.//ItemRateChange'):
            name_filter = rate_change_config.find('NameItemToChangeRate')

            name_filter_value = name_filter.get('Name')

            if name_filter_value is not None and name_filter_value in name_value:
                rate = int(float(rate_change_config.get('Rate')))
                monster.set('Rate', str(rate))

                print(f"Modified Monster (MonsterID {monster.get('MonsterID')}):")
                print(f"  Modified Rate: {rate}")
                print("-" * 30)

                total_updated_lines += 1

    tree.write(xml_file)

    return total_updated_lines

folder_path = 'EachMonsterMapDrop'

xml_files = [file for file in os.listdir(folder_path) if file.endswith('.xml')]

for xml_file in xml_files:
    full_path = os.path.join(folder_path, xml_file)
    
    modified_lines = modify_xml(full_path, 'rate.xml')
    print(f"Total lines updated in {xml_file}: {modified_lines}")

print("All XML files have been modified successfully.")
