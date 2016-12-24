"""Parse Single Tag(return Tag):
> Tag.parse(TEXT)
---------------------------------------------------------
Parse Multiple Tags(no name):
> index = 0
> tags = []
> while index < len(TEXT) - 1
>     key, value, index = Tag.parse_key_value(TEXT, index)
>     tags.append(Tag.parse(value))
---------------------------------------------------------
Parse Multiple Tags(with name):
> index = 0
> tags = {}
> while index < len(TEXT) - 1
>     key, value, index = Tag.parse_key_value(TEXT, index)
>     tags[key] = Tag.parse(value)
---------------------------------------------------------
Get Item of Compound Tag(return Tag):
> compound['key']
---------------------------------------------------------
Get Item of List Tag(return Tag):
> list[index]
---------------------------------------------------------
Iterate over Items in Compound Tag:
> for key in compound.tags():
>     tag = compound[key]
---------------------------------------------------------
Iterate over Items in List Tag:
> for tag in list:
>     # do what ever here
>     pass
---------------------------------------------------------
Check Type(return Boolean):
> tag.type_match(type)

Example: tag.type_match(TagByte)

Usage: the type of the tag read may not be the type in
game, such as Count:1 is parsed as TagInt, but it should
be TagByte in game. This function can check if the tag
can be converted into the type in game.
--------------------------------------------------------
String representation of Tag(return string, no indent):
> str(tag)
---------------------------------------------------------
Pretty print(return string, with indent and line break)
> tag.tree()
---------------------------------------------------------
Error: NbtException
Sources of error:
+ Illegal black slash outside string, such as 'say \\nhi'
+ Imbalance bracket, such as '{[}]'
+ No ending bracket, such as '{'
+ No ending quote, such as '"abcd'"""

import re

class NbtException(Exception):
    def __init__(self, message):
        self.message = message
class Tag:
    multiline = re.compile('^', re.M)
    def __init__(self, value = None):
        self.value = value
    def __str__(self):
        return self.value
    def parse(text):
        success = False
        for i in (TagByte, TagCompound, TagDouble, TagFloat, TagInt, TagList, \
            TagLong, TagShort, TagString):
            success, tag = i.parse(text)
            if success:
                return tag
    def parse_key_value(text, index):
        has_key = True
        value = ''
        key = ''
        temp = []
        brackets = []
        string = False
        escape = False
        for j in range(index, len(text)):
            i = text[j]
            if string:
                if escape:
                    escape = False
                elif i == '\\':
                    escape = True
                elif i == '"':
                    string = False
                temp.append(i)
            else:
                if i == ':':
                    if has_key:
                        key = ''.join(temp)
                        temp.clear()
                        has_key = False
                        continue
                elif i == '{' or i == '[':
                    has_key = False
                    brackets.append(i)
                elif i == '}':
                    if len(brackets) == 0 or brackets[-1] == ']':
                        raise NbtException('Imbalance bracket at char %d.' % (j+1))
                    brackets.pop()
                elif i == ']':
                    if len(brackets) == 0 or brackets[-1] == '}':
                        raise NbtException('Imbalance bracket at char %d.' % (j+1))
                    brackets.pop()
                elif i == '"':
                    string = True
                elif i == '\\':
                    raise NbtException('Illegal back slash at char %d.' % (j+1))
                elif i == ',':
                    if len(brackets) == 0:
                        value = ''.join(temp)
                        return key, value, j+1
                temp.append(i)
        if len(brackets) > 0:
            raise NbtException('No ending bracket.')
        if string:
            raise NbtException('No ending quote')
        value = ''.join(temp)
        return key, value, len(text) - 1
    def tree(self):
        return str(self)
class TagByte(Tag):
    pattern = re.compile(r'(\d+)[bB]')
    def __str__(self):
        return str(self.value) + "b"
    def parse(text):
        match = TagByte.pattern.fullmatch(text)
        if match is not None:
            return True, TagByte(int(match.group(1)))
        return False, None
    def type_match(self, nbt_type):
        return nbt_type in [TagByte, TagString]
class TagCompound(Tag):
    def __contains__(self, item):
        return item in self.value
    def __getitem__(self, key):
        return self.value[key]
    def __setitem__(self, key, value):
        self.value[key] = value
    def __delitem__(self, key):
        del(self.value[key])
    def __init__(self, value = {}):
        self.value = value
    def __str__(self):
        temp = []
        for key, tag in self.value.items():
            temp.append(key + ":" + str(tag))
        return '{%s}' % ','.join(temp)
    def keys(self):
        return self.value.keys()
    def parse(text):
        if text[0] == '{' and text[-1] == '}':
            index = 0
            tags = {}
            while index < len(text[1:-1]) - 1:
                key, value, index = Tag.parse_key_value(text[1:-1], index)
                tags[key] = Tag.parse(value)
            return True, TagCompound(tags)
        return False, None
    def tree(self):
        temp = []
        for key in self.value:
            temp.append(Tag.multiline.sub(' ' * 4, key + ":" + self.value[key].tree()))
        if len(temp) > 0:
            return '{\n%s\n}' % ',\n'.join(temp)
        else:
            return '{}'
    def type_match(self, nbt_type):
        return nbt_type in [TagCompound, TagString]
class TagDouble(Tag):
    pattern = re.compile(r'(\d+\.\d+[dD]?)|(\d+[dD])')
    def __str__(self):
        return str(self.value) + "d"
    def parse(text):
        match = TagDouble.pattern.fullmatch(text)
        if match is not None:
            return True, \
                TagDouble(float(text if text[-1] not in ['b', 'B'] else text[:-1]))
        return False, None
    def type_match(self, nbt_type):
        return nbt_type in [TagDouble, TagString]
class TagFloat(Tag):
    pattern = re.compile(r'(\d+(\.\d+)?)[fF]')
    def __str__(self):
        return str(self.value) + "f"
    def parse(text):
        match = TagFloat.pattern.fullmatch(text)
        if match is not None:
            return True, TagFloat(float(match.group(1)))
        return False, None
    def type_match(self, nbt_type):
        return nbt_type in [TagFloat, TagString]
class TagInt(Tag):
    pattern = re.compile(r'\d+')
    def __str__(self):
        return str(self.value)
    def parse(text):
        match = TagInt.pattern.fullmatch(text)
        if match is not None:
            return True, TagInt(int(text))
        return False, None
    def type_match(self, nbt_type):
        return nbt_type in [TagInt, TagByte, TagShort, TagString]
class TagList(Tag):
    def __contains__(self, item):
        return item in self.value
    def __getitem__(self, key):
        return self.value[key]
    def __setitem__(self, key, value):
        self.value[key] = value
    def __delitem__(self, key):
        del(self.value[key])
    def __init__(self, value = []):
        self.value = value
    def __str__(self):
        temp = []
        for tag in self.value:
            temp.append(str(tag))
        return '[%s]' % ','.join(temp)
    def parse(text):
        if text[0] == '[' and text[-1] == ']':
            index = 0
            tags = []
            while index < len(text[1:-1]) - 1:
                key, value, index = Tag.parse_key_value(text[1:-1], index)
                tags.append(Tag.parse(value))
            return True, TagList(tags)
        return False, None
    def tree(self):
        temp = []
        for tag in self.value:
            temp.append(Tag.multiline.sub(' ' * 4, tag.tree()))
        if len(temp) > 0:
            return '[\n%s\n]' % ',\n'.join(temp)
        else:
            return '[]'
    def type_match(self, nbt_type):
        return nbt_type in [TagList, TagString]
class TagLong(Tag):
    pattern = re.compile(r'(\d+)[lL]')
    def __str__(self):
        return str(self.value) + "l"
    def parse(text):
        match = TagLong.pattern.fullmatch(text)
        if match is not None:
            return True, TagLong(int(match.group(1)))
        return False, None
    def type_match(self, nbt_type):
        return nbt_type in [TagLong, TagString]
class TagShort(Tag):
    pattern = re.compile(r'(\d+)[sS]')
    def __str__(self):
        return str(self.value) + "s"
    def parse(text):
        match = TagShort.pattern.fullmatch(text)
        if match is not None:
            return True, TagShort(int(match.group(1)))
        return False, None
    def type_match(self, nbt_type):
        return nbt_type in [TagShort, TagString]
class TagString(Tag):
    def __str__(self):
        if TagString.need_escape(self.value) or \
            re.fullmatch(r'\d+(\.\d+)?[bBdDfFlLsS]?', self.value) is not None or \
            (self.value[0] in ['{', '['] and self.value[-1] in ['}', ']']):
            return '"' + TagString.escape(self.value) + '"'
        else:
            return self.value
    def escape(text):
        return text.replace('\\', '\\\\').replace('"', '\\"')
    def need_escape(text):
        brackets = []
        in_string = False
        for char in text:
            if in_string:
                if char == '"':
                    in_string = False
                elif char == '\\':
                    return True
            else:
                if char == '{' or char == '[':
                    brackets.append(char)
                elif char == '}':
                    if len(brackets) == 0:
                        return True
                    if not brackets.pop() == '{':
                        return True
                elif char == ']':
                    if len(brackets) == 0:
                        return True
                    if not brackets.pop() == '[':
                        return True
                elif char == ',':
                    if len(brackets) == 0:
                        return True
                elif char == '"':
                    in_string = True
                elif char == '\\':
                    return True
        if len(brackets) > 0:
            return True
        if in_string:
            return True
        return False
    def parse(text):
        if text[0] == '"' and text[-1] == '"':
            return True, TagString(TagString.unescape(text[1:-1]))
        return True, TagString(text)
    def unescape(text):
        return text.replace('\\"', '"').replace('\\\\', '\\')
    def type_match(self, nbt_type):
        return nbt_type in [TagString]

if __name__ == '__main__':
    try:
        tag = Tag.parse(input())
        with open('nbttree.txt', 'w') as file:
            file.write(tag.tree())
    except NbtException as error:
        print(error.message)