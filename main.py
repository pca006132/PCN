import snbt

print('input nbt:')
text = input()
print('base tag:')
base_tag = input()
print('Use strict? t/f')
snbt.Tag.strict = input().strip() == 't'
try:
    tag = snbt.Tag.parse(text)
    json_text = ''
    with open('test.json','r') as file:
        json_text = file.read()
    snbt.check_compound_items(snbt.load_json(json_text), tag, base_tag)
    print('No problem!')
except snbt.NbtException as error:
    print(error.message)
